from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.api import auth
import math
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.get("/audit/{citizen_id}")
def get_inventory(citizen_id: int):
    """ 
    returns personal inventory
    """
    with db.engine.begin() as connection:
        num_voidex = connection.execute(
            sqlalchemy.text(
                """
                SELECT quantity
                FROM inventory
                WHERE citizen_id = :citizen_id
                AND type = 'voidex';
                """
            ),
            [{"citizen_id": citizen_id}]
        ).scalar_one()

        num_narcos = connection.execute(
            sqlalchemy.text(
                """
                SELECT COALESCE(SUM(quantity), 0)
                FROM inventory
                WHERE citizen_id = :citizen_id
                AND type = 'narcos';
                """
            ),
            [{"citizen_id": citizen_id}]
        ).scalar_one()

        num_substances = connection.execute(
            sqlalchemy.text(
                """
                SELECT COALESCE(SUM(quantity), 0)
                FROM inventory
                WHERE citizen_id = :citizen_id
                AND type = 'substances';
                """
            ),
            [{"citizen_id": citizen_id}]
        ).scalar_one()

    
    return {"num_narcos": num_narcos, "num_substances": num_substances, "num_voidex": num_voidex}

# Gets called once a day
@router.post("/plan/{citizen_id}")
def get_promotion_plan(citizen_id: int):
    """ 
    gets civilian info, checks narco quota, and executes role promotion if above the required amount.
    tier 1- civilians
    tier 2- miners (5 narcos owned)
    tier 3- chemist (20 narcos owned)
    tier 4- govt offical (30 narcos owned)
    """

    promotion = 0
    with db.engine.begin() as connection:
        num_narcos, role = connection.execute(
            sqlalchemy.text(
                """
                SELECT COALESCE(SUM(inventory.quantity), 0) as quantity, citizens.role as role
                FROM inventory
                JOIN citizens ON inventory.citizen_id = citizens.id
                WHERE inventory.citizen_id = :citizen_id
                AND inventory.type = 'narcos'
                GROUP BY role
                """
            ),
            [{"citizen_id": citizen_id}]
        ).first()

        if (role == 'civilian' and num_narcos < 5) or (role == 'miner' and num_narcos < 5) or (role == 'chemist' and num_narcos < 20) or (role == 'govt' and num_narcos < 30):
            role = role
        else:
            promotion = 1
            if role == 'civilian' and num_narcos >= 5:
                role = 'miner'
            elif role == 'miner' and num_narcos >= 20:
                role = 'chemist'
            elif role == 'chemist' and num_narcos >= 30:
                role = 'govt'

    return {"promotion": promotion, "role": role} # || error if not enough to promote

class Promotion(BaseModel):
    promotion: int
    role: str

@router.post("/deliver/{citizen_id}")
def deliver_capacity_plan(promotion: Promotion, citizen_id: int):

    if promotion:
        with db.engine.begin() as connection:
            connection.execute(
                sqlalchemy.text(
                    """
                    UPDATE citizens SET role = :role
                    WHERE id = :citizen_id
                    """
                ),
                [{"citizen_id": citizen_id, "role": promotion.role}]
            )

    return {
        "promoted": promotion.promotion
    }
