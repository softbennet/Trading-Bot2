import pandas as pd
from strategy import calculate_indicators, check_signal

def backtest(df, initial_balance=1000, position_size_pct=0.1):
    df = calculate_indicators(df)
    balance = initial_balance
    position = 0
    trade_log = []

    for i in range(1, len(df)):
        row = df.iloc[i]
        previous = df.iloc[i - 1]

        signal = check_signal(df.iloc[:i+1])  # Run signal on data up to this point

        if signal == 'buy' and balance > 0:
            position = (balance * position_size_pct) / row['close']
            balance -= position * row['close']
            trade_log.append((row['time'], 'BUY', row['close'], position, balance))

        elif signal == 'sell' and position > 0:
            balance += position * row['close']
            trade_log.append((row['time'], 'SELL', row['close'], position, balance))
            position = 0

    if position > 0:
        # Liquidate remaining position at last price
        balance += position * df.iloc[-1]['close']
        trade_log.append((df.iloc[-1]['time'], 'FINAL SELL', df.iloc[-1]['close'], position, balance))

    return pd.DataFrame(trade_log, columns=['time', 'action', 'price', 'amount', 'balance'])

# Example usage
if __name__ == "__main__":
    df = pd.read_csv('historical_data.csv')  # Make sure to have this data
    df['time'] = pd.to_datetime(df['time'])
    log = backtest(df)
    print(log)
    print(f"Final Balance: {log.iloc[-1]['balance']}")
