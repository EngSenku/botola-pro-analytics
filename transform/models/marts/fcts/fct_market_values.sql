with mv as (
    select
        team_slug,
        sum(market_value_eur)           as total_squad_value,
        avg(market_value_eur)           as avg_player_value,
        count(*)                        as squad_size,
        valuation_date
    from {{ ref('stg_market_values') }}
    group by team_slug, valuation_date
),
standings as (
    select team_name, position, points
    from {{ ref('fct_standings') }}
),
-- manual slug mapping since team names don't match transfermarkt slugs
slug_map as (
    select * from (values
        ('wydad-ac',        'Wydad AC'),
        ('raja-casablanca', 'Raja Casablanca'),
        ('rs-berkane',      'Renaissance Berkane'),
        ('far-rabat',       'FAR Rabat'),
        ('fus-rabat',       'FUS Rabat')
    ) t(slug, team_name)
)
select
    mv.team_slug,
    sm.team_name,
    mv.total_squad_value,
    mv.avg_player_value,
    mv.squad_size,
    mv.valuation_date,
    s.position          as league_position,
    s.points            as league_points
from mv
inner join slug_map sm on sm.slug = mv.team_slug
left join standings s  on s.team_name = sm.team_name
