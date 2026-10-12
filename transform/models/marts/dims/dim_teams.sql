select
    cast(team_id as varchar)        as team_id,
    team_name,
    city,
    stadium,
    cast(founded as integer)        as founded_year,
    badge_url,
    current_date                    as valid_from,
    cast('9999-12-31' as date)      as valid_to,
    true                            as is_current,
    source
from {{ source('raw', 'teams') }}
