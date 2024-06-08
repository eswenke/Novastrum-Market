# distribution of rows

- citizens: 160,001 rows
- inventory: 359,975 rows
- bids: 160,000 rows
- market: 80,187 rows
- transactions: 160,000
- transaction_items: 160,000
- planets table: 5 rows
- narcos table: 6 rows
- substances table: 5 rows
- wars table: 3 rows

- total: 1,080,181 rows

- Mainly, 5 tables are going to fill up the fastest with data in a real world production scenario with our project. These 5 would be the transactions and transaction_items table, the bids table, the inventory table, and the citizens table. The transaction related tables will fill up because the purpose of the black market is to facilitate transactions for customers, and so their 'cart' and the reference to the market listing they wish to buy are going to be pieces of data that fill up these tables fast. In a more efficient structure of this style transactions, we would probably only need 1 table and 1 enpoint that contains the id of the transaction and the id of the market listing. The bids table would also fill up quite fast, assuming most citizens like to gamble on the black market. It collects bids from every citizen and on every war in a ledger style, which allows easier querying for awarding money back upon a successful gamble. This ledger style would blow up the table quite a bit. Lastly, the citizens table and the attached inventory table for each citizen would also grow fast in size. The more citizens, the bigger that table becomes. The inventory for each citizen could potentially be composed of over 10 items, meaning the inventory table has the potential to be 10x the size of the citizens table. In this distribution, I kept the inventory relatively small in comparison to how it might get in the future - something I realized that, after reflection, might skew the row distribution a bit less toward what inventory might actually be scaled to be in a real production envrionment. But not every citizen is the same, so some inventories will naturally be smaller than others and the 10x number is highly unlikely. The rest of our tables are pre-set entities that are referenced by id or name in a relational style. They will not increase in size, and if they do, it will be via addition to the game's elements by a dev's hand and will not account for a significant size increase. In the future, if we decided wars are supposed to be waged infinitely, that would increase the wars table a lot as well. However, I don't foresee the game being played that way, and so I don't see that table expanding much either. This is a current functionality of the government official (they may start as many wars as they want), but this is more unintended than it is a feature.

# endpoint execution times (ms)

- inventory audit: 24.57451820373535 ms
- inventory promote: 31.912565231323242 ms

- transaction: 32.666683197021484 ms
- transaction items: 37.029266357421875 ms
- checkout: 55.73248863220215 ms

- market: 1078.0811309814453 ms

- government: 64.03136253356934 ms

- chemist: 63.29703330993652 ms

- narco: 43.5178279876709 ms

- miner: 81.86125755310059 ms

- citizen create: 274.5668888092041 ms
- citizen login: 127.87461280822754 ms
- citizen logout: 0.0 ms

- make bid: 47.19901084899902 ms
- end bid: 8725.508451461792 ms
- get wars: 24.649381637573242 ms

# 3 slowest endpoints

## citizen login:

| QUERY PLAN                                                                      |
| ------------------------------------------------------------------------------- |
| Limit  (cost=0.00..4053.01 rows=1 width=4)                                      |
|   ->  Seq Scan on citizens  (cost=0.00..4053.01 rows=1 width=4)                 |
|         Filter: ((name ~~ 'governor'::text) AND (password ~~ 'password'::text)) |

- I'm going to add an index on the name and password combination to try and speed up the scan.
- CREATE INDEX name_pass_idx ON citizens (name, password);

| QUERY PLAN                                                                         |
| ---------------------------------------------------------------------------------- |
| Limit  (cost=0.42..8.45 rows=1 width=4)                                            |
|   ->  Index Scan using name_pass_idx on citizens  (cost=0.42..8.45 rows=1 width=4) |
|         Index Cond: ((name = 'governor'::text) AND (password = 'password'::text))  |
|         Filter: ((name ~~ 'governor'::text) AND (password ~~ 'password'::text))    |

- This query significantly improved performance by around 4050 ms.

| QUERY PLAN                                                                      |
| ------------------------------------------------------------------------------- |
| Limit  (cost=0.00..4053.01 rows=1 width=7)                                      |
|   ->  Seq Scan on citizens  (cost=0.00..4053.01 rows=1 width=7)                 |
|         Filter: ((name ~~ 'governor'::text) AND (password ~~ 'password'::text)) |

- The prior index I created will also speed up this query as well.

| QUERY PLAN                                                                         |
| ---------------------------------------------------------------------------------- |
| Limit  (cost=0.42..8.45 rows=1 width=7)                                            |
|   ->  Index Scan using name_pass_idx on citizens  (cost=0.42..8.45 rows=1 width=7) |
|         Index Cond: ((name = 'governor'::text) AND (password = 'password'::text))  |
|         Filter: ((name ~~ 'governor'::text) AND (password ~~ 'password'::text))    |

- In the future, we could definitely combine these queries into one to improve performance, considering they are essentially the same query.

## end bid:

| QUERY PLAN                                                            |
| --------------------------------------------------------------------- |
| Index Scan using wars_pkey on wars  (cost=0.15..8.17 rows=1 width=64) |
|   Index Cond: (id = 3)                                                |

- No improvement needed.

| QUERY PLAN                                                                            |
| ------------------------------------------------------------------------------------- |
| Update on inventory  (cost=11054.34..11065.47 rows=0 width=0)                         |
|   InitPlan 1 (returns $0)                                                             |
|     ->  Aggregate  (cost=11045.73..11045.74 rows=1 width=8)                           |
|           ->  Hash Join  (cost=2722.77..10941.31 rows=41768 width=4)                  |
|                 Hash Cond: (i.citizen_id = b.citizen_id)                              |
|                 ->  Seq Scan on inventory i  (cost=0.00..7796.70 rows=160693 width=4) |
|                       Filter: (type = 'voidex'::text)                                 |
|                 ->  Hash  (cost=2221.65..2221.65 rows=40090 width=8)                  |
|                       ->  Seq Scan on bids b  (cost=0.00..2221.65 rows=40090 width=8) |
|                             Filter: ((planet <> 'Pyre'::text) AND (war_id = 3))       |
|   InitPlan 2 (returns $1)                                                             |
|     ->  Index Scan using wars_pkey on wars  (cost=0.15..8.17 rows=1 width=4)          |
|           Index Cond: (id = 3)                                                        |
|   ->  Index Scan using unique_entry on inventory  (cost=0.42..11.56 rows=2 width=10)  |
|         Index Cond: (citizen_id = $1)                                                 |

- For the above query plan, I will insert indexes on the type in inventory, along with the planet, war_id pairing in bids.
- CREATE INDEX inv_type_idx ON inventory (type);
- CREATE INDEX bids_planet_war_id_idx ON bids (planet, war_id);

| QUERY PLAN                                                                                            |
| ----------------------------------------------------------------------------------------------------- |
| Update on inventory  (cost=10361.16..10372.29 rows=0 width=0)                                         |
|   InitPlan 1 (returns $0)                                                                             |
|     ->  Aggregate  (cost=10352.55..10352.56 rows=1 width=8)                                           |
|           ->  Hash Join  (cost=4520.59..10248.13 rows=41768 width=4)                                  |
|                 Hash Cond: (i.citizen_id = b.citizen_id)                                              |
|                 ->  Bitmap Heap Scan on inventory i  (cost=1797.82..7103.52 rows=160696 width=4)      |
|                       Recheck Cond: (type = 'voidex'::text)                                           |
|                       ->  Bitmap Index Scan on inv_type_idx  (cost=0.00..1757.64 rows=160696 width=0) |
|                             Index Cond: (type = 'voidex'::text)                                       |
|                 ->  Hash  (cost=2221.65..2221.65 rows=40090 width=8)                                  |
|                       ->  Seq Scan on bids b  (cost=0.00..2221.65 rows=40090 width=8)                 |
|                             Filter: ((planet <> 'Pyre'::text) AND (war_id = 3))                       |
|   InitPlan 2 (returns $1)                                                                             |
|     ->  Index Scan using wars_pkey on wars  (cost=0.15..8.17 rows=1 width=4)                          |
|           Index Cond: (id = 3)                                                                        |
|   ->  Index Scan using unique_entry on inventory  (cost=0.42..11.56 rows=2 width=10)                  |
|         Index Cond: (citizen_id = $1)                                                                 |

- There was marginal improvement in the aggregate cost by around 700 ms, but this is still incredible slow. I don't know what
more to add in terms of indexes in order to speed this up further. The type index created the improvement, but the pair of 'planet' and 'war_id' did not change anything.

| QUERY PLAN                                                                                 |
| ------------------------------------------------------------------------------------------ |
| Update on inventory  (cost=6895.17..17209.76 rows=0 width=0)                               |
|   ->  Hash Join  (cost=6895.17..17209.76 rows=93403 width=22)                              |
|         Hash Cond: (inventory.citizen_id = c.id)                                           |
|         ->  Seq Scan on inventory  (cost=0.00..6896.76 rows=359976 width=14)               |
|         ->  Hash  (cost=6394.92..6394.92 rows=40020 width=24)                              |
|               ->  Hash Join  (cost=2721.90..6394.92 rows=40020 width=24)                   |
|                     Hash Cond: (c.id = b.citizen_id)                                       |
|                     ->  Seq Scan on citizens c  (cost=0.00..3253.01 rows=160001 width=10)  |
|                     ->  Hash  (cost=2221.65..2221.65 rows=40020 width=14)                  |
|                           ->  Seq Scan on bids b  (cost=0.00..2221.65 rows=40020 width=14) |
|                                 Filter: ((war_id = 3) AND (planet = 'Pyre'::text))         |

- I don't know what indexes to add here in order to speed up performance. I added the planet, war_id pairing index in the last query, so that seems to have very marginally improved the performace by around 50 ms. The query plan immediately below is the updated query after that pairing was added.

| QUERY PLAN                                                                                                              |
| ----------------------------------------------------------------------------------------------------------------------- |
| Update on inventory  (cost=6848.32..17178.45 rows=0 width=0)                                                            |
|   ->  Hash Join  (cost=6848.32..17178.45 rows=94398 width=22)                                                           |
|         Hash Cond: (inventory.citizen_id = c.id)                                                                        |
|         ->  Seq Scan on inventory  (cost=0.00..6899.82 rows=359982 width=14)                                            |
|         ->  Hash  (cost=6348.07..6348.07 rows=40020 width=24)                                                           |
|               ->  Hash Join  (cost=2675.05..6348.07 rows=40020 width=24)                                                |
|                     Hash Cond: (c.id = b.citizen_id)                                                                    |
|                     ->  Seq Scan on citizens c  (cost=0.00..3253.01 rows=160001 width=10)                               |
|                     ->  Hash  (cost=2174.80..2174.80 rows=40020 width=14)                                               |
|                           ->  Bitmap Heap Scan on bids b  (cost=554.50..2174.80 rows=40020 width=14)                    |
|                                 Recheck Cond: ((planet = 'Pyre'::text) AND (war_id = 3))                                |
|                                 ->  Bitmap Index Scan on bids_planet_war_id_idx  (cost=0.00..544.49 rows=40020 width=0) |
|                                       Index Cond: ((planet = 'Pyre'::text) AND (war_id = 3))                            |

| QUERY PLAN                                                                      |
| ------------------------------------------------------------------------------- |
| Update on planets  (cost=8.32..13.66 rows=0 width=0)                            |
|   ->  Bitmap Heap Scan on planets  (cost=8.32..13.66 rows=2 width=10)           |
|         Recheck Cond: (planet = ANY ('{Pyre,Zentharis}'::text[]))               |
|         ->  Bitmap Index Scan on planets_pkey  (cost=0.00..8.32 rows=2 width=0) |
|               Index Cond: (planet = ANY ('{Pyre,Zentharis}'::text[]))           |

- No improvements to be made.

| QUERY PLAN                                                      |
| --------------------------------------------------------------- |
| Delete on bids  (cost=0.00..2021.38 rows=0 width=0)             |
|   ->  Seq Scan on bids  (cost=0.00..2021.38 rows=80110 width=6) |
|         Filter: (war_id = 3)                                    |

- In order to speed up this endpoint, I'm going to add an index on the war id in bids to speed up the deletion
- CREATE INDEX war_id_idx ON bids (war_id);

| QUERY PLAN                                                      |
| --------------------------------------------------------------- |
| Delete on bids  (cost=0.00..2021.38 rows=0 width=0)             |
|   ->  Seq Scan on bids  (cost=0.00..2021.38 rows=80110 width=6) |
|         Filter: (war_id = 3)                                    |

- This led to no improvemnet, probably because the data is too small.

| QUERY PLAN                                                                 |
| -------------------------------------------------------------------------- |
| Delete on wars  (cost=0.15..8.17 rows=0 width=0)                           |
|   ->  Index Scan using wars_pkey on wars  (cost=0.15..8.17 rows=1 width=6) |
|         Index Cond: (id = 3)                                               |

- No improvements to be made

- Overall, only a couple of indexes made marginal differences in the run time here. It seems the joins take up the majority of the cost, so structuring our tables differently may be the way to move forward with improving execution in the future.

## market:

| QUERY PLAN                                                   |
| ------------------------------------------------------------ |
| Seq Scan on market  (cost=0.00..1515.87 rows=80187 width=39) |

- This returns all listings on the market. I don't know how adding an index here would help performance. In reality, the way I would improve the speed of this endpoint would be to have some sort of page system akin to the potion shop, where only a certain amount of results are returns at one time, and you could filter by search criteria to narrow down the results even further.