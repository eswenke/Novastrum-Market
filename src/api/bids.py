from fastapi import APIRouter, Depends
from enum import Enum
from pydantic import BaseModel
from src.api import auth
import sqlalchemy
from src import database as db
from src.api.govt import War
import src.api.citizen as citizen
import random

router = APIRouter(
    prefix="/bids",
    tags=["bids"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/make_bid/{war_id}")
def make_bid(war_id: int, bid: int, planet: str):
    """make a bid on the war"""
    
    if citizen.cit_id < 0:
        return "ERROR: Not logged in."

    with db.engine.begin() as connection:
        min_bid = connection.execute(
            sqlalchemy.text(
                """ 
                select price
                from market
                where type = 'wars' and name = :war_id
                """
            ), [{"war_id": str(war_id)}]
        ).scalar_one

        print(f"war bid on: {war_id}")

        gold = connection.execute(
            sqlalchemy.text(
                """ 
                select quantity
                from inventory
                where type = 'voidex' and citizen_id = :citizen_id
                """
            ), [{"citizen_id": citizen.cit_id}]
        ).scalar_one()

        if gold < min_bid or gold < bid:
            return "ERROR: not enough gold"
        
        connection.execute(
            sqlalchemy.text(
                """ 
                insert into bids (citizen_id, war_id, bid_amount, planet)
                values (:citizen_id, :war_id, :gold, :planet)
                """
            ), [{"citizen_id": citizen.cit_id, "war_id": war_id, "gold": gold, "planet": planet}]
        )
        
    return "OK"


@router.post("/end/{war_id}")
def end_bidding(war: War):
    """ end the war and awards all winning bids """

    if citizen.cit_id < 0:
        return "ERROR: not logged in."
    
    if citizen.role != 'govt':
        return "ERROR: only government official's have access to this role."

    winner = random.random()

    with db.engine.begin() as connection:
        print(f"war ended: {war.war_id}")

        # get the winning planet
        winning_planet = connection.execute(
            sqlalchemy.text(
                """ 
                select
                    (case when :winner = 0 then planet_1
                    else planet_2 end)
                from wars
                where id = :war_id
                """
            ), [{"winner": winner, "war_id": war.war_id}]
        ).first()[0]

        # update govt official's gold with the loss from the bid
        connection.execute(
            sqlalchemy.text(
                """ 
                with govt as (
                    select
                        sum(b.bid_amount) as loss
                    from bids b
                    join inventory i on i.citizen_id = b.citizen_id
                    where b.war_id = :war_id and not b.planet = :planet and i.type = 'voidex'
                )
                update inventory
                set quantity = quantity + (select loss from govt)
                where citizen_id = (select citizen_id from wars where id = :war_id)
                """
            ), [{"war_id": war.war_id, "planet": winning_planet}]
        )

        # update all winner's gold
        connection.execute(
            sqlalchemy.text(
                """ 
                with cit_bids as (
                    select
                        *
                    from bids b
                    join citizens c on c.id = b.citizen_id
                    where b.war_id = :war_id and b.planet = :planet
                )
                update inventory
                set quantity = quantity + 1.5 * cit_bids.bid_amount
                from cit_bids
                where cit_bids.id = inventory.citizen_id
                """
            ), [{"war_id": war.war_id, "planet": winning_planet}]
        )

        # delete listing
        connection.execute(
            sqlalchemy.text(
                """
                DELETE FROM wars
                WHERE id = :war_id
                """
            ), 
            [{"war_id": str(war.war_id)}]
        )


    return

@router.post("/get_wars")
def get_wars():
    """make a bid on the war"""
    
    if citizen.cit_id < 0:
        return "ERROR: not logged in."

    with db.engine.begin() as connection:
        result = connection.execute(
            sqlalchemy.text(
                """ 
                select * from wars
                """
            )
        ).fetchall()

        wars = []
        
        for row in result:
            print(row)
            id, planet_1, planet_2, citizen_id, min_bid = row
            wars.append({
                "id": id,
                "planet 1": planet_1,
                "planet 2": planet_2,
                "citizen id": citizen_id,
                "min bid": min_bid
            })
        
    return wars