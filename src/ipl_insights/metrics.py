import pandas as pd

def batting_average(balls: pd.DataFrame, player_name: str) -> float:
    player_balls = balls[balls["batter"] == player_name]
    total_runs = player_balls["batsman_run"].sum()
    dismissals = player_balls["isWicketDelivery"].sum()
    if dismissals == 0:
        return float(total_runs)  # never dismissed — average equals total runs, by convention
    return round(total_runs / dismissals, 2)


def strike_rate(balls: pd.DataFrame, player_name: str) -> float:
    player_balls = balls[balls["batter"] == player_name]
    total_runs = player_balls["batsman_run"].sum()
    total_balls_faced = player_balls["ballnumber"].count()
    if total_balls_faced == 0:
        return 0.0
    return round((total_runs / total_balls_faced) * 100, 2)

def dot_ball_percent(balls: pd.DataFrame, player_name: str) -> float:
    player_balls = balls[balls["batter"] == player_name]
    num_dot_balls = player_balls[player_balls["batsman_run"] == 0].shape[0]
    total_balls = player_balls["ballnumber"].count()
    if total_balls == 0:
        return 0.0
    return round((num_dot_balls / total_balls) * 100, 2)

def most_runs_in_a_match(balls: pd.DataFrame, player_name: str) -> int:
    player_balls = balls[balls["batter"] == player_name]
    runs_per_match = player_balls.groupby("ID")["batsman_run"].sum()
    return runs_per_match.max()

def team_matches_played(matches: pd.DataFrame, team_name: str) -> int:
    team_matches = matches[(matches["Team1"] == team_name) | (matches["Team2"] == team_name)]
    return team_matches["ID"].nunique()


def team_wins(matches: pd.DataFrame, team_name: str) -> int:
    team_matches = matches[(matches["Team1"] == team_name) | (matches["Team2"] == team_name)]
    return team_matches[team_matches["WinningTeam"] == team_name].shape[0]

def team_win_percentage(matches: pd.DataFrame, team_name: str) -> float:
    played = team_matches_played(matches, team_name)
    wins = team_wins(matches, team_name)
    if played == 0:
        return 0.0
    return round((wins / played) * 100, 2)

def summary_stats(matches: pd.DataFrame, balls: pd.DataFrame) -> pd.DataFrame:
    num_seasons = matches["Season"].nunique()
    num_matches = matches["ID"].nunique()
    num_teams = len(set(matches["Team1"].unique()) | set(matches["Team2"].unique()))
    num_umpires = len(set(matches["Umpire1"].unique()) | set(matches["Umpire2"].unique()))
    num_venues = matches["Venue"].nunique()

    batters = set(balls["batter"].unique())
    bowlers = set(balls["bowler"].unique())
    num_players = len(batters | bowlers)

    stats = pd.DataFrame({
        "Metric": [
            "Total seasons", "Total matches", "Total teams",
            "Total umpires", "Total venues", "Total players",
        ],
        "Value": [num_seasons, num_matches, num_teams, num_umpires, num_venues, num_players],
    })
    return stats

def matches_per_year(matches: pd.DataFrame) -> pd.DataFrame:
    result = (
        matches.groupby("year")["ID"]
        .nunique()
        .reset_index()
        .rename(columns={"ID": "match_count"})
    )
    return result

def toss_decision_counts(matches: pd.DataFrame, season: str = None) -> pd.DataFrame:
    if season and season != "Overall":
        matches = matches[matches["Season"] == season]
    result = matches["TossDecision"].value_counts().reset_index()
    result.columns = ["TossDecision", "count"]
    return result


def tournament_winners(matches: pd.DataFrame) -> pd.DataFrame:
    finals = matches[matches["MatchNumber"] == "Final"]
    result = finals.groupby("WinningTeam")["ID"].nunique().reset_index()
    result.columns = ["WinningTeam", "count"]
    return result

def win_distribution(matches: pd.DataFrame) -> pd.DataFrame:
    result = matches["WinningTeam"].value_counts().reset_index()
    result.columns = ["WinningTeam", "count"]
    return result


def popular_umpires(matches: pd.DataFrame) -> pd.DataFrame:
    ump1 = matches["Umpire1"].value_counts()
    ump2 = matches["Umpire2"].value_counts()
    combined = ump1.add(ump2, fill_value=0).sort_values(ascending=False)
    result = combined.reset_index()
    result.columns = ["Umpire", "count"]
    return result

def margin_distribution(matches: pd.DataFrame) -> pd.DataFrame:
    result = matches["Margin"].dropna().value_counts().reset_index()
    result.columns = ["Margin", "count"]
    return result.sort_values("Margin")

def top_batters_for_team(balls: pd.DataFrame, team_name: str, n: int = 15) -> pd.DataFrame:
    team_balls = balls[balls["BattingTeam"] == team_name]
    result = (
        team_balls.groupby("batter")["batsman_run"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )
    return result


def top_bowlers_for_team(balls: pd.DataFrame, team_name: str, n: int = 15) -> pd.DataFrame:
    team_balls = balls[balls["BattingTeam"] == team_name]
    result = (
        team_balls.groupby("bowler")["isWicketDelivery"]
        .sum()
        .sort_values(ascending=False)
        .head(n)
        .reset_index()
    )
    return result

def team_runs_over_years(matches: pd.DataFrame, balls: pd.DataFrame, team_name: str) -> pd.DataFrame:
    team_matches = matches[(matches["Team1"] == team_name) | (matches["Team2"] == team_name)]
    team_balls = balls[balls["BattingTeam"] == team_name]
    merged = team_matches.merge(team_balls, on="ID")
    result = merged.groupby("year")["total_run"].sum().reset_index()
    return result

def team_batting_profile(balls: pd.DataFrame, team_name: str) -> pd.DataFrame:
    team_balls = balls[balls["BattingTeam"] == team_name]
    runs = team_balls.groupby("batter")["total_run"].sum().reset_index()
    balls_faced = team_balls.groupby("batter")["ballnumber"].count().reset_index()
    dismissals = team_balls.groupby("batter")["isWicketDelivery"].sum().reset_index()

    result = runs.merge(balls_faced, on="batter").merge(dismissals, on="batter")
    result["strike_rate"] = round((result["total_run"] / result["ballnumber"]) * 100, 2)
    result["batting_average"] = round(result["total_run"] / result["isWicketDelivery"], 2)
    return result

def player_summary(balls: pd.DataFrame, player_name: str) -> pd.DataFrame:
    player_balls = balls[balls["batter"] == player_name]
    num_matches = player_balls["ID"].nunique()
    total_runs = player_balls["batsman_run"].sum()
    num_fours = player_balls[player_balls["batsman_run"] == 4].shape[0]
    num_sixes = player_balls[player_balls["batsman_run"] == 6].shape[0]

    stats = pd.DataFrame({
        "Metric": [
            "Matches Played", "Total Runs", "Fours", "Sixes",
            "Batting Average", "Strike Rate", "Best Score", "Dot Ball %",
        ],
        "Value": [
            num_matches, total_runs, num_fours, num_sixes,
            batting_average(balls, player_name),
            strike_rate(balls, player_name),
            most_runs_in_a_match(balls, player_name),
            dot_ball_percent(balls, player_name),
        ],
    })
    return stats


def player_fours_sixes_by_year(balls: pd.DataFrame, matches: pd.DataFrame, player_name: str) -> pd.DataFrame:
    merged = balls.merge(matches[["ID", "year"]], on="ID")
    player_data = merged[merged["batter"] == player_name]

    fours = player_data[player_data["batsman_run"] == 4].groupby("year").size().reset_index(name="fours")
    sixes = player_data[player_data["batsman_run"] == 6].groupby("year").size().reset_index(name="sixes")

    result = fours.merge(sixes, on="year", how="outer").fillna(0)
    return result.sort_values("year")


def player_team_contribution(balls: pd.DataFrame, player_name: str) -> pd.DataFrame:
    player_team = balls[balls["batter"] == player_name]["BattingTeam"].iloc[0]
    team_total = balls[balls["BattingTeam"] == player_team]["total_run"].sum()
    player_total = balls[balls["batter"] == player_name]["total_run"].sum()

    result = pd.DataFrame({
        "Metric": ["Team Total Runs", "Player Runs"],
        "Value": [team_total, player_total],
    })
    return result

def two_team_batting_profile(balls: pd.DataFrame, team1: str, team2: str) -> pd.DataFrame:
    combined = balls[(balls["BattingTeam"] == team1) | (balls["BattingTeam"] == team2)]

    runs = combined.groupby(["BattingTeam", "batter"])["total_run"].sum().reset_index()
    balls_faced = combined.groupby(["BattingTeam", "batter"])["ballnumber"].count().reset_index()
    dismissals = combined.groupby(["BattingTeam", "batter"])["isWicketDelivery"].sum().reset_index()

    result = runs.merge(balls_faced, on=["BattingTeam", "batter"]).merge(dismissals, on=["BattingTeam", "batter"])
    result["strike_rate"] = round((result["total_run"] / result["ballnumber"]) * 100, 2)
    result["batting_average"] = round(result["total_run"] / result["isWicketDelivery"], 2)
    return result

def compare_teams(matches: pd.DataFrame, team1: str, team2: str) -> pd.DataFrame:
    team1_played = team_matches_played(matches, team1)
    team2_played = team_matches_played(matches, team2)
    team1_wins = team_wins(matches, team1)
    team2_wins = team_wins(matches, team2)

    result = pd.DataFrame({
        "Metric": ["Matches Played", "Matches Won"],
        team1: [team1_played, team1_wins],
        team2: [team2_played, team2_wins],
    })
    return result

def player_bowling_stats(balls: pd.DataFrame, player_name: str) -> dict:
    player_balls = balls[(balls["batter"] == player_name) | (balls["bowler"] == player_name)]
    total_matches = player_balls["ID"].nunique()
    num_balls = player_balls["ballnumber"].count()
    total_runs = player_balls["total_run"].sum()
    num_fours = player_balls[player_balls["total_run"] == 4].shape[0]
    num_sixes = player_balls[player_balls["total_run"] == 6].shape[0]
    num_dismissals = player_balls["isWicketDelivery"].sum()

    runs_per_match = player_balls.groupby("ID")["batsman_run"].sum().reset_index()
    fifties = runs_per_match[(runs_per_match["batsman_run"] >= 50) & (runs_per_match["batsman_run"] < 100)].shape[0]
    centuries = runs_per_match[runs_per_match["batsman_run"] >= 100].shape[0]

    return {
        "Total Matches Played": total_matches,
        "Total Balls Played": num_balls,
        "Total Runs Scored": total_runs,
        "Strike Rate": strike_rate(balls, player_name),
        "Batting Average": batting_average(balls, player_name),
        "Fours": num_fours,
        "Sixes": num_sixes,
        "Fifties": fifties,
        "Hundreds": centuries,
        "Number of Dismissals": num_dismissals,
    }


def compare_players(balls: pd.DataFrame, player1: str, player2: str) -> pd.DataFrame:
    stats1 = player_bowling_stats(balls, player1)
    stats2 = player_bowling_stats(balls, player2)

    result = pd.DataFrame({
        "Metric": list(stats1.keys()),
        player1: list(stats1.values()),
        player2: list(stats2.values()),
    })
    return result

def avg_margin_by_venue(matches: pd.DataFrame) -> pd.DataFrame:
    result = (
        matches.groupby("Venue")["Margin"]
        .mean()
        .round(2)
        .reset_index()
        .sort_values("Margin")
    )
    return result


def player_of_match_text(matches: pd.DataFrame) -> str:
    return " ".join(matches["Player_of_Match"].dropna())