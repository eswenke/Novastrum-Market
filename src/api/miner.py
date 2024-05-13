from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth

router = APIRouter(
    prefix="/civilian/miner",
    tags=["miner"],
    dependencies=[Depends(auth.get_api_key)],
)

class Substance(BaseModel):
    name: str
    planet_id: str
    quantity: int
    price: int
    
@router.post("/deliver")
def post_substance(subst_delivered: list[Substance]):
    """adds to substance table after mining, reduce miner voidex inventory"""

    print(f"substances delievered: {subst_delivered}")
    return "OK"


@router.post("/plan")
def create_miner_plan():
    """ gets substances from current planet, creates plan for mining substance on planet """

    return [
        {
            "name": "string",
            "quantity": int,
            "price": int
        }
    ]

