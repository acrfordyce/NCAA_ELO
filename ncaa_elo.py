__author__ = 'afordyce'


import operator
from schedule import Schedule


if __name__ == "__main__":
    schedule = Schedule()
    schedule.process()
    for team in sorted(schedule.teamDict.values(), key=operator.attrgetter('elo_score'), reverse=True):
        print team.name, team.elo_score