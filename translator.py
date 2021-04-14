from datetime import datetime
from datetime import timedelta


# player single stat selection
# allow for aggrgation (max, count, min)
# options in the CLI will be flags for where or not 

# "SELECT (stat) FROM Atbats INNER JOIN Games ON gameid INNER JOIN PlayerNames ON playerId WHERE  dateTime"

def dt_date_converter(date):
    return datetime.strptime(date, '%d/%m/%Y')

# input is datetime objects
def dr_dt(start,end):
    return "dateTime > {start} AND dateTime < {end}".format(start=start,end=end)

# -d exact
def d_option(date):
    dt = dt_date_converter(date)
    return "dateTime = {date}".format(date=dt)

# -dr date range 
def dr_option(start,end):
    start_dt = dt_date_converter(start)
    end_dt = dt_date_converter(end)
    return dr_dt(start_dt,end_dt)

# -s season
def season_option(s):
    start = "01/01/" + s
    start_dt = dt_date_converter(start)
    end_dt = start_dt + timedelta(days=365) 
    return dr_dt(start_dt,end_dt)

# -e event (flyout, strikout..)
def event_option(e):
    return "event = {event}".format(event=e)

def stat_count_option(stat, count):
    return "{stat} = {count}".format(stat=stat, count=count)

def player_name_option(first,last):
    return "firstName = {first} AND lastName = {last}"



# TODO finish off adding player options


# single player stat
def select_player_stat(stat, get_min=False, get_max=False):
    q = "SELECT "

    if get_min: q += "MIN({stat})".format(stat=stat)
    elif get_max: q += "MAX({stat})".format(stat=stat)
    else: q += "COUNT({stat})".format(stat=stat)

    q += " FROM "

    return q


# TODO add team stats query functionality


def from_statement(options):
    #TODO classify diff types and figure out joins
    if "batter" in options:
        return "FROM AtBats INNER JOIN Game INNER JOIN PlayerName"
    return ""

def where_statement(options):
    #TODO iterate thorugh options to be appended to query
    return ""

def query_builder(stat, options):
    
    # iterate through options and build string
    query = select_stat_statement(stat)
    query += from_statement()
    query += where_statement()
    return query

#print(select_player_stat("event") + from_statement() +  + event_option("Strikeout"))