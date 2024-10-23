import streamlit as st
import time
import datetime
import yfinance as yf
import matplotlib as pyplot
import pandas as pd

st.title("FINANCE TEST DASHBOARD")
with st.sidebar:
  ticker = st.text_input('Stock ticker', 'MSFT')
  col1, col2 = st.columns(2)
  start_date = col1.date_input("Start date", datetime.date(2019, 1, 1))
  end_date = col2.date_input("End date", datetime.date(2022, 1, 1))
  
  analyze_btn = st.button('Analyze')
  
if analyze_btn:
  with st.spinner("Loading..."):
    company = yf.Ticker(ticker)
    historical_prices = company.history(start=start_date, end=end_date)
    earnings = company.earnings

    change = company.info['previousClose'] - company.info['currentPrice'] 
    change_percent = round(change / company.info['previousClose'] * 100, ndigits=2)
    
    change_percent = round((company.info['previousClose'] - company.info['currentPrice']) / company.info['previousClose'] * 100, 2)
    
    cl1, cl2, cl3, cl4, cl5, cl6 = st.columns(6)
    cl1.metric("Price", company.info['currentPrice'], f"{-change_percent}%")
    cl2.metric("Current ratio", company.info['currentRatio'])
    cl3.metric("Quick ratio", company.info['quickRatio'])
    cl4.metric("Short ratio", company.info['shortRatio'])
    cl5.metric("Peg ratio", company.info['pegRatio'])
    cl6.metric("Payout ratio", company.info['payoutRatio'])

    with st.expander("Related News"):
      for news in company.news:
        st.write(f"[{news['title']}]({news['link']})")

  #   currentRatio, quickRatio, shortRatio, pegRatio, payoutRatio

    st.header(f"{ticker} historical prices")
    st.write(historical_prices)
    st.line_chart(historical_prices[['Open', 'Close', 'High', 'Low']])

    st.header("Earnings")
    c1, c2 = st.columns([7, 3])
    c1.line_chart(earnings)
    c2.write(earnings)

    st.header("Finances")
    st.write(company.financials)

    st.header("Balance sheet")
    st.write(company.balance_sheet)
