import argparse
import connect

parser = argparse.ArgumentParser(description='Welcome to the our project focusing on the MLB. This is meant for fans interested is determining all kinds of stats and relationships over the course of the MLB from 2015-2018.')

parser.add_argument('--quit', action='store_true', help='Exit the cli.')

# Only allow batter, pitcher, team, batter and pitcher, batter and team, pitcher and team, never all three
parser.add_argument('--batter_fn', dest='batter_fn', nargs='+', default=None, help='Specify batter first name.')
parser.add_argument('--pitcher_fn', dest='pitcher_fn', nargs='+', default=None, help='Specify pitcher first name.')
parser.add_argument('--batter_ln', dest='batter_ln', nargs='+', default=None, help='Specify batter last name.')
parser.add_argument('--pitcher_ln', dest='pitcher_ln', nargs='+', default=None, help='Specify pitcher last name.')
parser.add_argument('--team', dest='team', default=None, nargs='+', choices=[
    'Angels',
    'Diamondbacks',
    'Braves',
    'Orioles',
    'Red Sox',
    'White Sox',
    'Cubs',
    'Reds',
    'Indians',
    'Rockies',
    'Tigers',
    'Astros',
    'Royals',
    'Dodgers',
    'Marlins',
    'Brewers',
    'Reds',
    'Yankees',
    'Mets',
    'Athletics',
    'Phillies',
    'Pirates',
    'Padres',
    'Mariners',
    'Giants',
    'Cardinals',
    'Rays',
    'Rangers',
    'Blue Jays',
    'Nationals'
],help='Specify team name.')

parser.add_argument('--opp_team_vs_t', dest='opp_team_vs_t', default=None, nargs='+', choices=[
    'Angels',
    'Diamondbacks',
    'Braves',
    'Orioles',
    'Red Sox',
    'White Sox',
    'Cubs',
    'Reds',
    'Indians',
    'Rockies',
    'Tigers',
    'Astros',
    'Royals',
    'Dodgers',
    'Marlins',
    'Brewers',
    'Reds',
    'Yankees',
    'Mets',
    'Athletics',
    'Phillies',
    'Pirates',
    'Padres',
    'Mariners',
    'Giants',
    'Cardinals',
    'Rays',
    'Rangers',
    'Blue Jays',
    'Nationals'
],help='Specify opposing team name.')

parser.add_argument('--opp_team_vs_b', dest='opp_team_vs_b', default=None, nargs='+', choices=[
    'Angels',
    'Diamondbacks',
    'Braves',
    'Orioles',
    'Red Sox',
    'White Sox',
    'Cubs',
    'Reds',
    'Indians',
    'Rockies',
    'Tigers',
    'Astros',
    'Royals',
    'Dodgers',
    'Marlins',
    'Brewers',
    'Reds',
    'Yankees',
    'Mets',
    'Athletics',
    'Phillies',
    'Pirates',
    'Padres',
    'Mariners',
    'Giants',
    'Cardinals',
    'Rays',
    'Rangers',
    'Blue Jays',
    'Nationals'
],help='Specify opposing team name.')

parser.add_argument('--opp_team_vs_p', dest='opp_team_vs_p', default=None, nargs='+', choices=[
    'Angels',
    'Diamondbacks',
    'Braves',
    'Orioles',
    'Red Sox',
    'White Sox',
    'Cubs',
    'Reds',
    'Indians',
    'Rockies',
    'Tigers',
    'Astros',
    'Royals',
    'Dodgers',
    'Marlins',
    'Brewers',
    'Reds',
    'Yankees',
    'Mets',
    'Athletics',
    'Phillies',
    'Pirates',
    'Padres',
    'Mariners',
    'Giants',
    'Cardinals',
    'Rays',
    'Rangers',
    'Blue Jays',
    'Nationals'
],help='Specify opposing team name.')

# date and season filters 
parser.add_argument('--d', dest='d', default=None, help='Specify date in form of DD/MM/YYYY.')
parser.add_argument('--dr', dest='dr', nargs=2, default=None, help='Specify daterange in form of DD/MM/YYYY DD/MM/YYYY.')
parser.add_argument('--season', dest='season', default=None, help='Specify season in form of YYYY.')

# events that can be selected
parser.add_argument('--event_count', dest='event_count', nargs='+', default=None, choices=
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

# specific batter stats
parser.add_argument('--batter_stat', dest='batter_stat', default=None, choices=
[
    'BA', 
    'OBP',
    'OPS',
    'SLG',
    'BB/K'
]
, help='Specify the stat you want to know for a given batter.')

# specific pitcher stats
parser.add_argument('--pitcher_stat', dest='pitcher_stat', default=None, choices=
[
    'WHIP', 
    'K/9',
    'BB/9',
    'K/BB',
    'BB/K'
]
, help='Specify the stat you want to know for a given batter.')

# specific pitch stats
parser.add_argument('--pitch_stat', dest='pitch_stat', default=None, choices=
[
    #averages
    'startSpeed',
    'endSpeed',
    'spinRate',
    'spinDir',
    'breakAngle',
    'breakLength',
    'px',
    'pz',
    'nasty',
    #count, return distrubtion
    'pitch_type',
    'zone'
]
, help='Specify the stat you want to know for a given batter.')

# specific team stats
parser.add_argument('--team_stat', dest='team_stat', default=None, choices=
[
    #averages
    'attendance',
    'avg_runs_for',
    'avg_runs_against',
    'avg_run_dif'
    #count
    'wins',
    'losses',
    'run_dif',
    #math
    'win_percentage'
]
, help='Specify the stat you want to know for a given team.')

# stat filters, not including pitcher/batter names or date filters
parser.add_argument('--pitcher_throws', dest='pitcher_throws', default=None, choices=
[
    'L', 
    'R'
]
, help='Specify whether you want stats solely against LHP or RHP.')

parser.add_argument('--batter_stands', dest='batter_stands', default=None, choices=
[
    'L', 
    'R'
]
, help='Specify whether you want stats solely against L or R standing batters.')

# ONLY ALLOW FOR PITCHER QUERIES
parser.add_argument('--zone_filter', dest='zone_filter', default=None, choices=
[
'1',
'2',
'3',
'4',
'5',
'6',
'7',
'8',
'9',
'10',
'11',
'12',
'13',
'14'
]
, help='Specify whether you want stats solely for a given zone')

# ONLY ALLOW FOR PITCHER QUERIES
parser.add_argument('--pitch_filter', dest='pitch_filter', default=None, choices=
[
'CH',
'CU',
'EP',
'FC',
'FF',
'FS',
'FT',
'IN',
'KC'
'KN',
'PO',
'SC',
'SI',
'SL'
]
, help='Specify whether you want stats solely for a given pitch type')

parser.add_argument('--num_outs', dest='num_outs', default=None, choices=
[
    '0',
    '1', 
    '2',
    '3'
]
, help='Specify how many outs as a filter.')

# ONLY ALLOW FOR PITCHER QUERIES
parser.add_argument('--men_on_base', dest='men_on_base', default=None, choices=
[
    '1B', 
    '2B',
    '3B',
    'Any',
    'None'
]
, help='Specify whether you want stats for batters on base already.')

# ONLY ALLOW FOR PITCHER QUERIES
parser.add_argument('--ball_count', dest='ball_count', default=None, choices=
[
    '0', 
    '1',
    '2',
    '3'
]
, help='Specify whether you want stats regarding a specific ball count.')

# ONLY ALLOW FOR PITCHER QUERIES
parser.add_argument('--strike_count', dest='strike_count', default=None, choices=
[
    '0', 
    '1',
    '2'
]
, help='Specify whether you want stats regarding a specific strike count.')

parser.add_argument('--home_or_away', dest='home_or_away', default=None, choices=
[
    'H',
    'A'
]
, help='Specify whether you want stats when home or away.')

# Explicitly showing help at start
try:
    args = parser.parse_args(['-h'])
except SystemExit as e:
    pass

# Loop until --quit
while True:
    command = input("Command: ")
    
    try:
        args = parser.parse_args(command.split())
    except SystemExit as e:
        if str(e) != '0':
            print('Error with input. See line above for details. Run -h for help.')
        continue
    
    print(args)
    if args.quit:
        print("Goodbye!")
        break