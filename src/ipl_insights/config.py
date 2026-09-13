from pathlib import Path

# path setup
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# load data
DATA_RAW = PROJECT_ROOT / "data" / "raw"
MATCHES_CSV = DATA_RAW / "IPL_Matches_2008_2022.csv"
BALLS_CSV = DATA_RAW / "IPL_Ball_by_Ball_2008_2022.csv"

# corrections in data
CITY_NAME_FIXES = {
    "Bengaluru": "Bangalore",
}

TEAM_NAME_FIXES = {
    "Rising Pune Supergiant": "Rising Pune Supergiants",
    "Rising Pune Supergiantss": "Rising Pune Supergiants",
}