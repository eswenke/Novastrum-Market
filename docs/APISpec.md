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

```json
[
    {
        "role": "string", 
    }
]
```

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

### Get Market Listing - `/market_listing/` (GET)

Retrieves the a market list of items. Each unique item combination should have only a single price.

**Returns**:

```json
[
    {
        "seller_id" : "string",
        "item_type" : "string",
        "name": "string",
        "quantity": "integer", /* Between 1 and 10000 */
        "price": "integer", /* Between 1 and 500 */
    }
]
```

### Post Market Listing - `/transactions/` (POST)

Create a transaction.

**Request**:

```json
[
    {
        "civilian_id" : "integer",
        "transaction_id" : "integer"
    }
]
```

**Return**:

```json
[
    {
        "transaction_id" : "integer"
    }
]
```

### Adding Item to Transaction - `/transactions/{transaction_id}/items/{items_name}` (PUT)

**Request**:

```json
[
    {
        "quantity" : "integer"
    }
]
```

**Respons**:

```json
[
    {
        "success" : "boolean"
    }
]
```

/chemist/plan

/chemist/deliver

/miner/plan

/miner/deliver

/govt/plan

