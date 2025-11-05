import streamlit as st
import pandas as pd
import numpy as np
from datetime import date

# Page settings
st.set_page_config(page_title="ATP/WTA Matchup Predictor", layout="wide", page_icon="🎾")

# --- HEADER ---
st.title("ATP/WTA Matchup Prediction Demo")
st.markdown("""
This demo showcases how the **tennis outcome prediction interface** will look and work.  
The predictions below use **sample data**, but the final system will use live ATP/WTA matches and real odds.
""")

# --- TOURNAMENT SELECTION ---
tournaments = [
    "Paris Masters", "Billie Jean King Cup", "ATP Finals", "WTA Finals", "Basel Open"
]
selected_tourney = st.selectbox("Select Tournament", tournaments)

matches = [
    "Novak Djokovic vs Carlos Alcaraz",
    "Daniil Medvedev vs Alexander Zverev",
    "Iga Swiatek vs Coco Gauff",
    "Aryna Sabalenka vs Jessica Pegula",
    "Stefanos Tsitsipas vs Andrey Rublev"
]
selected_match = st.selectbox(" Select Match", matches)

surface = np.random.choice(["Hard", "Clay", "Grass", "Indoor Hard"])
match_date = date.today().strftime("%B %d, %Y")

st.markdown(f"**Surface:** {surface} | **Date:** {match_date}")

# --- FAKE MODEL PREDICTIONS ---
player1, player2 = selected_match.split(" vs ")
np.random.seed(len(selected_match))
p1_win_prob = np.random.uniform(0.45, 0.75)
p2_win_prob = 1 - p1_win_prob
expected_sets = np.random.uniform(2.1, 2.8)
game_spread = np.random.choice([-3.5, -2.5, -1.5, +1.5, +2.5, +3.5])
over_under_line = 2.5
over_prob = np.random.uniform(0.4, 0.7)

# --- DISPLAY METRICS ---
st.subheader("📈 Model Predictions")

col1, col2 = st.columns(2)
with col1:
    st.metric(f"Win Probability ({player1})", f"{p1_win_prob*100:.1f}%", delta=f"{(p1_win_prob-0.5)*100:.1f}% vs. 50/50")
    st.metric("Expected Sets", f"{expected_sets:.2f}")
    st.metric("Game Spread", f"{game_spread:+.1f}")

with col2:
    st.metric(f"Win Probability ({player2})", f"{p2_win_prob*100:.1f}%", delta=f"{(p2_win_prob-0.5)*100:.1f}% vs. 50/50")
    st.metric(f"Over/Under ({over_under_line} sets)", f"Over {over_prob*100:.0f}% / Under {100-over_prob*100:.0f}%")

# --- HEAD TO HEAD ---
st.subheader(f" Head-to-Head Record: {player1} vs {player2}")

h2h_data = pd.DataFrame({
    "Year": [2024, 2023, 2022, 2021],
    "Tournament": ["Wimbledon", "US Open", "Madrid Open", "Rome Masters"],
    "Winner": np.random.choice([player1, player2], size=4),
    "Score": ["3–1", "3–2", "2–1", "2–0"],
    "Surface": np.random.choice(["Hard", "Clay", "Grass"], size=4)
})

st.dataframe(h2h_data, use_container_width=True)

# --- VISUALIZATION ---
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.bar([player1, player2], [p1_win_prob*100, p2_win_prob*100])
ax.set_ylabel("Win Probability (%)")
ax.set_title("Predicted Win Probabilities")
st.pyplot(fig)

st.divider()

# --- FOOTER ---
st.markdown("""
✅ **Next steps for full version:**
- Integrate live scraping of ATP/WTA match and odds data.  
- Replace fake model with trained ML model (surface-aware).  
- Embed this Streamlit app into your website or host standalone.  

*Demo by Hezekiah — designed for ATP/ WTA Tennis Prediction Model.*
""")
