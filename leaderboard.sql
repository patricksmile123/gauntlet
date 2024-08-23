WITH scored_games AS (
    SELECT g.game_id, g.user_id, COUNT(1) AS score, g.start_time, g.end_time
    FROM games g 
    INNER JOIN wordle_guess w ON w.game_id = g.game_id
    WHERE g.outcome IS NOT NULL
      AND LENGTH(g.answer) = 5
    GROUP BY g.game_id, g.user_id, g.start_time, g.end_time
)
SELECT u.firstname,
       ROUND(AVG(g.score), 2) AS score,
       ROUND(AVG(EXTRACT(EPOCH FROM g.end_time) - EXTRACT(EPOCH FROM g.start_time)), 2) AS avg_time,
       RANK() OVER (
           ORDER BY ROUND(AVG(g.score), 2) ASC, 
                    ROUND(AVG(EXTRACT(EPOCH FROM g.end_time) - EXTRACT(EPOCH FROM g.start_time)), 2) ASC
       ) AS rank
FROM users u
INNER JOIN scored_games g ON u.user_id = g.user_id
GROUP BY u.firstname
ORDER BY score, avg_time;
