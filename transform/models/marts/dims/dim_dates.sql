select
    match_date                          as date_key,
    extract(year from match_date)       as year,
    extract(month from match_date)      as month,
    extract(quarter from match_date)    as quarter,
    extract(week from match_date)       as week_of_year,
    extract(dow from match_date)        as day_of_week,
    strftime(match_date, '%Y-%m-%d')    as date_string
from {{ ref('stg_fixtures') }}
group by match_date
order by match_date