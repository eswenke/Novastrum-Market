from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from src import database as db
import sqlalchemy
import random
import src.api.citizen as citizen

router = APIRouter(
    prefix="/citizen",
    tags=["miner"],
    dependencies=[Depends(auth.get_api_key)],
)

class Substance(BaseModel):
    name: str
    planet: str
    quantity: int
    price: int

@router.post("/mine")
def mine_substance():
    if citizen.cit_id < 0:
        return "ERROR: Not logged in."
    
    if citizen.role != 'miner':
        return "Not authorized. You must be a miner to access this service."

    with db.engine.begin() as connection:
        # get substance by citizen role
        subst_data = connection.execute(sqlalchemy.text("""SELECT substances.name, substances.planet, substances.quantity, substances.price from substances JOIN citizens ON substances.planet = citizens.planet WHERE citizens.id = :id""")
                                                        , [{"id": citizen.cit_id}]).first()
        
        cap_mining = round(subst_data[2] * 0.25) # can at most mine 1/4 of the planet
        if cap_mining == 0: return {} # planet substance depleted, maybe we add substance after certain time
        mining_amt = random.randint(0, cap_mining)
   
    #Substance(substances[0], substances[2], mining_amt, substances[1])
        # add substance to market
        connection.execute(sqlalchemy.text(
                        """
                        INSERT INTO market (quantity, price, seller_id, name, type)
                        VALUES (:quantity, :price, :id, :name, 'substances')
                        """
                        ), {"quantity": mining_amt, "price": subst_data[3], 
                            "id": citizen.cit_id, "name":subst_data[0]})
        
        # update inventory 
        connection.execute(sqlalchemy.text("""INSERT INTO inventory (citizen_id, type, quantity, name, status) 
                                                VALUES (:id, 'substances', :quant, :name, 'selling')"""),
                                        {'id' : citizen.cit_id, 'quant' : mining_amt, 'name' : subst_data[0]})
            
        # update substance quantity 
        connection.execute(sqlalchemy.text("""UPDATE substances SET quantity = quantity - :mined
                                            WHERE name = :name"""),
                                        {'mined' : mining_amt, 'name' : subst_data[0]})
        
        print({
                "name": subst_data[0],
                "planet": subst_data[1],
                "quantity": mining_amt,
                "price": subst_data[3]
            })
        
    return "OK"
    


