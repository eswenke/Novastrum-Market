from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db
import src.api.citizen as citizen


router = APIRouter(
    prefix="/citizen",
    tags=["chemist"],
    dependencies=[Depends(auth.get_api_key)],
)

class Narcotic(BaseModel):
    name: str
    quantity: int
    price: int
    
@router.post("/brew")
def brew():
    """insert narcos to market listings table and update chemist inventory"""

    if citizen.cit_id < 0:
        return "ERROR: Not logged in."
    
    if citizen.role != "chemist":
        return "Not authorized. You must be a chemist to access this service."

    
    with db.engine.begin() as connection:
        subst_avail = connection.execute(sqlalchemy.text("SELECT name, quantity FROM inventory where type = 'substances' and citizen_id = :id"), {'id' : citizen.cit_id})
        substances = []
        for substance in subst_avail:
            name, quantity = substance
            substances.append([name, quantity])
        narcos_delivered = []

        # Take in substances, return list of drugs that can be made, decrement based on that
        for subst in substances: 
            rarity = connection.execute(sqlalchemy.text("SELECT rarity FROM substances where name = :name"), {'name' : subst[0]}).scalar()
            if subst[1] > 10: # can make
                drug_quant = subst[1] // 10
                subst_lost = drug_quant * 10
                drug_name, drug_price = connection.execute(sqlalchemy.text("SELECT name, price FROM narcos where rarity = :rare"), {'rare' : rarity}).first()
                
                narcos_delivered.append(Narcotic(name=drug_name, quantity=drug_quant, price=drug_price))
                
                # Update substance stores, increase drug stores
                connection.execute(sqlalchemy.text("UPDATE inventory SET quantity = quantity - :subst_lost WHERE name = :subst_name and citizen_id = :cit_id"),
                                    {'subst_lost' : subst_lost, 'subst_name' : subst[0], 'cit_id' : citizen.cit_id})
                
                # If drug already in inventory, update, else insert new row
                if connection.execute(sqlalchemy.text("SELECT name FROM inventory where name = :name and status = 'selling' and citizen_id = :cit_id FOR UPDATE"), {'name' : drug_name, 'cit_id' : citizen.cit_id}).scalar():
                    connection.execute(sqlalchemy.text("UPDATE inventory SET quantity = quantity + :drug_gain WHERE name = :drug_name and citizen_id = :cit_id"),
                                    {'drug_gain' : drug_quant, 'drug_name' : drug_name, 'cit_id' : citizen.cit_id})
                
                else:
                    connection.execute(sqlalchemy.text("""INSERT INTO inventory (citizen_id, type, quantity, name, status) VALUES (:cit_id, 'narcos', :quant, :name, 'selling')"""),
                                    {'cit_id' : citizen.cit_id, 'quant' : drug_quant, 'name' : drug_name})

        print(narcos_delivered)
        if len(narcos_delivered) == 0:
            return "Cannot create narcotics: No substances in inventory!"

        for narco in narcos_delivered: # Switch "owned" to selling, insert listing into market
            # connection.execute(sqlalchemy.text("UPDATE inventory SET status = 'selling' WHERE name = :drug_name and citizen_id = :cit_id"),
            #                         {'drug_name' : narco.name, 'cit_id' : citizen.cit_id})
            
            price = narco.quantity * narco.price
            
            connection.execute(sqlalchemy.text(
                """
                    INSERT INTO market (name, type, price, quantity, seller_id)
                    VALUES (:name, 'narcos', :price, :quantity, :cit_id)                           
                """),[{'name' : narco.name, 'price': price,  'quantity': narco.quantity, 'cit_id': citizen.cit_id}])

    print(f"narcos delievered: {narcos_delivered}")

    return f"Narcos delievered: {narcos_delivered}"