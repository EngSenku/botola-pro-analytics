import dlt
import requests

LEAGUE_ID = "4520"
BASE = "https://www.thesportsdb.com/api/v1/json/123"

@dlt.resource(name="historical_results", write_disposition="append")
def load_season_results(season: str = "2024-2025"):
    r = requests.get(f"{BASE}/eventsseason.php",
                     params={"id": LEAGUE_ID, "s": season})
    r.raise_for_status()
    for event in (r.json().get("events") or []):
        yield {
            "event_id":       event.get("idEvent"),
            "date":           event.get("dateEvent"),
            "matchweek":      event.get("intRound"),
            "home_team":      event.get("strHomeTeam"),
            "away_team":      event.get("strAwayTeam"),
            "home_goals":     event.get("intHomeScore"),
            "away_goals":     event.get("intAwayScore"),
            "season":         season,
            "source":         "thesportsdb",
        }

@dlt.resource(name="teams_sportsdb", write_disposition="replace")
def load_teams():
    r = requests.get(f"{BASE}/lookup_all_teams.php",
                     params={"id": LEAGUE_ID})
    r.raise_for_status()
    for team in (r.json().get("teams") or []):
        yield {
            "team_id":     team.get("idTeam"),
            "team_name":   team.get("strTeam"),
            "founded":     team.get("intFormedYear"),
            "stadium":     team.get("strStadium"),
            "city":        team.get("strStadiumLocation"),
            "description": team.get("strDescriptionEN"),
            "badge_url":   team.get("strTeamBadge"),
            "source":      "thesportsdb",
        }

if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="botola_sportsdb",
        destination=dlt.destinations.duckdb("warehouse/botola.duckdb"),
        dataset_name="raw",
    )
    seasons = ["2022-2023", "2023-2024", "2024-2025"]
    pipeline.run([load_season_results(s) for s in seasons] + [load_teams()])
    print("TheSportsDB loaded.")
