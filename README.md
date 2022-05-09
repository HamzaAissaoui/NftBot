# NftBot
A bot that buys and sells Nfts with a profit margin, it consists of 3 parts


1. Scrapping:
    Every 3-5 hours, the bot will:
        - Open the app, go to the sneakers page
        - Apply a few filters on the sneakers list
        - Access each sneaker and save its information in the database (first 1000 sneakers at least)
        - (Important) : We should always keep the numeber of sneakers fixed (1000) and remove the oldest records every time
            - ID
            - Sneaker ID
            - Efficiency
            - Luck
            - Resilience
            - Attributes sum
            - Price
        
        - After We finish scrapping we fill the average prices inside the table in the database containing:
            - ID
            - minimum attribute sum (0.1, 1.1, 2.1 ... 29.1)
            - maximum attribute sum (1, 2, 3... 30)
            - Number of sneakers in this interval
            - average price of cheapest 10 sneakers inside the interval (default 0)
    
2. Buying sneakers:
    Every 30 seconds - minute
        - In the sneakers page, we filter by the latest sneakers
        - We check the price of each sneaker:
            - if it's at least 15% cheaper than the average price for its attributes sum interval we buy it
            - else: we go back and refresh and check for latest sneakers
        - We keep doing this until we don't have money (solana) left
        - For each sneaker we buy we save it in our database in a table:
            - ID
            - Sneaker ID
            - Buying Price
            - Selling Price (between 5-10% higher than we bought it)

3. Selling Sneakers:
    After we're done buying, I.E we don't have any more money
        - We go into our bought sneakers and we put them for sale at 5-10% higher than we bought them to make a profit
        - We do it for all the sneakers we have bought

We need:
    - Redis server
    - erlang
    - rabitmq server
    - install android studio and build-tools