class EpisodeMatch(object):
    def __init__(self, season, number, **kwargs):
        self.season = season
        self.number = number

    def __eq__(self, other):
        return self.season == other.season and self.number == other.number
