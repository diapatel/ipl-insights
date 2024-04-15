import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from io import BytesIO

matches = pd.read_csv("./IPL_Matches_2008_2022.csv")
matches['Date'] = pd.to_datetime(matches['Date'])
matches["year"] = matches["Date"].dt.year
matches["Team1"] = matches["Team1"].str.replace("Rising Pune Supergiant", "Rising Pune Supergiants")
matches["Team2"] = matches["Team2"].str.replace("Rising Pune Supergiant", "Rising Pune Supergiants")
matches["Team1"] = matches["Team1"].str.replace("Rising Pune Supergiantss", "Rising Pune Supergiants")
matches["Team2"] = matches["Team2"].str.replace("Rising Pune Supergiantss", "Rising Pune Supergiants")

# importing ball by ball data
balls = pd.read_csv("./IPL_Ball_by_Ball_2008_2022.csv")


selected_team = st.selectbox("Select a team", options=matches["Team1"].unique())

def get_team_details(team_name):
    team_df = matches[(matches["Team1"] == team_name) | (matches["Team2"] == team_name)]
    balls_df = balls[balls["BattingTeam"] == team_name]
    num_matches_played = team_df.shape[0]
    num_matches_won = team_df[team_df["WinningTeam"] == team_name].shape[0]
    num_tournaments_won = team_df[(team_df["MatchNumber"] == "Final") & (team_df["WinningTeam"] == team_name)].shape[0]


    result_df = pd.DataFrame()
    result_df["Metric"] = [ "Number of matches played till date","Number of matches won till date" , "Number of tournaments won till date"]
    result_df["Value"] = [num_matches_played, num_matches_won, num_tournaments_won]
    st.dataframe(result_df)

    # 2. Distribution of wins againts other IPL teams
    st.title("Distribution of wins against other IPL teams")
    team_df = matches[(matches["Team1"] == team_name) | (matches["Team2"] == team_name)]
    team_df["Opponent"] = team_df.apply(lambda x: x["Team1"] if x["Team2"] == team_name else x["Team2"],
                                        axis=1)
    team_wins = team_df[team_df["WinningTeam"] == team_name]
    csk_wins_count = team_wins.groupby("Opponent")["ID"].count().reset_index()
    fig1 = px.pie(data_frame=team_wins, names="Opponent", values="ID")
    st.plotly_chart(fig1)

    # Total runs over years
    st.title("Total runs over years")
    runs_df = team_df.merge(balls_df, on="ID")[["year", "total_run"]]
    temp = runs_df.groupby("year")["total_run"].sum().reset_index()
    fig5 = px.line(data_frame=temp, x="year", y="total_run")
    fig5.update_xaxes(tickvals=temp["year"])
    st.plotly_chart(fig5)

    # Top 15 Batsmen
    st.title("Top 15 Batsmen")
    team_balls_df = balls[balls["BattingTeam"] == team_name]
    top_15_batter = team_balls_df.groupby("batter")["batsman_run"].sum().sort_values(ascending=False).head(15).reset_index()
    fig2 = px.bar(data_frame=top_15_batter, x="batter", y='batsman_run')
    st.plotly_chart(fig2)

    # 3. Top 15 Bowlers
    st.title("Top 15 Bowlers")
    team_balls_df = balls[balls["BattingTeam"] == team_name]
    top_15_bowler = team_balls_df.groupby("bowler")["isWicketDelivery"].sum().sort_values(ascending=False).head(
        15).reset_index()
    fig3 = px.bar(data_frame=top_15_bowler, x="bowler", y='isWicketDelivery')
    st.plotly_chart(fig3)

    # 4. Batting average vs strike rate of players
    st.title("Batting Average vs. Strike rate")
    team_df = balls[balls["BattingTeam"] == team_name]
    total_runs_df = team_df.groupby("batter")["total_run"].sum().reset_index()
    total_balls_df = team_df.groupby("batter")["ballnumber"].count().reset_index()
    total_dismissals_df = team_df.groupby("batter")["isWicketDelivery"].sum().reset_index()

    final_df = total_runs_df.merge(total_balls_df).merge(total_dismissals_df)
    final_df["strike_rate"] = round((final_df["total_run"] / final_df["ballnumber"]) * 100, 2)
    final_df["batting_average"] = round(final_df["total_run"] / final_df["isWicketDelivery"], 2)

    fig4 = px.scatter(data_frame=final_df, x="strike_rate", y="batting_average", hover_name="batter")
    st.plotly_chart(fig4)

    # Players of the match wordcloud
    st.title("Players of the match")
    temp_df = matches[(matches["Team1"] == team_name) | (matches["Team2"] == team_name)]
    potm_text = " ".join(temp_df["Player_of_Match"].dropna())
    wordcloud = WordCloud(height=600, width=1000).generate(potm_text)
    fig6 = plt.imshow(wordcloud)
    # Save the plot to BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Display the Word Cloud in Streamlit
    st.image(image_stream, caption='Word Cloud of Player of the Match')

    # Distribution of wickets
    st.title("Distribution of dismissal kinds")
    temp = team_df["kind"].dropna().value_counts().reset_index()
    fig7 = px.pie(data_frame=temp, names="kind", values="count")
    st.plotly_chart(fig7)

    # Toss decision
    st.title("Toss Decision")
    selected_team_matches = matches[(matches["Team1"] == team_name) | (matches["Team2"] == team_name)]
    toss = selected_team_matches["TossDecision"].value_counts().reset_index()
    fig8 = px.pie(data_frame=toss, names="TossDecision", values="count")
    st.plotly_chart(fig8)
















# # 1. Team
#stats
get_team_details(selected_team)



















