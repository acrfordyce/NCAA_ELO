__author__ = 'afordyce'


import urllib
import urllib2
import re
from datetime import date, timedelta
from team import Team
from elo import elo_calc


class Schedule:

    baseURL = 'http://www.sports-reference.com/cbb/boxscores/index.cgi?'

    def __init__(self, startDate=date(2014,11,1), endDate=date(2015,3,15)):
        self.teamDict = {}
        self.scores = []
        period = endDate.toordinal() - startDate.toordinal()
        dateList = [startDate + timedelta(days=x) for x in range(period)]
        m = re.compile("no_highlight stats_table wide_table.*?<td>.*?<td>(.*?)</td>.*?>(.*?)</td>" + \
                       ".*?<td>(.*?)</td>.*?>(.*?)</td>", re.DOTALL)
        for d in dateList:
            print "Checking for games on " + str(d)
            args = urllib.urlencode({'month':d.month, 'day':d.day, 'year':d.year})
            request = urllib2.Request(self.baseURL + args)
            result = urllib2.urlopen(request)
            page = result.read()
            matches = m.finditer(page)
            for match in matches:
                # stripping out html tags
                team1 = re.sub("<.*?>", "", match.group(1))
                team2 = re.sub("<.*?>", "", match.group(3))
                # final re.sub removes ranking from some times, e.g. (2)
                game = {re.sub("\([0-9]*\) ", "", team1):int(match.group(2)),
                        re.sub("\([0-9]*\) ", "", team2):int(match.group(4))}
                self.scores.append(game)
            print "Game queue is now " + str(len(self.scores))

    def process(self):
        count = len(self.scores)
        for game in self.scores:
            for team in game.keys():
                if not (team in self.teamDict):
                    self.teamDict[team] = Team(team)
            teams = game.keys()
            team0 = self.teamDict.get(teams[0])
            team1 = self.teamDict.get(teams[1])
            if game.get(teams[0]) == max(game.values()):
                new_ratings = elo_calc(team0.elo_score, team1.elo_score, 1)
                team0.setELO(new_ratings[0])
                self.teamDict[team0.name] = team0
                team1.setELO(new_ratings[1])
                self.teamDict[team1.name] = team1
            else:
                new_ratings = elo_calc(team0.elo_score, team1.elo_score, 2)
                team0.setELO(new_ratings[0])
                self.teamDict[team0.name] = team0
                team1.setELO(new_ratings[1])
                self.teamDict[team1.name] = team1
            count += 1
            print "%d games processed" % count
