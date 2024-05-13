from fastapi import APIRouter, Depends
from src.api import auth
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/market_listings",
    tags=["market"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/market_listings/", tags=["market_listings"])
def get_market_listings():
    """
    returns all listings on the market. 
    """

    return [
            {
                "seller_id": int,
                "product_type": "text",
                "product_sku": "text",
                "quantity": int,
                "price": 50,

            }
        ]
