import dlt
import requests
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("APIFOOTBALL_KEY")
HEADERS = {"x-apisports-key": API_KEY}
BASE = "https://v3.football.api-sports.io"
LEAGUE = 200
SEASON = 2024

@dlt.resource(name="fixtures", write_disposition="replace")
def load_fixtures():
    r = requests.get(f"{BASE}/fixtures",
                     headers=HEADERS,
                     params={"league": LEAGUE, "season": SEASON})
    r.raise_for_status()
    for item in r.json()["response"]:
        yield {
            "fixture_id":    item["fixture"]["id"],
            "date":          item["fixture"]["date"],
            "matchweek":     item["league"]["round"],
            "home_team":     item["teams"]["home"]["name"],
            "home_team_id":  item["teams"]["home"]["id"],
            "away_team":     item["teams"]["away"]["name"],
            "away_team_id":  item["teams"]["away"]["id"],
            "home_goals":    item["goals"]["home"],
            "away_goals":    item["goals"]["away"],
            "status":        item["fixture"]["status"]["short"],
            "source":        "api_football",
        }

@dlt.resource(name="standings", write_disposition="replace")
def load_standings():
    r = requests.get(f"{BASE}/standings",
                     headers=HEADERS,
                     params={"league": LEAGUE, "season": SEASON})
    r.raise_for_status()
    for league in r.json()["response"]:
        for entry in league["league"]["standings"][0]:
            yield {
                "team_id":        entry["team"]["id"],
                "team_name":      entry["team"]["name"],
                "position":       entry["rank"],
                "played":         entry["all"]["played"],
                "won":            entry["all"]["win"],
                "drawn":          entry["all"]["draw"],
                "lost":           entry["all"]["lose"],
                "goals_for":      entry["all"]["goals"]["for"],
                "goals_against":  entry["all"]["goals"]["against"],
                "goal_diff":      entry["goalsDiff"],
                "points":         entry["points"],
                "season":         SEASON,
                "source":         "api_football",
            }

@dlt.resource(name="top_scorers", write_disposition="replace")
def load_top_scorers():
    r = requests.get(f"{BASE}/players/topscorers",
                     headers=HEADERS,
                     params={"league": LEAGUE, "season": SEASON})
    r.raise_for_status()
    for item in r.json()["response"]:
        p = item["player"]
        s = item["statistics"][0]
        yield {
            "player_id":      p["id"],
            "player_name":    p["name"],
            "nationality":    p["nationality"],
            "age":            p["age"],
            "team_id":        s["team"]["id"],
            "team_name":      s["team"]["name"],
            "goals":          s["goals"]["total"],
            "assists":        s["goals"]["assists"],
            "minutes_played": s["games"]["minutes"],
            "appearances":    s["games"]["appearences"],
            "season":         SEASON,
            "source":         "api_football",
        }

@dlt.resource(name="teams", write_disposition="replace")
def load_teams():
    r = requests.get(f"{BASE}/teams",
                     headers=HEADERS,
                     params={"league": LEAGUE, "season": SEASON})
    r.raise_for_status()
    for item in r.json()["response"]:
        t = item["team"]
        v = item["venue"]
        yield {
            "team_id":    t["id"],
            "team_name":  t["name"],
            "founded":    t["founded"],
            "city":       v["city"],
            "stadium":    v["name"],
            "capacity":   v["capacity"],
            "badge_url":  t["logo"],
            "source":     "api_football",
        }

if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="botola_apifootball",
        destination=dlt.destinations.duckdb("warehouse/botola.duckdb"),
        dataset_name="raw",
    )
    load_info = pipeline.run([
        load_fixtures(),
        load_standings(),
        load_top_scorers(),
        load_teams(),
    ])
    print(load_info)
