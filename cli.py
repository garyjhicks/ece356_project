from connect import mycursor
from parser import parser

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

    # Pass to translator
    # execute query
    # print

    mycursor.execute("select * from Teams")
    myresult = mycursor.fetchall()
    print(myresult)
    for x in myresult:
        print(x)
    