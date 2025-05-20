import csv
from datetime import datetime

def log_trade(action, price, amount, balance):
    with open('trade_log.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([datetime.now(), action, price, amount, balance])
