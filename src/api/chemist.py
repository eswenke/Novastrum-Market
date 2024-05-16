from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/civilian/miner",
    tags=["miner"],
    dependencies=[Depends(auth.get_api_key)],
)

class Narcotic(BaseModel):
    name: str
    quantity: int
    price: int
    # type: list[int] **** maybe add later for complexity?
    
@router.post("/deliver/{citizen_id}")
def post_market_listings(narcos_delivered: list[Narcotic], citizen_id:int):
    """insert narcos to market listings table,
    * [seller_id, type = narco, prod_sku, quant, price]"""

    with db.engine.begin() as connection:
        for narco in narcos_delivered: # Switch "owned" to selling, insert listing into market
            connection.execute(sqlalchemy.text("UPDATE inventory SET status = 'selling' WHERE name = :drug_name and citizen_id = :cit_id"),
                                    {'name' : narco[0], 'cit_id' : citizen_id})


    print(f"narcos delievered: {narcos_delivered}")
    return "OK"

@router.post("/plan/{citizen_id}") # Assuming substances are in inventory. Turn substances into narcos and post
def create_chemist_plan(citizen_id: int):
    """ gets substances from subst table, 
    * creates plan for making narcos, 
    * add substances to chemist inventory
    * remove substance from table
    * reduce chemist voidex
    * increase miner voidex"""
    with db.engine.begin() as connection:
        subst_avail = connection.execute(sqlalchemy.text("SELECT name, quantity FROM inventory where type = 'substances' and citizen_id = :id"), {'id' : citizen_id})
        substances = []
        for substance in subst_avail:
            name, quantity = substance
            substances.append([name, quantity])
        ret = []
        #[name, quantity]
        for subst in substances: # Take in substances, return list of drugs that can be made, decrement based on that
            rarity = connection.execute(sqlalchemy.text("SELECT rarity FROM substances where name = :name"), {'name' : subst[0]}).scalar()
            if subst[1] > 10: # can make
                drug_quant = subst[1] // 10
                subst_lost = drug_quant * 10
                drug_name, drug_price = connection.execute(sqlalchemy.text("SELECT name, price FROM narcos where rarity = :rare"), {'rare' : rarity}).scalar()
                ret.append({
                    "name": drug_name,
                    "quantity": drug_quant,
                    "price": drug_price})
                # Update substance stores, increase drug stores
                connection.execute(sqlalchemy.text("UPDATE inventory SET quantity = quantity - :subst_lost WHERE name = :subst_name and citizen_id = :cit_id"),
                                    {'subst_lost' : subst_lost, 'name' : subst[0], 'cit_id' : citizen_id})
                # If drug already in inventory, update, else insert new row
                if connection.execute(sqlalchemy.text("SELECT name FROM inventory where name = :name and status = 'owned'"), {'name' : drug_name}).scalar():
                    connection.execute(sqlalchemy.text("UPDATE inventory SET quantity = quantity + :drug_gain WHERE name = :drug_name and citizen_id = :cit_id"),
                                    {'drug_gain' : drug_quant, 'name' : drug_name, 'cit_id' : citizen_id})
                else:
                    connection.execute(sqlalchemy.text("""INSERT INTO inventory (citizen_id, type, quantity, name, status) VALUES (:cit_id, 'narcos', :quant, :name, 'owned')"""),
                                    {'cit_id' : citizen_id, 'quant' : drug_quant, 'name' : drug_name})

    return ret
