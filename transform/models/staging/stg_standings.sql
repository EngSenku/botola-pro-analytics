select
    cast(position as integer)       as position,
    team_id,
    team_name,
    cast(played as integer)         as played,
    cast(won as integer)            as won,
    cast(drawn as integer)          as drawn,
    cast(lost as integer)           as lost,
    cast(goals_for as integer)      as goals_for,
    cast(goals_against as integer)  as goals_against,
    cast(goal_diff as integer)      as goal_diff,
    cast(points as integer)         as points,
    season,
    source,
    current_timestamp               as loaded_at
from {{ source('raw', 'standings') }}
