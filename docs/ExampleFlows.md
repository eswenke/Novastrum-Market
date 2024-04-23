**Example Civilian Buying A Narcotic:**
Theodore is a civilian who is a new user on the Novastrum market. He is looking to explore space narcotics after hearing about the incredible reactions that his friend Alvin experienced from synth. First, Theo requests the listings to see the latest offerings available on the Novamarket GET /market_listings/narcos. He sees in the listings that there are 9 synth pods available with SKU "SYNTH_02" at a reasonable price of 70 voidex each.
Theadore, with a plentiful amount of Voidex, initiates a purchase of 2 synth
* starts by calling POST /carts to get a new cart with ID “Theodore-[randomized id]”
* then Theo calls POST /carts/$id/narcos/SYNTH_02 and passes in a quantity of 2.
* he calls POST /carts/9001/checkout to finish her checkout. T
* he checkout charges him 140 voidex and adds 2 synth to his inventory. 

**Example Miner Mining Minerals and Selling to chemists:**
Thorgin Fluxcore is a miner on the Novastrum market. He is looking to explore and harvest on Sylvaria after noticing a spike in price for the resources found there, due to its main derivative, Quantum Bliss, being in short supply. First, Thorgin pays and requests a random deposit on Sylvaria, hoping to strike “gold”. He calls GET /miner/plan and passes “Sylvaria” and “Deposit_2” returning a mine-ID. This gives access to GET /miner/deliver/mine-ID.  He sees his efforts have paid off, 20 kilos of rich Quantonium ore!: SKU "QUANT_ORE_01" which at the elevated going rate, will fetch him 35 voidex each.

To do so, 
* He creates a listing on the Novastrum Market by calling POST /market_sales to return a listing ID of 123
* Then Thorgin calls POST /market_listings/minerals/123/QUANT_ORE_01 and passes a quantity of 10, not too eager to lower the price by increasing supply.
* Should an interested buyer purchase his listing, he will be granted the 350 voidex and deducted 10 Quantonium Ore.

**Example Government Official Swaying Results of a Space War:**
Griva Tane is a government official on Ecliptix. She has recently placed a high-risk bet on the Siege of Lyxion IV’s main trading city by an aggressing faction. As losing the bet would mean ruin for her, or worse, getting caught caught, Griva would like to supply a little “help” to the defending people of the city. 
To do so, 
* She calls POST /wars/Lyxion_IV/support and passes 300 voidex in favor of the defense. This directly increases the chances of the defending side winning
* When the battle has concluded, she may call GET /wars/Lyxion_IV/bet_ID to receive her winnings or know she has lost it all. 
Given she is a government official and meddling with wars is highly illegal, there is a chance she will be stripped of her title and imprisoned upon going to collect her winnings.

etc. 
**Example Chemist Creating Narcotic:**
Bob is a chemist who has at least 20 drugs on the Novastrum market. He is looking to create space narcotics after hearing about the incredible reactions that his chemist friend Joe produced with synth. First, Bob requests his plan to see the recipes available on the Novamarket GET /market_listings/minerals. He sees in the recipes that there is an availability of 10 quantonium ore! Oh Joy! He could use this with some of his synthus to create a variation of synthpods, MEGASYNTH . . .
