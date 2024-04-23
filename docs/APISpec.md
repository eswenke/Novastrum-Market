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

/status : {role, voidex, narcos_owned: {narco, quant}} …

/market_listings: {narcos{name, proportions of ms}, mineable substances:{name, planet-origin}}

/carts

/chemist/plan

/chemist/deliver

/miner/plan

/miner/deliver

/govt/plan

