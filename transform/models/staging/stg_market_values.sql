select
    player_name,
    team_slug,
    cast(market_value as double)      as market_value_eur,
    currency,
    cast(scrape_date as date)         as valuation_date,
    source
from {{ source('raw', 'market_values') }}
