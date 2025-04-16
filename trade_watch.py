import asyncio
import aiohttp
import sqlite3
import json
import os
import time
from datetime import datetime
from binance import AsyncClient
import config  # Your config file

# Markets to monitor (start with 3 to manage load)
MARKETS = ['ADAUSDT', 'ETHUSDT', 'BTCUSDT']

# Ensure directories exist
for dir_path in [config.DATABASES_DIR, config.LOG_DIR]:
    os.makedirs(dir_path, exist_ok=True)

# Initialize SQLite databases
def init_db(market):
    db_path = config.MarketDatabases[market]
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_book (
            timestamp INTEGER PRIMARY KEY,
            symbol TEXT,
            bids TEXT,
            asks TEXT
        )
    ''')
    conn.commit()
    return conn

# Fetch order book data via REST API
async def fetch_order_book(session, market):
    url = f"https://api.binance.com/api/v3/depth?symbol={market}&limit=20"
    try:
        async with session.get(url) as response:
            if response.status != 200:
                print(f"Error fetching order book for {market}: {response.status}")
                return None
            data = await response.json()
            timestamp = int(time.time())
            return {
                'timestamp': timestamp,
                'symbol': market,
                'bids': json.dumps(data['bids']),
                'asks': json.dumps(data['asks'])
            }
    except Exception as e:
        print(f"Exception fetching order book for {market}: {e}")
        return None

# Store order book data in SQLite
def store_order_book(conn, data):
    if data is None:
        return
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR REPLACE INTO order_book (timestamp, symbol, bids, asks)
        VALUES (?, ?, ?, ?)
    ''', (data['timestamp'], data['symbol'], data['bids'], data['asks']))
    conn.commit()

# Main loop to fetch and store order book data
async def monitor_order_books():
    # Initialize database connections
    db_connections = {market: init_db(market) for market in MARKETS}
    
    # Create aiohttp session
    async with aiohttp.ClientSession() as session:
        while True:
            start_time = time.time()
            tasks = [fetch_order_book(session, market) for market in MARKETS]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Store results
            for market, result in zip(MARKETS, results):
                if isinstance(result, dict):
                    store_order_book(db_connections[market], result)
                else:
                    print(f"Failed to fetch order book for {market}")
            
            # Log progress
            print(f"[{datetime.now()}] Fetched and stored order books for {MARKETS}")
            
            # Control fetch frequency (1-second intervals)
            elapsed = time.time() - start_time
            await asyncio.sleep(max(0, 1.0 - elapsed))

# Cleanup on shutdown
def cleanup(db_connections):
    for conn in db_connections.values():
        conn.close()

# Run the monitoring loop
if __name__ == "__main__":
    db_connections = {market: init_db(market) for market in MARKETS}
    try:
        asyncio.run(monitor_order_books())
    except KeyboardInterrupt:
        print("Shutting down...")
        cleanup(db_connections)
    except Exception as e:
        print(f"Error: {e}")
        cleanup(db_connections)