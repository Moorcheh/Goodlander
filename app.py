import streamlit as st
import numpy as np
import plotly.graph_objects as go
from theory import Option

# Set the page to wide mode
st.set_page_config(layout="wide")

# --- TITLE ---
st.title("Goodlander")
st.write("") 

# --- ROW 1: BROKERAGE INPUTS ---
c1, c2, c3, c4, c5 = st.columns(5)
with c1: 
    symbol = st.text_input("Symbol", "AMD")
with c2: 
    expiration = st.text_input("Expiration", "May 29")
with c3: 
    strike = st.number_input("Strike", value=160.0, step=1.0)
with c4: 
    option_type = st.selectbox("Type", ["call"])
with c5: 
    price = st.number_input("Market Price", value=3.50, step=0.10)

# --- ROW 2: THE GREEKS ---
st.write("") 
g1, g2, g3, g4, g5 = st.columns(5)

with g1:
    st.latex(r"\Delta")
    delta = st.number_input("Delta", value=0.45, step=0.01, label_visibility="collapsed")
with g2:
    st.latex(r"\Gamma")
    gamma = st.number_input("Gamma", value=0.08, step=0.01, label_visibility="collapsed")

st.divider()

# --- ROW 3: VOL & RATE ADJUSTERS ---
v_col, r_col = st.columns(2)
with v_col:
    vol = st.slider("Implied Volatility", min_value=0.01, max_value=2.00, value=0.45, step=0.01)
with r_col:
    rate = st.slider("Risk-Free Rate", min_value=0.00, max_value=0.20, value=0.05, step=0.01)

# --- ROW 4: THE TACTICAL GRAPH ---
contract = Option(symbol, expiration, strike, option_type, price, delta, gamma)

# Generate a wide range with 500 points for a perfectly smooth curve
lower_bound = strike * 0.75
upper_bound = strike * 1.25
x_vals = np.linspace(lower_bound, upper_bound, 500)

pnl_vals = [contract.calculatePrice(x, vol, rate) - price for x in x_vals]

fig = go.Figure()

# Add the main PnL trace with spline smoothing
fig.add_trace(go.Scatter(
    x=x_vals,
    y=pnl_vals,
    mode='lines',
    name='Current PnL',
    line=dict(color='#00ffcc', width=3, shape='spline'), 
    fill='tozeroy',
    fillcolor='rgba(0, 255, 204, 0.05)', 
    hovertemplate="Underlying: $%{x:.2f}<br>PnL: $%{y:.2f}<extra></extra>"
))

# Add the Zero Line (Breakeven)
fig.add_hline(y=0, line_width=1.5, line_color="#ff4b4b")

# Add the Strike Line
fig.add_vline(x=strike, line_width=1, line_dash="dash", line_color="#888888")

# Minimalist Layout Updates
fig.update_layout(
    template="plotly_dark", 
    xaxis_title="Underlying Price ($)",
    yaxis_title="Theoretical PnL ($)",
    hovermode="x unified",
    dragmode=False, # Disables the clunky zoom boxes
    xaxis=dict(
        showgrid=False, # Removes grid lines
        zeroline=False,
        showspikes=True, 
        spikemode='across',
        spikedash='solid',
        spikethickness=1,
        spikecolor='#ffffff',
        fixedrange=True # Prevents accidental scrolling/zooming
    ),
    yaxis=dict(
        showgrid=False, # Removes grid lines
        zeroline=False,
        fixedrange=True
    ),
    plot_bgcolor='rgba(15, 15, 15, 1)',
    paper_bgcolor='rgba(15, 15, 15, 1)',
    margin=dict(l=0, r=0, t=30, b=0),
    height=550
)

# Render the graph and hide the modebar
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})