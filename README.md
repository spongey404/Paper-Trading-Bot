# NLP Based Algorithmic Paper Trading Bot 

A Python-based paper trading bot that uses **Natural Language Processing (NLP)** for sentiment analysis on financial news, combined with **technical analysis** indicators for more informed trading decisions. This project is currently under active development.

---

## Overview

This bot uses:
- **Hugging Face’s FinBERT** model to process news article headlines and summaries and assign a sentiment score (positive, negative, or neutral)
- Various **technical indicators** (MACD, RSI, Bollinger Bands, and more) for technical analysis
- **Alpaca’s paper trading API** for simulating trades
- **Yahoo Finance data** for backtesting historical performance of the strategies

---

## Features

1. **Sentiment Analysis**  
   - Retrieves recent news for a given ticker (currently from Benzinga).  
   - Uses a finetuned BERT model (FinBERT) to classify news sentiment as negative, neutral, or positive.  
   - Translates multiple article sentiments into a single, aggregated sentiment score per ticker.

2. **Technical Analysis**  
   - Implements popular indicators (MACD, RSI, Stochastic Oscillator, Bollinger Bands, SMA, EMA, etc.).  
   - Processes and merges these indicators with price data for signal generation.

3. **Paper Trading & Backtesting**  
   - Utilizes Alpaca’s paper trading platform to place simulated orders.  
   - Performs backtesting on historical data from Yahoo Finance to validate the system’s performance before live paper trading.

4. **Modular Codebase**  
   - Clear separation of concerns: 
     - `sentiment_analysis.py` for NLP sentiment scoring  
     - `indicators.py` and `technical_analysis.py` for technical metrics  
     - `historical_data_retriever.py` for fetching historical market data  
     - `yahoo_backtesting.py` for running strategy backtests  
     - `trading_bot.py` for connecting to Alpaca’s paper trading API

---

## Improvements being worked on:
- Analysis of multiple symbols at once
- Documentation
- Different news retrieval library (Current implementation only allows for news from Benzinga to be used which might be succeptable to bias)
- Identify more accurate range for aggregated sentiment scores classifications for positive, negative and neutral signals
