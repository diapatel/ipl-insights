import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

matches = pd.read_csv(r'./IPL_Matches_2008_2022.csv')
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


def get_player_stats(player_name):
    player_df = balls[balls['batter'] == player_name]
    num_matches_played = player_df['ID'].nunique()
    total_runs = player_df['batsman_run'].sum()
    num_innings = player_df['ID'].nunique()
    num_sixes = player_df[player_df['batsman_run'] == 6].shape[0]
    num_fours = player_df[player_df['batsman_run'] == 4].shape[0]


    def batting_average(batsman_name):
        """This function takes a batsman's name as input and returns their batting average."""
        batsman_df = balls[balls['batter'] == batsman_name]
        total_runs = batsman_df['batsman_run'].sum()
        out_count = batsman_df['isWicketDelivery'].sum()
        return round(total_runs / out_count, 2)

    def get_strike_rate(batsman_name):
        batsman_df = balls[balls['batter'] == batsman_name]
        return round((batsman_df['batsman_run'].sum() / batsman_df['ballnumber'].count()) * 100, 2)

    def most_runs_scored(batsman_name):
        batsman_df = balls[balls['batter'] == batsman_name]
        return batsman_df.groupby('ID')['batsman_run'].sum().sort_values(ascending=False).head(1).values[0]

    def dot_ball_percent(batsman_name):
        batsman_df = balls[balls['batter'] == batsman_name]
        num_dot_balls = player_df[player_df['batsman_run'] == 0].shape[0]
        total_balls = player_df['ballnumber'].count()
        return round((num_dot_balls / total_balls) * 100, 2)

    player_most_runs = most_runs_scored(player_name)
    player_strike_rate = get_strike_rate(player_name)
    player_batting_avg = batting_average(player_name)
    player_dot_ball_percent = dot_ball_percent(player_name)


    player_df_col1 = ['Total matches played', 'Total runs', 'Total innings', 'Fours', 'Sixes', 'Batting Average', 'Strike Rate',
                      'Maximum runs scored in a single match', 'Dot ball percentage']
    player_df_values = [num_matches_played, total_runs, num_innings, num_fours, num_sixes, player_batting_avg, player_strike_rate,
                        player_most_runs, player_dot_ball_percent]

    player_df = pd.DataFrame({
        'Statistics': player_df_col1,
        'Values': player_df_values
    })

    return player_df


# Player stats
selected_player = st.selectbox("Select a player", options=list(sorted(balls["batter"].unique())))
button = st.button("Show Analysis")

if button:

    # 1.Player statistics
    st.title('Player Statistics')
    player_stats_df = get_player_stats(selected_player)
    st.dataframe(player_stats_df)

    # Trend of fours and sixes over years
    st.title("Trends of fours and sixes over years")
    df_for_runs = balls.merge(matches, how='inner', left_on='ID', right_on='ID')[['batter', 'ID', 'innings', 'batsman_run','year', 'Season']]
    player_runs_df = df_for_runs[df_for_runs['batter'] == selected_player]
    temp1 = (player_runs_df[player_runs_df['batsman_run'] == 4]
             .groupby('year')['batsman_run']
             .count()
             .reset_index()
             .rename(columns={"batsman_run":"num_fours"}))
    temp2 = (player_runs_df[player_runs_df['batsman_run'] == 6]
             .groupby('year')['batsman_run']
             .count()
             .reset_index()
             .rename(columns={"batsman_run":"num_sixes"}))

    fig = px.line(data_frame=temp1, x="year", y="num_fours", markers="o")
    fig.add_scatter(x=temp2["year"], y=temp2["num_sixes"], name="num_sixes")
    fig.update_xaxes(tickvals=temp1["year"])
    st.plotly_chart(fig)


    # Contribution by the player to their team's total runs
    st.title("Contribution by the player to their team's total runs")
    player_team = balls[balls["batter"] == selected_player]["BattingTeam"].values[0]
    total_team_runs = balls[balls["BattingTeam"] == player_team]["total_run"].sum()
    total_player_runs = balls[balls["batter"] == selected_player]["total_run"].sum()

    viz_df = pd.DataFrame()
    viz_df["Metric"] = ["Total Runs by the team", "Total runs by the player"]
    viz_df["Value"] = [total_team_runs, total_player_runs]

    fig2 = px.pie(data_frame=viz_df, names="Metric", values="Value")
    fig2.update_layout(showlegend=False)
    st.plotly_chart(fig2)

    # Trends of Strike rate and batting average over years
    st.title("Trends of Strike rate and Batting average over years")

    strike_rates = []
    merged = matches.merge(balls, on="ID")
    for year in matches["year"].unique():
        temp = merged[merged["year"] == year]
        batsman_df = temp[temp["batter"] == "V Kohli"]
        strike_rates.append(round((batsman_df['batsman_run'].sum() / batsman_df['ballnumber'].count()) * 100, 2))

    batting_avgs = []
    for year in matches["year"].unique():
        temp = merged[merged['year'] == year]
        batsman_df = temp[temp['batter'] == "V Kohli"]
        total_runs = batsman_df['batsman_run'].sum()
        out_count = batsman_df['isWicketDelivery'].sum()
        batting_avgs.append(round(total_runs / out_count, 2))

    final_df = pd.DataFrame()
    final_df["Year"] = matches["year"].unique()
    final_df["Strike rate"] = strike_rates
    final_df["Batting average"] = batting_avgs

    fig3 = px.line(data_frame=final_df, x="Year", y="Strike rate")
    fig3.add_scatter(x=final_df["Year"], y=final_df["Batting average"], name="Batting average")
    fig3.update_xaxes(tickvals=final_df["Year"])
    st.plotly_chart(fig3)