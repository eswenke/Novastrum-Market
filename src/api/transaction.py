from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel
from src.api import auth
from enum import Enum

router = APIRouter(
    prefix="/transaction",
    tags=["transaction"],
    dependencies=[Depends(auth.get_api_key)],
)

class Civilian(BaseModel):
    civilian_id: int
    name: str
    role: str
    home: str # planet name ?
    num_strikes: int

@router.post("/")
def start_transaction(new_cart: Civilian):
    """init a transaction, insert to transaction table with civ id"""
    return {"transaction_id": 1}


class TrItem(BaseModel):
    quantity: int

@router.post("/{transaction_id}/product/{product_sku}")
def add_items(transaction_id: int, product_sku: str, transaction_item: TrItem):
    """insert item into transaction_items table with product_sku"""

    return "OK"


class TrCheckout(BaseModel):
    payment: str

@router.post("/{transaction_id}/checkout")
def checkout(cart_id: int, cart_checkout: TrCheckout):
    """subtract voidex from inventory, add voidex to seller_id inventory, subtract product from seller inv, add to buyer inv"""

    return {"quantity": int, "voidex_paid": 50}
