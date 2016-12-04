from event import Event
import re

class Athlete:
    TIME = "TIME"
    KG = "KG"
    LB = "LB"
    NUM = "NUM"
    IN = "IN"
    CM = "CM"
    STRING = "STRING"
    UNKNOWN = "UNKNOWN"


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
        data_type = self.get_data_type(value)
        if data_type == self.UNKNOWN:
            return

        self.stats[exercise] = self.get_standard_type(data_type, value)

        return self

    def set_personal(self, key, value):
        data_type = self.get_data_type(value)
        if data_type == self.UNKNOWN:
            return

        self.personal[key] = self.get_standard_type(data_type, value)

        return self

    def get_stats_insert_values(self):
        insert_query = ""

        for stats_index in self.stats:
            insert_query += "(" + str(self.athlete_id) + ", '" + str(stats_index) + "', " + str(self.stats[stats_index]) + "),"
        
        for personal_index in self.personal:
            insert_query += "(" + str(self.athlete_id) + ", '" + str(personal_index) + "', \"" + str(self.personal[personal_index]) + "\"),"

        return insert_query;

    def get_events_insert_values(self):
        insert_query = ""

        for event_index in self.events:
            event = self.events[event_index]
            insert_query += "(" + str(self.athlete_id) + ", " + event.to_string() + "),"

        return insert_query

    def get_standard_type(self, data_type, value):
        if data_type == self.TIME:
            time_data = value.split(":")
            return (int(time_data[0]) * 60) + int(time_data[1])
        elif data_type == self.CM:
            return int(int(re.search("\d+", value).group(0))) * 0.393701
        elif data_type == self.KG:
            return int(int(re.search("\d+", value).group(0))) * 2.20462
        elif data_type == self.LB:
            return int(re.search("\d+", value).group(0))
        elif data_type == self.IN:
            ft_in = re.search("(?P<feet>\d+)\'(?P<inches>\d+)\"", value)
            return (int(ft_in.group("feet")) * 12) + int(ft_in.group("inches"))
        return value

    def get_data_type(self, value):
        if re.search("\d?\d:\d\d", value):
            return self.TIME
        elif re.search("\d+ ?lb", value):
            return self.LB
        elif re.search("\d+ ?kg", value):
            return self.KG
        elif re.search("cm", value):
            return self.CM
        elif re.search("\d+\'\d+\"", value):
            return self.IN
        elif not bool(re.search("[^0-9]", value)):
            return self.NUM
        elif re.search("[a-zA-Z0-9 \']+", value):
            return self.STRING
        else:
            return self.UNKNOWN
