class Options:
    
    def __init__(self):
        self.batter_fn = None
        self.batter_ln = None
        self.pitcher_fn = None
        self.pitcher_ln = None
        self.dr = None
        self.d = None
        self.event_count = None
        self.team = None
        self.opp_team_vs_b = None
        self.opp_team_vs_p = None
        self.opp_team_vs_t = None
        self.season = None
        self.pitch_stat = None
        self.pitch_filter = None
        self.zone_filter = None
        self.men_on_base = None
        self.ball_count = None
        self.strikecount = None
        self.team_stat = None
        self.pitcher_stat = None
        self.batter_stat = None
        self.pitcher_throws = None
        self.batter_stands = None
        self.num_outs = None
        self.home_or_away = None
    
    
    def set_to_args(self, args):
        self.batter_fn = args.batter_fn
        self.batter_ln = args.batter_ln
        self.pitcher_fn = args.pitcher_fn
        self.pitcher_ln = args.pitcher_ln
        self.dr = args.dr
        self.d = args.d
        self.event_count = args.event_count
        self.team = args.team
        self.opp_team_vs_b = args.opp_team_vs_b
        self.opp_team_vs_p = args.opp_team_vs_p
        self.opp_team_vs_t = args.opp_team_vs_t
        self.season = args.season
        self.pitch_stat = args.pitch_stat
        self.pitch_filter = args.pitch_filter
        self.zone_filter = args.zone_filter
        self.men_on_base = args.men_on_base
        self.ball_count = args.ball_count
        self.strikecount = args.strikecount
        self.team_stat = args.team_stat
        self.pitcher_stat = args.pitcher_stat
        self.batter_stat = args.batter_stat
        self.pitcher_throws = args.pitcher_throws
        self.batter_stands = args.batter_stands
        self.num_outs = args.num_outs
        self.home_or_away = arg.home_or_away

