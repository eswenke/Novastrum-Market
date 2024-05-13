from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import math

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/audit")
def get_inventory():
    """ 
    returns personal inventory
    """
    
    return {"num_narcos": 0, "num_substances": 0, "num_voidex": 0}

# Gets called once a day
@router.post("/plan")
def get_promotion_plan():
    """ 
    gets civilian info, checks narco quota, and executes role promotion if above the required amount.
    tier 1- civilians
    tier 2- miners (5 narcos owned)
    tier 3- chemist (20 narcos owned)
    tier 4- govt offical (30 narcos owned)

    """

    return "OK" # || error if not enough to promote

class CapacityPurchase(BaseModel):
    potion_capacity: int
    ml_capacity: int

# Gets called once a day
@router.post("/reset")
def reset_inventory():
    """ 
    resets inventory to state 0 narcos, 0 substances, 100 voidex
    """

    return "OK"
