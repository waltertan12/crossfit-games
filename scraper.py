import requests, bs4, sys
from parser import Parser

class Scraper():
    URL_ONE   = "http://games.crossfit.com/scores/leaderboard.php?stage=0&sort=0&page="
    URL_TWO   = "&division=1&region=0&numberperpage=100&competition=0&frontpage=0&expanded=0&year=" 
    URL_THREE = "&full=0&showtoggles=1&hidedropdowns=1&showathleteac=0&=&is_mobile=&scaled=0&fittest=1&fitSelect=0"

    def scrape(self):
        url = self.get_crossfit_games_url()
        self.scrape_url(url)

    def scrape_url(self, url):
        response = requests.get(url)
        response.raise_for_status()
        
        self.parser.parse(response)

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

    def get_clean_data(self):
        if verbose:
            print("Getting clean data\n")
        return self.parser.parse({})

    # End Region Private Methods


if __name__ == '__main__':
    Scraper(True).scrape()