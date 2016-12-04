from event import Event

class Athlete:
    def __init__(self, athlete_id):
        self.athlete_id = athlete_id
        self.events = {}
        self.stats = {}
        self.personal = {}

    def set_event(self, event_id, rank, score):
        event = Event(event_id)
        event.set_score(score).set_rank(rank)

        self.events[event_id] = event

        return self

    def set_stat(self, exercise, value):
        if value == "--":
            return

        print(exercise + " " + value)

        self.stats[exercise] = value

        return self

    def set_personal(self, key, value):
        if value == "--":
            return

        print(key + " " + value)

        self.personal[key] = value

        return self

    def get_stats_insert_values(self):
        insert_query = ""

        for stats_index in stats:
            insert_query += "(" + str(self.athlete_id) + ", '" + str(stats_index) + "', " + str(self.stats[stats_index]) + ")"

        return insert_query;

    def get_events_insert_values(self):
        insert_query = ""

        for event_index in self.events:
            event = self.events[event_index]
            insert_query += "(" + str(self.athlete_id) + ", " + event.to_string() + "),"

        return insert_query