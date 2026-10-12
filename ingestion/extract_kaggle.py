import dlt
import pandas as pd

CSV_PATH = "data/Botola Pro 1 Moroccan League.csv"

@dlt.resource(name="historical_csv", write_disposition="replace")
def load_historical_csv():
    df = pd.read_csv(CSV_PATH)
    df.columns = [c.lower().strip().replace(" ", "_") for c in df.columns]

    # split "2 - 0" into home_goals and away_goals
    if "score" in df.columns:
        df[["home_goals", "away_goals"]] = (
            df["score"]
            .str.strip()
            .str.split(r"\s*-\s*", expand=True)
            .astype(float)
            .astype("Int64")
        )
        df = df.drop(columns=["score"])

    # align column names with the warehouse schema
    df = df.rename(columns={
        "team_1": "home_team",
        "team_2": "away_team",
        "round":  "matchweek",
        "date":   "match_date",
    })

    for row in df.to_dict(orient="records"):
        row["source"] = "kaggle_csv"
        yield row

if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="botola_kaggle",
        destination=dlt.destinations.duckdb("warehouse/botola.duckdb"),
        dataset_name="raw",
    )
    pipeline.run(load_historical_csv())
    print("Kaggle CSV loaded.")
