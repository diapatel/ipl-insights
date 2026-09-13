import streamlit as st

st.set_page_config(page_title="IPL Insights", layout="wide")

st.title("What are IPL and IPL Insights all about?")

st.markdown(
    """
    Indian Premier League, fondly known as the IPL, isn't merely a sporting event; it's a grand festival that
    transcends boundaries, captivating not just India but the entire world. It's a unique amalgamation where cricket
    merges seamlessly with entertainment, crafting an unparalleled spectacle!

    IPL Insights opens the gateway to the dynamic realm of IPL cricket, offering interactive visualizations that
    dissect matches, scrutinize player performances, and unravel team strategies.
    """
)

st.header("A few notes for the best experience")
st.markdown(
    """
    - Use the sidebar to navigate between Match Analysis, Know a Team, Know a Player, Team vs Team, and Player vs Player.
    - This app works best in wide mode — check the settings menu (top-right) if it looks cramped.
    """
)

