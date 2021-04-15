from datetime import datetime
from datetime import timedelta


class Options:
    def __init__(self):
        self.batter_fn='John'
        self.batter_ln='Fluffy'
        self.pitcher_fn=None
        self.pitcher_ln=None
        self.dr=["29/01/2018","30/01/2019"]
        self.event_count = None
        self.team = None
        
# player single stat selection
# allow for aggrgation (max, count, min)
# options in the CLI will be flags for where or not 

# "SELECT (stat) FROM Atbats INNER JOIN Games ON gameid INNER JOIN PlayerNames ON playerId WHERE  dateTime"
# stringify
def s(string):
    return "\'" + string + "\'"

def dt_date_converter(date):
    return datetime.strptime(date, '%d/%m/%Y')

# input is datetime objects
def dr_dt(start,end):
    start_date = start.strftime('%x %X')
    end_date = end.strftime('%x %X')
    return "dateTime > {start} AND dateTime < {end}".format(start=s(start_date),end=s(end_date))

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
    return "event = {event}".format(event=s(e))

def pitch_filter_option(p):
    return "pitchType = {p}".format(p=s(p))

def stat_count_option(stat, count):
    return "{stat} = {count}".format(stat=s(stat), count=count)

def stand_option(stand):
    return "stand = {stand}".format(stand=s(stand))

def player_name_option(first,last):
    return "firstName = {first} AND lastName = {last}".format(first=s(first),last=s(last))

def player_id_filter(pid):
    return "playerID = {playerID}".format(playerID=pid)

def playerID_where_subquery(first,last):
    return "playerID = (SELECT first(playerID) FROM PlayerInfo WHERE {})".format(player_name_option(first,last))

def teamID_where_subquery(name):
    home = "homeTeamID = (SELECT teamID FROM Teams WHERE name = {})".format(s(name))
    away = "awayTeamID = (SELECT teamID FROM Teams WHERE name = {})".format(s(name))
    return "({home} OR {away})".format(home=home,away=away)
# TODO finish off adding player options


# single player stat
def select_player_stat(options):
    q = "SELECT "
    if options.event_count:
        q += ("COUNT(event)")

    # stat thats not pitch_type or zone
    if options.pitch_stat:
        q += ("AVG(event)")

    return q


# TODO add team stats query functionality


def from_statement(options):
    #TODO classify diff types and figure out joins
    tables_needed = set()
    arr = []
    if (options.batter_fn or
        options.event_count or
        options.pitcher_throws or
        options.batter_stands or
        options.num_outs):
        tables_needed.add("AtBats")
    if (options.pitch_stat or 
        options.pitch_stat or 
        options.pitch_filter or 
        options.zone_filter or 
        options.men_on_base or
        options.ball_count or
        options.strikecount):
        tables_needed.add("Pitches")
    if (options.d or
        options.dr or
        options.season or
        options.team_stat or
        options.home_or_away):
        tables_needed.add("Games")
    if (options.team or
        options.team_stat):
        tables_needed.add("Teams")
    if "AtBats" in tables_needed and "Games" in tables_needed:
        arr.append("AtBats INNER JOIN Games ON AtBats.gameID = Games.gameID")
    if "AtBats" in tables_needed and "Pitches" in tables_needed:
        arr.append("AtBats INNER JOIN (Pitches INNER JOIN (SELECT abID,MAX(pitchNum) as maxPitchNum FROM Pitches GROUP BY abID) as A ON Pitches.abID = A.abID AND Pitches.pitchNum = A.maxPitchNum) ON Pitches.abID = AtBats.abID")



def where_statement(options):
    #TODO iterate thorugh options to be appended to query
    q = "WHERE "
    arr = []
    if options.batter_fn: # need to get playerID
        firstName = options.batter_fn
        lastName = options.batter_ln
        arr.append(playerID_where_subquery(firstName,lastName))
    if options.pitcher_fn: # need to get playerID
        firstName = options.pitcher_fn
        lastName = options.pitcher_ln
        arr.append(playerID_where_subquery(firstName,lastName))
    if options.team:
        team = " ".join(option.team)
        arr.append(teamID_where_subquery(options.team))
    if options.dr:
        start = options.dr[0]
        end = options.dr[1]
        arr.append(dr_option(start,end))
    if options.event_count:
        arr.append(event_option(option.event_count))
    if options.pitch_filter:
        arr.append(pitch_filter_option(options.pitch_filter))

    return q + " AND ".join(arr) + ";"

def query_builder(options):
    
    # iterate through options and build string
    query = select_stat_statement()
    query += from_statement()
    query += where_statement()
    return query

#print(select_player_stat("event") + from_statement() +  + event_option("Strikeout"))


options = Options()
print(where_statement(options))