__author__ = 'afordyce'


import math


def elo_calc(rating1, rating2, result):
    exp = (rating2 - rating1)/400.
    Ea = 1/(1 + math.pow(10, exp))
    Eb = 1/(1 + math.pow(10, -exp))
    if result == 1:
        winner = rating1
        Sa = 1
        Sb = 0
    else:
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


def expected_result(rating1, rating2):
    exp = (rating2 - rating1)/400.
    Ea = 1/(1 + math.pow(10, exp))
    Eb = 1/(1 + math.pow(10, -exp))
    return Ea, Eb

