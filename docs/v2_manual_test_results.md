# flows

## SUBSTANCE TO NARCO TO PURCHASE FLOW:
- pick a miner
- call miner plan to figure how much to mine from their planet
- call miner deliver to put that substance in their inventoy and post a market listing for it
- pick a chemist
- get market listings to see the miner's listing
- chemist will create a transaction
- chemist will add that listing to their transaction
- chemist will checkout and add that substance to their inventory as 'owned', update the miners inventory, listing taken off
- call chemist plan to create the narcos from given substance in inventory
- call chemist deliver to change the 'owned' substances to 'selling' narcos, post it on market listing
- pick a civilian
- get market listings to see the chemists's listing
- civilian will create a transaction
- civilian will add the narcos listing to their transaction
- civilian will checkout their transaction, update their inventory, update the chemists inventory, listing taken off
- call inventory on audit on the citizen's id, miner's id, chemist's id
- get market to verify the listings have been taken off

curl -X 'POST' \
  'https://novastrum-market.onrender.com/civilian/miner/plan/2' \
  -H 'accept: application/json' \
  -H 'access_token: novastrum-market' \
  -d ''

response:
```json
{
  "name": "Siltrite",
  "planet": "Lyxion IV",
  "quantity": 218,
  "price": 2
}
```

curl -X 'POST' \
  'https://novastrum-market.onrender.com/civilian/miner/deliver/2' \
  -H 'accept: application/json' \
  -H 'access_token: novastrum-market' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "Siltrite",
  "planet": "Lyxion IV",
  "quantity": 218,
  "price": 2
}'

response:
```json
"OK"
```

curl -X 'GET' \
  'https://novastrum-market.onrender.com/market_listings/' \
  -H 'accept: application/json' \
  -H 'access_token: novastrum-market'

response:
```json
[
  {
    "name": "Siltrite",
    "type": "substance",
    "quantity": 218,
    "price": 436,
    "seller id": 2,
    "listing id": 1
  }
]
```

curl -X 'POST' \
  'https://novastrum-market.onrender.com/transaction/' \
  -H 'accept: application/json' \
  -H 'access_token: novastrum-market' \
  -H 'Content-Type: application/json' \
  -d '{
  "civilian_id": 3,
  "name": "citizen 3",
  "role": "chemist",
  "home": "Zentharis",
  "num_strikes": 0
}'

response:
```json
{
  "transaction_id": 1
}
```

curl -X 'POST' \
  'https://novastrum-market.onrender.com/transaction/items/1/1' \
  -H 'accept: application/json' \
  -H 'access_token: novastrum-market' \
  -d ''

response:
```json
"OK"
```

curl -X 'POST' \
  'https://novastrum-market.onrender.com/transaction/checkout/1' \
  -H 'accept: application/json' \
  -H 'access_token: novastrum-market' \
  -d ''

response:
```json
{
  "quantity": 218,
  "voidex_paid": 436
}
```

curl -X 'POST' \
  'https://novastrum-market.onrender.com/civilian/chemist/plan/3' \
  -H 'accept: application/json' \
  -H 'access_token: novastrum-market' \
  -d ''

response:
```json
[
  {
    "name": "SLT",
    "quantity": 21,
    "price": 8
  }
]
```

curl -X 'POST' \
  'https://novastrum-market.onrender.com/civilian/chemist/deliver/3' \
  -H 'accept: application/json' \
  -H 'access_token: novastrum-market' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "name": "SLT",
    "quantity": 21,
    "price": 8
  }
]'

response:
```json
"OK"
```

curl -X 'GET' \
  'https://novastrum-market.onrender.com/market_listings/' \
  -H 'accept: application/json' \
  -H 'access_token: novastrum-market'

response:
```json
[
  {
    "name": "SLT",
    "type": "narcos",
    "quantity": 21,
    "price": 168,
    "seller id": 3,
    "listing id": 2
  }
]
```

curl -X 'POST' \
  'https://novastrum-market.onrender.com/transaction/' \
  -H 'accept: application/json' \
  -H 'access_token: novastrum-market' \
  -H 'Content-Type: application/json' \
  -d '{
  "civilian_id": 1,
  "name": "citizen 1",
  "role": "civilian",
  "home": "Pyre",
  "num_strikes": 0
}'

response:
```json
{
  "transaction_id": 2
}
```

curl -X 'POST' \
  'https://novastrum-market.onrender.com/transaction/items/2/2' \
  -H 'accept: application/json' \
  -H 'access_token: novastrum-market' \
  -d ''

response:
```json
"OK"
```

curl -X 'POST' \
  'https://novastrum-market.onrender.com/transaction/checkout/2' \
  -H 'accept: application/json' \
  -H 'access_token: novastrum-market' \
  -d ''

response:
```json
{
  "quantity": 21,
  "voidex_paid": 168
}
```

curl -X 'GET' \
  'https://novastrum-market.onrender.com/inventory/audit/1' \
  -H 'accept: application/json' \
  -H 'access_token: novastrum-market'

response:
```json
{
  "num_narcos": 21,
  "num_substances": 0,
  "num_voidex": 332
}
```

curl -X 'POST' \
  'https://novastrum-market.onrender.com/inventory/plan/1' \
  -H 'accept: application/json' \
  -H 'access_token: novastrum-market' \
  -d ''

response:
```json
{
  "promotion": 1,
  "role": "miner"
}
```

curl -X 'POST' \
  'https://novastrum-market.onrender.com/inventory/deliver/1' \
  -H 'accept: application/json' \
  -H 'access_token: novastrum-market' \
  -H 'Content-Type: application/json' \
  -d '{
  "promotion": 1,
  "role": "miner"
}'

response:
```json
{
  "promoted": 1
}
```

- citizen 1, in a former civilian role, is now promoted to the role of 'miner'
- inventories of everyone involved in the pipeline have been updated appropriately
- market listings that were utilized are no longer on the market


## GOVT FLOW:
- call govt plan
- call govt deliver
- verify the space war has started in planets table/listing created on market for bidding

curl -X 'POST' \
  'https://novastrum-market.onrender.com/civilian/govt/plan' \
  -H 'accept: application/json' \
  -H 'access_token: novastrum-market' \
  -d ''

response:
```json
[
  {
    "war_id": 2,
    "planet_1": "Zentharis",
    "planet_2": "Ecliptix",
    "bid": 100
  },
  {
    "war_id": 3,
    "planet_1": "Lyxion IV",
    "planet_2": "Sylvaria",
    "bid": 100
  }
]
```

curl -X 'POST' \
  'https://novastrum-market.onrender.com/civilian/govt/deliver/4' \
  -H 'accept: application/json' \
  -H 'access_token: novastrum-market' \
  -H 'Content-Type: application/json' \
  -d '[
  {
    "war_id": 2,
    "planet_1": "Zentharis",
    "planet_2": "Ecliptix",
    "bid": 100
  },
  {
    "war_id": 3,
    "planet_1": "Lyxion IV",
    "planet_2": "Sylvaria",
    "bid": 100
  }
]'

```json
"OK"
```

curl -X 'GET' \
  'https://novastrum-market.onrender.com/market_listings/' \
  -H 'accept: application/json' \
  -H 'access_token: novastrum-market'

```json
[
  {
    "name": "2",
    "type": "wars",
    "quantity": 1,
    "price": 100,
    "seller id": 4,
    "listing id": 3
  },
  {
    "name": "3",
    "type": "wars",
    "quantity": 1,
    "price": 100,
    "seller id": 4,
    "listing id": 4
  }
]
```

- 2 wars have been started
- getting market listings shows they have been listed on the market with minimum bid pricing