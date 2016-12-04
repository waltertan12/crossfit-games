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