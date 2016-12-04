CREATE TABLE IF NOT EXISTS event(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    athlete_id INTEGER NOT NULL,
    event_id INTEGER,
    event_type STRING,
    rank INTEGER,
    score INTEGER
);

CREATE UNIQUE INDEX athlete_id_event_id_index ON event (athlete_id, event_id);

CREATE TABLE IF NOT EXISTS athlete(
    athlete_id INTEGER NOT NULL,
    stat STRING,
    value STRING
);

CREATE UNIQUE INDEX athlete_id_stat_index ON athlete(athlete_id, stat);

CREATE TABLE IF NOT EXISTS rank(
    athlete_id INTEGER PRIMARY KEY,
    week_one INTEGER,
    week_two INTEGER,
    week_three INTEGER,
    week_four INTEGER,
    week_five INTEGER,
    week_one_aggregate INTEGER,
    week_two_aggregate INTEGER,
    week_three_aggregate INTEGER,
    week_four_aggregate INTEGER,
    week_five_aggregate INTEGER
);

CREATE UNIQUE INDEX athlete_id ON rank(athlete_id);
CREATE INDEX week_one_aggregate ON rank(week_one_aggregate);
CREATE INDEX week_two_aggregate ON rank(week_two_aggregate);
CREATE INDEX week_three_aggregate ON rank(week_three_aggregate);
CREATE INDEX week_four_aggregate ON rank(week_four_aggregate);
CREATE INDEX week_five_aggregate ON rank(week_five_aggregate);

INSERT INTO rank (
    athlete_id, week_one, week_two, week_three, week_four, week_five, week_one_aggregate, week_two_aggregate, 
    week_three_aggregate, week_four_aggregate, week_five_aggregate
)
SELECT 
    event.athlete_id AS athlete_id,  
    e1.rank AS week_one,
    e2.rank AS week_two, 
    e3.rank AS week_three, 
    e4.rank AS week_four, 
    e5.rank AS week_five,
    (e1.rank) AS week_one_aggregate,
    (e1.rank + e2.rank) AS week_two_aggregate,
    (e1.rank + e2.rank + e3.rank) AS week_three_aggregate,
    (e1.rank + e2.rank + e3.rank + e4.rank) AS week_four_aggregate,
    (e1.rank + e2.rank + e3.rank + e4.rank + e5.rank) AS week_five_aggregate
FROM event
JOIN (SELECT DISTINCT(athlete_id) FROM event) as athlete_id ON (event.athlete_id = athlete_id.athlete_id)
LEFT JOIN event AS e1 ON (athlete_id.athlete_id = e1.athlete_id AND e1.event_id = 1)
LEFT JOIN event AS e2 ON (athlete_id.athlete_id = e2.athlete_id AND e2.event_id = 2)
LEFT JOIN event AS e3 ON (athlete_id.athlete_id = e3.athlete_id AND e3.event_id = 3)
LEFT JOIN event AS e4 ON (athlete_id.athlete_id = e4.athlete_id AND e4.event_id = 4)
LEFT JOIN event AS e5 ON (athlete_id.athlete_id = e5.athlete_id AND e5.event_id = 5)
GROUP BY event.athlete_id
ORDER BY week_five_aggregate ASC
;