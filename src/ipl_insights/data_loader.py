import pandas as pd
import streamlit as st
from ipl_insights import config

@st.cache_data
def load_matches() -> pd.DataFrame:
    matches = pd.read_csv(config.MATCHES_CSV)
    matches["Date"] = pd.to_datetime(matches["Date"])
    matches["year"] = matches["Date"].dt.year

    matches["City"] = matches["City"].str.strip()
    for old_name, new_name in config.CITY_NAME_FIXES.items():
        matches["City"] = matches["City"].str.replace(old_name, new_name)

    team_columns = ["Team1", "Team2", "WinningTeam", "TossWinner"]
    for col in team_columns:
        for old_name, new_name in config.TEAM_NAME_FIXES.items():
            matches[col] = matches[col].str.replace(old_name, new_name)

    return matches

@st.cache_data
def load_balls() -> pd.DataFrame:
    balls = pd.read_csv(config.BALLS_CSV)
    return balls