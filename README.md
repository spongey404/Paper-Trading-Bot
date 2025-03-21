# NLP Based Algorithmic Paper Trading Bot 

A Python-based paper trading bot that uses **Natural Language Processing (NLP)** for sentiment analysis on financial news, combined with **technical analysis** indicators for more informed trading decisions. This project is currently under active development.

---

## Overview

This bot uses:
- **Hugging Face’s ProsusAI/FinBERT** model to process news article headlines and summaries and assign a sentiment score (positive, negative, or neutral)
- Various **technical indicators** (MACD, RSI, Bollinger Bands, and more) for technical analysis
- **Alpaca’s paper trading API** for simulating trades
- **Yahoo Finance data** for backtesting historical performance of the strategies

---

## Features

1. **Sentiment Analysis**  
   - Retrieves recent news for a given ticker (currently from Benzinga).  
   - Uses a BERT model (FinBERT) to classify news sentiment as negative, neutral, or positive.  
   - Translates multiple article sentiments into a single, aggregated sentiment score per ticker.

2. **Technical Analysis**  
   - Implements popular indicators (MACD, RSI, Stochastic Oscillator, Bollinger Bands, SMA, EMA, etc.).  
   - Processes and merges these indicators with price data to generate a trade signal.

3. **Paper Trading & Backtesting**  
   - Uses Alpaca’s paper trading platform to place simulated orders.  
   - Performs backtesting on historical data from Yahoo Finance to validate the system’s performance before live paper trading.

4. **Modular Code**  
   - Clear separation of components: 
     - `sentiment_analysis.py` for NLP sentiment scoring  
     - `indicators.py` and `technical_analysis.py` for technical metrics  
     - `historical_data_retriever.py` for fetching historical market data  
     - `yahoo_backtesting.py` for running strategy backtests  
     - `trading_bot.py` for connecting to Alpaca’s paper trading API

---

## Improvements being worked on:
- Documentation
- Different news retrieval library (Current implementation only allows for news from Benzinga to be used which might be susceptible to bias)
- Identify a more accurate range for aggregated sentiment score classifications for positive, negative and neutral signals
- Implement more robust error handling

## Upgrades for future versions:
- Analysis of multiple symbols at once
- Have symbols be chosen entirely by the algorithm with no user input from current news
- Add machine learning elements
