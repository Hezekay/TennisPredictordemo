import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="ATP/WTA Tennis Predictor", layout="wide")

# ------------------ STYLES ------------------
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: #EAEAEA;
}
h1, h2, h3 {
    color: #FFFFFF;
}
.match-card {
    background-color: #1A1C22;
    border: 1px solid #2E2E2E;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 12px;
    transition: 0.2s ease-in-out;
}
.match-card:hover {
    border-color: #4A90E2;
    box-shadow: 0 0 8px rgba(74,144,226,0.4);
}
.match-title {
    font-weight: 600;
    font-size: 16px;
    color: #FFFFFF;
}
.match-info {
    font-size: 13px;
    color: #AAAAAA;
}
.metric-line {
    display: flex;
    justify-content: space-between;
    margin-top: 8px;
    color: #DDDDDD;
}
.view-btn {
    background-color: #2E2E2E;
    border-radius: 6px;
    padding: 6px 10px;
    text-align: center;
    margin-top: 8px;
    color: #4A90E2;
    font-weight: 500;
}
.view-btn:hover {
    background-color: #3A3A3A;
}
</style>
""", unsafe_allow_html=True)

# ------------------ SAMPLE DATA ------------------
matches = [
    {
        "match": "Novak Djokovic vs Carlos Alcaraz",
        "tournament": "Paris Masters",
        "court": "Hard",
        "spread": "-2.5",
        "over": "2.5",
        "p1_prob": 63,
        "p2_prob": 37,
        "aces": [8, 6],
        "breaks": [3, 2],
        "first_serve": [67, 64],
        "rank": [1, 2],
        "h2h": "Djokovic leads 3–2"
    },
    {
        "match": "Iga Swiatek vs Coco Gauff",
        "tournament": "WTA Finals",
        "court": "Hard",
        "spread": "-1.5",
        "over": "2.5",
        "p1_prob": 59,
        "p2_prob": 41,
        "aces": [5, 7],
        "breaks": [4, 2],
        "first_serve": [70, 62],
        "rank": [1, 3],
        "h2h": "Swiatek leads 7–2"
    },
    {
        "match": "Daniil Medvedev vs Alexander Zverev",
        "tournament": "ATP Finals",
        "court": "Hard",
        "spread": "+1.5",
        "over": "2.5",
        "p1_prob": 46,
        "p2_prob": 54,
        "aces": [9, 12],
        "breaks": [2, 4],
        "first_serve": [65, 69],
        "rank": [3, 5],
        "h2h": "Medvedev leads 10–8"
    },
]

# ------------------ PAGE STATE ------------------
if "selected_match" not in st.session_state:
    st.session_state.selected_match = None

# ------------------ TOURNAMENT DROPDOWN ------------------
tournaments = ["All"] + sorted(list(set([m["tournament"] for m in matches])))
selected_tourney = st.sidebar.selectbox("Select Tournament", tournaments)

# ------------------ MAIN TITLE ------------------
st.title("🎾 ATP / WTA Match Predictor")

# ------------------ FILTER MATCHES ------------------
if selected_tourney != "All":
    filtered_matches = [m for m in matches if m["tournament"] == selected_tourney]
else:
    filtered_matches = matches

# ------------------ OVERVIEW OR DETAILS ------------------
if st.session_state.selected_match is None:
    st.subheader("Today's Matches & Predictions")
    for i, m in enumerate(filtered_matches):
        col1, col2, col3 = st.columns([4, 2, 1])
        with col1:
            st.markdown(f"""
            <div class='match-card'>
                <div class='match-title'>{m["match"]}</div>
                <div class='match-info'>{m["tournament"]} • {m["court"]} Court</div>
                <div class='metric-line'>
                    <div>{m["match"].split(" vs ")[0]}: <b>{m["p1_prob"]}%</b></div>
                    <div>{m["match"].split(" vs ")[1]}: <b>{m["p2_prob"]}%</b></div>
                </div>
                <div class='match-info'>Spread: {m["spread"]} | O/U Sets: {m["over"]}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("View Details", key=i):
                st.session_state.selected_match = i
else:
    # ------------------ DETAILS VIEW ------------------
    m = matches[st.session_state.selected_match]
    st.button("← Back to Matches", on_click=lambda: st.session_state.update(selected_match=None))

    player1, player2 = m["match"].split(" vs ")
    st.header(f"{player1} vs {player2}")
    st.caption(f"{m['tournament']} • {m['court']} Court")

    # Win Probability
    st.subheader("Win Probability")
    prob_chart = go.Figure(go.Bar(
        x=[player1, player2],
        y=[m["p1_prob"], m["p2_prob"]],
        marker_color=['#4A90E2', '#E24A4A']
    ))
    prob_chart.update_layout(
        yaxis_title="Win Probability (%)",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#EAEAEA')
    )
    st.plotly_chart(prob_chart, use_container_width=True)

    # Player Stats
    st.subheader("Key Match Stats (Simulated)")
    stats_df = pd.DataFrame({
        "Stat": ["Aces", "Breaks", "1st Serve %"],
        player1: [m["aces"][0], m["breaks"][0], m["first_serve"][0]],
        player2: [m["aces"][1], m["breaks"][1], m["first_serve"][1]]
    })
    st.dataframe(stats_df, hide_index=True, use_container_width=True)

    # H2H + Rank
    st.markdown(f"**Head-to-Head:** {m['h2h']}")
    st.markdown(f"**ATP/WTA Ranks:** {player1} - #{m['rank'][0]} | {player2} - #{m['rank'][1]}")
