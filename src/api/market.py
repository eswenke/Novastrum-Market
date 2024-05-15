from fastapi import APIRouter, Depends
from src.api import auth
import sqlalchemy
from src import database as db

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
            id, quantity, price, seller_id, name, type, timestamp = row
            listings.append({
                "name": name,
                "type": type,
                "quantity": quantity,
                "price": price,
                "seller id": seller_id,
                "listing id": id
            })
        
    return listings
