-- Players dimension table
select
    cast(player_id as varchar)      as player_id,
    full_name                       as player_name,
    nationality,
    age,
    cast(team_id as varchar)        as team_id,
    team_name,
    current_date                    as valid_from,
    cast('9999-12-31' as date)      as valid_to,
    true                            as is_current,
    source,
    loaded_at
from {{ ref('stg_players') }}
