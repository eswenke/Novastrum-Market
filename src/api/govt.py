from fastapi import APIRouter, Depends
from enum import Enum
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db
import random

router = APIRouter(
    prefix="/civilian/govt",
    tags=["government"],
    dependencies=[Depends(auth.get_api_key)],
)

class War(BaseModel):
    war_id: int
    planet_1: str
    planet_2: str
    bid: int

@router.post("/deliver/{citizen_id}")
def commence_wars(wars_commenced: list[War], citizen_id: int):
    """updates planet status to waring, post wars to gamble on to market
       * [seller_id, type = war, name, quantity??, bid] """
    with db.engine.begin() as connection:
        print(f"wars commenced: {wars_commenced}")
        for war in wars_commenced:
            # place new war into war table with conflict handling
            connection.execute(sqlalchemy.text(
                """
                INSERT INTO wars (id, planet_1, planet_2)
                VALUES (:id, :planet_1, :planet_2)
                ON CONFLICT (id) DO NOTHING
                """
            ), {'id': war.war_id , 'planet_1': war.planet_1, 'planet_2': war.planet_2})

            # status of planets updated to waring
            connection.execute(sqlalchemy.text(
                """
                UPDATE planets
                SET war_id = :war_id
                WHERE planet IN (:planet_1, :planet_2)
                """
            ), {'war_id': war.war_id, 'planet_1': war.planet_1, 'planet_2': war.planet_2})

            # post new war to market
            connection.execute(sqlalchemy.text(
                """
                INSERT INTO market (seller_id, type, name, quantity, price)
                VALUES (:seller_id, :type, :name, :quantity, :price)
                """
            ), {'seller_id': citizen_id, 'type': 'wars', 'name': str(war.war_id), 'quantity': 1, 'price': war.bid})

    return "OK"


@router.post("/plan")
def get_war_plan():
    """
    gets planet status, randomly pairs up planets for wars 
    """

    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("SELECT planet FROM planets WHERE war_id = 1"))
        planets = [row[0] for row in result]  # Accessing the first element of the tuple
        
        if len(planets) < 2:
            return []

        random.shuffle(planets)
        war_plans = []  
        war_id = connection.execute(sqlalchemy.text("SELECT id FROM wars ORDER BY id DESC LIMIT 1")).scalar_one()
        initial_bid = 100  # generate dynamically??


        for i in range(0, len(planets) - 1, 2):
            war_id += 1
            planet_1 = planets[i]
            planet_2 = planets[i + 1]
            war_plans.append({
                "war_id": war_id,
                "planet_1": planet_1,
                "planet_2": planet_2,
                "bid": initial_bid
            })

        return war_plans

if __name__ == "__main__":
    print(get_war_plan())
