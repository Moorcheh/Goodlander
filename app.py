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

# Generate dense X values for smooth shading
x_raw = np.linspace(strike * 0.75, strike * 1.25, 1000)
pnl_raw = np.array([contract.calculatePrice(x, vol, rate) - price for x in x_raw])
theo_raw = np.array([contract.calculatePrice(x, vol, rate) for x in x_raw])

# Find exact Breakeven to ensure no visual gaps between red and green fills
zero_crossings = np.where(np.diff(np.sign(pnl_raw)))[0]
be_x = None

if len(zero_crossings) > 0:
    idx = zero_crossings[0]
    x0, x1 = x_raw[idx], x_raw[idx+1]
    y0, y1 = pnl_raw[idx], pnl_raw[idx+1]
    
    # Linear interpolation to find the exact zero intercept
    t = (0 - y0) / (y1 - y0)
    be_x = x0 + t * (x1 - x0)
    be_theo = theo_raw[idx] + t * (theo_raw[idx+1] - theo_raw[idx])
    
    # Insert exact 0 point into our arrays
    x_vals = np.insert(x_raw, idx+1, be_x)
    pnl_vals = np.insert(pnl_raw, idx+1, 0.0)
    theo_vals = np.insert(theo_raw, idx+1, be_theo)
else:
    x_vals, pnl_vals, theo_vals = x_raw, pnl_raw, theo_raw

# Mask arrays for Red/Green splits
pos_mask = pnl_vals >= 0
neg_mask = pnl_vals <= 0

# Convert false values to NaN so Plotly only draws the relevant sections
pnl_pos = np.where(pos_mask, pnl_vals, np.nan)
pnl_neg = np.where(neg_mask, pnl_vals, np.nan)

# Format text strings here so the hover template remains clean
custom_pos = np.column_stack((
    [f"${t:.2f}" for t in theo_vals],
    [f"+${p:.2f}" for p in pnl_vals]
))

custom_neg = np.column_stack((
    [f"${t:.2f}" for t in theo_vals],
    [f"-${abs(p):.2f}" for p in pnl_vals]
))

fig = go.Figure()

# Green Area (Positive PnL)
fig.add_trace(go.Scatter(
    x=x_vals, y=pnl_pos,
    mode='lines',
    line=dict(color='#00e676', width=2),
    fill='tozeroy',
    fillcolor='rgba(0, 230, 118, 0.15)',
    customdata=custom_pos,
    hovertemplate="<span style='font-size:24px; color:#00e676'><b>%{customdata[1]}</b></span><br><span style='font-size:16px; color:#ffffff'>Price: %{customdata[0]}</span><extra></extra>",
    hoverlabel=dict(bgcolor="rgba(15,15,15,0.9)", bordercolor="#00e676")
))

# Red Area (Negative PnL)
fig.add_trace(go.Scatter(
    x=x_vals, y=pnl_neg,
    mode='lines',
    line=dict(color='#ff5252', width=2),
    fill='tozeroy',
    fillcolor='rgba(255, 82, 82, 0.15)',
    customdata=custom_neg,
    hovertemplate="<span style='font-size:24px; color:#ff5252'><b>%{customdata[1]}</b></span><br><span style='font-size:16px; color:#ffffff'>Price: %{customdata[0]}</span><extra></extra>",
    hoverlabel=dict(bgcolor="rgba(15,15,15,0.9)", bordercolor="#ff5252")
))

# Add Breakeven Node
if be_x is not None:
    fig.add_trace(go.Scatter(
        x=[be_x], y=[0],
        mode='markers',
        marker=dict(color='#ffffff', size=8, line=dict(color='#111111', width=2)),
        hoverinfo="skip" # Let the main line handle the hover data
    ))

# Add Strike Node
pnl_at_strike = contract.calculatePrice(strike, vol, rate) - price
fig.add_trace(go.Scatter(
    x=[strike], y=[pnl_at_strike],
    mode='markers',
    marker=dict(color='#ffffff', size=8, line=dict(color='#111111', width=2)),
    hoverinfo="skip"
))

# Minimalist Layout
fig.update_layout(
    template="plotly_dark",
    showlegend=False,
    hovermode="x", # Snaps the massive tooltip directly to the cursor crosshair
    dragmode=False,
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=True,
        showspikes=True,
        spikemode='across',
        spikesnap='cursor',
        spikedash='solid',
        spikethickness=1,
        spikecolor='#ffffff',
        fixedrange=True
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=True,
        zerolinecolor='rgba(255,255,255,0.1)',
        zerolinewidth=1,
        showticklabels=False, # Kills the useless Y-axis text
        fixedrange=True
    ),
    plot_bgcolor='rgba(15, 15, 15, 1)',
    paper_bgcolor='rgba(15, 15, 15, 1)',
    margin=dict(l=0, r=0, t=10, b=20),
    height=450
)

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})