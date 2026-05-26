import streamlit as st
import numpy as np
import plotly.graph_objects as go
from theory import Option

# Set the page to wide mode for a cleaner dashboard look
st.set_page_config(layout="wide")

# --- TITLE ---
st.title("Goodlander")
st.write("") # Quick spacer

# --- ROW 1: BROKERAGE INPUTS ---
c1, c2, c3, c4, c5 = st.columns(5)
with c1: 
    symbol = st.text_input("Symbol", "AAPL")
with c2: 
    expiration = st.text_input("Expiration", "May 29")
with c3: 
    strike = st.number_input("Strike", value=210.0, step=1.0)
with c4: 
    option_type = st.selectbox("Type", ["call"])
with c5: 
    price = st.number_input("Market Price", value=3.50, step=0.10)

# --- ROW 2: THE GREEKS ---
st.write("") 
g1, g2, g3, g4, g5 = st.columns(5)

with g1:
    # Render the literal, elegant Greek symbol, then hide the input's text label
    st.latex(r"\Delta")
    delta = st.number_input("Delta", value=0.45, step=0.01, label_visibility="collapsed")
with g2:
    st.latex(r"\Gamma")
    gamma = st.number_input("Gamma", value=0.08, step=0.01, label_visibility="collapsed")

st.divider()

# --- ROW 3: VOL & RATE ADJUSTERS ---
v_col, r_col = st.columns(2)
with v_col:
    # Sliders allow for rapid "playing around" to see the graph react
    vol = st.slider("Implied Volatility", min_value=0.01, max_value=2.00, value=0.25, step=0.01)
with r_col:
    rate = st.slider("Risk-Free Rate", min_value=0.00, max_value=0.20, value=0.05, step=0.01)

# --- ROW 4: THE GRAPH ---
# 1. Instantiate the contract using your exact theory.py logic
contract = Option(symbol, expiration, strike, option_type, price, delta, gamma)

# 2. Generate a range of underlying prices for the X-axis (+/- 20% of strike)
lower_bound = strike * 0.8
upper_bound = strike * 1.2
x_vals = np.linspace(lower_bound, upper_bound, 100)

# 3. Calculate theoretical option prices for every X value
y_vals = [contract.calculatePrice(x, vol, rate) for x in x_vals]

# 4. Build the interactive Plotly graph
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=x_vals,
    y=y_vals,
    mode='lines',
    name='Theoretical Price',
    line=dict(color='#0068c9', width=3),
    # This formats the hover box cleanly
    hovertemplate="Underlying: $%{x:.2f}<br>Option Price: $%{y:.2f}<extra></extra>" 
))

# Add a dashed vertical line to clearly mark the Strike Price on the graph
fig.add_vline(x=strike, line_width=1, line_dash="dash", line_color="gray", annotation_text="Strike")

fig.update_layout(
    xaxis_title="Underlying Price ($)",
    yaxis_title="Theoretical Option Price ($)",
    hovermode="x unified", # Places a clean vertical line when you hover
    margin=dict(l=0, r=0, t=30, b=0),
    height=500
)

# Render the graph
st.plotly_chart(fig, use_container_width=True)