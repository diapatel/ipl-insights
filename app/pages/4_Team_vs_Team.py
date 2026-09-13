import streamlit as st
from ipl_insights import data_loader, metrics, charts

st.set_page_config(page_title="Team vs Team", layout="wide")
st.title("Team vs Team")

matches = data_loader.load_matches()
balls = data_loader.load_balls()

team_options = sorted(matches["Team1"].unique().tolist())

col1, col2 = st.columns(2)
with col1:
    team1 = st.selectbox("Choose Team 1", options=team_options, key="team1")
with col2:
    team2 = st.selectbox("Choose Team 2", options=team_options, key="team2")

show_analysis = st.button("Show Analysis")

if show_analysis:
    if team1 == team2:
        st.warning("Please select two distinct teams to compare.")
    else:
        st.subheader("Head-to-Head Overview")
        comparison = metrics.compare_teams(matches, team1, team2)
        st.dataframe(comparison, hide_index=True)

        st.subheader("Total Runs Over the Years")
        team1_runs = metrics.team_runs_over_years(matches, balls, team1)
        team2_runs = metrics.team_runs_over_years(matches, balls, team2)
        merged = team1_runs.merge(team2_runs, on="year", suffixes=(f"_{team1}", f"_{team2}"))
        fig = charts.multi_line_chart(merged, x_col="year", y_cols=[f"total_run_{team1}", f"total_run_{team2}"])
        st.plotly_chart(fig)

        st.subheader("Batting Average vs Strike Rate")
        profile = metrics.two_team_batting_profile(balls, team1, team2)
        fig = charts.scatter_chart(profile, x_col="strike_rate", y_col="batting_average", hover_name="batter", color_col="BattingTeam")
        st.plotly_chart(fig)

        st.subheader(f"Contribution of Each Batsman — {team1}")
        team1_batters = balls[balls["BattingTeam"] == team1].groupby("batter")["total_run"].sum().reset_index()
        fig = charts.treemap_chart(team1_batters, path_col="batter", values_col="total_run", title=team1)
        st.plotly_chart(fig)

        st.subheader(f"Contribution of Each Batsman — {team2}")
        team2_batters = balls[balls["BattingTeam"] == team2].groupby("batter")["total_run"].sum().reset_index()
        fig = charts.treemap_chart(team2_batters, path_col="batter", values_col="total_run", title=team2)
        st.plotly_chart(fig)