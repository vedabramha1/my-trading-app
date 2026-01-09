{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import streamlit as st\
import yfinance as yf\
import plotly.graph_objects as go\
import pandas as pd\
\
# --- 1. SETUP THE APP PAGE ---\
st.set_page_config(page_title="Alpha Intelligence 2026", layout="wide")\
\
# --- 2. SIDEBAR: WORLD NEWS & MACRO ---\
with st.sidebar:\
    st.header("\uc0\u55356 \u57102  World Intelligence")\
    st.info("\uc0\u55357 \u56522  **FED:** Market expects a rate cut in the next meeting.")\
    st.warning("\uc0\u9876 \u65039  **GEOPOLITICS:** NATO & China trade monitoring active.")\
    st.error("\uc0\u55357 \u56521  **WAR IMPACT:** Monitoring energy supply lines in Europe.")\
    st.divider()\
    \
    st.subheader("\uc0\u55357 \u56496  Commodities")\
    # Quick function to get prices for Gold, Oil, Silver\
    def get_comm_price(symbol):\
        return round(yf.Ticker(symbol).history(period="1d")['Close'].iloc[-1], 2)\
    \
    st.metric("Gold", f"$\{get_comm_price('GC=F')\}")\
    st.metric("Silver", f"$\{get_quick_price('SI=F') if 'get_quick_price' in locals() else get_comm_price('SI=F')\}")\
    st.metric("Crude Oil", f"$\{get_comm_price('CL=F')\}")\
\
# --- 3. MAIN DASHBOARD ---\
st.title("\uc0\u55357 \u56520  2026 Global Trading Intelligence")\
\
# Ticker Selection Dropdown\
ticker_list = ["META", "AAPL", "TSLA", "NVDA", "GOOGL", "MSFT", "BTC-USD", "ETH-USD"]\
selected_stock = st.selectbox("\uc0\u55357 \u56589  Select Asset to Analyze (Meta, Tesla, etc.)", ticker_list)\
\
# Fetch Data for the selected stock\
stock = yf.Ticker(selected_stock)\
hist = stock.history(period="1mo")\
\
# --- 4. DISPLAY STOCK INFO & NEWS ---\
col1, col2 = st.columns([1, 2])\
\
with col1:\
    st.subheader(f"About \{selected_stock\}")\
    st.metric("Price", f"$\{round(hist['Close'].iloc[-1], 2)\}")\
    st.write(f"**Recent \{selected_stock\} News:**")\
    # Fetch top 3 news stories for that stock\
    news = stock.news[:3]\
    for item in news:\
        st.markdown(f"\'95 [\{item['title']\}](\{item['link']\})")\
\
with col2:\
    # Professional Candlestick Chart\
    fig = go.Figure(data=[go.Candlestick(x=hist.index,\
                open=hist['Open'], high=hist['High'],\
                low=hist['Low'], close=hist['Close'])])\
    fig.update_layout(title=f"\{selected_stock\} 30-Day Trend", template="plotly_dark", xaxis_rangeslider_visible=False)\
    st.plotly_chart(fig, use_container_width=True)\
\
# --- 5. OPTIONS SPREAD VISUALIZER ---\
st.divider()\
st.header("\uc0\u55358 \u56814  Options Spread Strategy")\
s_col1, s_col2 = st.columns([1, 2])\
\
with s_col1:\
    long_strike = st.number_input("Long Strike (Buy)", value=150)\
    short_strike = st.number_input("Short Strike (Sell)", value=160)\
    cost = st.number_input("Total Cost (Debit)", value=5.0)\
\
with s_col2:\
    # Math to show Profit/Loss on a graph\
    prices = list(range(long_strike - 20, short_strike + 20))\
    profit = [min(max(p - long_strike, 0), short_strike - long_strike) - cost for p in prices]\
    \
    fig_opt = go.Figure()\
    fig_opt.add_trace(go.Scatter(x=prices, y=profit, fill='tozeroy', name='Profit/Loss'))\
    fig_opt.update_layout(title="Bull Call Spread Payoff", template="plotly_dark")\
    st.plotly_chart(fig_opt, use_container_width=True)\
\
st.write("---")\
st.caption("Data source: Yahoo Finance. For information only."}