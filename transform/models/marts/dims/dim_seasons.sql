select
    row_number() over (order by season_label) as season_id,
    season_label,
    null::integer                   as start_year,
    null::integer                   as end_year,
    false                           as is_current
from {{ ref('stg_champions') }}
group by season_label
order by season_label desc
