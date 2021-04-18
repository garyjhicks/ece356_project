from datetime import datetime
from datetime import timedelta
from options import Options

def s(string):
    return "\'" + string + "\'"

def dt_date_converter(date):
    return datetime.strptime(date, '%d/%m/%Y')

# input is datetime objects
def dr_dt(start,end):
    start_date = start.strftime('%Y-%m-%d %X')
    end_date = end.strftime('%Y-%m-%d %X')
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

def men_on_base_option(base):
    if base == '1B':
        return "on1b = 1"
    if base == '2B':
        return "on2b = 1"
    if base == '3B':
        return "on3b = 1"
    if base == "Any":
        return "(on1b = 1 OR on2b = 1 OR on3b = 1)" 
    if base == "None":
        return "(on1b = 0 AND on2b = 0 AND on3b = 0)"

def num_outs_option(outs):
    return "AtBats.outs = {o} ".format(o=outs)

def player_name_option(first,last):
    return "firstName = {first} AND lastName = {last}".format(first=s(first),last=s(last))

def player_id_filter(pid):
    return "playerID = {playerID}".format(playerID=pid)

def pitcherID_where_subquery(first,last):
    fname = " ".join(first)
    lname = " ".join(last)
    return "pitcherID = (SELECT playerID FROM PlayerNames WHERE {})".format(player_name_option(fname,lname))

def batterID_where_subquery(first,last):
    fname = " ".join(first)
    lname = " ".join(last)
    return "batterID = (SELECT playerID FROM PlayerNames WHERE {})".format(player_name_option(fname,lname))

def teamID_where_subquery(name):
    team = " ".join(name)
    home = "homeTeamID = (SELECT teamID FROM Teams WHERE name = {})".format(s(team))
    away = "awayTeamID = (SELECT teamID FROM Teams WHERE name = {})".format(s(team))
    return "({home} OR {away})".format(home=home,away=away)

def teamID_from_teamName_subquery(name):
    team = " ".join(name)
    return "(SELECT teamID FROM Teams WHERE name = {})".format(s(team))

def opp_team_vs_b_option(team):
    if_b_home = "(isTop = true AND homeTeamID = {})".format(teamID_from_teamName_subquery(team))
    if_b_away = "(isTop = false AND awayTeamID = {})".format(teamID_from_teamName_subquery(team))
    return "({h} OR {a})".format(h=if_b_home,a=if_b_away)

def opp_team_vs_p_option(team):
    if_p_home = "(isTop = false AND homeTeamID = {})".format(teamID_from_teamName_subquery(team))
    if_p_away = "(isTop = true AND awayTeamID = {})".format(teamID_from_teamName_subquery(team))
    return "({h} OR {a})".format(h=if_p_home,a=if_p_away)

def opp_team_vs_t_option(team):
    if_t_home = "(homeTeamID = {})".format(teamID_from_teamName_subquery(team))
    if_t_away = "(awayTeamID = {})".format(teamID_from_teamName_subquery(team))
    return "({h} OR {a})".format(h=if_t_home,a=if_t_away)

# single player stat
def select_player_stat(options):
    q = "SELECT "
    if options.event_count:
        q += ("COUNT(event)")
    
    if options.pitcher_stat:
        if options.pitcher_stat == 'K/9':
            q += "COUNT(event) / ( SELECT COUNT(DISTINCT AtBats.gameID, inning) {f} {where})".format(f=from_statement(options),where=where_statement(options,is_numerator=True))
        if options.pitcher_stat == 'WHIP':
            q += "COUNT(event) / ( SELECT COUNT(DISTINCT AtBats.gameID, inning) {f} {where})".format(f=from_statement(options),where=where_statement(options,is_numerator=True))
        if options.pitcher_stat == 'HR/9':
            q += "COUNT(event) / ( SELECT COUNT(DISTINCT AtBats.gameID, inning) {f} {where})".format(f=from_statement(options),where=where_statement(options,is_numerator=True))
        if options.pitcher_stat == 'BB/9':
            q += "COUNT(event) / ( SELECT COUNT(DISTINCT AtBats.gameID, inning) {f} {where})".format(f=from_statement(options),where=where_statement(options,is_numerator=True))
        if options.pitcher_stat == 'K/BB':
            q += "(SELECT COUNT(event) FROM AtBats WHERE {} AND event = \'Strikeout\')/ COUNT(event)".pitcherID_where_subquery(options.pitcher_fn,options.pitcher_fn)
    
    if options.batter_stat:
        date = ""
        if options.batter_stat == 'BA':
            q += "(SELECT COUNT(*) {f} {where} AND (event = \'Single\' OR event = \'Double\' OR event = \'Triple\' OR event = \'Home Run\')) / COUNT(*)".format(f=from_statement(options),where=where_statement(options, True))
        if options.batter_stat == 'SLG':
            q += "((SELECT COUNT(event) {f} {where} AND event = \'Single\') + 2 * (SELECT COUNT(event) {f} {where} AND event = \'Double\') + 3 * (SELECT COUNT(event) {f} {where} AND event = \'Triple\') + 4 * (SELECT COUNT(event) {f} {where} AND event = \'Home Run\') ) / Count(*)".format(f=from_statement(options),where=where_statement(options, True))
        if options.batter_stat == 'OBP':
            q += "(SELECT COUNT(*) {f} {where} AND (event = \'Hit By Pitch\' OR event = \'Walk\' OR event = \'Single\' OR event = \'Double\' OR event = \'Triple\' OR event = \'Home Run\')) / COUNT(*)".format(f=from_statement(options),where=where_statement(options, True))
        if options.batter_stat == 'OPS':
            SLG = "((SELECT COUNT(event) {f} {where} AND event = \'Single\') + 2 * (SELECT COUNT(event) {f} {where} AND event = \'Double\') + 3 * (SELECT COUNT(event) {f} {where} AND event = \'Triple\') + 4 * (SELECT COUNT(event) {f} {where} AND event = \'Home Run\') ) / Count(*)".format(f=from_statement(options),where=where_statement(options, True))
            OBP = "(SELECT COUNT(*) {f} {where} AND (event = \'Hit By Pitch\' OR event = \'Walk\' OR event = \'Single\' OR event = \'Double\' OR event = \'Triple\' OR event = \'Home Run\')) / COUNT(*)".format(f=from_statement(options),where=where_statement(options, True))
            q += "({} + {})".format(SLG,OBP)
        if options.batter_stat == 'BB/K':
            q += "(SELECT COUNT(*) {f} {where} AND event = \'Walk\') / COUNT(*)".format(f=from_statement(options),where=where_statement(options, True))


    if options.team_stat:
        if options.team_stat == 'avg_runs_for':
            home = "SUM(homeScore) {f} {where} AND homeTeamId = {team}".format(f=from_statement(options),where=where_statement(options),team=teamID_from_teamName_subquery(options.team))
            away = "SUM(awayScore) {f} {where} AND awayTeamId = {team}".format(f=from_statement(options),where=where_statement(options),team=teamID_from_teamName_subquery(options.team))
            q += "({home} + {away}) / COUNT(gameID)".format(home=home,away=away)
        if options.team_stat == 'avg_runs_against':
            home = "SUM(homeScore) {f} {where} AND awayTeamId = {team}".format(f=from_statement(options),where=where_statement(options),team=teamID_from_teamName_subquery(options.team))
            away = "SUM(awayScore) {f} {where} AND homeTeamId = {team}".format(f=from_statement(options),where=where_statement(options),team=teamID_from_teamName_subquery(options.team))
            q += "({home} + {away}) / COUNT(gameID)".format(home=home,away=away)
        if options.team_stat == 'avg_run_dif':
            home = "SUM(homeScore) {f} {where} AND homeTeamId = {team}".format(f=from_statement(options),where=where_statement(options),team=teamID_from_teamName_subquery(options.team))
            away = "SUM(awayScore) {f} {where} AND awayTeamId = {team}".format(f=from_statement(options),where=where_statement(options),team=teamID_from_teamName_subquery(options.team))
            opphome = "SUM(homeScore) {f} {where} AND awayTeamId = {team}".format(f=from_statement(options),where=where_statement(options),team=teamID_from_teamName_subquery(options.team))
            oppaway = "SUM(awayScore) {f} {where} AND homeTeamId = {team}".format(f=from_statement(options),where=where_statement(options),team=teamID_from_teamName_subquery(options.team))
            q += "({home} - {oh} + {away} - {oa}) / COUNT(gameID)".format(home=home,oh=opphome,away=away,oa=oppaway)
        if options.team_stat == 'wins':
            q += "(COUNT(*) {f} {where} AND homeTeamScore > awayTeamScore AND homeTeamID = {team}) + COUNT(*)".format(f=from_statement(options),where=where_statement(options),team=teamID_from_teamName_subquery(options.team))
        if options.team_stat == 'losses':
            q += "(COUNT(*) {f} {where} AND homeTeamScore < awayTeamScore AND homeTeamID = {team}) + COUNT(*)".format(f=from_statement(options),where=where_statement(options),team=teamID_from_teamName_subquery(options.team))

    # stat thats not pitch_type or zone

    if options.pitch_stat:
        q += "AVG({})".format(options.pitch_stat)

    return q




def from_statement(options):
    tables_needed = set()
    arr = []
    if (options.batter_fn or
        options.pitcher_fn or
        options.event_count or
        options.pitcher_throws or
        options.batter_stands or
        options.num_outs or
        options.pitcher_stat):
        tables_needed.add("AtBats")
    if (options.pitch_stat or 
        options.pitch_filter or 
        options.men_on_base or
        options.ball_count or
        options.strike_count):
        tables_needed.add("Pitches")
    if (options.d or
        options.dr or
        options.season or
        options.team_stat or
        options.home_or_away or 
        options.opp_team_vs_b or
        options.opp_team_vs_p or
        options.opp_team_vs_t):
        tables_needed.add("Games")
    if (options.team or
        options.team_stat):
        tables_needed.add("Teams")
    if "AtBats" in tables_needed and "Games" in tables_needed and "Pitches" in tables_needed:
        arr.append("AtBats INNER JOIN Games ON AtBats.gameID = Games.gameID INNER JOIN (Pitches INNER JOIN (SELECT abID,MAX(pitchNum) as maxPitchNum FROM Pitches GROUP BY abID) as A ON Pitches.abID = A.abID AND Pitches.pitchNum = A.maxPitchNum) ON Pitches.abID = AtBats.abID")
    elif "AtBats" in tables_needed and "Games" in tables_needed:
        arr.append("AtBats INNER JOIN Games ON AtBats.gameID = Games.gameID")
    elif "AtBats" in tables_needed and "Pitches" in tables_needed:
        arr.append("AtBats INNER JOIN (Pitches INNER JOIN (SELECT abID,MAX(pitchNum) as maxPitchNum FROM Pitches GROUP BY abID) as A ON Pitches.abID = A.abID AND Pitches.pitchNum = A.maxPitchNum) ON Pitches.abID = AtBats.abID")
    if not arr:
        arr.append("AtBats")
    return " FROM " + "".join(arr)

def where_statement(options,is_numerator=False):
    q = " WHERE "
    arr = []
    if options.batter_fn: # need to get playerID
        firstName = options.batter_fn
        lastName = options.batter_ln
        arr.append(batterID_where_subquery(firstName,lastName))
    if options.pitcher_fn: # need to get playerID
        firstName = options.pitcher_fn
        lastName = options.pitcher_ln
        arr.append(pitcherID_where_subquery(firstName,lastName))
    if options.team:
        arr.append(teamID_where_subquery(options.team))
    if options.dr:
        start = options.dr[0]
        end = options.dr[1]
        arr.append(dr_option(start,end))
    if options.season:
        arr.append(season_option(options.season))
    if options.event_count:
        event = " ".join(options.event_count)
        arr.append(event_option(event))
    if options.pitch_filter:
        arr.append(pitch_filter_option(options.pitch_filter))
    if options.opp_team_vs_b:
        arr.append(opp_team_vs_b_option(options.opp_team_vs_b))
    if options.opp_team_vs_p:
        arr.append(opp_team_vs_p_option(options.opp_team_vs_p))
    if options.opp_team_vs_t:
        arr.append(opp_team_vs_t_option(options.opp_team_vs_t))
    if options.men_on_base:
        arr.append(men_on_base_option(options.men_on_base))
    if options.num_outs:
        arr.append(num_outs_option(options.num_outs))
    if options.team_stat:
        if options.team_stat == "wins":
            arr.append("homeTeamScore < awayTeamScore AND awayTeamID = {}".format(teamID_from_teamName_subquery(options.team)))
        if options.team_stat == "losses":
            arr.append("homeTeamScore > awayTeamScore AND awayTeamID = {}".format(teamID_from_teamName_subquery(options.team)))
    if options.pitcher_stat and not is_numerator:
        if options.pitcher_stat == 'K/9':
            arr.append(event_option('Strikeout'))
        if options.pitcher_stat == 'WHIP':
            scores = []
            scores.append(event_option('Walk'))
            scores.append(event_option('Single'))
            scores.append(event_option('Double'))
            scores.append(event_option('Triple'))
            scores.append(event_option('Home Run'))
            arr.append("({})".format(" OR ".join(scores)))
        if options.pitcher_stat == 'HR/9':
            arr.append(event_option('Home Run'))
        if options.pitcher_stat == 'BB/9':
            arr.append(event_option('Walk'))
        if options.pitcher_stat == 'K/BB':
            arr.append(event_option('Walk'))
    if options.batter_stat and not is_numerator:
        if options.batter_stat == 'BA' or options.batter_stat == 'SLG' or options.batter_stat == 'OPS':
            events = []
            events.append(event_option('Bunt Groundout'))
            events.append(event_option('Field Error'))
            events.append(event_option('Fielders Choice'))
            events.append(event_option('Fielders Choice Out'))
            events.append(event_option('Flyout'))
            events.append(event_option('Forceout'))
            events.append(event_option('Grounded Into DP'))
            events.append(event_option('Groundout'))
            events.append(event_option('Lineout'))
            events.append(event_option('Popout'))
            events.append(event_option('Strikeout'))
            events.append(event_option('Strikeout DP'))
            events.append(event_option('Triple Play'))
            events.append(event_option('Single'))
            events.append(event_option('Double'))
            events.append(event_option('Triple'))
            events.append(event_option('Home Run'))
            arr.append("({})".format(" OR ".join(events)))
        if options.batter_stat == 'OBP':
            events = []
            events.append(event_option('Walk'))
            events.append(event_option('Hit By Pitch'))
            events.append(event_option('Bunt Groundout'))
            events.append(event_option('Field Error'))
            events.append(event_option('Fielders Choice'))
            events.append(event_option('Fielders Choice Out'))
            events.append(event_option('Flyout'))
            events.append(event_option('Forceout'))
            events.append(event_option('Grounded Into DP'))
            events.append(event_option('Groundout'))
            events.append(event_option('Lineout'))
            events.append(event_option('Popout'))
            events.append(event_option('Strikeout'))
            events.append(event_option('Strikeout DP'))
            events.append(event_option('Triple Play'))
            events.append(event_option('Single'))
            events.append(event_option('Double'))
            events.append(event_option('Triple'))
            events.append(event_option('Home Run'))
            arr.append("({})".format(" OR ".join(events)))
        if options.batter_stat == 'BB/K':
            arr.append(event_option('Strikeout'))



    return q + " AND ".join(arr)

def query_builder(options):
    
    # iterate through options and build string
    query = select_player_stat(options)
    query += from_statement(options)
    query += where_statement(options)
    query += ";"
    return query

#print(select_player_stat("event") + from_statement() +  + event_option("Strikeout"))
