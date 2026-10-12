import dlt
import pandas as pd
import requests
from io import StringIO

WIKI_URL = "https://en.wikipedia.org/wiki/Botola_Pro"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


@dlt.resource(name="champions_history", write_disposition="replace")
def load_champions():
    response = requests.get(WIKI_URL, headers=HEADERS, timeout=15)
    response.raise_for_status()

    tables = pd.read_html(StringIO(response.text))

    # Table 13: ['Rank', 'Club', 'Winners', 'Seasons']
    # Table 16: ['Teams', '11-12', ...] — season by season results
    champions_table = tables[13]
    print(f"Columns: {list(champions_table.columns)}")
    print(champions_table.head(3))

    champions_table.columns = [
        str(c).lower().strip().replace(" ", "_") for c in champions_table.columns
    ]

    for row in champions_table.to_dict(orient="records"):
        if not row.get("club"):
            continue
        row["source"] = "wikipedia"
        yield row


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="botola_wikipedia",
        destination=dlt.destinations.duckdb("warehouse/botola.duckdb"),
        dataset_name="raw",
    )
    load_info = pipeline.run(load_champions())
    print(load_info)
