from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from src import database as db
import sqlalchemy
import random

router = APIRouter(
    prefix="/civilian/miner",
    tags=["miner"],
    dependencies=[Depends(auth.get_api_key)],
)

class Substance(BaseModel):
    name: str
    planet: str
    quantity: int
    price: int
    
@router.post("/deliver/{citizen_id}")
def post_substance(citizen_id: int, substance: Substance):

    cost = substance.price * substance.quantity 
  
    with db.engine.begin() as connection:
        connection.execute(sqlalchemy.text(
                    """
                    INSERT INTO market (quantity, price, seller_id, name, type)
                    VALUES (:quantity, :price, :id, :name, 'substances')
                    """
                    ), {"quantity": substance.quantity, "price": cost, 
                        "id": citizen_id, "name":substance.name})
    
        # update inv to reflect selling status
        connection.execute(sqlalchemy.text("""UPDATE inventory SET status = 'selling'
                                           WHERE type = 'substances' 
                                           AND citizen_id = :id
                                           AND name = :name"""),
                                    {'id' : citizen_id, 'name': substance.name})
        
        connection.execute(sqlalchemy.text("""UPDATE substances SET quantity = quantity - :mined
                                           WHERE name = :name"""),
                                    {'mined' : substance.quantity, 'name' : substance.name})
    print(f"substances delievered: {substance}") # each miner mines a single planets substance, only one returned
    return "OK"


@router.post("/plan/{citizen_id}")
def create_miner_plan(citizen_id: int):

    with db.engine.begin() as connection:
        subst_data = connection.execute(sqlalchemy.text("""SELECT substances.name, substances.planet, substances.quantity, substances.price from substances JOIN citizens ON substances.planet = citizens.planet WHERE citizens.id = :id""")
                                                        , [{"id": citizen_id}]).first()
        
        cap_mining = round(subst_data[2] * 0.25) # can at most mine 1/4 of the planet
        if cap_mining == 0: return {} # planet substance depleted, maybe we add substance after certain time
        mining_amt = random.randint(0, cap_mining)


        # substance added to miner inventory
        connection.execute(sqlalchemy.text("""INSERT INTO inventory (citizen_id, type, quantity, name, status) 
                                            VALUES (:id, 'substances', :quant, :name, 'owned')"""),
                                   {'id' : citizen_id, 'quant' : mining_amt, 'name' : subst_data[0]})
        
    #Substance(substances[0], substances[2], mining_amt, substances[1])
    return  {
                "name": subst_data[0],
                "planet": subst_data[1],
                "quantity": mining_amt,
                "price": subst_data[3]
            }


