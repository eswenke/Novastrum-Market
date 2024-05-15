-- SUBSTANCE TO NARCO TO PURCHASE FLOW:
-- pick a miner
-- call miner plan to figure how much to mine from their planet
-- call miner deliver to put that substance in their inventoy and post a market listing for it
-- pick a chemist
-- get market listings to see the miner's listing
-- chemist will create a transaction
-- chemist will add that listing to their transaction
-- chemist will checkout and add that substance to their inventory as 'owned', update the miners inventory, listing taken off
-- call chemist plan to create the narcos from given substance in inventory
-- call chemist deliver to change the 'owned' substances to 'selling' narcos, post it on market listing
-- pick a civilian
-- get market listings to see the chemists's listing
-- civilian will create a transaction
-- civilian will add the narcos listing to their transaction
-- civilian will checkout their transaction, update their inventory, update the chemists inventory, listing taken off
-- call inventory on audit on the citizen's id, miner's id, chemist's id
-- get market to verify the listings have been taken off

-- PROMOTION FLOW
-- assuming a citizen has x amount of inventory greater than their threshold (maunally put in or through the pipeline)
-- call promotion plan on that citizen's id
-- call promotion deliver on that citizen's id
-- verify they are now promoted

-- GOVT FLOW:
-- call govt plan
-- call govt deliver
-- verify the space war has started in planets table/listing created on market for bidding

## endpoint curl tests:

# example inventory audit test:
curl -X 'GET' \
  'https://novastrum-market.onrender.com/inventory/audit/3' \
  -H 'accept: application/json' \
  -H 'access_token: novastrum-market'

response:
{
  "num_narcos": 11,
  "num_substances": 25,
  "num_voidex": 100
}

# example inventory promotion test:
curl -X 'POST' \
  'https://novastrum-market.onrender.com/inventory/plan/3' \
  -H 'accept: application/json' \
  -H 'access_token: novastrum-market' \
  -d ''

response:
{
  "promotion": 0,
  "role": "miner"
}

curl -X 'POST' \
  'https://novastrum-market.onrender.com/inventory/deliver/3' \
  -H 'accept: application/json' \
  -H 'access_token: novastrum-market' \
  -H 'Content-Type: application/json' \
  -d '{
  "promotion": 0,
  "role": "miner"
}'

response:
{
  "promoted": 0
}


