select
    team_name,
    count(*)                                        as played,
    sum(won)                                        as won,
    sum(drawn)                                      as drawn,
    sum(lost)                                       as lost,
    sum(gf)                                         as goals_for,
    sum(ga)                                         as goals_against,
    sum(gf) - sum(ga)                               as goal_diff,
    sum(pts)                                        as points,
    round(sum(gf)::double / nullif(count(*), 0), 2) as avg_goals_scored,
    round(sum(ga)::double / nullif(count(*), 0), 2) as avg_goals_conceded,
    sum(clean_sheet)                                as clean_sheets,
    row_number() over (order by sum(pts) desc,
                       sum(gf) - sum(ga) desc)      as position
from {{ ref('int_team_season_stats') }}
where source = 'api_football'
group by team_name
having count(*) >= 10
order by position
