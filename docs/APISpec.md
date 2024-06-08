ALL TIERS:
get all market listings, 
post transactions (purchase), 
get inventory, 
get promoted (except govt officials, already highest rank), 
consume narcotics, 
post space war bets

tier 1 - civilians (0 drugs)
no unique actions

tier 2 - miners (5 drugs)
post substances mined to market

tier 3 - chemist (20 drugs)
post narcotics brewed onto market

tier 4 - govt officials (30 drugs)
create wars to bid on, 
end bidding on those wars

## endpoints: 

### Get promotion - `/inventory/promote` (POST)

**Response**:

```json
[
    {
        "Successfully promoted to: {role}"
    }
]
```


### Get inventory - `/inventory/audit` (GET)

**Response**:

```json
[
    {
        "num_narcotics": "integer",
        "num_substances": "integer",
        "num_voidex": "integer"
    }
]
```


### Get Market Listings - `/market_listings` (GET)

Retrieves the a market list of items. Each unique item combination should have only a single price.

**Returns**:

```json
[
    {
        "name": "string",
        "type": "string",
        "quantity": "integer",
        "price": "integer",
        "seller id": "integer",
        "listing id": "integer"
    },
    ...
]
```


### Create Transaction - `/transactions` (POST)

Create a transaction.

**Response**:

```json
[
    {
        "transaction_id" : "integer"
    }
]
```


### Adding Item to Transaction - `/transactions/items/{transaction_id}/{listing_id}` (POST)


**Response**:

```json
[
    {
        "OK"
    }
]
```


### Checkout- `/transactions/checkout/{transaction_id}` (POST)


**Response**:

```json
[
    {
        "quantity": "integer",
        "voidex_paid": "integer"
    }
]
```


### Brew - `/civilian/brew` (POST)

**Response**:

```json
[
    {
        "Narcos delievered: {narcos_delivered}"
    }
]
```


### Mine `/civilian/mine` (POST)
### [COMPLEX ENDPOINT 1](../src/api/bids.py)

**Response**:

```json
[
    {
        "OK: {{'name': '{subst_data[0]}', 'planet': '{subst_data[1]}', 'quantity': {mining_amt}, 'price': '{subst_data[3]}'}}"
    }
]
```


### Start War - `/civilian/begin/wars` (POST)

**Response**:

```json
[
    {
        "{planet_1} at war with {planet_2}, minimum bid: {initial_bid}",
        ...
    }
]
```


### End War - `/bids/end/{war_id}` (POST)
### [COMPLEX ENDPOINT 2](../src/api/miner.py)

**Response**:

```json
[
    {
        "War ended! Winner: {winning_planet}!"
    }
]
```


### Get Wars - `/bids/get_wars` (GET)

**Response**:

```json
[
    {
        "id": "integer",
        "planet 1": "string",
        "planet 2": "string",
        "citizen id": "integer",
        "min bid": "integer"
    },
    ...
]
```


### Take Narcos - `/narcos/consume` (POST)

**Response**:

```json
[
    {
        "narcos consumed: {narcos_delivered}"
    }
]
```


### Create Citizen - `/citizen/create` (POST)

**Response**:

```json
[
    {
        "OK: User successfully created. Log into account."
    }
]
```


### Login - `/citizen/login` (POST)

**Response**:

```json
[
    {
        "OK: Successfully logged in. Welcome to the NovaStrum Market, {username}!"
    }
]
```


### Logout - `/citizen/logout` (POST)

**Response**:

```json
[
    {
        "OK: Successfully logged out."
    }
]
```
