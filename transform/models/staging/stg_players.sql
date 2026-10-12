select
    cast(player_id as varchar)   as player_id,
    player_name                  as full_name,
    nationality,
    cast(age as integer)         as age,
    cast(team_id as varchar)     as team_id,
    team_name,
    source,
    current_timestamp            as loaded_at
from {{ source('raw', 'top_scorers') }}
