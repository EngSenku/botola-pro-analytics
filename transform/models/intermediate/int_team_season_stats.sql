-- One row per team per match: each result unpivoted into a home and an away row.
with matches as (
    select * from {{ ref('int_matches') }}
),

home as (
    select
        match_id,
        match_date,
        matchweek,
        season_start_year,
        home_team_id                                        as team_id,
        home_team                                           as team_name,
        home_goals                                          as gf,
        away_goals                                          as ga,
        home_goals - away_goals                             as gd,
        case result when 'H' then 3 when 'D' then 1 else 0 end as pts,
        case result when 'H' then 1 else 0 end              as won,
        case result when 'D' then 1 else 0 end              as drawn,
        case result when 'A' then 1 else 0 end              as lost,
        home_clean_sheet                                    as clean_sheet,
        btts,
        'home'                                              as venue,
        source
    from matches
),

away as (
    select
        match_id,
        match_date,
        matchweek,
        season_start_year,
        away_team_id                                        as team_id,
        away_team                                           as team_name,
        away_goals                                          as gf,
        home_goals                                          as ga,
        away_goals - home_goals                             as gd,
        case result when 'A' then 3 when 'D' then 1 else 0 end as pts,
        case result when 'A' then 1 else 0 end              as won,
        case result when 'D' then 1 else 0 end              as drawn,
        case result when 'H' then 1 else 0 end              as lost,
        away_clean_sheet                                    as clean_sheet,
        btts,
        'away'                                              as venue,
        source
    from matches
)

select * from home
union all
select * from away