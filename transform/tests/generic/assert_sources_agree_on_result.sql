{% test assert_sources_agree_on_result(model) %}

-- Fails if a match present in both API-Football and TheSportsDB disagrees on the result.
with api_football as (
    select
        home_team,
        away_team,
        match_date,
        result
    from {{ model }}
    where source = 'api_football'
),

thesportsdb as (
    select
        home_team,
        away_team,
        match_date,
        result
    from {{ model }}
    where source = 'thesportsdb'
),

conflicts as (
    select
        a.home_team,
        a.away_team,
        a.match_date,
        a.result                as api_football_result,
        s.result                as thesportsdb_result
    from api_football a
    inner join thesportsdb s
        on  a.home_team  = s.home_team
        and a.away_team  = s.away_team
        and a.match_date = s.match_date
    where a.result != s.result
)

select * from conflicts

{% endtest %}