from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth

router = APIRouter(
    prefix="/civilian/chemist",
    tags=["chemist"],
    dependencies=[Depends(auth.get_api_key)],
)

class Narcotic(BaseModel):
    name: str
    # type: list[int] **** maybe add later for complexity?
    quantity: int
    price: int
    
@router.post("/deliver")
def post_market_listings(narcos_delivered: list[Narcotic]):
    """insert narcos to market listings table,
    * [seller_id, type = narco, prod_sku, quant, price]"""

    print(f"narcos delievered: {narcos_delivered}")
    return "OK"

@router.post("/plan")
def create_chemist_plan():
    """ gets substances from subst table, 
    * creates plan for making narcos, 
    * add substances to chemist inventory
    * remove substance from table
    * reduce chemist voidex
    * increase miner voidex"""

    return [
        {
            "name": str,
            "quantity": int,
            "price": int
        }
    ]

