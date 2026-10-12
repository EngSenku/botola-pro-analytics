-- explode multi-season rows into one row per season
with raw as (
    select
        club            as champion_team,
        cast(seasons as varchar) as seasons_raw,
        source
    from {{ source('raw', 'champions_history') }}
    where club is not null
),
-- split comma-separated seasons into individual rows
split as (
    select
        champion_team,
        trim(unnest(string_split(seasons_raw, ','))) as season_label,
        source
    from raw
)
select * from split
where season_label != ''
