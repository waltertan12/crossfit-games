import re

class Event:
    TIME_REGEX = "(?P<minutes>\d+):(?P<seconds>\d+)"

    EVENT_TYPE_TIME = "TIME"
    EVENT_TYPE_REPS = "REPS"

    def __init__(self, event_id):
        self.event_id = event_id
        self.event_type = None
        self.score = None
        self.rank = None

    def set_rank(self, rank):
        if not rank:
            return self
        elif (type(rank) is str):
            rank = int(rank)

        self.rank = rank

        return self

    def set_score(self, score):
        if not score:
            return self;
        elif re.search(self.TIME_REGEX, score):
            time = re.search(self.TIME_REGEX, score)
            score = self.convert_time_to_seconds(time)
            self.event_type = self.EVENT_TYPE_TIME
        else:
            self.event_type = self.EVENT_TYPE_REPS

        self.score = score

        return self

    def to_string(self):
        return str(self.event_id) + ", '" + str(self.event_type) + "', " + str(self.rank) + ", " + str(self.score)

    def convert_time_to_seconds(self, time):
        return (int(time.group("minutes")) * 60) + int(time.group("seconds"))


