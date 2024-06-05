from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
from enum import Enum
import sqlalchemy
from src import database as db
import src.api.citizen as citizen

router = APIRouter(
    prefix="/transaction",
    tags=["transaction"],
    dependencies=[Depends(auth.get_api_key)],
)

@router.post("/")
def start_transaction():
    """init a transaction, insert to transaction table with civ id"""

    if citizen.cit_id < 0:
        return "ERROR: not logged in."

    with db.engine.begin() as connection:
        id = connection.execute(
            sqlalchemy.text(
                "INSERT INTO transactions (buyer_id) VALUES (:civilian_id) RETURNING transaction_id"
            ),
            [
                {
                    "civilian_id": citizen.cit_id
                }
            ],
        ).scalar_one()

    return {"transaction_id": id}


@router.post("/items/{transaction_id}/{listing_id}")
def add_items(transaction_id: int, listing_id: int):
    """insert item into transaction_items table with product_sku"""

    print(f"cart: {transaction_id} listing_id: {listing_id}")

    if citizen.cit_id < 0:
        return "ERROR: not logged in."

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


@router.post("/checkout/{transaction_id}")
def checkout(transaction_id: int):
    """subtract voidex from inventory, 
    add voidex to seller_id inventory, 
    subtract product from seller inv, 
    add to buyer inv"""

    if citizen.cit_id < 0:
        return "ERROR: not logged in."
    
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
                    SELECT market.seller_id as seller, market.quantity as quantity, market.type as type, market.name as name, 'selling' as status
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

        connection.execute(
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
        )

        quantity = connection.execute(
            sqlalchemy.text(
                """
                DELETE FROM market
                WHERE id = (SELECT listing_id FROM transaction_items WHERE transaction_id = :transaction_id)
                RETURNING quantity
                """
            ), 
            [{"transaction_id": transaction_id}]
        ).scalar_one()

    return {"quantity": quantity, "voidex_paid": price}