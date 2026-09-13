import streamlit as st
from ipl_insights import data_loader, metrics, charts

st.set_page_config(page_title="Player vs Player", layout="wide")
st.title("Player vs Player")

matches = data_loader.load_matches()
balls = data_loader.load_balls()

batters = balls["batter"].unique().tolist()
bowlers = balls["bowler"].unique().tolist()
player_options = sorted(set(batters) | set(bowlers))

col1, col2 = st.columns(2)
with col1:
    player1 = st.selectbox("Choose Player 1", options=player_options, key="player1")
with col2:
    player2 = st.selectbox("Choose Player 2", options=player_options, key="player2")

show_analysis = st.button("Show Analysis")

if show_analysis:
    if player1 == player2:
        st.warning("Please select two distinct players to compare.")
    else:
        st.subheader("Player Statistics")
        comparison = metrics.compare_players(balls, player1, player2)
        st.dataframe(comparison, hide_index=True)

        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"{player1}'s Contribution to Team")
            contribution1 = metrics.player_team_contribution(balls, player1)
            fig = charts.distribution_pie_chart(contribution1, names_col="Metric", values_col="Value")
            st.plotly_chart(fig)
        with col2:
            st.subheader(f"{player2}'s Contribution to Team")
            contribution2 = metrics.player_team_contribution(balls, player2)
            fig = charts.distribution_pie_chart(contribution2, names_col="Metric", values_col="Value")
            st.plotly_chart(fig)