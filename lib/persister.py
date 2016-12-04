import sqlite3
import os 

class Persister():
    def __init__(self, sqlite_file = "/../db/crossfit_open_data.db"):
        self.db_path = os.path.dirname(os.path.realpath(__file__)) + sqlite_file

    def get_athlete_ids(self, starting_id = 0):
        data = self.select("SELECT DISTINCT(athlete_id) FROM event WHERE athlete_id > " + str(starting_id) + ";")
        athlete_ids = []

        for tup in data:
            athlete_ids.append(tup[0])

        return athlete_ids

    def persist_athlete(self, athlete):
        insert_query = self.get_athlete_insert_query(athlete)
        try:
            self.insert(insert_query)
        except(Exception):
            print(insert_query)

    def persist_events(self, event_data):
        insert_query = self.get_events_insert_query(event_data)
        self.insert(insert_query)

    def select(self, query):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        data = cursor.execute(query).fetchall()
        connection.commit()
        connection.close()

        return data

    def insert(self, query):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
        connection.close()

    def get_athlete_insert_query(self, athlete):
        insert_query = "REPLACE INTO athlete(athlete_id, stat, value) VALUES "
        insert_query += athlete.get_stats_insert_values()
        return insert_query[:-1] + ";"

    def get_events_insert_query(self, data):
        insert_query = '''
            REPLACE INTO event(athlete_id, event_id, event_type, rank, score)
            VALUES 
        '''

        for athlete in data:
            insert_query += athlete.get_events_insert_values()

        insert_query = insert_query[:-1] + ";"

        return insert_query
