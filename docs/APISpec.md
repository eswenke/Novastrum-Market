tier 1 - civilians (0 drugs)
get list of substances on market narcotics
post orders (purchase)
get inventory
post space war bets

tier 2 - miners (5 drugs)
get list of substances on that planet
post substances to (materials mined on that tick)

tier 3 - chemist (20 drugs)
get list of mined substances 
/market_listings now reveals mineable subst
creates narcotics
post narcotics onto market
NOT ALLOWED: can’t be miner

tier 4 - govt officials (30 drugs)
post to imprison individuals
set winners of space wars
modify narcotics supply … etc
NOT ALLOWED: can’t be miner, can’t be chemist …  

## endpoints: 

/civilian_id/status

**Request:** (GET)
[
  {
  }
]

**Response:**
```json
[
    {
        "role": "string", 
    }
]
```

civilian_id/inventory

**Request:** (GET)
[
  {
  }
]

**Response:**
[
    {
        "num_voidex": int,
        "num_drugs": int,
        "num_substances": null or int
    }
]

/market_listings: {narcos{name, proportions of ms}, mineable substances:{name, planet-origin}}

Request: (GET)
[
  {
  }
]

Response:
``` json
[
    {
        "item": Narco, Bid, Substance,
        "item_id": int,
        "name": "String",
        "seller_id": "String",
        "price": int,
        "quantity": int
    }
]```

/carts

Request: (GET)
``` json
{
  "civilian_id": int,
  "transaction_id": int
} ```

Response:
``` json
[
    {
        "transaction_id": int
    }
]```
/chemist/plan

/chemist/deliver

/miner/plan

/miner/deliver

/govt/plan



```json
[
    {
        "name": "string", 
        "quantity": "integer", 
        "price": "integer", 
        "item_type": "string" /* can be narco, substance, or bid */
    }
]
```
