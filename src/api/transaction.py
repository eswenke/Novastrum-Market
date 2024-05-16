from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
from enum import Enum
import sqlalchemy
from src import database as db

router = APIRouter(
    prefix="/transaction",
    tags=["transaction"],
    dependencies=[Depends(auth.get_api_key)],
)

class Civilian(BaseModel):
    civilian_id: int
    name: str
    role: str
    home: str
    num_strikes: int

@router.post("/")
def start_transaction(new_cart: Civilian):
    """init a transaction, insert to transaction table with civ id"""

    with db.engine.begin() as connection:
        id = connection.execute(
            sqlalchemy.text(
                "INSERT INTO transactions (buyer_id) VALUES (:civilian_id) RETURNING transaction_id"
            ),
            [
                {
                    "civilian_id": new_cart.civilian_id
                }
            ],
        ).scalar_one()

    return {"transaction_id": id}


@router.post("/{transaction_id}/{listing_id}")
def add_items(transaction_id: int, listing_id: int):
    """insert item into transaction_items table with product_sku"""

    print(f"cart: {transaction_id} listing_id: {listing_id}")

    with db.engine.begin() as connection:
        connection.execute(
            sqlalchemy.text(
                """
                INSERT INTO transaction_items (transaction_id, listing_id)
                VALUES (:transaction_id, :listing_id)"""
            ),
            [{"transaction_id": transaction_id, "listing_id": listing_id}],
        )

    return "OK"


@router.post("/{transaction_id}/checkout")
def checkout(transaction_id: int):
    """subtract voidex from inventory, 
    add voidex to seller_id inventory, 
    subtract product from seller inv, 
    add to buyer inv"""

    # need to make sure the listing gets taken off the market
    
    with db.engine.begin() as connection:
        price = connection.execute(
            sqlalchemy.text(
                """
                WITH target AS (
                    SELECT transaction_items.listing_id AS listing, transactions.buyer_id as buyer
                    FROM transactions
                    JOIN transaction_items ON transactions.transaction_id = transaction_items.transaction_id
                    WHERE transaction_items.transaction_id = :transaction_id
                ),
                source AS (
                    SELECT buyer, market.quantity as quantity, market.price as price, market.type as type, market.name as name, 'owned' as status
                    FROM target
                    JOIN market ON listing = market.id
                    ORDER BY market.timestamp desc
                    LIMIT 1
                )
                INSERT INTO inventory (citizen_id, quantity, type, name, status)
                SELECT source.buyer, source.quantity, source.type, source.name, source.status
                FROM source
                ON CONFLICT (citizen_id, type, name, status)
                DO UPDATE SET quantity = inventory.quantity + (SELECT source.quantity FROM source)
                WHERE inventory.citizen_id = (SELECT source.buyer FROM source)
                AND inventory.name = (SELECT source.name FROM source)
                AND inventory.type = (SELECT source.type FROM source)
                AND inventory.status = (SELECT source.status FROM source)
                RETURNING (SELECT source.price FROM source);
                """
            ),
            [{"transaction_id": transaction_id}]
        ).scalar_one()

        connection.execute(
            sqlalchemy.text(
                """
                UPDATE inventory
                SET quantity = quantity - :price
                WHERE citizen_id = (SELECT buyer_id FROM transactions WHERE transaction_id = :transaction_id)
                AND type = 'voidex'
                """
            ),
            [{"price": price, "transaction_id": transaction_id}]
        )

        seller_id = connection.execute(
            sqlalchemy.text(
                """
                WITH target AS (
                    SELECT transaction_items.listing_id AS listing
                    FROM transactions
                    JOIN transaction_items ON transactions.transaction_id = transaction_items.transaction_id
                    WHERE transaction_items.transaction_id = :transaction_id
                ),
                source AS (
                    SELECT market.seller_id as seller, market.quantity as quantity, market.type as type, market.name as name, 'owned' as status
                    FROM target
                    JOIN market ON listing = market.id
                    ORDER BY market.timestamp desc
                    LIMIT 1
                )
                UPDATE inventory SET quantity = inventory.quantity - (SELECT source.quantity FROM source)
                WHERE inventory.citizen_id = (SELECT source.seller FROM source)
                AND inventory.name = (SELECT source.name FROM source)
                AND inventory.type = (SELECT source.type FROM source)
                AND inventory.status = (SELECT source.status FROM source)
                RETURNING (SELECT source.seller FROM source);
                """
            ),
            [{"transaction_id": transaction_id}]
        ).scalar_one()

        quantity = connection.execute(
            sqlalchemy.text(
                """
                UPDATE inventory
                SET quantity = quantity + :price
                WHERE citizen_id = :seller_id
                AND type = 'voidex'
                RETURNING quantity
                """
            ),
            [{"price": price, "seller_id": seller_id}]
        ).scalar_one()

        connection.execute(
            sqlalchemy.text(
                """
                DELETE FROM market
                WHERE id = (SELECT listing_id FROM transaction_items WHERE transaction_id = :transaction_id)
                """
            ), 
            [{"transaction_id": transaction_id}]
        )

    #   CASE govt:
    #       bid logic, do at a later time for complexity reasons
    #       civilians who bid will pick a side to bet on (higher than the minimum bet set in the listing)
    #       civilian bid id set to that war_id in the listing's 'name', 
    #           store the amount they bid, and what planet they bid on
    #       need a way to keep track of the total bids for either side
    #       once that war comes to a close, civilians who bid on the winning planet get 2.5x their bid
    #       those who bid on the losing planet will get nothing
    #       the govt official who created the bid gets all the losing bid money
    #       potentially create a bid file with bid plan/deliver?

    # before testing:
    #   NEED TO GIVE ALL CIVILIANS AT LEAST 100 VOIDEX AS DEFAULT INVENTORY.

    return {"quantity": quantity, "voidex_paid": price}