import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

st.set_page_config(page_title="2026 Alpha Terminal", layout="wide")

# --- SIDEBAR ---
with st.sidebar:
    st.header("🌎 Global Context")
    st.info("FED: Watching 2026 rate cut path.")
    gold_price = yf.Ticker('GC=F').history(period='1d')['Close'].iloc[-1]
    st.metric("Gold (Safe Haven)", f"${gold_price:.2f}")

# --- SEARCH & ASSET SELECTION ---
st.title("🚀 2026 Institutional Trading Dashboard")
ticker = st.text_input("🔍 Type ANY Stock Ticker (e.g., AAPL, NVDA, META):", value="META").upper()

if ticker:
    stock = yf.Ticker(ticker)
    
    # 1. OPTION VOLUME & DOLLAR IMPACT (MINDSET)
    st.header(f"🧠 Institutional Mindset: {ticker}")
    try:
        expiry = stock.options[0]
        opts = stock.option_chain(expiry)
        
        # Calculate $ Impact (Open Interest * Last Price)
        opts.calls['dollar_impact'] = opts.calls['openInterest'] * opts.calls['lastPrice'] * 100
        opts.puts['dollar_impact'] = opts.puts['openInterest'] * opts.puts['lastPrice'] * 100
        
        call_val = opts.calls['dollar_impact'].sum()
        put_val = opts.puts['dollar_impact'].sum()
        total_val = call_val + put_val
        
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Total Call Value ($)", f"${call_val/1e6:.2f}M")
            st.progress(call_val / total_val if total_val > 0 else 0)
            st.caption("Call Side Concentration")
            
        with col_m2:
            st.metric("Total Put Value ($)", f"${put_val/1e6:.2f}M")
            st.progress(put_val / total_val if total_val > 0 else 0)
            st.caption("Put Side Concentration")

        if call_val > put_val:
            st.success(f"🔥 BULLS DOMINATING: Bulls have ${ (call_val - put_val)/1e6 :.1f}M more skin in the game.")
        else:
            st.error(f"📉 BEARS DOMINATING: Bears have ${ (put_val - call_val)/1e6 :.1f}M more skin in the game.")
    except:
        st.warning("⚠️ This asset might not have active Options data for the nearest expiry.")

    # 2. CHART + SUPPORT/RESISTANCE
    hist = stock.history(period="6mo")
    if not hist.empty:
        resistance = hist['High'].max()
        support = hist['Low'].min()
        curr = hist['Close'].iloc[-1]
        
        st.divider()
        st.header("📊 Price Levels & Technical Zones")
        
        # Visual Candlestick Chart
        chart_df = hist.tail(45)
        fig = go.Figure(data=[go.Candlestick(x=chart_df.index, open=chart_df['Open'], 
                        high=chart_df['High'], low=chart_df['Low'], close=chart_df['Close'], name="Price")])
        
        fig.add_hline(y=resistance, line_dash="dash", line_color="red", annotation_text=f"RESISTANCE: ${resistance:.2f}")
        fig.add_hline(y=support, line_dash="dash", line_color="green", annotation_text=f"SUPPORT: ${support:.2f}")
        
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        # 3. VOLUME BREAKOUT NOTIFICATION
        avg_vol = hist['Volume'].mean()
        curr_vol = hist['Volume'].iloc[-1]
        if curr_vol > (avg_vol * 1.5):
            st.toast(f"🚨 MASSIVE VOLUME DETECTED on {ticker}!", icon="🔊")
            st.warning(f"Extreme Volume: {curr_vol/1e6:.1f} Million shares traded today!")

    else:
        st.error("Could not find data for this ticker. Please check the symbol.")