with ranked as (
    select
        team_name,
        match_date,
        pts,
        row_number() over (
            partition by team_name
            order by match_date desc
        ) as game_num
    from {{ ref('int_team_season_stats') }}
    where source = 'api_football'
),
last5 as (
    select * from ranked where game_num <= 5
)
select
    team_name,
    count(*)                                    as games,
    sum(case when pts = 3 then 1 else 0 end)    as w,
    sum(case when pts = 1 then 1 else 0 end)    as d,
    sum(case when pts = 0 then 1 else 0 end)    as l,
    sum(pts)                                    as form_pts,
    string_agg(
        case when pts=3 then 'W' when pts=1 then 'D' else 'L' end,
        '' order by match_date desc
    )                                           as form_string
from last5
group by team_name
order by form_pts desc
