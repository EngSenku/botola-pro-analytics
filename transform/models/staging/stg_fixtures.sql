with api_football as (
    select
        cast(fixture_id as varchar)                         as match_id,
        cast(home_team_id as varchar)                       as home_team_id,
        cast(away_team_id as varchar)                       as away_team_id,
        home_team,
        away_team,
        cast(date AT TIME ZONE 'UTC' as date)               as match_date,
        regexp_extract(matchweek, '\d+')                    as matchweek,
        cast(home_goals as integer)                         as home_goals,
        cast(away_goals as integer)                         as away_goals,
        case
            when home_goals > away_goals then 'H'
            when away_goals > home_goals then 'A'
            when home_goals = away_goals then 'D'
        end                                                 as result,
        source
    from {{ source('raw', 'fixtures') }}
    where status = 'FT'
),

sportsdb as (
    select
        cast(event_id as varchar)                           as match_id,
        null                                                as home_team_id,
        null                                                as away_team_id,
        home_team,
        away_team,
        cast(date as date)                                  as match_date,
        cast(matchweek as varchar)                          as matchweek,
        cast(home_goals as integer)                         as home_goals,
        cast(away_goals as integer)                         as away_goals,
        case
            when cast(home_goals as int) > cast(away_goals as int) then 'H'
            when cast(away_goals as int) > cast(home_goals as int) then 'A'
            else 'D'
        end                                                 as result,
        source
    from {{ source('raw', 'historical_results') }}
    where home_goals is not null
),

combined as (
    select * from api_football
    union all
    select * from sportsdb
    where match_date < (select min(match_date) from api_football)
)

select * from combined
