-- Unified match results from API-Football, TheSportsDB and the Kaggle CSV.
with source as (
    select * from {{ ref('stg_fixtures') }}
),

enriched as (
    select
        match_id,
        home_team_id,
        away_team_id,
        home_team,
        away_team,
        match_date,
        try_cast(matchweek as integer)                  as matchweek,
        home_goals,
        away_goals,
        result,

        home_goals + away_goals                         as total_goals,
        case when home_goals = 0 then 1 else 0 end      as away_clean_sheet,
        case when away_goals = 0 then 1 else 0 end      as home_clean_sheet,
        case when home_goals > 0
              and away_goals > 0 then 1 else 0 end      as btts,  -- both teams scored

        -- season derived from match date
        case
            when extract(month from match_date) >= 8
            then extract(year from match_date)
            else extract(year from match_date) - 1
        end                                             as season_start_year,

        source,
        current_timestamp                               as dbt_loaded_at
    from source
)

select * from enriched