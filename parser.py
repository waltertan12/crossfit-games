import bs4

class Parser():
    REGEX = "//"

    def __init__(self, verbose=False):
        if verbose:
            print("Initializing Parse\n")

        self.verbose = verbose

    def parse(self, response):
        soup = bs4.BeautifulSoup(response.text)
        info = soup.select('tr > td')
        print(info)
        return info