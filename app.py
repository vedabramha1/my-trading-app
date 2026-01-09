import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# --- 1. SETUP THE APP ---
st.set_page_config(page_title="Alpha Intelligence 2026", layout="wide")

# --- 2. SIDEBAR ---
with st.sidebar:
    st.header("🌎 World Intelligence")
    st.info("📊 FED: Rate cut expected.")
    st.warning("⚔️ NATO & China monitoring active.")
    st.divider()
    st.subheader("💰 Commodities")
    
    def get_price(symbol):
        try:
            p = yf.Ticker(symbol).history(period="1d")['Close']
            return round(p.iloc[-1], 2) if not p.empty else 0.0
        except:
            return 0.0

    st.metric("Gold", f"${get_price('GC=F')}")
    st.metric("Crude Oil", f"${get_price('CL=F')}")

# --- 3. MAIN DASHBOARD ---
st.title("📈 2026 Global Trading Intelligence")

ticker_list = ["META", "AAPL", "TSLA", "NVDA", "GOOGL", "MSFT", "BTC-USD"]
selected_stock = st.selectbox("🔍 Select Asset", ticker_list)

stock = yf.Ticker(selected_stock)
# We fetch 6 months of data to find accurate Support/Resistance
hist = stock.history(period="6mo")

if not hist.empty:
    # --- MATH FOR SUPPORT & RESISTANCE ---
    resistance = float(hist['High'].max())
    support = float(hist['Low'].min())
    current_price = float(hist['Close'].iloc[-1])
    avg_volume = hist['Volume'].mean()
    current_volume = hist['Volume'].iloc[-1]

    # --- MARKET SENTIMENT LOGIC ---
    # Comparing 20-day average to current price
    ma20 = hist['Close'].tail(20).mean()
    if current_price > ma20:
        sentiment = "🚀 BULLISH (Bulls are in control)"
        sent_color = "green"
    else:
        sentiment = "🐻 BEARISH (Bears are in control)"
        sent_color = "red"

    # --- DISPLAY METRICS ---
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Price", f"${round(current_price, 2)}")
    col2.metric("Resistance Line", f"${round(resistance, 2)}")
    col3.metric("Support Line", f"${round(support, 2)}")

    st.subheader(f"Market Sentiment: :{sent_color}[{sentiment}]")

    # --- VOLUME & BREAKOUT NOTIFICATIONS ---
    if current_volume > (avg_volume * 1.5): # If volume is 50% higher than average
        if current_price >= (resistance * 0.99):
            st.toast(f"🚨 ALERT: HUGE VOLUME BREAKOUT ABOVE RESISTANCE for {selected_stock}!", icon="🔥")
            st.error(f"🔥 MASSIVE VOLUME DETECTED! Price is testing Resistance (${round(resistance, 2)})")
        elif current_price <= (support * 1.01):
            st.toast(f"🚨 ALERT: HUGE VOLUME BREAKDOWN BELOW SUPPORT for {selected_stock}!", icon="📉")
            st.warning(f"📉 DANGER: Price is testing Support (${round(support, 2)}) with heavy volume!")

    # --- 4. THE CHART WITH HORIZONTAL LINES ---
    # We show only the last 1 month on the chart for clarity
    chart_df = hist.tail(30)
    fig = go.Figure(data=[go.Candlestick(x=chart_df.index,
                open=chart_df['Open'], high=chart_df['High'],
                low=chart_df['Low'], close=chart_df['Close'], name="Price")])

    # Draw Resistance Line (Red)
    fig.add_hline(y=resistance, line_dash="dash", line_color="red", annotation_text="RESISTANCE")
    # Draw Support Line (Green)
    fig.add_hline(y=support, line_dash="dash", line_color="green", annotation_text="SUPPORT")

    fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=600)
    st.plotly_chart(fig, use_container_width=True)

# --- 5. OPTIONS SPREAD (Keeping your previous tool) ---
st.divider()
st.header("🧮 Options Spread Strategy")
# ... (rest of your options code remains the same)