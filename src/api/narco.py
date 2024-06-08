from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db
import src.api.citizen as citizen
import time

router = APIRouter(
    prefix="/narco",
    tags=["narco"],
    dependencies=[Depends(auth.get_api_key)],
)

class Narcotic(BaseModel):
    name: str
    quantity: int
    price: int
    
@router.post("/consume")
def post_drugs_done(narcos_delivered: list[Narcotic]):
    "Remove drugs from inventory, be cooler"

    begin = time.time()

    if citizen.cit_id < 0:
        return "ERROR: not logged in."

    with db.engine.begin() as connection:
        for narco in narcos_delivered: 
            # Switch decrement number owned, increment coolness, dont if drug not owned
            in_table = connection.execute(sqlalchemy.text("""SELECT EXISTS (
                                                          SELECT 1 FROM inventory 
                                                          WHERE citizen_id = :cit_id
                                                          AND name = :narco_name
                                                          AND quantity > 0
                                                          AND (quantity - :quant) >= 0);"""),
                                    {'narco_name' : narco.name, 'cit_id' : citizen.cit_id, 'quant' : narco.quantity}).scalar()
            
            # Determining coolness, quantity * rarity
            coolness = narco.quantity * connection.execute(sqlalchemy.text("""SELECT COALESCE((
                                                                     SELECT rarity FROM narcos 
                                                                     WHERE name = :drug_name 
                                                                     LIMIT 1), -1) as result;"""), 
                                                    {'drug_name' : narco.name}).scalar()
            
            if coolness < 0:
                return "Unidentified narcotic or impossible quantity"
            
            if in_table == 1: # Proceed with consumption
                connection.execute(sqlalchemy.text("""UPDATE inventory SET quantity = quantity - :quant WHERE name = :drug_name and citizen_id = :cit_id;
                                               UPDATE citizens SET coolness = coolness + :cool WHERE id = :cit_id;"""),
                                    {'cit_id' : citizen.cit_id, 'cool' : coolness, 'quant' : narco.quantity, 'drug_name' : narco.name})
            else:
                return "Narco not found in inventory or not enough narcos"

    print(f"narcos consumed: {narcos_delivered}")
    
    end = time.time() 
    print(f"Total runtime of the program is {1000 * (end - begin)} ms")  

    return f"narcos consumed: {narcos_delivered}"
