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
matches["Team1Players"] = matches["Team1Players"].apply(lambda x: ast.literal_eval(x))
matches["Team2Players"] = matches["Team2Players"].apply(lambda x: ast.literal_eval(x))

batter_list = balls["batter"].unique().tolist()
bowler_list = balls["bowler"].unique().tolist()
player_list = set(batter_list + bowler_list)

col1, col2 = st.columns(2)
with col1:
    player1 = st.selectbox("Choose Player 1", options=sorted(player_list))
with col2:
    player2 = st.selectbox("Choose Player 2", options=sorted(player_list))

button = st.button("Show Analysis")

# creating a dataframe that consists of players and their corresponding teams
new_data = []

for index, row in matches.iterrows():
    team_name = row['Team1']
    players_list = row['Team1Players']

    for player in players_list:
        if player not in new_data:
            new_data.append({'Player': player, 'Team': team_name})

player_team_df = pd.DataFrame(new_data)
player_team_df.drop_duplicates(inplace=True)

def get_player_stats(player_name):
    player_balls = balls[(balls["batter"] == player_name) | (balls["bowler"] == player_name)]
    total_matches = player_balls["ID"].nunique()
    num_balls = player_balls["ballnumber"].count()
    total_runs = player_balls["total_run"].sum()
    num_fours = player_balls[player_balls["total_run"] == 4].shape[0]
    num_sixes = player_balls[player_balls["total_run"] == 6].shape[0]
    num_dismissals = player_balls["isWicketDelivery"].sum()
    teams = player_team_df[player_team_df["Player"] == player_name]["Team"].unique().tolist()

    # 50s and 100s
    runs_per_match = player_balls.groupby('ID')['batsman_run'].sum().reset_index()
    filt = (runs_per_match['batsman_run'] >= 50) & (runs_per_match['batsman_run'] < 100)
    fifties = runs_per_match[filt].shape[0]
    centuries = runs_per_match[runs_per_match['batsman_run'] >= 100].shape[0]

    def batting_average(batsman_name):
        """This function takes a batsman's name as input and returns their batting average."""
        batsman_df = balls[balls['batter'] == batsman_name]
        total_runs = batsman_df['batsman_run'].sum()
        out_count = batsman_df['isWicketDelivery'].sum()
        return round(total_runs / out_count, 2)

    def get_strike_rate(batsman_name):
        batsman_df = balls[balls['batter'] == batsman_name]
        return round((batsman_df['batsman_run'].sum() / batsman_df['ballnumber'].count()) * 100, 2)

    batting_avg = batting_average(player_name)
    strike_rate = get_strike_rate(player_name)

    player_stats_df = pd.DataFrame()
    player_stats_df["Metric"] = ["Total Matches Played", "Total Balls Played", "Total Runs scored", "Strike rate",
                                 "Batting average", "Fours", "Sixes", "Fifties", "Hundreds", "Number of dismissals",
                                 "Teams Played For"]
    player_stats_df["Value"] = [total_matches, num_balls, total_runs, strike_rate, batting_avg, num_fours, num_sixes,
                                fifties, centuries, num_dismissals, teams]
    return player_stats_df


def get_contribution_piechart(player_name):

    player_team = balls[balls["batter"] == player_name]["BattingTeam"].values[0]
    total_team_runs = balls[balls["BattingTeam"] == player_team]["total_run"].sum()
    total_player_runs = balls[balls["batter"] == player_name]["total_run"].sum()

    viz_df = pd.DataFrame()
    viz_df["Metric"] = ["Total Runs by the team", "Total runs by the player"]
    viz_df["Value"] = [total_team_runs, total_player_runs]

    fig = px.pie(data_frame=viz_df, names="Metric", values="Value")
    fig.update_layout(showlegend=False)
    return fig


if button:
    if player1 == player2:
        st.text("Please select 2 distinct players for rational comparison.")

    else:
        # 1. Player Stats dataframe
        player1_stats = get_player_stats(player1)
        player2_stats = get_player_stats(player2)
        return_df = (player1_stats
                     .merge(player2_stats, on="Metric")
                     .rename(columns={"Value_x":player1, "Value_y":player2}))

        st.dataframe(return_df)

        # 2. Contribution pie chart
        player1_pie = get_contribution_piechart(player1)
        player2_pie = get_contribution_piechart(player2)

        col1, col2 = st.columns(2)
        with col1:
            title1 = f"Contribution of {player1} to their team"
            st.title(title1)
            st.plotly_chart(player1_pie)
        with col2:
            title2 = f"Contribution of {player2} to their team"
            st.title(title2)
            st.plotly_chart(player2_pie)
