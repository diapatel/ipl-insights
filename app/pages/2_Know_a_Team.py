import pandas as pd
import streamlit as st
from ipl_insights import data_loader, metrics, charts

import streamlit as st
from ipl_insights import data_loader, metrics, charts

st.set_page_config(page_title="Know a Team", layout="wide")
st.title("Know a Team")

matches = data_loader.load_matches()
balls = data_loader.load_balls()

team_options = sorted(matches["Team1"].unique().tolist())
selected_team = st.selectbox("Select a team", options=team_options)

st.subheader("Overview")
played = metrics.team_matches_played(matches, selected_team)
wins = metrics.team_wins(matches, selected_team)
win_pct = metrics.team_win_percentage(matches, selected_team)

overview = pd.DataFrame({
    "Metric": ["Matches Played", "Matches Won", "Win Percentage"],
    "Value": [played, wins, f"{win_pct}%"],
})
st.dataframe(overview, hide_index=True)

st.subheader("Total Runs Over the Years")
yearly_runs = metrics.team_runs_over_years(matches, balls, selected_team)
fig = charts.runs_over_years_chart(yearly_runs)
st.plotly_chart(fig)

st.subheader("Top 15 Batsmen")
top_batters = metrics.top_batters_for_team(balls, selected_team)
fig = charts.bar_chart(top_batters, x_col="batter", y_col="batsman_run")
st.plotly_chart(fig)

st.subheader("Top 15 Bowlers")
top_bowlers = metrics.top_bowlers_for_team(balls, selected_team)
fig = charts.bar_chart(top_bowlers, x_col="bowler", y_col="isWicketDelivery")
st.plotly_chart(fig)

st.subheader("Players of the Match")
potm_text = metrics.team_player_of_match_text(matches, selected_team)
fig = charts.wordcloud_figure(potm_text)
st.pyplot(fig)

st.subheader("Batting Average vs Strike Rate")
profile = metrics.team_batting_profile(balls, selected_team)
fig = charts.scatter_chart(profile, x_col="strike_rate", y_col="batting_average", hover_name="batter")
st.plotly_chart(fig)