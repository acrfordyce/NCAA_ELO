#!/usr/bin/env python

import math
import urllib
import re

def elo_calc(rating1, rating2, result):
    exp = (rating2 - rating1)/400.
    Ea = 1/(1 + math.pow(10, exp))
    Eb = 1/(1 + math.pow(10, -exp))
    if result == 1:
        winner = rating1
        Sa = 1
        Sb = 0
    elif result == 2:
        winner = rating2
        Sa = 0
        Sb = 1
    if rating1 < 2100:
        ka = 32
    elif rating1 >= 2100 and rating1 < 2400:
        ka = 24
    else:
        ka = 16
    if rating2 < 2100:
        kb = 32
    elif rating2 >= 2100 and rating2 < 2400:
        kb = 24
    else:
        kb = 16
    newrating1 = int(rating1 + ka * (Sa - Ea))
    newrating2 = int(rating2 + kb * (Sb - Eb))
    return newrating1, newrating2

def schedule_results():
    baseurl = "http://www.cbssports.com/collegebasketball/scoreboard/div1/"    
    november = range(20121101, 20121131)
    december = range(20121201, 20121232)
    january = range(20130101, 20130132)
    february = range(20130201, 20130229)
    march = range(20130301, 20130317)
    m = re.compile(r'id="final".*?b>(.*?)</b>(.*?)</td>')
    scores = []
    for j in november + december + january + february + march:
        content = urllib.urlopen(baseurl + str(j)).read()        
        teams = m.finditer(content)
        teamlist = []
        winlist = []
        for match in teams:
            teamlist.append(match.group(1))
            winlist.append(match.group(2))
        score_temp = []
        for i in range(len(teamlist)/2):
            if len(winlist[2*i])>len(winlist[2*i+1]):
                winner = 1
            else:
                winner = 2
            result = (teamlist[i*2], teamlist[i*2+1], winner)
            scores.append(result)
    return scores

def ratings_calc(scores):
    ratings = {}
    for i in scores:
        side1, side2, winner = i
        if side1 in ratings.keys():
            side1 = side1
        else:
            ratings[side1] = 1600
        if side2 in ratings.keys():
            side2 = side2
        else:
            ratings[side2] = 1600
        newrating1, newrating2 = elo_calc(ratings[side1], ratings[side2], winner)
        ratings[side1] = newrating1
        ratings[side2] = newrating2
    return ratings

if __name__ == "__main__":
    scores = schedule_results()
    ratings = ratings_calc(scores)
    for r in sorted(ratings, key=ratings.get, reverse=True):
        print r, ratings[r]
    
