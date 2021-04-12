

# player single stat selection
# allow for aggrgation (max, count, min)
# options in the CLI will be flags for where or not 

# "SELECT (stat) FROM Atbats INNER JOIN Games ON gameid INNER JOIN PlayerNames ON playerId WHERE  dateTime"

# -dr date range 
def dr_option(start,end):
    return "dateTime > {start} AND dateTime < {end}".format(start=start,end=end)

# -d exact
def d_option(date):
    return "dateTime = {date}".format(date=date)

# -e event (flyout, strikout..)
def event_option(e):
    return "event = {event}".format(event=e)

def playerID_option(id):
    return "playerID = {id}".format(id=id)

def player_name_option(first,last):
    return "firstName = {first} AND lastName = {last}"

# TODO finish off adding player options


# single player stat
def select_stat_statement(stat, get_min=False, get_max=False, get_count=False):
    q = "SELECT "

    if get_min: q += "MIN({stat})".format(stat=stat)
    elif get_max: q += "MAX({stat})".format(stat=stat)
    elif get_count: q += "COUNT({stat})".format(stat=stat)
    else: q += stat

    q += " FROM "

    return q


# TODO add team stats query functionality


def from_statement():
    #TODO classify diff types and figure out joins
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