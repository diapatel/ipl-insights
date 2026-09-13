import pandas as pd
import plotly.graph_objects as go
from ipl_insights import charts


def test_runs_over_years_chart():
    fake_yearly_runs = pd.DataFrame({
        "year": [2020, 2021, 2022],
        "total_run": [100, 150, 200],
    })

    fig = charts.runs_over_years_chart(fake_yearly_runs)

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1


def test_distribution_pie_chart():
    fake_data = pd.DataFrame({
        "TossDecision": ["bat", "field"],
        "count": [30, 70],
    })

    fig = charts.distribution_pie_chart(fake_data, names_col="TossDecision", values_col="count")

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1

def test_bar_chart():
    fake_data = pd.DataFrame({
        "batter": ["V Kohli", "MS Dhoni", "AB de Villiers"],
        "batsman_run": [300, 250, 280],
    })

    fig = charts.bar_chart(fake_data, x_col="batter", y_col="batsman_run")

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1


def test_scatter_chart():
    fake_data = pd.DataFrame({
        "batter": ["V Kohli", "MS Dhoni"],
        "strike_rate": [130.5, 135.2],
        "batting_average": [37.2, 38.9],
    })

    fig = charts.scatter_chart(fake_data, x_col="strike_rate", y_col="batting_average", hover_name="batter")

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1

def test_treemap_chart():
    fake_data = pd.DataFrame({
        "batter": ["V Kohli", "MS Dhoni"],
        "total_run": [300, 250],
    })

    fig = charts.treemap_chart(fake_data, path_col="batter", values_col="total_run", title="CSK")

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1

def test_multi_line_chart():
    fake_data = pd.DataFrame({
        "year": [2020, 2021],
        "fours": [10, 15],
        "sixes": [5, 8],
    })

    fig = charts.multi_line_chart(fake_data, x_col="year", y_cols=["fours", "sixes"])

    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 2