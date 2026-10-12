# Dashboard (Metabase)

The visualization layer for the Botola Pro Analytics platform. Metabase is
served from its own container and connects directly to the DuckDB warehouse
built by dbt.

![Metabase](https://img.shields.io/badge/Metabase-0.49-509EE3?logo=metabase&logoColor=white)

## Run

```bash
docker compose up --build metabase
```

Metabase is then available at http://localhost:3000.

## Connect to the warehouse

Add a **DuckDB** database in Metabase with the file path:

```
/warehouse/botola.duckdb
```

The `warehouse/` directory is mounted into the container by
`docker-compose.yml`, so no extra volume is needed.

## Suggested dashboards

The marts layer is designed to power these dashboards:

- **League table** — `fct_standings`
- **Form** — `fct_form_table` (includes the `WDL` string)
- **Points progression** — `fct_points_progression`
- **Top scorers** — `fct_top_scorers`
- **Match results** — `fct_matches`
- **Market value vs position** — `fct_market_values`
- **Champions history** — `fct_champions_history`

## Refresh

Dashboards read the tables built by dbt. Refresh the data by re-running the
pipeline (or let the Airflow DAG do it on schedule).

See the main [README](../README.md) for setup details.
