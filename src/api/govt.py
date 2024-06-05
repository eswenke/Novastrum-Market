from fastapi import APIRouter, Depends
from enum import Enum
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db
import src.api.citizen as citizen
import random

router = APIRouter(
    prefix="/citizen",
    tags=["government"],
    dependencies=[Depends(auth.get_api_key)],
)

class War(BaseModel):
    war_id: int
    planet_1: str
    planet_2: str
    min_bid: int

@router.post("/begin/wars")
def commence_wars():
    if citizen.cit_id < 0:
        return "ERROR: Not logged in."
    
    if citizen.role != 'govt':
        return "Not authorized. You must be a government official to access this service."
    
    """
    gets planet status, randomly pairs up planets for wars 
    """
    with db.engine.begin() as connection:
        result = connection.execute(sqlalchemy.text("SELECT planet FROM planets WHERE war_id = 5"))
        planets = [row[0] for row in result]  # Accessing the first element of the tuple
        
        if len(planets) < 2:
            return []

        random.shuffle(planets)
        war_id = connection.execute(sqlalchemy.text("SELECT id FROM wars ORDER BY id DESC LIMIT 1")).scalar_one()
        initial_bid = random.randint(25,100)  # generate dynamically??

        for i in range(0, len(planets) - 1, 2):
            war_id += 1
            planet_1 = planets[i]
            planet_2 = planets[i + 1]
             # place new war into war table with conflict handling
            connection.execute(sqlalchemy.text(
                """
                INSERT INTO wars (id, planet_1, planet_2, citizen_id, min_bid)
                VALUES (:id, :planet_1, :planet_2, :citizen_id, :min_bid)
                ON CONFLICT (id) DO NOTHING
                """
            ), {'id': war_id, 'planet_1': planet_1, 'planet_2': planet_2, 'citizen_id': citizen.cit_id, 'min_bid': initial_bid})

            # status of planets updated to waring
            connection.execute(sqlalchemy.text(
                """
                UPDATE planets
                SET war_id = :war_id
                WHERE planet IN (:planet_1, :planet_2)
                """
            ), {'war_id': war_id, 'planet_1': planet_1, 'planet_2': planet_2})
    return "OK"

if __name__ == "__main__":
    print(commence_wars())
