import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from io import BytesIO

st.set_page_config(page_title="IPL Data Analyzer")
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

def display_match_analysis(dataframe):
    num_seasons = matches["Season"].nunique()
    num_matches = matches["ID"].count()
    num_teams = len(set(matches["Team1"].unique().tolist()) | set(matches["Team2"].unique().tolist()))
    num_umpires = len(set(matches["Umpire1"].unique().tolist()) | set(matches["Umpire2"].unique().tolist()))
    num_venues = matches["Venue"].nunique()

    # counting the number of all the players who have participated in IPL till date
    players = []

    for batter in balls["batter"].unique():
        if batter not in players:
            players.append(batter)

    for bowler in balls["bowler"].unique():
        if bowler not in players:
            players.append(bowler)

    num_players = len(players)

    stats_df = pd.DataFrame()
    stats_df["Metric"] = ["Total number of seasons till date", "Total number of matches till date",
                          "Total number of participating teams till date", \
                          "Total number of umpires till date", "Total number of venues IPL was organized at",
                          "Total number of players participated in IPL"]
    stats_df["Value"] = [num_seasons, num_matches, num_teams, num_umpires, num_venues, num_players]
    st.dataframe(stats_df)


    # 1. match count per season/year
    st.title("Match Count per year")
    temp = (matches
            .groupby(matches['Date'].dt.year)['ID']
            .count()
            .reset_index()
            .rename(columns={'Date': 'Year', 'ID': 'count'})
            )
    # st.dataframe(temp)
    fig1 = px.bar(data_frame=temp, x='Year', y='count')
    fig1.update_xaxes(tickvals=temp['Year'])
    st.plotly_chart(fig1)




    # 2. city where maximum number of matches were played each season
    col1, col2 = st.columns(2)
    with col1:
        st.title("Cities where maximum number of matches were played each season")
        match_count = matches.groupby(['Season', 'City']).size().reset_index(name='match_count')
        city_with_max_matches = match_count.loc[match_count.groupby('Season')['match_count'].idxmax()].reset_index(
            drop=True).rename(columns={'match_count': 'Match count'})
        st.dataframe(city_with_max_matches)

    with col2:
        # 3. Toss Decision
        st.title("Distribution of Toss decisions")
        toss_select = st.selectbox("Select a season: ", options=["Overall"] + matches["Season"].unique().tolist())
        if toss_select == "Overall":
            temp = matches
        else:
            temp = matches[matches["Season"] == toss_select]
        fig2 = px.pie(data_frame=temp, values="ID", names="TossDecision")
        st.plotly_chart(fig2)

    # 4. Trends of superovers over years
    st.title("Trends of superovers over the years")
    temp_superover = matches.groupby("year")['SuperOver'].count().reset_index(name='superover_count')
    fig3 = px.line(data_frame=temp_superover, x='year', y='superover_count', markers='o')
    fig3.update_layout(title_text='Trends of superover over years')
    fig3.update_xaxes(tickvals=matches["year"].unique())
    st.plotly_chart(fig3)



    # 5. Distribution of matches won over the years
    st.title("Distribution of matches won  over years")
    temp_winners = (matches["WinningTeam"]
            .value_counts()
            .reset_index())
    #temp_winners.rename(columns={"index": "Winner", "WinningTeam": "count"}, inplace=True)
    fig4 = px.pie(data_frame=temp_winners, values="count", names="WinningTeam")
    st.plotly_chart(fig4)


    # 6. Tournament winners over the years
    st.title("Tournament winners over the years")
    winner_df = matches[matches["MatchNumber"] == "Final"].groupby("WinningTeam")["ID"].count().reset_index()
    fig5 = px.pie(data_frame=winner_df, names="WinningTeam", values="ID")
    st.plotly_chart(fig5)



    # 7. Margin Of Victory Distribution
    st.title("Margin of Victory Distribution")
    fig6 = px.histogram(data_frame=matches, x="Margin")
    st.plotly_chart(fig6)

    # 8. Wordcloud of Player of the matches
    st.title("Players of the match")
    potm_text = " ".join(matches["Player_of_Match"].dropna())
    wordcloud= WordCloud(height=600, width=1000).generate(potm_text)
    fig7 = plt.imshow(wordcloud)
    # Save the plot to BytesIO object
    image_stream = BytesIO()
    plt.savefig(image_stream, format='png')
    plt.close()

    # Display the Word Cloud in Streamlit
    st.image(image_stream, caption='Word Cloud of Player of the Match')


    # 9. Outcome decision
    st.title("Outcome Distribution")
    temp_outcome = matches["WonBy"].value_counts().reset_index()
    fig7 = px.pie(data_frame=temp_outcome, names="WonBy", values="count")
    st.plotly_chart(fig7)

    # 10. Avg. Margins vs Venue
    st.title("Average margins vs Venue")
    temp_margin = matches.groupby("Venue")["Margin"].mean().round(2).sort_values()
    fig8 = px.bar(data_frame=temp_margin, x="Margin", orientation="h")
    st.plotly_chart(fig8)

    # 11. Popular Umpires
    st.title("Popular Umpires")
    fav_ump1 = matches['Umpire1'].value_counts().head(1)
    fav_ump2 = matches['Umpire2'].value_counts().head(1)
    st.text(f"{fav_ump1.index[0]} has assumed the role of Umpire 1 {fav_ump1.values[0]} times till 2022.")
    st.text(f"{fav_ump2.index[0]} has assumed the role of Umpire 2 {fav_ump2.values[0]} times till 2022.")





display_match_analysis(matches)
