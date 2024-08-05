WITH scored_games (game_id, user_id, score, start_time, end_time) as (
    SELECT g.game_id, g.user_id, count(1) as score, g.start_time, g.end_time
    from games g 
    INNER JOIN wordle_guess w on w.game_id = g.game_id
    WHERE g.outcome = 'win'
    GROUP BY g.game_id, g.user_id, g.start_time, g.end_time
)
SELECT u.firstname, avg(g.score) as score, avg(unixepoch(g.end_time)) - avg(unixepoch(g.start_time)) as avg_time,
rank() over (order by avg(g.score) asc, avg(unixepoch(g.end_time)) - avg(unixepoch(g.start_time)) asc) as rank
FROM users u
INNER JOIN scored_games g on (
	u.user_id = g.user_id
)
GROUP by u.firstname
ORDER by avg(g.score), avg(unixepoch(g.end_time)) - avg(unixepoch(g.start_time))