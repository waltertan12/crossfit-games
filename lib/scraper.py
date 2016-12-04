import requests, bs4, sys, sqlite3, os
from parser import Parser
from persister import Persister

class Scraper():
    OPEN_URL_ONE   = "http://games.crossfit.com/scores/leaderboard.php?stage=0&sort=0&page="
    OPEN_URL_TWO   = "&division=1&region=0&numberperpage=100&competition=0&frontpage=0&expanded=0&year=" 
    OPEN_URL_THREE = "&full=0&showtoggles=1&hidedropdowns=1&showathleteac=0&=&is_mobile=&scaled=0&fittest=1&fitSelect=0"
    ATHLETE_URL    = "http://games.crossfit.com/athlete/"

    # Start Region Public Methods

    def scrape_athletes(self, starting_id = 0):
        athlete_ids = self.persister.get_athlete_ids()
        for athlete_id in athlete_ids:
            self.scrape_athlete(athlete_id)

    def scrape_open(self, start = 1, end = 50):
        while start <= end:
            url = self.get_crossfit_games_url(str(start))
            self.scrape_open_url(url)
            start = start + 1

    # End Region Public Methods

    # Start Region Private Methods
    def __init__(self, verbose=False):
        if verbose:
            print("Initializing Scraper")

        self.verbose = verbose
        self.parser = Parser(verbose)
        self.persister = Persister()

    def scrape_athlete(self, athlete_id):
        if self.verbose:
            print("Scraping athlete " + str(athlete_id))

        response = requests.get(self.ATHLETE_URL + str(athlete_id))
        response.raise_for_status()
        athlete = self.parser.parse_athlete(athlete_id, response)
        self.persister.persist_athlete(athlete)

    def scrape_open_url(self, url):
        response = requests.get(url)
        response.raise_for_status()
        
        event_data = self.parser.parse_open(response)
        self.persister.persist_events(event_data)

    def get_crossfit_games_url(self, page="1", year="16"):
        url = self.OPEN_URL_ONE + page + self.OPEN_URL_TWO + year + self.OPEN_URL_THREE

        if self.verbose:
            print("Getting URL:\n" + url + "\n") 

        return url

    # End Region Private Methods