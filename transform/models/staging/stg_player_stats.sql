select
    cast(player_id as varchar)          as player_id,
    player_name,
    team_name,
    nationality,
    cast(goals as integer)              as goals,
    -- API-Football's top_scorers endpoint has no assists; default to 0.
    0                                   as assists, 
    cast(minutes_played as integer)     as minutes_played,
    cast(appearances as integer)        as appearances,
    cast(season as varchar)             as season,
    source,
    current_timestamp                   as loaded_at
from {{ source('raw', 'top_scorers') }}