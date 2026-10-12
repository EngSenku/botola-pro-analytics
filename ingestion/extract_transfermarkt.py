import dlt
import requests
import time
import pandas as pd
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

BOTOLA_TEAMS = {
    "wydad-ac":        "https://www.transfermarkt.com/wydad-ac/kader/verein/5048",
    "raja-casablanca": "https://www.transfermarkt.com/raja-club-athletic/kader/verein/2068",
    "rs-berkane":      "https://www.transfermarkt.com/rs-berkane/kader/verein/19978",
    "far-rabat": "https://www.transfermarkt.com/as-far-rabat/kader/verein/9099",
    "fus-rabat":       "https://www.transfermarkt.com/fus-rabat/kader/verein/6090",
}


def parse_market_value(val_str: str) -> float:
    """Convert strings like '€500k' or '€1.20m' to float in EUR."""
    if not val_str or val_str.strip() in ["-", "", "?"]:
        return 0.0
    val_str = val_str.replace("€", "").replace(",", ".").strip()
    if "m" in val_str:
        return float(val_str.replace("m", "")) * 1_000_000
    if "k" in val_str:
        return float(val_str.replace("k", "")) * 1_000
    try:
        return float(val_str)
    except ValueError:
        return 0.0


@dlt.resource(name="market_values", write_disposition="replace")
def load_market_values():
    for team_slug, url in BOTOLA_TEAMS.items():
        time.sleep(2)  # polite delay
        print(f"Scraping {team_slug}...")

        r = requests.get(url, headers=HEADERS, timeout=15)
        if r.status_code != 200:
            print(f"  Skipped {team_slug} — status {r.status_code}")
            continue

        soup = BeautifulSoup(r.content, "lxml")
        table = soup.find("table", class_="items")
        if not table:
            print(f"  No items table found for {team_slug}")
            continue

        rows = table.find_all("tr", class_=["odd", "even"])
        print(f"  Found {len(rows)} players")

        for row in rows:
            cells = row.find_all("td")
            if len(cells) < 9:
                continue

            # Cell 3 = player name (hauptlink)
            # Cell 4 = position
            # Cell 5 = age
            # Cell 8 = market value (rechts hauptlink)
            player_name = cells[3].get_text(strip=True)
            position    = cells[4].get_text(strip=True)
            age_str     = cells[5].get_text(strip=True)
            mv_str      = cells[8].get_text(strip=True)

            if not player_name:
                continue

            try:
                age = int(age_str) if age_str.isdigit() else None
            except (ValueError, AttributeError):
                age = None

            yield {
                "team_slug":     team_slug,
                "player_name":   player_name,
                "position":      position,
                "age":           age,
                "market_value":  parse_market_value(mv_str),
                "market_value_raw": mv_str,
                "currency":      "EUR",
                "scrape_date":   pd.Timestamp.today().date().isoformat(),
                "source":        "transfermarkt",
            }


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="botola_transfermarkt",
        destination=dlt.destinations.duckdb("warehouse/botola.duckdb"),
        dataset_name="raw",
    )
    load_info = pipeline.run(load_market_values())
    print(load_info)