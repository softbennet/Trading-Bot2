# Buy/sell Logic

import pandas as pd

# Calculate MACD, Signal Line, and Moving Averages
def calculate_indicators(df):
    # Exponential Moving Averages (EMA)
    df['ema_12'] = df['close'].ewm(span=12).mean()
    df['ema_26'] = df['close'].ewm(span=26).mean()

    # MACD and its Signal line
    df['macd'] = df['ema_12'] - df['ema_26']
    df['signal'] = df['macd'].ewm(span=9).mean()

    # Simple Moving Averages (SMA)
    df['ma_50'] = df['close'].rolling(window=50).mean()
    df['ma_200'] = df['close'].rolling(window=200).mean()

    return df

# Generate trade signal based on indicators
def check_signal(df):
    df = calculate_indicators(df)  # Add indicators to dataframe
    latest = df.iloc[-1]  # Get the latest candle

    # Entry conditions:
    # 1. MACD line crosses above signal line (momentum)
    # 2. 50 MA is above 200 MA (trend confirmation)
    if latest['macd'] > latest['signal'] and latest['ma_50'] > latest['ma_200']:
        return 'buy'
    # Exit conditions:
    # 1. MACD crosses below signal line
    # 2. 50 MA is below 200 MA
    elif latest['macd'] < latest['signal'] and latest['ma_50'] < latest['ma_200']:
        return 'sell'

    # Otherwise, do nothing
    return 'hold'
