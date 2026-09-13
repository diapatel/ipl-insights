import pandas as pd
from ipl_insights import metrics


def test_batting_average():
    fake_balls = pd.DataFrame({
        "batter": ["V Kohli", "V Kohli", "V Kohli", "MS Dhoni"],
        "batsman_run": [4, 6, 0, 1],
        "isWicketDelivery": [0, 0, 1, 0],
    })

    result = metrics.batting_average(fake_balls, "V Kohli")

    assert result == 10.0


def test_strike_rate():
    fake_balls = pd.DataFrame({
        "batter": ["V Kohli", "V Kohli", "V Kohli", "V Kohli", "MS Dhoni"],
        "batsman_run": [4, 6, 0, 0, 1],
        "ballnumber": [1, 2, 3, 4, 1],
    })

    result = metrics.strike_rate(fake_balls, "V Kohli")

    assert result == 250.0


def test_dot_ball_percent():
    fake_balls = pd.DataFrame({
        "batter": ["V Kohli", "V Kohli", "V Kohli", "V Kohli", "MS Dhoni", "MS Dhoni"],
        "batsman_run": [0, 0, 4, 6, 1, 1],
        "ballnumber": [1, 2, 3, 4, 1, 2],
    })

    result = metrics.dot_ball_percent(fake_balls, "V Kohli")

    assert result == 50.0

def test_most_runs_in_a_match():
    fake_balls = pd.DataFrame({
        "ID": [1, 1, 2, 2, 2],
        "batter": ["V Kohli", "V Kohli", "V Kohli", "V Kohli", "V Kohli"],
        "batsman_run": [10, 20, 5, 5, 5],
    })

    result = metrics.most_runs_in_a_match(fake_balls, "V Kohli")

    assert result == 30

def test_team_matches_played():
    fake_matches = pd.DataFrame({
        "ID": [1, 2, 3],
        "Team1": ["CSK", "MI", "CSK"],
        "Team2": ["MI", "RCB", "RCB"],
        "WinningTeam": ["CSK", "MI", "RCB"],
    })

    result = metrics.team_matches_played(fake_matches, "CSK")

    assert result == 2


def test_team_wins():
    fake_matches = pd.DataFrame({
        "ID": [1, 2, 3],
        "Team1": ["CSK", "MI", "CSK"],
        "Team2": ["MI", "RCB", "RCB"],
        "WinningTeam": ["CSK", "MI", "RCB"],
    })

    result = metrics.team_wins(fake_matches, "CSK")

    assert result == 1

def test_team_win_percentage():
    fake_matches = pd.DataFrame({
        "ID": [1, 2, 3, 4],
        "Team1": ["CSK", "MI", "CSK", "CSK"],
        "Team2": ["MI", "RCB", "RCB", "MI"],
        "WinningTeam": ["CSK", "MI", "RCB", "CSK"],
    })

    result = metrics.team_win_percentage(fake_matches, "CSK")

    assert result == 66.67

def test_summary_stats():
    fake_matches = pd.DataFrame({
        "Season": [2020, 2020, 2021],
        "ID": [1, 2, 3],
        "Team1": ["CSK", "MI", "CSK"],
        "Team2": ["MI", "RCB", "RCB"],
        "Umpire1": ["A", "B", "A"],
        "Umpire2": ["C", "D", "C"],
        "Venue": ["V1", "V2", "V1"],
    })
    fake_balls = pd.DataFrame({
        "batter": ["V Kohli", "MS Dhoni"],
        "bowler": ["J Bumrah", "V Kohli"],
    })

    result = metrics.summary_stats(fake_matches, fake_balls)

    assert result[result["Metric"] == "Total seasons"]["Value"].iloc[0] == 2
    assert result[result["Metric"] == "Total matches"]["Value"].iloc[0] == 3
    assert result[result["Metric"] == "Total teams"]["Value"].iloc[0] == 3
    assert result[result["Metric"] == "Total players"]["Value"].iloc[0] == 3

def test_matches_per_year():
    fake_matches = pd.DataFrame({
        "year": [2020, 2020, 2021],
        "ID": [1, 2, 3],
    })

    result = metrics.matches_per_year(fake_matches)

    assert result[result["year"] == 2020]["match_count"].iloc[0] == 2
    assert result[result["year"] == 2021]["match_count"].iloc[0] == 1

def test_toss_decision_counts():
    fake_matches = pd.DataFrame({
        "Season": ["2020", "2020", "2021"],
        "TossDecision": ["bat", "field", "bat"],
    })

    result_all = metrics.toss_decision_counts(fake_matches)
    assert result_all[result_all["TossDecision"] == "bat"]["count"].iloc[0] == 2

    result_2020 = metrics.toss_decision_counts(fake_matches, season="2020")
    assert result_2020[result_2020["TossDecision"] == "bat"]["count"].iloc[0] == 1


def test_tournament_winners():
    fake_matches = pd.DataFrame({
        "ID": [1, 2, 3],
        "MatchNumber": ["Final", "Qualifier", "Final"],
        "WinningTeam": ["CSK", "MI", "MI"],
    })

    result = metrics.tournament_winners(fake_matches)

    assert result[result["WinningTeam"] == "CSK"]["count"].iloc[0] == 1
    assert result[result["WinningTeam"] == "MI"]["count"].iloc[0] == 1

def test_win_distribution():
    fake_matches = pd.DataFrame({
        "WinningTeam": ["CSK", "MI", "CSK"],
    })

    result = metrics.win_distribution(fake_matches)

    assert result[result["WinningTeam"] == "CSK"]["count"].iloc[0] == 2


def test_popular_umpires():
    fake_matches = pd.DataFrame({
        "Umpire1": ["A", "A", "B"],
        "Umpire2": ["B", "C", "B"],
    })

    result = metrics.popular_umpires(fake_matches)

    assert result[result["Umpire"] == "B"]["count"].iloc[0] == 3

def test_top_batters_for_team():
    fake_balls = pd.DataFrame({
        "BattingTeam": ["CSK", "CSK", "CSK", "MI"],
        "batter": ["MS Dhoni", "MS Dhoni", "R Jadeja", "R Sharma"],
        "batsman_run": [30, 20, 10, 50],
    })

    result = metrics.top_batters_for_team(fake_balls, "CSK", n=15)

    assert result.iloc[0]["batter"] == "MS Dhoni"
    assert result.iloc[0]["batsman_run"] == 50


def test_top_bowlers_for_team():
    fake_balls = pd.DataFrame({
        "BattingTeam": ["CSK", "CSK", "CSK", "MI"],
        "bowler": ["J Bumrah", "J Bumrah", "T Boult", "Y Chahal"],
        "isWicketDelivery": [1, 0, 1, 1],
    })

    result = metrics.top_bowlers_for_team(fake_balls, "CSK", n=15)

    assert result.iloc[0]["bowler"] == "J Bumrah"
    assert result.iloc[0]["isWicketDelivery"] == 1


def test_team_runs_over_years():
    fake_matches = pd.DataFrame({
        "ID": [1, 2],
        "Team1": ["CSK", "CSK"],
        "Team2": ["MI", "RCB"],
        "year": [2020, 2021],
    })
    fake_balls = pd.DataFrame({
        "ID": [1, 2],
        "BattingTeam": ["CSK", "CSK"],
        "total_run": [180, 190],
    })

    result = metrics.team_runs_over_years(fake_matches, fake_balls, "CSK")

    assert result[result["year"] == 2020]["total_run"].iloc[0] == 180
    assert result[result["year"] == 2021]["total_run"].iloc[0] == 190


def test_team_batting_profile():
    fake_balls = pd.DataFrame({
        "BattingTeam": ["CSK", "CSK", "CSK"],
        "batter": ["MS Dhoni", "MS Dhoni", "MS Dhoni"],
        "total_run": [10, 20, 0],
        "ballnumber": [1, 2, 3],
        "isWicketDelivery": [0, 0, 1],
    })

    result = metrics.team_batting_profile(fake_balls, "CSK")

    row = result[result["batter"] == "MS Dhoni"].iloc[0]
    assert row["total_run"] == 30
    assert row["strike_rate"] == 1000.0
    assert row["batting_average"] == 30.0

def test_player_summary():
    fake_balls = pd.DataFrame({
        "ID": [1, 1, 2],
        "batter": ["V Kohli", "V Kohli", "V Kohli"],
        "batsman_run": [4, 6, 0],
        "ballnumber": [1, 2, 1],
        "isWicketDelivery": [0, 0, 1],
    })

    result = metrics.player_summary(fake_balls, "V Kohli")

    total_runs = result[result["Metric"] == "Total Runs"]["Value"].iloc[0]
    fours = result[result["Metric"] == "Fours"]["Value"].iloc[0]
    sixes = result[result["Metric"] == "Sixes"]["Value"].iloc[0]

    assert total_runs == 10
    assert fours == 1
    assert sixes == 1


def test_player_fours_sixes_by_year():
    fake_balls = pd.DataFrame({
        "ID": [1, 2],
        "batter": ["V Kohli", "V Kohli"],
        "batsman_run": [4, 6],
    })
    fake_matches = pd.DataFrame({
        "ID": [1, 2],
        "year": [2020, 2021],
    })

    result = metrics.player_fours_sixes_by_year(fake_balls, fake_matches, "V Kohli")

    row_2020 = result[result["year"] == 2020].iloc[0]
    row_2021 = result[result["year"] == 2021].iloc[0]

    assert row_2020["fours"] == 1
    assert row_2020["sixes"] == 0
    assert row_2021["fours"] == 0
    assert row_2021["sixes"] == 1


def test_player_team_contribution():
    fake_balls = pd.DataFrame({
        "batter": ["V Kohli", "V Kohli", "F du Plessis"],
        "BattingTeam": ["RCB", "RCB", "RCB"],
        "total_run": [10, 20, 5],
    })

    result = metrics.player_team_contribution(fake_balls, "V Kohli")

    team_total = result[result["Metric"] == "Team Total Runs"]["Value"].iloc[0]
    player_total = result[result["Metric"] == "Player Runs"]["Value"].iloc[0]

    assert team_total == 35
    assert player_total == 30

def test_two_team_batting_profile():
    fake_balls = pd.DataFrame({
        "BattingTeam": ["CSK", "CSK", "MI"],
        "batter": ["MS Dhoni", "MS Dhoni", "R Sharma"],
        "total_run": [10, 20, 15],
        "ballnumber": [1, 2, 1],
        "isWicketDelivery": [0, 1, 0],
    })

    result = metrics.two_team_batting_profile(fake_balls, "CSK", "MI")

    assert set(result["BattingTeam"].unique()) == {"CSK", "MI"}
    dhoni_row = result[result["batter"] == "MS Dhoni"].iloc[0]
    assert dhoni_row["total_run"] == 30


def test_compare_teams():
    fake_matches = pd.DataFrame({
        "ID": [1, 2, 3],
        "Team1": ["CSK", "MI", "CSK"],
        "Team2": ["MI", "RCB", "RCB"],
        "WinningTeam": ["CSK", "MI", "RCB"],
    })

    result = metrics.compare_teams(fake_matches, "CSK", "MI")

    played_row = result[result["Metric"] == "Matches Played"].iloc[0]
    assert played_row["CSK"] == 2
    assert played_row["MI"] == 2

def test_player_bowling_stats():
    fake_balls = pd.DataFrame({
        "ID": [1, 1, 2],
        "batter": ["V Kohli", "V Kohli", "V Kohli"],
        "bowler": ["J Bumrah", "J Bumrah", "J Bumrah"],
        "batsman_run": [4, 6, 0],
        "total_run": [4, 6, 0],
        "ballnumber": [1, 2, 1],
        "isWicketDelivery": [0, 0, 1],
    })

    result = metrics.player_bowling_stats(fake_balls, "V Kohli")

    assert result["Total Runs Scored"] == 10
    assert result["Fours"] == 1
    assert result["Sixes"] == 1


def test_compare_players():
    fake_balls = pd.DataFrame({
        "ID": [1, 2],
        "batter": ["V Kohli", "MS Dhoni"],
        "bowler": ["J Bumrah", "T Boult"],
        "batsman_run": [10, 20],
        "total_run": [10, 20],
        "ballnumber": [1, 1],
        "isWicketDelivery": [0, 0],
    })

    result = metrics.compare_players(fake_balls, "V Kohli", "MS Dhoni")

    runs_row = result[result["Metric"] == "Total Runs Scored"].iloc[0]
    assert runs_row["V Kohli"] == 10
    assert runs_row["MS Dhoni"] == 20

