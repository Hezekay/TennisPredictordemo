import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="Tennis Predictor Pro",
    page_icon="🎾",
    layout="wide"
)

# ===================== STYLE =====================
st.markdown("""
<style>
body {
    background-color: #0E1117;
    color: #EAEAEA;
    font-family: 'Inter', sans-serif;
}
h1, h2, h3, h4 {
    color: #FFFFFF;
}
.sidebar .sidebar-content {
    background-color: #0E1117 !important;
}
.match-card {
    background: #1A1C22;
    border: 1px solid #2C2C2C;
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 16px;
    transition: all 0.25s ease;
    color: #FFFFFF !important;
}
.match-card:hover {
    border-color: #4A90E2;
    transform: translateY(-2px);
    box-shadow: 0 0 10px rgba(74,144,226,0.3);
}
.match-title {
    font-weight: 600;
    font-size: 16px;
    color: #FFFFFF;
}
.match-subtitle {
    font-size: 13px;
    color: #AAAAAA;
}
.metric-line {
    display: flex;
    justify-content: space-between;
    margin-top: 6px;
}
.metric-value {
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    opacity: 1 !important;
}
.metric-label {
    color: #DDDDDD !important;
    font-weight: 500;
}
.flag {
    width: 22px;
    height: 14px;
    margin-right: 6px;
    border-radius: 3px;
}
.view-btn {
    display: inline-block;
    margin-top: 10px;
    padding: 6px 12px;
    background: #2C2C2C;
    border-radius: 6px;
    color: #4A90E2;
    font-weight: 500;
    font-size: 13px;
    text-align: center;
}
.view-btn:hover {
    background: #333333;
}
</style>
""", unsafe_allow_html=True)

# ===================== MOCK DATA =====================
matches = [
    {
        "match": "Novak Djokovic vs Carlos Alcaraz",
        "tournament": "ATP Paris Masters",
        "court": "Indoor Hard",
        "spread": "-2.5",
        "over": "2.5",
        "p1_prob": 63,
        "p2_prob": 37,
        "flag1": "🇷🇸",
        "flag2": "🇪🇸",
        "rank": [1, 2],
        "aces": [9, 7],
        "breaks": [3, 2],
        "serve": [68, 65],
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
        "flag1": "🇵🇱",
        "flag2": "🇺🇸",
        "rank": [1, 3],
        "aces": [6, 8],
        "breaks": [4, 3],
        "serve": [71, 67],
        "h2h": "Swiatek leads 7–2"
    },
    {
        "match": "Daniil Medvedev vs Alexander Zverev",
        "tournament": "ATP Finals",
        "court": "Indoor Hard",
        "spread": "+1.5",
        "over": "2.5",
        "p1_prob": 48,
        "p2_prob": 52,
        "flag1": "🇷🇺",
        "flag2": "🇩🇪",
        "rank": [3, 5],
        "aces": [11, 13],
        "breaks": [2, 3],
        "serve": [66, 69],
        "h2h": "Medvedev leads 10–8"
    }
]

# ===================== APP STATE =====================
if "selected_match" not in st.session_state:
    st.session_state.selected_match = None

# ===================== SIDEBAR =====================
tournaments = ["All"] + sorted(list(set([m["tournament"] for m in matches])))
selected_tourney = st.sidebar.selectbox("🎾 Select Tournament", tournaments)

# ===================== HEADER =====================
st.title("🎾 Tennis Match Predictor ")
st.caption("Predicting Win Probabilities, Spreads & Key Match Stats")

# ===================== FILTER =====================
if selected_tourney != "All":
    filtered_matches = [m for m in matches if m["tournament"] == selected_tourney]
else:
    filtered_matches = matches

# ===================== MAIN VIEW =====================
if st.session_state.selected_match is None:
    st.subheader("Today's Matches")
    for i, m in enumerate(filtered_matches):
        player1, player2 = m["match"].split(" vs ")
        col1, col2 = st.columns([4, 1])
        with col1:
            st.markdown(f"""
            <div class='match-card'>
                <div class='match-title'>{m["flag1"]} {player1} vs {m["flag2"]} {player2}</div>
                <div class='match-subtitle'>{m["tournament"]} • {m["court"]}</div>
                <div class='metric-line'>
                    <span>{player1}: <b>{m["p1_prob"]}%</b></span>
                    <span>{player2}: <b>{m["p2_prob"]}%</b></span>
                </div>
                <div class='match-subtitle'>Spread: {m["spread"]} | O/U Sets: {m["over"]}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            if st.button("View Details", key=i):
                st.session_state.selected_match = i

else:
    m = matches[st.session_state.selected_match]
    player1, player2 = m["match"].split(" vs ")
    st.button("← Back to Matches", on_click=lambda: st.session_state.update(selected_match=None))

    st.header(f"{m['flag1']} {player1} vs {m['flag2']} {player2}")
    st.caption(f"{m['tournament']} • {m['court']}")

    # WIN PROB CHART
    st.subheader("Win Probability")
    chart = go.Figure(go.Bar(
        x=[player1, player2],
        y=[m["p1_prob"], m["p2_prob"]],
        marker_color=['#4A90E2', '#E24A4A']
    ))
    chart.update_layout(
        yaxis_title="Win Probability (%)",
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font=dict(color="#EAEAEA")
    )
    st.plotly_chart(chart, use_container_width=True)

    # STATS
    st.subheader("Key Match Stats")
    stats_df = pd.DataFrame({
        "Stat": ["Aces", "Breaks", "1st Serve %"],
        player1: [m["aces"][0], m["breaks"][0], m["serve"][0]],
        player2: [m["aces"][1], m["breaks"][1], m["serve"][1]]
    })
    st.dataframe(stats_df, use_container_width=True, hide_index=True)

    # H2H + RANKS
    st.markdown(f"**Head-to-Head:** {m['h2h']}")
    st.markdown(f"**ATP/WTA Rank:** {player1} (#{m['rank'][0]}) • {player2} (#{m['rank'][1]})")
