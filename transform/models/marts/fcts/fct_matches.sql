select
    match_id,
    match_date,
    cast(matchweek as varchar)    as matchweek,
    home_team,
    away_team,
    home_goals,
    away_goals,
    result,
    total_goals,
    btts,
    source
from {{ ref('int_matches') }}
order by match_date desc
