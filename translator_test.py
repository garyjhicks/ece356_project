from options import Options
from translator import *

test_suite = []

def count_events_batter():
    o = Options()
    o.batter_fn = "Tommy"
    o.batter_ln = "Pham"
    o.event_count = "Single"
    o.season = "2018"
    q = query_builder(o)
    assert q == "SELECT COUNT(event) FROM AtBats INNER JOIN Games ON AtBats.gameID = Games.gameID WHERE batterID = (SELECT first(playerID) FROM PlayerInfo WHERE firstName = 'Tommy' AND lastName = 'Pham') AND dateTime > '01/01/18 00:00:00' AND dateTime < '01/01/19 00:00:00' AND event = 'Single';" , "count_events_batter failed"
    print("count_events_batter test passed")

def batter_stat_BA_batter_season():
    o = Options()
    o.batter_fn = "Tommy"
    o.batter_ln = "Pham"
    o.batter_stat = "BA"
    o.season = "2016"
    q = query_builder(o)
    assert q == "SELECT (SELECT COUNT(*) from AtBats WHERE batterID = (SELECT first(playerID) FROM PlayerInfo WHERE firstName = 'Tommy' AND lastName = 'Pham') AND (event = 'Single' OR event = 'Double' OR event = 'Triple' OR event = 'Home Run')) / COUNT(*) FROM AtBats INNER JOIN Games ON AtBats.gameID = Games.gameID WHERE batterID = (SELECT first(playerID) FROM PlayerInfo WHERE firstName = 'Tommy' AND lastName = 'Pham') AND dateTime > '01/01/16 00:00:00' AND dateTime < '12/31/16 00:00:00' AND (event = 'Bunt Groundout' OR event = 'Field Error' OR event = 'Fielders Choice' OR event = 'Fielders Choice Out' OR event = 'Flyout' OR event = 'Forceout' OR event = 'Grounded Into DP' OR event = 'Groundout' OR event = 'Lineout' OR event = 'Popout' OR event = 'Strikeout' OR event = 'Strikeout DP' OR event = 'Triple Play' OR event = 'Single' OR event = 'Double' OR event = 'Triple' OR event = 'Home Run');" , "batter_stat_BA_batter_season"
    print("batter_stat_batter test passed")

def pitcher_stat_K9_batter_dr():
    o = Options()
    o.pitcher_fn = "Yu"
    o.pitcher_ln = "Darvish"
    o.pitcher_stat = "K/9"
    o.season = "2016"
    q = query_builder(o)
    assert q == "SELECT COUNT(event) / ( COUNT DISTINCT gameID, inning, outs / 3) FROM AtBats INNER JOIN Games ON AtBats.gameID = Games.gameID WHERE pitcherID = (SELECT first(playerID) FROM PlayerInfo WHERE firstName = 'Yu' AND lastName = 'Darvish') AND dateTime > '01/01/16 00:00:00' AND dateTime < '12/31/16 00:00:00' AND event = 'Strikeout';" , "pitcher_stat_K9_batter_dr"
    print("pitcher_stat_K9_batter_dr passed")



test_suite.append(count_events_batter)
test_suite.append(batter_stat_BA_batter_season)
test_suite.append(pitcher_stat_K9_batter_dr)

for test in test_suite:
    test()