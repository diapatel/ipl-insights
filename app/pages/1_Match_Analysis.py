import streamlit as st
from ipl_insights import data_loader, metrics, charts

st.set_page_config(page_title="Match Analysis", layout="wide")
st.title("Match Analysis")

matches = data_loader.load_matches()
balls = data_loader.load_balls()

st.subheader("Overview")
stats = metrics.summary_stats(matches, balls)
st.dataframe(stats, hide_index=True)

st.subheader("Match Count per Year")
yearly_matches = metrics.matches_per_year(matches)
fig = charts.bar_chart(yearly_matches, x_col="year", y_col="match_count")
st.plotly_chart(fig)

st.subheader("Toss Decision Distribution")
season_options = ["Overall"] + sorted(matches["Season"].unique().tolist())
selected_season = st.selectbox("Select a season", options=season_options)
toss_data = metrics.toss_decision_counts(matches, season=selected_season)
fig = charts.distribution_pie_chart(toss_data, names_col="TossDecision", values_col="count")
st.plotly_chart(fig)

st.subheader("Tournament Winners Over the Years")
winners_data = metrics.tournament_winners(matches)
fig = charts.distribution_pie_chart(winners_data, names_col="WinningTeam", values_col="count")
st.plotly_chart(fig)

st.subheader("Match Wins Distribution")
win_data = metrics.win_distribution(matches)
fig = charts.distribution_pie_chart(win_data, names_col="WinningTeam", values_col="count")
st.plotly_chart(fig)

st.subheader("Players of the Match")
potm_text = metrics.player_of_match_text(matches)
fig = charts.wordcloud_figure(potm_text)
st.pyplot(fig)

st.subheader("Margin of Victory Distribution")
margin_data = metrics.margin_distribution(matches)
fig = charts.bar_chart(margin_data, x_col="Margin", y_col="count")
st.plotly_chart(fig)

st.subheader("Average Margin of Victory by Venue")
venue_margins = metrics.avg_margin_by_venue(matches)
fig = charts.bar_chart(venue_margins, x_col="Margin", y_col="Venue", orientation="h")
st.plotly_chart(fig)

st.subheader("Popular Umpires")
umpire_data = metrics.popular_umpires(matches)
st.dataframe(umpire_data.head(10), hide_index=True)