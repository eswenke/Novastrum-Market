from fastapi import APIRouter, Depends
from enum import Enum
from pydantic import BaseModel
from src.api import auth

router = APIRouter(
    prefix="/civilian/govt",
    tags=["government"],
    dependencies=[Depends(auth.get_api_key)],
)

class War(BaseModel):
    war_id: int
    planet_1: str
    planet_2: str
    bid: int

@router.post("/deliver")
def commence_wars(wars_commenced: list[War]):
    """updates planet status to waring, post wars to gamble on to market
       * [seller_id, type = war, name, quantity??, bid] """
    
    print(f"wars commenced: {wars_commenced}")

    return "OK"

@router.post("/plan")
def get_war_plan():
    """
    gets planet status, randomly pairs up planets for wars 
    """

    return [
            {
                "war_id" : int,
                "planet_1": "string",
                "planet_2": "string",
                "initial_bid" : int
                # "length_bid" : int, **** we can wait on this and add in complexity phase
            }
        ]

if __name__ == "__main__":
    print(get_war_plan())