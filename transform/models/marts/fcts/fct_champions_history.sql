select
    champion_team,
    season_label,
    count(*) over (partition by champion_team)  as total_titles,
    row_number() over (
        partition by champion_team
        order by season_label
    )                                           as title_number
from {{ ref('stg_champions') }}
order by total_titles desc, season_label desc
