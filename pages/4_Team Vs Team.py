import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import ast

matches = pd.read_csv("./IPL_Matches_2008_2022.csv")
balls = pd.read_csv("./IPL_Ball_by_Ball_2008_2022.csv")
# st.dataframe(matches)
matches['Date'] = pd.to_datetime(matches['Date'])

# replacing instances of Bengaluru with Bangalore
matches['City'] = matches['City'].str.replace("Bengaluru", "Bangalore")
matches['City'] = matches['City'].str.strip()

# extracting year from date column
matches["year"] = matches["Date"].dt.year

# replacing "Rising Pune Supergiant" with "Rising Pune Supergiants"
cols = ["Team1","Team2","WinningTeam","TossWinner"]
for col in cols:
    matches[col] = matches[col].str.replace("Rising Pune Supergiant", "Rising Pune Supergiants")

teams = balls["BattingTeam"].unique().tolist()

col1, col2 = st.columns(2)
with col1:
    team1 = st.selectbox("Choose Team 1", options=sorted(teams))
with col2:
    team2 = st.selectbox("Choose Team 2", options=sorted(teams))

button = st.button("Show Analysis")

if button:
    if team1 == team2:
        st.text("Please select 2 distinct teams to make a comparison.")
    else:
        # Team stats
        def get_team_stats(team_name):
            team_matches_df = matches[(matches["Team1"] == team_name) | (matches["Team2"] == team_name)]
            team_balls_df = balls[balls["BattingTeam"] == team_name]
            total_matches = team_matches_df["ID"].nunique()
            num_wins = team_matches_df[team_matches_df["WinningTeam"] == team_name].shape[0]

            # counting the number of players who've played for this team till date
            team_players = []
            team1_team = team_matches_df[team_matches_df["Team1"] == team_name]
            team2_team = team_matches_df[team_matches_df["Team2"] == team_name]

            team1_lists = team1_team["Team1Players"].apply(lambda x: ast.literal_eval(x))
            for l in team1_lists:
                team_players.extend(l)

            team2_lists = team1_team["Team1Players"].apply(lambda x: ast.literal_eval(x))
            for l in team2_lists:
                team_players.extend(l)

            num_players_till_date = len(set(team_players))

            # total runs scored till date
            total_runs_till_date = team_balls_df["total_run"].sum()

            team_stats_df = pd.DataFrame()
            team_stats_df["Metric"] = ["Total matches played till date", "Number of matches won",
                                       "Number of players till date", "Total runs till date"]
            team_stats_df["Value"] = [total_matches, num_wins, num_players_till_date, total_runs_till_date]

            return team_stats_df

        team1_stats = get_team_stats(team1)
        team2_stats = get_team_stats(team2)
        merged_stats_df = team1_stats.merge(team2_stats, on="Metric").rename(columns={"Value_x":team1, "Value_y":team2})
        st.dataframe(merged_stats_df)


        # Win percentage analysis
        def get_win_percent_viz(team_name):
            team_df = matches[(matches["Team1"] == team_name) | (matches["Team2"] == team_name)]
            total_matches = team_df["ID"].nunique()
            num_wins = team_df[team_df["WinningTeam"] == team_name].shape[0]
            viz_df = pd.DataFrame()
            viz_df["Metric"] = ["Total Matches Played", "Total Matches Won"]
            viz_df["Value"] = [total_matches, num_wins]
            return viz_df

        col1, col2= st.columns(2)

        with col1:
            st.title("Win percentage of Team1")
            team1_viz_df = get_win_percent_viz(team1)
            fig1 = px.pie(data_frame=team1_viz_df, names="Metric", values="Value")
            fig1.update_layout(showlegend=False)
            st.plotly_chart(fig1)

        with col2:
            st.title("Win percentage of Team2")
            team2_viz_df = get_win_percent_viz(team2)
            colors=["purple", "green"]
            fig2 = px.pie(data_frame=team2_viz_df, names="Metric", values="Value", color_discrete_sequence=colors)
            fig2.update_layout(showlegend=False)
            st.plotly_chart(fig2)


        # Total runs over years
        st.title("Total runs over years")
        def yearly_total_runs(team_name):
            team_matches_df = matches[(matches["Team1"] == team_name) | (matches["Team2"] == team_name)]
            team_balls_df = balls[balls["BattingTeam"] == team_name]

            team_merged_df = team_matches_df.merge(team_balls_df, on='ID')
            team_yearly_runs = team_merged_df.groupby("year")["total_run"].sum().reset_index()
            return team_yearly_runs

        team1_yearly_runs = yearly_total_runs(team1)
        team2_yearly_runs = yearly_total_runs(team2)

        fig3 = px.line(data_frame=team1_yearly_runs, x="year", y="total_run", markers='o')
        fig3.add_scatter(x=team2_yearly_runs["year"], y=team2_yearly_runs["total_run"], name=team2)
        fig3.update_xaxes(tickvals=team1_yearly_runs["year"])
        st.plotly_chart(fig3)

        # Batting average vs. strike rate of teams' players
        st.title("Batting average vs. Strike rate for the team players")
        team_df = balls[(balls["BattingTeam"] == "Chennai Super Kings") | (balls["BattingTeam"] == "Mumbai Indians")]
        total_runs_df = team_df.groupby(["BattingTeam", "batter"])["total_run"].sum().reset_index()
        total_balls_df = team_df.groupby(["BattingTeam", "batter"])["ballnumber"].count().reset_index()
        total_dismissals_df = team_df.groupby(["BattingTeam", "batter"])["isWicketDelivery"].sum().reset_index()

        final_df = total_runs_df.merge(total_balls_df).merge(total_dismissals_df)
        final_df["strike_rate"] = round((final_df["total_run"] / final_df["ballnumber"]) * 100, 2)
        final_df["batting_average"] = round(final_df["total_run"] / final_df["isWicketDelivery"], 2)
        fig6 = px.scatter(data_frame=final_df, x="strike_rate", y="batting_average", hover_name="batter", color="BattingTeam")
        st.plotly_chart(fig6)

        # Treemap to show contribution of each batsman
        st.title("Contribution of each batsman")
        def get_treemap(team1, team2):
            team1_balls = balls[balls["BattingTeam"] == team1].groupby("batter")["total_run"].sum().reset_index()
            team2_balls = balls[balls["BattingTeam"] == team2].groupby("batter")["total_run"].sum().reset_index()
            team1_balls["all"] = "all"
            team2_balls["all"] = "all"

            fig4 = px.treemap(team1_balls, path=["all","batter"], values="total_run", title=team1)
            fig5 = px.treemap(team2_balls, path=["all", "batter"], values="total_run", title=team2)

            return fig4, fig5

        treemap1, treemap2 = get_treemap(team1, team2)
        st.plotly_chart(treemap1)
        st.plotly_chart(treemap2)



