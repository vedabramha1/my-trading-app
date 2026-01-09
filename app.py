import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# --- SETUP THE APP ---
st.set_page_config(page_title="Alpha Intelligence 2026", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🌎 World Intelligence")
    st.info("📊 FED: Rate cut expected.")
    st.warning("⚔️ NATO & China monitoring active.")
    st.divider()
    st.subheader("💰 Commodities")
    
    def get_price(symbol):
        try:
            return round(yf.Ticker(symbol).history(period="1d")['Close'].iloc[-1], 2)
        except:
            return 0.0

    st.metric("Gold", f"${get_price('GC=F')}")
    st.metric("Crude Oil", f"${get_price('CL=F')}")

# --- MAIN DASHBOARD ---
st.title("📈 2026 Global Trading Intelligence")

ticker_list = ["META", "AAPL", "TSLA", "NVDA", "GOOGL", "MSFT", "BTC-USD"]
selected_stock = st.selectbox("🔍 Select Asset", ticker_list)

stock = yf.Ticker(selected_stock)
hist = stock.history(period="1mo")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(f"About {selected_stock}")
    if not hist.empty:
        st.metric("Price", f"${round(hist['Close'].iloc[-1], 2)}")
    st.write("**Recent News:**")
    for item in stock.news[:3]:
        st.markdown(f"• [{item['title']}]({item['link']})")

with col2:
    if not hist.empty:
        fig = go.Figure(data=[go.Candlestick(x=hist.index,
                    open=hist['Open'], high=hist['High'],
                    low=hist['Low'], close=hist['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

# --- OPTIONS SPREAD ---
st.divider()
st.header("🧮 Options Spread Strategy")
s_col1, s_col2 = st.columns([1, 2])

with s_col1:
    l_strike = st.number_input("Long Strike", value=150)
    s_strike = st.number_input("Short Strike", value=160)
    cost = st.number_input("Net Cost", value=5.0)

with s_col2:
    prices = list(range(int(l_strike - 20), int(s_strike + 20)))
    profit = [min(max(p - l_strike, 0), s_strike - l_strike) - cost for p in prices]
    fig_opt = go.Figure(data=go.Scatter(x=prices, y=profit, fill='tozeroy'))
    fig_opt.update_layout(title="Payoff Graph", template="plotly_dark")
    st.plotly_chart(fig_opt, use_container_width=True)

st.caption("Data source: Yahoo Finance.")