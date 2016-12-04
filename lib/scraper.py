import requests, bs4, sys, sqlite3, os
from parser import Parser
from persister import Persister

class Scraper():
    URL_ONE   = "http://games.crossfit.com/scores/leaderboard.php?stage=0&sort=0&page="
    URL_TWO   = "&division=1&region=0&numberperpage=100&competition=0&frontpage=0&expanded=0&year=" 
    URL_THREE = "&full=0&showtoggles=1&hidedropdowns=1&showathleteac=0&=&is_mobile=&scaled=0&fittest=1&fitSelect=0"
    ATHLETE_URL = "http://games.crossfit.com/athlete/"

    def scrape_athletes(self):
        connection = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + "/../db/crossfit_open_data.db")
        cursor = connection.cursor()
        data = cursor.execute("SELECT DISTINCT(athlete_id) FROM event;").fetchall()
        connection.commit()
        connection.close()

        for tup in data:
            athlete_id = tup[0]
            self.scrape_athlete(athlete_id)

    def scrape_athlete(self, athlete_id):
        response = requests.get(self.ATHLETE_URL + str(athlete_id))
        response.raise_for_status()
        data = self.parser.parse_athlete(athlete_id, response)
        self.persister.persist_athlete(data)

    def scrape_open(self, start = 1, end = 50):
        while start <= end:
            url = self.get_crossfit_games_url(str(start))
            self.scrape_open_url(url)
            start = start + 1

    def scrape_open_url(self, url):
        response = requests.get(url)
        response.raise_for_status()
        
        data = self.parser.parse_open_data(response)
        self.persister.persist_events(data)

    def get_crossfit_games_url(self, page="1", year="16"):
        url = self.URL_ONE + page + self.URL_TWO + year + self.URL_THREE

        if self.verbose:
            print("Getting URL:\n" + url + "\n") 

        return url

    # End Region Public Methods

    # Start Region Private Methods
    def __init__(self, verbose=False):
        if verbose:
            print("Initializing Scraper")

        self.verbose = verbose
        self.parser = Parser(verbose)
        self.persister = Persister()

    def get_clean_data(self):
        if verbose:
            print("Getting clean data\n")
        return self.parser.parse({})

    # End Region Private Methods


if __name__ == '__main__':
    Scraper(True).scrape_athlete(649347)