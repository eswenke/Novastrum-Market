from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
from src import database as db
import sqlalchemy
import random
import src.api.citizen as citizen
import time

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
    """mine substances from planet, post to market"""

    begin = time.time() 

    if citizen.cit_id < 0:
        return "ERROR: Not logged in."
    
    if citizen.role != 'miner':
        return "Not authorized. You must be a miner to access this service."

    with db.engine.begin() as connection:
        # get substance by citizen role
        subst_data = connection.execute(sqlalchemy.text("""SELECT substances.name, substances.planet, substances.quantity, substances.price from substances 
                                                        JOIN citizens ON substances.planet = citizens.planet WHERE citizens.id = :id""")
                                                        , [{"id": citizen.cit_id}]).first()
        
        cap_mining = round(subst_data[2] * 0.25) # can at most mine 1/4 of the planet
        if cap_mining == 0: 
            return "This planet has been drained of substances. Reset the planet in order to continue mining."
        mining_amt = random.randint(1, cap_mining)
   
        #Substance(substances[0], substances[2], mining_amt, substances[1])
        # add substance to market
        connection.execute(sqlalchemy.text(
                        """
                        INSERT INTO market (quantity, price, seller_id, name, type)
                        VALUES (:quantity, :price, :id, :name, 'substances')
                        """
                        ), {"quantity": mining_amt, "price": subst_data[3], 
                            "id": citizen.cit_id, "name":subst_data[0]})
        
        # update inventory if it already exist, otherwise insert into inventory
        if connection.execute(sqlalchemy.text("SELECT name FROM inventory where name = :name and status = 'selling' and citizen_id = :cit_id"), {'name' : subst_data[0], 'cit_id' : citizen.cit_id}).scalar():
            connection.execute(sqlalchemy.text("""UPDATE inventory SET quantity = quantity + :mined
                                            WHERE name = :name and citizen_id = :cit_id"""),
                                        {'mined' : mining_amt, 'name' : subst_data[0], 'cit_id': citizen.cit_id})
        else:
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
        
    end = time.time() 
    print(f"Total runtime of the program is {1000 * (end - begin)} ms") 

    return f"OK: {{'name': '{subst_data[0]}', 'planet': '{subst_data[1]}', 'quantity': {mining_amt}, 'price': '{subst_data[3]}'}}"

    


