import ccxt  # Crypto exchange library
import pandas as pd
import time
from strategy import check_signal  # Your trading logic
from config import API_KEY, API_SECRET  # API keys
import csv
from datetime import datetime

def log_trade(action, price, amount, balance):
    with open('trade_log.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), action, price, amount, balance])

# Initialize Binance with your API credentials
exchange = ccxt.binance({
    'apiKey': API_KEY,
    'secret': API_SECRET,
    'enableRateLimit': True,  # Prevents rate limit errors
})

# Define your trading pair and timeframe
symbol = 'BTC/USDT'
timeframe = '1h'  # 1-hour candles for swing trading
limit = 100  # Number of candles to fetch

# Function to fetch recent OHLCV (candlestick) data
def fetch_data():
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
    df = pd.DataFrame(ohlcv, columns=['time', 'open', 'high', 'low', 'close', 'volume'])
    df['time'] = pd.to_datetime(df['time'], unit='ms')  # Convert timestamps to readable format
    return df

RISK_PERCENT = 0.02  # 2% per trade

def get_position_size(balance, price):
    risk_amount = balance * RISK_PERCENT
    return round(risk_amount / price, 6)  # 6 decimals for crypto precision

# Main trading loop
while True:
    try:
        df = fetch_data()  # Get historical price data
        signal = check_signal(df)  # Determine trade signal

        # React to signal
        if signal == 'buy':
            print("📈 Buy Signal Triggered")
            # Place your buy order here, e.g.
            # exchange.create_market_buy_order(symbol, qty)
        elif signal == 'sell':
            print("📉 Sell Signal Triggered")
            # Place your sell order here
            # exchange.create_market_sell_order(symbol, qty)
        else:
            print("🔍 No Trade Signal")

    except Exception as e:
        print(f"❌ Error: {e}")  # Log any errors

    time.sleep(60 * 60)  # Sleep for 1 hour before next check
