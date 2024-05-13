from fastapi import APIRouter

router = APIRouter()


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
