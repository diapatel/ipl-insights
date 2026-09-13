import pandas as pd
import plotly.express as px


def runs_over_years_chart(yearly_runs: pd.DataFrame) -> "px.Figure":
    fig = px.line(data_frame=yearly_runs, x="year", y="total_run", markers=True)
    fig.update_xaxes(tickvals=yearly_runs["year"])
    return fig

def distribution_pie_chart(data: pd.DataFrame, names_col: str, values_col: str) -> "px.Figure":
    fig = px.pie(data_frame=data, names=names_col, values=values_col)
    return fig

def bar_chart(data: pd.DataFrame, x_col: str, y_col: str, orientation: str = "v") -> "px.Figure":
    fig = px.bar(data_frame=data, x=x_col, y=y_col, orientation=orientation)
    return fig


def scatter_chart(data: pd.DataFrame, x_col: str, y_col: str, hover_name: str = None, color_col: str = None) -> "px.Figure":
    fig = px.scatter(data_frame=data, x=x_col, y=y_col, hover_name=hover_name, color=color_col)
    return fig

def treemap_chart(data: pd.DataFrame, path_col: str, values_col: str, title: str = "") -> "px.Figure":
    data = data.copy()
    data["_all"] = "all"
    fig = px.treemap(data, path=["_all", path_col], values=values_col, title=title)
    return fig

def multi_line_chart(data: pd.DataFrame, x_col: str, y_cols: list[str]) -> "px.Figure":
    fig = px.line(data_frame=data, x=x_col, y=y_cols, markers=True)
    fig.update_xaxes(tickvals=data[x_col])
    return fig