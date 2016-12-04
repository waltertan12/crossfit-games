import bs4, re
from athlete import Athlete

class Parser():
    ATHLETE_ID_REGEX = "https?:\/\/games\.crossfit\.com\/athlete\/(?P<athlete_id>\d+)"
    RANK_AND_SCORE_REGEX = "<span.*>(?P<rank>\d+)\s*\((?P<score>.*)\)\s*<[^\/]*span.*>"
    EVENT_ID_REGEX = "column(?P<event_id>\d+)"

    def __init__(self, verbose=False):
        if verbose:
            print("Initializing Parse\n")

        self.verbose = verbose

    def parse_athlete(self, athlete_id, response):
        soup = bs4.BeautifulSoup(response.text)
        trs = soup.select('tr')
        dl = soup.select('.profile-details dl')
        athlete = Athlete(athlete_id)

        for tr in trs:
            contents = tr.contents
            if len(tr.contents) < 2:
                continue

            exercise = contents[0].getText()
            value = contents[1].getText()

            athlete.set_stat(exercise, value)

        counter = 0
        for content in dl[0].contents:
            counter += 1
            if counter % 2 == 0:
                value = content.getText()
                athlete.set_personal(label, value)
            else:
                label = content.getText()[:-1]

        return athlete

    def parse_open(self, response):
        soup = bs4.BeautifulSoup(response.text)
        tds = soup.select('tr > td')
        data = []

        for td in tds:
            str_td = str(td)
            athlete_match = re.search(self.ATHLETE_ID_REGEX, str_td)
            rank_and_score = re.search(self.RANK_AND_SCORE_REGEX, str_td)
            event_id = re.search(self.EVENT_ID_REGEX, str_td)

            if athlete_match:
                athlete_id = athlete_match.group("athlete_id")
                athlete = Athlete(athlete_id)
            elif self.has_rank_score_and_event(rank_and_score, event_id):
                event_id = event_id.group("event_id")
                rank = rank_and_score.group("rank")
                score = rank_and_score.group("score")
                athlete.set_event(event_id, rank, score)
                if self.verbose:
                    print("Getting event " + event_id + " for " + athlete_id + "\n")

            if event_id == "5":
                data.append(athlete)

        return data

    def has_rank_score_and_event(self, rank_and_score, event_id):
        return rank_and_score and rank_and_score.group("rank") and rank_and_score.group("score") and event_id
