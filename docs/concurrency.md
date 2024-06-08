**Read Phenomenon Summaries:**
* Dirty Read: transaction reads data written by another uncommitted transaction. 
* Non-Repeatable Read: Transaction reads the same row twice and gets different values each time because another transaction modified data and committed between reads. 
* Phantom Read: Transaction reads set of rows that satisfy a condition, another transaction inserts/deletes rows satisfying condition, leading to different results if transaction re-reads

**Concurrency control mechanisms used in the Novastrum Market:**
* Serializable isolation level set in checkout function to ensure the most strict level of isolation for a vital function- and to prevent dirty reads, non-repeatable reads, and phantom reads.
* Pessimistic concurrency control: Using for update to lock rows in chemist and miner functions so other transactions can't use specific resources at the same time. 

**Cases where we may encounter a phenomenon:**
* miner.py
  * Non-repeatable Reads: The quantity of the substance could be updated by another transaction after it is initially read, but before it is updated in the substances table || When checking if the substance already exists in the inventory, if chemist transactions occur and rows are modified from miner inventory, the set of values retrieved from miner inventory will change. 
* _chemist.py:_
  * Non-repeatable Reads: Suppose transaction T1 retrieves a set of rows for matching drug by name in chemist inventory. Now, Transaction T2 updates quantity of the chemist drug inventory after a customer purchase. If transaction T1 re-executes the statement that reads the rows, it gets a different set of values this time.
* _transaction.py_
  * Dirty reads: In checkout, if the inventory or market table that another transaction has written but not committed.
  * Phantom Reads: In checkout, when reading items from the market and the inventory, another transaction could delete rows on the market table, or add to the inventory rows – leading to different results if the transaction re-reads. 
