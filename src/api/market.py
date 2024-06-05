from fastapi import APIRouter, Depends
from src.api import auth
import sqlalchemy
from src import database as db
import src.api.citizen as citizen


router = APIRouter(
    prefix="/market_listings",
    tags=["market"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/")
def get_market_listings():
    """
    returns all listings on the market. 
    """

    if citizen.cit_id < 0:
        return "ERROR: not logged in."

    listings = []

    with db.engine.begin() as connection:
        result = connection.execute(
                sqlalchemy.text(
                    """
                    SELECT * FROM market
                    """
                )
            ).fetchall()
        
        for row in result:
            print(row)
            id, name, type, price, quantity, seller_id, timestamp = row
            listings.append({
                "name": name,
                "type": type,
                "quantity": quantity,
                "price": price,
                "seller id": seller_id,
                "listing id": id
            })
        
    return listings
