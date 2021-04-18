from connect import mycursor
from parser import parser
from options import Options
from translator import *

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

    if args.quit:
        print("Goodbye!")
        break

    if args.event_count:
        args.event_count[0] = args.event_count[0].replace('_', ' ')

    if args.team:
        args.team[0] = args.team[0].replace('_', ' ')

    if args.opp_team_vs_b:
        args.opp_team_vs_b[0] = args.opp_team_vs_b[0].replace('_', ' ')

    if args.opp_team_vs_p:
        args.opp_team_vs_p[0] = args.opp_team_vs_p[0].replace('_', ' ')
    
    if args.opp_team_vs_t:
        args.opp_team_vs_t[0] = args.opp_team_vs_t[0].replace('_', ' ')

    # Pass to translator
    opt = Options()
    opt.set_to_args(args)
    # execute query
    q = query_builder(opt)
    print(q)
    # print

    mycursor.execute(q)
    myresult = mycursor.fetchall()
    print(myresult)
    for x in myresult:
        print(x)
    