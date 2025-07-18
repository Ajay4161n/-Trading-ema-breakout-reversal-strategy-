# trading_strategy_project.py

import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import talib

# === 1. Download Historical Data ===
def fetch_data(ticker='AAPL', start='2022-01-01', end='2023-01-01'):
    data = yf.download(ticker, start=start, end=end)
    return data

# === 2. Compute Indicators ===
def compute_indicators(data):
    data['EMA9'] = data['Close'].ewm(span=9, adjust=False).mean()
    data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
    data['Candle'] = np.where(data['Close'] > data['Open'], 'Bullish', 'Bearish')
    return data

# === 3. Breakout Strategy ===
def detect_breakouts(data):
    data['Breakout'] = (data['High'] > data['High'].shift(1)) & (data['Close'] > data['High'].shift(1))
    return data

# === 4. Reversal Candlestick Patterns ===
def detect_candle_patterns(data):
    data['Hammer'] = talib.CDLHAMMER(data['Open'], data['High'], data['Low'], data['Close'])
    data['HangingMan'] = talib.CDLHANGINGMAN(data['Open'], data['High'], data['Low'], data['Close'])
    data['Engulfing'] = talib.CDLENGULFING(data['Open'], data['High'], data['Low'], data['Close'])
    data['DarkCloudCover'] = talib.CDLDARKCLOUDCOVER(data['Open'], data['High'], data['Low'], data['Close'])
    data['Piercing'] = talib.CDLPIERCING(data['Open'], data['High'], data['Low'], data['Close'])
    return data

# === 5. Generate Buy/Sell Signals ===
def generate_signals(data):
    data['Buy'] = ((data['EMA9'] > data['EMA20']) & data['Breakout']) | (data['Hammer'] > 0) | (data['Piercing'] > 0)
    data['Sell'] = ((data['EMA9'] < data['EMA20']) & data['Breakout']) | (data['HangingMan'] < 0) | (data['DarkCloudCover'] < 0) | (data['Engulfing'] < 0)
    return data

# === 6. Plotting ===
def plot_strategy(data):
    plt.figure(figsize=(15, 7))
    plt.plot(data['Close'], label='Close Price', alpha=0.5)
    plt.plot(data['EMA9'], label='EMA 9')
    plt.plot(data['EMA20'], label='EMA 20')
    plt.scatter(data.index[data['Buy']], data['Close'][data['Buy']], label='Buy Signal', marker='^', color='green')
    plt.scatter(data.index[data['Sell']], data['Close'][data['Sell']], label='Sell Signal', marker='v', color='red')
    plt.title('Trading Strategy: 9/20 EMA + Breakout + Reversal Patterns')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

# === Main Execution ===
if __name__ == "__main__":
    data = fetch_data('AAPL', start='2022-01-01', end='2023-01-01')
    data = compute_indicators(data)
    data = detect_breakouts(data)
    data = detect_candle_patterns(data)
    data = generate_signals(data)
    plot_strategy(data)
