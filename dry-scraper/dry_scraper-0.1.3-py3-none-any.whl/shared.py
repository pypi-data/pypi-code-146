TEAM_MAP = {'ATLANTA THRASHERS': 'ATL',
            'WASHINGTON CAPITALS': 'WSH',
            'CAROLINA HURRICANES': 'CAR',
            'TAMPA BAY LIGHTNING': 'TBL',
            'FLORIDA PANTHERS': 'FLA',
            'PITTSBURGH PENGUINS': 'PIT',
            'PHILADELPHIA FLYERS': 'PHI',
            'NEW YORK RANGERS': 'NYR',
            'NEW YORK ISLANDERS': 'NYI',
            'NEW JERSEY DEVILS': 'NJD',
            'BOSTON BRUINS': 'BOS',
            'MONTREAL CANADIENS': 'MTL',
            'MONTRÉAL CANADIENS': 'MTL',
            'CANADIENS MONTREAL': 'MTL',
            'OTTAWA SENATORS': 'OTT',
            'BUFFALO SABRES': 'BUF',
            'TORONTO MAPLE LEAFS': 'TOR',
            'DETROIT RED WINGS': 'DET',
            'CHICAGO BLACKHAWKS': 'CHI',
            'ST. LOUIS BLUES': 'STL',
            'NASHVILLE PREDATORS': 'NSH',
            'MINNESOTA WILD': 'MIN',
            'VANCOUVER CANUCKS': 'VAN',
            'EDMONTON OILERS': 'EDM',
            'CALGARY FLAMES': 'CGY',
            'WINNIPEG JETS': 'WPG',
            'COLORADO AVALANCHE': 'COL',
            'COLUMBUS BLUE JACKETS': 'CBJ',
            'SAN JOSE SHARKS': 'SJS',
            'LOS ANGELES KINGS': 'LAK',
            'VEGAS GOLDEN KNIGHTS': 'VGK',
            'SEATTLE KRAKEN': 'SEA',
            'ANAHEIM DUCKS': 'ANA',
            'DALLAS STARS': 'DAL',
            'PHOENIX COYOTES': 'PHX',
            'ARIZONA COYOTES': 'ARI',
            'EASTERN': 'EAS',
            'WESTERN': 'WES',
            'TEAM LIDSTROM': 'ASB',
            'TEAM STAAL': 'ASR',
            'TEAM CHARA': 'BLU',
            'TEAM ALFREDSSON': 'RED',
            'ATLANTIC': 'ATL',
            'METROPOLITAN': 'MET',
            'PACIFIC': 'PAC',
            'CENTRAL': 'CEN',
            'TEAM SWEDEN': 'SWE',
            'TEAM FINLAND': 'FIN',
            'TEAM RUSSIA': 'RUS',
            'TEAM CZECH REPUBLIC': 'CZE',
            'TEAM EUROPE': 'EUR',
            'TEAM NORTH AMERICA': 'NAT',
            'TEAM CANADA': 'CAN',
            'TEAM USA': 'USA'
            }

ESPN_EVENTS = {'505': 'GOAL',
               '506': 'SHOT',
               '502': 'FACEOFF',
               '507': 'MISSED_SHOT',
               '503': 'HIT',
               '1401': 'TAKEAWAY',
               '1402': 'GIVEAWAY',
               '508': 'BLOCKED_SHOT',
               '509': 'PENALTY',
               '516': 'STOP',
               '518': 'PERIOD_START',
               '519': 'PERIOD_END',
               '521': 'SHOOTOUT_END',
               '522': 'GAME_END'
               }

EVENTTYPEID_EVENT = {
    'GOAL': 'Goal',
    'SHOT': 'Shot',
    'FACEOFF': 'Faceoff',
    'MISSED_SHOT': 'Missed Shot',
    'HIT': 'Hit',
    'TAKEAWAY': 'Takeaway',
    'GIVEAWAY': 'Giveaway',
    'BLOCKED_SHOT': 'Blocked Shot',
    'PENALTY': 'Penalty',
    'STOP': 'Stoppage'
}

ESPN_PENALTIES_DICT = {'Hi-sticking': 'HIGH STICKING',
                       'Kneeing': 'KNEEING',
                       'Illegal Equipment': 'ILLEGAL EQUIPMENT',
                       'Hooking': 'HOOKING',
                       'Slashing': 'SLASHING',
                       'Roughing': 'ROUGHING',
                       'Elbowing': 'ELBOWING',
                       'Spearing': 'SPEARING',
                       'Interference': 'INTERFERENCE',
                       'Penalty': 'PENALTY',
                       'Tripping': 'TRIPPING',
                       'Instigator': 'INSTIGATOR',
                       'Illegal check to head': 'ILLEGAL CHECK TO HEAD',
                       'Clipping': 'CLIPPING',
                       'Too many men on the ice': 'TOO MANY MEN',
                       'Holding the stick': 'HOLDING THE STICK',
                       'Holding': 'HOLDING',
                       'Closing hand on puck': 'CLOSING HAND ON THE PUCK',
                       'Fighting': 'FIGHTING',
                       'Cross checking': 'CROSS CHECKING',
                       'Charging': 'CHARGING',
                       'Boarding': 'BOARDING',
                       'Misconduct': 'MISCONDUCT',
                       'Delaying game - Puck over glass': 'DELAYING GAME - PUCK OVER GLASS',
                       'Unsportsmanlike Conduct': 'UNSPORTSMANLIKE CONDUCT',
                       'Delay of game': 'DELAYING THE GAME',
                       'Delay of Game': 'DELAYING THE GAME',
                       }

ESPN_PENALTIES = {"55": {"description": "",
                         "event": "Penalty",
                         "eventTypeId": "PENALTY",
                         "penaltyMinutes": 2,
                         "penaltySeverity": "Minor",
                         "secondaryType": "Tripping"
                         },
                  "58": {
                      "description": "",
                      "event": "Penalty",
                      "eventTypeId": "PENALTY",
                      "penaltyMinutes": 2,
                      "penaltySeverity": "Minor",
                      "secondaryType": "Too many men on the ice"
                  },
                  "31": {
                      "description": "",
                      "event": "Penalty",
                      "eventTypeId": "PENALTY",
                      "penaltyMinutes": 2,
                      "penaltySeverity": "Minor",
                      "secondaryType": "Holding"
                  },
                  "45": {
                      "description": "",
                      "event": "Penalty",
                      "eventTypeId": "PENALTY",
                      "penaltyMinutes": 2,
                      "penaltySeverity": "Minor",
                      "secondaryType": "Roughing"
                  },
                  "37": {
                      "description": "",
                      "event": "Penalty",
                      "eventTypeId": "PENALTY",
                      "penaltyMinutes": 2,
                      "penaltySeverity": "Minor",
                      "secondaryType": "Interference"
                  },
                  "33": {
                      "description": "",
                      "event": "Penalty",
                      "eventTypeId": "PENALTY",
                      "penaltyMinutes": 2,
                      "penaltySeverity": "Minor",
                      "secondaryType": "Hooking"
                  },
                  "29": {
                      "description": "",
                      "event": "Penalty",
                      "eventTypeId": "PENALTY",
                      "penaltyMinutes": 2,
                      "penaltySeverity": "Minor",
                      "secondaryType": "Hi-sticking"
                  },
                  "49": {
                      "description": "",
                      "event": "Penalty",
                      "eventTypeId": "PENALTY",
                      "penaltyMinutes": 2,
                      "penaltySeverity": "Minor",
                      "secondaryType": "Slashing"
                  },
                  "13": {
                      "description": "",
                      "event": "Penalty",
                      "eventTypeId": "PENALTY",
                      "penaltyMinutes": 2,
                      "penaltySeverity": "Minor",
                      "secondaryType": "Cross checking"
                  },
                  "7": {
                      "description": "",
                      "event": "Penalty",
                      "eventTypeId": "PENALTY",
                      "penaltyMinutes": 2,
                      "penaltySeverity": "Minor",
                      "secondaryType": "Boarding"
                  },
                  "80": {
                      "description": "",
                      "event": "Penalty",
                      "eventTypeId": "PENALTY",
                      "penaltyMinutes": 5,
                      "penaltySeverity": "Major",
                      "secondaryType": "Fighting"
                  },
                  "38": {
                      "description": "",
                      "event": "Penalty",
                      "eventTypeId": "PENALTY",
                      "penaltyMinutes": 2,
                      "penaltySeverity": "Minor",
                      "secondaryType": "Instigator"
                  },
                  "91": {
                      "description": "",
                      "event": "Penalty",
                      "eventTypeId": "PENALTY",
                      "penaltyMinutes": 0,
                      "penaltySeverity": "Minor",
                      "secondaryType": "Misconduct"
                  },
                  "32": {
                      "description": "",
                      "event": "Penalty",
                      "eventTypeId": "PENALTY",
                      "penaltyMinutes": 2,
                      "penaltySeverity": "Minor",
                      "secondaryType": "Holding"
                  },
                  "30": {
                      "description": "",
                      "event": "Penalty",
                      "eventTypeId": "PENALTY",
                      "penaltyMinutes": 4,
                      "penaltySeverity": "Minor",
                      "secondaryType": "Hi-sticking"
                  },
                  "57": {
                      "description": "",
                      "event": "Penalty",
                      "eventTypeId": "PENALTY",
                      "penaltyMinutes": 2,
                      "penaltySeverity": "Minor",
                      "secondaryType": "Unsportsmanlike Conduct"
                  },
                  "22": {
                      "description": "",
                      "event": "Penalty",
                      "eventTypeId": "PENALTY",
                      "penaltyMinutes": 2,
                      "penaltySeverity": "Minor",
                      "secondaryType": "Delay of Game"
                  },
                  "39": {
                      "description": "",
                      "event": "Penalty",
                      "eventTypeId": "PENALTY",
                      "penaltyMinutes": 2,
                      "penaltySeverity": "Minor",
                      "secondaryType": "Kneeing"
                  },
                  "-1": {
                      "description": "",
                      "event": "Penalty",
                      "eventTypeId": "PENALTY",
                      "penaltyMinutes": 2,
                      "penaltySeverity": "Minor",
                      "secondaryType": "Penalty"
                  },
                  "20": {
                      "description": "",
                      "event": "Penalty",
                      "eventTypeId": "PENALTY",
                      "penaltyMinutes": 2,
                      "penaltySeverity": "Minor",
                      "secondaryType": "Illegal check to head"
                  },
                  "17": {
                      "description": "",
                      "event": "Penalty",
                      "eventTypeId": "PENALTY",
                      "penaltyMinutes": 2,
                      "penaltySeverity": "Minor",
                      "secondaryType": "Elbowing"
                  },
                  "12": {
                      "description": "",
                      "event": "Penalty",
                      "eventTypeId": "PENALTY",
                      "penaltyMinutes": 2,
                      "penaltySeverity": "Minor",
                      "secondaryType": "Closing hand on puck"
                  }
                  }

ROSTER_CSV_COLUMNS = [
    'position',
    'jersey_number',
    'captain',
    'name',
    'team_tricode',
    'home',
    'scratched',
    'head_coach',
    'official'
]

SHIFTS_CSV_COLUMNS = [
    'player',
    'shift_start',
    'shift_end'
]

ESPN_CSV_COLUMNS = [
    'x-coord',
    'y-coord',
    'event_type_id',
    'time_elapsed',
    'period',
    'player1_id',
    'player2_id',
    'player3_id',
    'description',
    'event_detail_id',
    'home_score',
    'away_score',
    'penalty_server',
    'strength_state_id',
    'team_id',
    'TBD',
    'season_goal_total',
    'season_assist_total',
    'season_assist_total'
]

GOAL_TEMPLATE = {
    "result": {
        "emptyNet": False,
        "strength": {
            "name": "",
            "code": ""},
        "gameWinningGoal": False,
        "eventTypeId": "GOAL",
        "description": "",
        "event": "Goal"},
    "team": {},
    "coordinates": {
        "y": 0,
        "x": 0},
    "players": [
        {
            "player": {},
            "playerType": "Scorer"},
        {
            "player": {},
            "playerType": "Assist"},
        {
            "player": {},
            "playerType": "Assist"},
        {
            "player": {},
            "playerType": "Goalie"}],
    "about": {
        "periodTime": "",
        "eventIdx": 0,
        "periodTimeRemaining": "",
        "goals": {
            "home": 0,
            "away": 0},
        "period": 0}}

SHOT_TEMPLATE = {
    "players": [
        {
            "player": {},
            "playerType": "Shooter"},
        {
            "player": {},
            "playerType": "Goalie"}],
    "result": {
        "event": "Shot",
        "eventTypeId": "SHOT",
        "description": "",
        "secondaryType": ""},
    "about": {
        "eventIdx": 0,
        "eventId": 0,
        "period": 0,
        "periodType": "",
        "periodTime": "",
        "periodTimeRemaining": "",
        "goals": {
            "away": 0,
            "home": 0}},
    "coordinates": {
        "x": 0,
        "y": 0},
    "team": {}}

FACEOFF_TEMPLATE = {
    "about": {
        "eventId": 0,
        "eventIdx": 0,
        "goals": {
            "away": 0,
            "home": 0},
        "period": 0,
        "periodTime": "",
        "periodTimeRemaining": "",
        "periodType": ""},
    "coordinates": {
        "x": 0,
        "y": 0},
    "players": [
        {
            "player": {},
            "playerType": "Winner"},
        {
            "player": {},
            "playerType": "Loser"}],
    "result": {
        "description": "",
        "event": "Faceoff",
        "eventTypeId": "FACEOFF"},
    "team": {}}

MISSED_SHOT_TEMPLATE = {
    "about": {
        "eventId": 0,
        "eventIdx": 0,
        "goals": {
            "away": 0,
            "home": 0},
        "period": 0,
        "periodTime": "",
        "periodTimeRemaining": "",
        "periodType": ""},
    "coordinates": {
        "x": 0,
        "y": 0},
    "players": [
        {
            "player": {},
            "playerType": "Shooter"}],
    "result": {
        "description": "",
        "event": "Missed Shot",
        "eventTypeId": "MISSED_SHOT"},
    "team": {}}

HIT_TEMPLATE = {
    "about": {
        "eventId": 0,
        "eventIdx": 0,
        "goals": {
            "away": 0,
            "home": 0},
        "period": 0,
        "periodTime": "",
        "periodTimeRemaining": "",
        "periodType": "REGULAR"},
    "coordinates": {
        "x": 0,
        "y": 0},
    "players": [
        {
            "player": {},
            "playerType": "Hitter"},
        {
            "player": {},
            "playerType": "Hittee"}],
    "result": {
        "description": "",
        "event": "Hit",
        "eventTypeId": "HIT"},
    "team": {}}

TAKEAWAY_TEMPLATE = {
    "about": {
        "eventId": 0,
        "eventIdx": 0,
        "goals": {
            "away": 0,
            "home": 0},
        "period": 0,
        "periodTime": "",
        "periodTimeRemaining": "",
        "periodType": "REGULAR"},
    "coordinates": {
        "x": 0,
        "y": 0},
    "players": [
        {
            "player": {}}],
    "result": {
        "description": "",
        "event": "Takeaway",
        "eventTypeId": "TAKEAWAY"},
    "team": {}}

GIVEAWAY_TEMPLATE = {
    "about": {
        "eventId": 0,
        "eventIdx": 0,
        "goals": {
            "away": 0,
            "home": 0},
        "period": 0,
        "periodTime": "",
        "periodTimeRemaining": "",
        "periodType": "REGULAR"},
    "coordinates": {
        "x": 0,
        "y": 0},
    "players": [
        {
            "player": {}}],
    "result": {
        "description": "",
        "event": "Giveaway",
        "eventTypeId": "GIVEAWAY"},
    "team": {}}

BLOCKED_SHOT_TEMPLATE = {
    "about": {
        "eventId": 0,
        "eventIdx": 0,
        "goals": {
            "away": 0,
            "home": 0},
        "period": 0,
        "periodTime": "",
        "periodTimeRemaining": "",
        "periodType": ""},
    "coordinates": {
        "x": 0,
        "y": 0},
    "players": [
        {
            "player": {},
            "playerType": "Blocker"},
        {
            "player": {},
            "playerType": "Shooter"}],
    "result": {
        "description": "",
        "event": "Blocked Shot",
        "eventTypeId": "BLOCKED_SHOT"},
    "team": {}}

PENALTY_TEMPLATE = {"about": {
    "eventId": 0,
    "eventIdx": 0,
    "goals": {
        "away": 0,
        "home": 0},
    "period": 0,
    "periodTime": "",
    "periodTimeRemaining": "",
    "periodType": ""},
    "coordinates": {
        "x": 0,
        "y": 0},
    "players": [
        {
            "player": {},
            "playerType": "PenaltyOn"},
        {
            "player": {},
            "playerType": "DrewBy"},
        {
            "player": {},
            "playerType": "ServedBy"}],
    "result": {
        "description": "",
        "event": "Penalty",
        "eventTypeId": "PENALTY",
        "penaltyMinutes": 0,
        "penaltySeverity": "",
        "secondaryType": ""},
    "team": {}}

STOP_TEMPLATE = {
    "about": {
        "eventId": 0,
        "eventIdx": 0,
        "goals": {
            "away": 0,
            "home": 0},
        "period": 0,
        "periodTime": "",
        "periodTimeRemaining": "",
        "periodType": ""
    },
    "coordinates": {},
    "result": {
        "description": "",
        "event": "Stoppage",
        "eventTypeId": "STOP"
    }}

PERIOD_START_TEMPLATE = {
    "about": {
        "eventId": 0,
        "eventIdx": 0,
        "goals": {
            "away": 0,
            "home": 0},
        "period": 0,
        "periodTime": "",
        "periodTimeRemaining": "",
        "periodType": ""},
    "coordinates": {},
    "result": {
        "description": "Period Start",
        "event": "Period Start",
        "eventTypeId": "PERIOD_START"}}

PERIOD_END_TEMPLATE = {
    "about": {
        "eventId": 0,
        "eventIdx": 0,
        "goals": {
            "away": 0,
            "home": 0},
        "period": 0,
        "periodTime": "",
        "periodTimeRemaining": "",
        "periodType": ""},
    "coordinates": {},
    "result": {
        "description": "",
        "event": "Period End",
        "eventTypeId": "PERIOD_END"}}

GAME_END_TEMPLATE = {
    "about": {
        "eventId": 0,
        "eventIdx": 0,
        "goals": {
            "away": 0,
            "home": 0},
        "period": 0,
        "periodTime": "",
        "periodTimeRemaining": "",
        "periodType": ""},
    "coordinates": {},
    "result": {
        "description": "Game End",
        "event": "Game End",
        "eventTypeId": "GAME_END"}}

SHOOTOUT_END_TEMPLATE = {
    "about": {
        "eventId": 0,
        "eventIdx": 0,
        "goals": {
            "away": 0,
            "home": 0},
        "period": 0,
        "periodTime": "",
        "periodTimeRemaining": "",
        "periodType": ""},
    "coordinates": {},
    "result": {
        "description": "Shootout End",
        "event": "Shootout End",
        "eventTypeId": "SHOOTOUT_END"}}

GAME_DATA_TEMPLATE = {
    "game": {},
    "datetime": {},
    "venue": {},
    "players": {}}

TEAM_TEMPLATE = {
    "id": '',
    "name": '',
    "triCode": '',
    "teamName": '',
    "locationName": ''}

TEAM_BOX_TEMPLATE = {
    "season": '',
    "gamePk": '',
    "team": {
        "id": '',
        "name": '',
        "triCode": '',
        "teamName": '',
        "locationName": ''},
    "teamStats": {},
    "players": {},
    "goalies": {},
    "skaters": {},
    "scratches": {},
    "coaches": {}}

LIVE_DATA_TEMPLATE = {
    "season": '',
    "gamePk": '',
    "boxscore": {
        "officials": {}},
    "decisions": {}}

SHIFTS_TEMPLATE = {
    "season": '',
    "gamePk": '',
    "home": None,
    "shifts": []
}

ROSTER_TEMPLATE = {
    "season": '',
    "gamePk": '',
    "home": {
        "team": {},
        "dressed": [],
        "scratched": [],
        "headCoach": ''},
    "away": {
        "team": {},
        "dressed": [],
        "scratched": [],
        "headCoach": ''},
    "officials": {
        "referees": [],
        "linesmen": []}}

ROSTER_PLAYER_TEMPLATE = {
    "name": '',
    "jerseyNumber": 99,
    "position": '',
    "captain": False,
    "alternate": False}

OFFICIAL_TEMPLATE = {
    "name": '',
    "jerseyNumber": 99,
    "role": ''
}
