import argparse
import connect


parser = argparse.ArgumentParser(description='Welcome to the our project focusing on the MLB.')

parser.add_argument('--batter', dest='batter', default=None, help='Specify batter name.')
parser.add_argument('--pitcher', dest='pitcher', default=None, help='Specify pitcher name.')
parser.add_argument('--team', dest='team', default=None, help='Specify team name.')

#date, daterange (day two digits, month two digits, year four digits), season, event, stat, at least one on base, numOuts, pitcherName, let vs right handed pitcher,

parser.add_argument('--d', dest='d', default=None, help='Specify date in form of DD/MM/YYYY.')
parser.add_argument('--dr', dest='dr', nargs=2, default=None, help='Specify daterange in form of DD/MM/YYYY DD/MM/YYYY.')
parser.add_argument('--season', dest='season', default=None, help='Specify season in form of YYYY.')
parser.add_argument('--batter_event_count', dest='batter_event', default=None, choices=
[
    'Batter Interference', 
    'Bunt Groundout',
    'Bunt Lineout',
    'Bunt Popout',
    'Catcher Interference',
    'Double',
    'Double Play',
    'Field Error',
    'Fielders Choice',
    'Fielders Choice Out',
    'Flyout',
    'Forceout',
    'Grounded Into DP'
    'Groundout',
    'Hit By Pitch',
    'Home Run',
    'Intent Walk',
    'Lineout',
    'Pop Out',
    'Runner Out',
    'Sac Bunt',
    'Sac Fly',
    'Sac Fly DP',
    'Sacrifice Bunt DP',
    'Single',
    'Strikeout',
    'Strikeout DP',
    'Triple',
    'Triple Play',
    'Walk'
]
, help='Specify the event you want to check for a given batter.')

parser.add_argument('--batter_stat', dest='batter_stat', default=None, choices=
[
    'BA', 
    'OBP',
    'OPS'
]
, help='Specify the stat you want to know for a given batter.')

args = parser.parse_args()

print(args.batter)