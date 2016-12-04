import sqlite3
import os 

class Persister():
    def __init__(self, sqlite_file = "/../db/crossfit_open_data.db"):
        self.db_path = os.path.dirname(os.path.realpath(__file__)) + sqlite_file

    def persist_athlete(self, athlete):
        return True

    def persist_events(self, data):
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()
        insert_query = self.get_events_insert_query(data)
        cursor.execute(insert_query)
        connection.commit()
        connection.close()

    def get_events_insert_query(self, data):
        insert_query = '''
            REPLACE INTO event(athlete_id, event_id, event_type, rank, score)
            VALUES 
        '''

        for athlete in data:
            insert_query += athlete.get_events_insert_values()

        insert_query = insert_query[:-1] + ";"

        return insert_query
