import streamlit as st
from ipl_insights import data_loader, metrics, charts

st.set_page_config(page_title="Know a Player", layout="wide")
st.title("Know a Player")

matches = data_loader.load_matches()
balls = data_loader.load_balls()

player_options = sorted(balls["batter"].unique().tolist())
selected_player = st.selectbox("Select a player", options=player_options)
show_analysis = st.button("Show Analysis")

if show_analysis:
    st.subheader("Player Statistics")
    summary = metrics.player_summary(balls, selected_player)
    st.dataframe(summary, hide_index=True)

    st.subheader("Fours and Sixes Over the Years")
    fours_sixes = metrics.player_fours_sixes_by_year(balls, matches, selected_player)
    fig = charts.multi_line_chart(fours_sixes, x_col="year", y_cols=["fours", "sixes"])
    st.plotly_chart(fig)

    st.subheader("Contribution to Team's Total Runs")
    contribution = metrics.player_team_contribution(balls, selected_player)
    fig = charts.distribution_pie_chart(contribution, names_col="Metric", values_col="Value")
    st.plotly_chart(fig)