import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="2026 Pro Trader", layout="wide")

# --- SIDEBAR: MACRO & COMMODITIES ---
with st.sidebar:
    st.header("🌎 World Sentiment")
    st.info("FED: Watching 2026 rate cut path.")
    st.metric("Gold (Safe Haven)", f"${yf.Ticker('GC=F').history(period='1d')['Close'].iloc[-1]:.2f}")

# --- MAIN APP ---
ticker = st.selectbox("Select Asset", ["META", "AAPL", "NVDA", "TSLA", "BTC-USD"])
stock = yf.Ticker(ticker)

# 1. OPTION SENTIMENT (TRADERS' MINDSET)
st.header(f"🧠 Traders' Mindset for {ticker}")
try:
    # Fetch first available option expiration
    expiry = stock.options[0]
    opts = stock.option_chain(expiry)
    total_calls_oi = opts.calls['openInterest'].sum()
    total_puts_oi = opts.puts['openInterest'].sum()
    pcr = total_puts_oi / total_calls_oi

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("Put/Call Ratio (OI)", f"{pcr:.2f}")
    with col_s2:
        if pcr < 0.7:
            st.success("🔥 BULLISH MINDSET: People are buying more Calls.")
        elif pcr > 1.1:
            st.error("📉 BEARISH MINDSET: People are buying more Puts.")
        else:
            st.warning("🤝 NEUTRAL: Traders are undecided.")
except:
    st.write("Options data currently unavailable for this asset.")

# 2. TECHNICALS: SUPPORT & RESISTANCE
hist = stock.history(period="6mo")
resistance = hist['High'].max()
support = hist['Low'].min()
curr = hist['Close'].iloc[-1]

st.divider()
st.header("📊 Technical Analysis (Support & Resistance)")
col_p1, col_p2, col_p3 = st.columns(3)
col_p1.metric("Current Price", f"${curr:.2f}")
col_p2.write(f"**Resistance:** :red[${resistance:.2f}]")
col_p3.write(f"**Support:** :green[${support:.2f}]")

# Chart with S/R Lines
chart_df = hist.tail(40)
fig = go.Figure(data=[go.Candlestick(x=chart_df.index, open=chart_df['Open'], 
                high=chart_df['High'], low=chart_df['Low'], close=chart_df['Close'])])
fig.add_hline(y=resistance, line_dash="dash", line_color="red", annotation_text="RESISTANCE")
fig.add_hline(y=support, line_dash="dash", line_color="green", annotation_text="SUPPORT")
fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False)
st.plotly_chart(fig, use_container_width=True)

# 3. VOLUME & POP-UP ALERTS
avg_vol = hist['Volume'].mean()
curr_vol = hist['Volume'].iloc[-1]
if curr_vol > (avg_vol * 1.5):
    st.toast(f"🚨 VOLUME SPIKE DETECTED for {ticker}!", icon="🔊")
    st.warning(f"High Volume Alert: {curr_vol/1e6:.1f}M shares traded!")