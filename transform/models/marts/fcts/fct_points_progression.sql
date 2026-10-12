with base as (
    select
        team_name,
        matchweek,
        pts,
        cast(
            regexp_extract(cast(matchweek as varchar), '(\d+)$', 1)
        as integer)                             as week_num
    from {{ ref('int_team_season_stats') }}
    where source = 'api_football'
      and regexp_extract(cast(matchweek as varchar), '(\d+)$', 1) != ''
)
select
    team_name,
    matchweek,
    week_num,
    sum(pts)                                    as pts_this_week,
    sum(sum(pts)) over (
        partition by team_name
        order by week_num
        rows between unbounded preceding and current row
    )                                           as cumulative_points
from base
group by team_name, matchweek, week_num
order by team_name, week_num
