__author__ = 'afordyce'


class Team():

    def __init__(self, name):
        self.elo_score = 1600
        self.name = name

    def setELO(self, newELO):
        self.elo_score = newELO