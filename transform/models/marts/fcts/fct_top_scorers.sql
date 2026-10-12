select
    player_name,
    team_name,
    nationality,
    goals,
    coalesce(assists, 0)                                          as assists,
    minutes_played,
    round(goals::double / nullif(minutes_played, 0) * 90, 2)     as goals_per_90,
    round(coalesce(assists, 0)::double / nullif(minutes_played, 0) * 90, 2) as assists_per_90,
    goals + coalesce(assists, 0)                                  as goal_contributions,
    source
from {{ ref('stg_player_stats') }}
where goals > 0
order by goals desc