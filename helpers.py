def calculate_player_points(player_data):
    points = {}

    _initialize_points(player_data, points)
    _calculate_points_for_goals(player_data, points)
    _calculate_points_for_assists(player_data, points)
    _calculate_points_for_cards(player_data, points)
    _calculate_points_for_playing_time(player_data, points)
    _calculate_points_for_saves(player_data, points)

    return points


def _initialize_points(player_data, points):
    for player_entry in player_data:
        player_id = player_entry["player"]["id"]
        points[player_id] = 0


def _calculate_points_for_goals(player_data, points):
    for player_entry in player_data:
        player_id = player_entry["player"]["id"]
        stats = player_entry["statistics"]["goals"]
        if stats["total"] is not None:
            player_position = player_entry["statistics"]["games"]["position"]
            if player_position == "G":
                points[player_id] += 10 * stats["total"]
            elif player_position in ["D"]:
                points[player_id] += 8 * stats["total"]
            elif player_position in ["M"]:
                points[player_id] += 6 * stats["total"]
            else:  # Forward or other positions
                points[player_id] += 4 * stats["total"]


def _calculate_points_for_assists(player_data, points):
    for player_entry in player_data:
        player_id = player_entry["player"]["id"]
        stats = player_entry["statistics"]["goals"]
        if stats["assists"] is not None:
            points[player_id] += 3 * stats["assists"]


def _calculate_points_for_cards(player_data, points):
    for player_entry in player_data:
        player_id = player_entry["player"]["id"]
        cards = player_entry["statistics"]["cards"]
        points[player_id] -= 1 * cards["yellow"]
        points[player_id] -= 3 * cards["red"]


def _calculate_points_for_playing_time(player_data, points):
    for player_entry in player_data:
        player_id = player_entry["player"]["id"]
        minutes_played = player_entry["statistics"]["games"]["minutes"]
        if minutes_played >= 60:
            points[player_id] += 2
        elif minutes_played > 0:
            points[player_id] += 1


def _calculate_points_for_saves(player_data, points):
    for player_entry in player_data:
        player_id = player_entry["player"]["id"]
        stats = player_entry["statistics"]
        if stats["games"]["position"] == "G":  # Check if the player is a goalkeeper
            points[player_id] += stats["goals"]["saves"]


# Example usage
data = [
    {
        "area": {
            "id": 2081,
            "name": "France",
            "code": "FRA",
            "flag": "https://crests.football-data.org/773.svg",
        },
        "competition": {
            "id": 2015,
            "name": "Ligue 1",
            "code": "FL1",
            "type": "LEAGUE",
            "emblem": "https://crests.football-data.org/FL1.png",
        },
        "season": {
            "id": 746,
            "startDate": "2021-08-06",
            "endDate": "2022-05-21",
            "currentMatchday": 38,
            "winner": None,
            "stages": ["REGULAR_SEASON"],
        },
        "id": 330299,
        "utcDate": "2022-02-27T16:05:00Z",
        "status": "FINISHED",
        "minute": 90,
        "injuryTime": 7,
        "attendance": 16871,
        "venue": "Stade de l'Aube",
        "matchday": 26,
        "stage": "REGULAR_SEASON",
        "group": None,
        "lastUpdated": "2022-06-06T08:20:24Z",
        "homeTeam": {
            "id": 531,
            "name": "ES Troyes AC",
            "shortName": "Troyes",
            "tla": "ETR",
            "crest": "https://crests.football-data.org/531.svg",
            "coach": {"id": 108988, "name": "Bruno Irles", "nationality": "France"},
            "leagueRank": None,
            "formation": "3-4-1-2",
            "lineup": [
                {
                    "id": 899,
                    "name": "Gauthier Gallon",
                    "position": "Goalkeeper",
                    "shirtNumber": 30,
                },
                {
                    "id": 8775,
                    "name": "Yoann Salmier",
                    "position": "Centre-Back",
                    "shirtNumber": 17,
                },
                {
                    "id": 8348,
                    "name": "Adil Rami",
                    "position": "Centre-Back",
                    "shirtNumber": 23,
                },
                {
                    "id": 9004,
                    "name": "Erik Palmer-Brown",
                    "position": "Centre-Back",
                    "shirtNumber": 2,
                },
                {
                    "id": 123574,
                    "name": "Issa Kaboré",
                    "position": "Right-Back",
                    "shirtNumber": 29,
                },
                {
                    "id": 37728,
                    "name": "Abdu Conté",
                    "position": "Left-Back",
                    "shirtNumber": 12,
                },
                {
                    "id": 507,
                    "name": "Florian Tardieu",
                    "position": "Defensive Midfield",
                    "shirtNumber": 10,
                },
                {
                    "id": 8623,
                    "name": "Tristan Dingomé",
                    "position": "Central Midfield",
                    "shirtNumber": 5,
                },
                {
                    "id": 43707,
                    "name": "Mama Baldé",
                    "position": "Right Winger",
                    "shirtNumber": 25,
                },
                {
                    "id": 8415,
                    "name": "Rominigue Kouamé",
                    "position": "Central Midfield",
                    "shirtNumber": 6,
                },
                {
                    "id": 6406,
                    "name": "Iké Ugbo",
                    "position": "Centre-Forward",
                    "shirtNumber": 13,
                },
            ],
            "bench": [
                {
                    "id": 74570,
                    "name": "Sébastien Rénot",
                    "position": "Goalkeeper",
                    "shirtNumber": 16,
                },
                {
                    "id": 99805,
                    "name": "Giulian Biancone",
                    "position": "Right-Back",
                    "shirtNumber": 4,
                },
                {
                    "id": 811,
                    "name": "Youssouf Koné",
                    "position": "Left-Back",
                    "shirtNumber": 3,
                },
                {
                    "id": 133766,
                    "name": "Yasser Larouci",
                    "position": "Left-Back",
                    "shirtNumber": 22,
                },
                {
                    "id": 8544,
                    "name": "Dylan Chambost",
                    "position": "Attacking Midfield",
                    "shirtNumber": 14,
                },
                {
                    "id": 824,
                    "name": "Xavier Chavalerin",
                    "position": "Central Midfield",
                    "shirtNumber": 24,
                },
                {
                    "id": 1043,
                    "name": "Lebo Mothiba",
                    "position": "Centre-Forward",
                    "shirtNumber": 26,
                },
                {
                    "id": 519,
                    "name": "Yoann Touzghar",
                    "position": "Centre-Forward",
                    "shirtNumber": 7,
                },
                {
                    "id": 169252,
                    "name": "Metinho",
                    "position": "Central Midfield",
                    "shirtNumber": 31,
                },
            ],
            "statistics": {
                "corner_kicks": 4,
                "free_kicks": 10,
                "goal_kicks": 5,
                "offsides": 4,
                "fouls": 16,
                "ball_possession": 41,
                "saves": 1,
                "throw_ins": 12,
                "shots": 8,
                "shots_on_goal": 3,
                "shots_off_goal": 5,
                "yellow_cards": 5,
                "yellow_red_cards": 0,
                "red_cards": 0,
            },
        },
        "awayTeam": {
            "id": 516,
            "name": "Olympique de Marseille",
            "shortName": "Marseille",
            "tla": "MAR",
            "crest": "https://crests.football-data.org/516.png",
            "coach": {
                "id": 33636,
                "name": "Jorge Sampaoli",
                "nationality": "Argentina",
            },
            "leagueRank": None,
            "formation": "4-3-3",
            "lineup": [
                {
                    "id": 32695,
                    "name": "Pau López",
                    "position": "Goalkeeper",
                    "shirtNumber": 16,
                },
                {
                    "id": 80171,
                    "name": "William Saliba",
                    "position": "Centre-Back",
                    "shirtNumber": 2,
                },
                {
                    "id": 10206,
                    "name": "Duje Ćaleta-Car",
                    "position": "Centre-Back",
                    "shirtNumber": 15,
                },
                {
                    "id": 8346,
                    "name": "Boubacar Kamara",
                    "position": "Defensive Midfield",
                    "shirtNumber": 4,
                },
                {
                    "id": 8695,
                    "name": "Valentin Rongier",
                    "position": "Central Midfield",
                    "shirtNumber": 21,
                },
                {
                    "id": 1086,
                    "name": "Luan Peres",
                    "position": "Centre-Back",
                    "shirtNumber": 14,
                },
                {
                    "id": 1815,
                    "name": "Gerson",
                    "position": "Central Midfield",
                    "shirtNumber": 8,
                },
                {
                    "id": 600,
                    "name": "Mattéo Guendouzi",
                    "position": "Central Midfield",
                    "shirtNumber": 6,
                },
                {
                    "id": 1818,
                    "name": "Cengiz Ünder",
                    "position": "Right Winger",
                    "shirtNumber": 17,
                },
                {
                    "id": 8360,
                    "name": "Dimitri Payet",
                    "position": "Attacking Midfield",
                    "shirtNumber": 10,
                },
                {
                    "id": 166640,
                    "name": "Ahmadou Bamba Dieng",
                    "position": None,
                    "shirtNumber": 12,
                },
            ],
            "bench": [
                {
                    "id": 3356,
                    "name": "Steve Mandanda",
                    "position": "Goalkeeper",
                    "shirtNumber": 30,
                },
                {
                    "id": 33108,
                    "name": "Álvaro González",
                    "position": "Centre-Back",
                    "shirtNumber": 3,
                },
                {
                    "id": 7786,
                    "name": "Sead Kolašinac",
                    "position": "Left-Back",
                    "shirtNumber": 23,
                },
                {
                    "id": 3714,
                    "name": "Amine Harit",
                    "position": "Attacking Midfield",
                    "shirtNumber": 7,
                },
                {
                    "id": 633,
                    "name": "Pape Gueye",
                    "position": "Defensive Midfield",
                    "shirtNumber": 22,
                },
                {
                    "id": 2105,
                    "name": "Arkadiusz Milik",
                    "position": "Centre-Forward",
                    "shirtNumber": 9,
                },
                {
                    "id": 115074,
                    "name": "Luis Henrique",
                    "position": "Left Winger",
                    "shirtNumber": 11,
                },
                {
                    "id": 21583,
                    "name": "Cédric Bakambu",
                    "position": "Centre-Forward",
                    "shirtNumber": 13,
                },
                {
                    "id": 166642,
                    "name": "Pol Lirola",
                    "position": None,
                    "shirtNumber": 29,
                },
            ],
            "statistics": {
                "corner_kicks": 8,
                "free_kicks": 20,
                "goal_kicks": 7,
                "offsides": 0,
                "fouls": 10,
                "ball_possession": 59,
                "saves": 2,
                "throw_ins": 14,
                "shots": 4,
                "shots_on_goal": 2,
                "shots_off_goal": 2,
                "yellow_cards": 3,
                "yellow_red_cards": 0,
                "red_cards": 0,
            },
        },
        "score": {
            "winner": "DRAW",
            "duration": "REGULAR",
            "fullTime": {"home": 1, "away": 1},
            "halfTime": {"home": 0, "away": 1},
        },
        "goals": [
            {
                "minute": 28,
                "injuryTime": None,
                "type": "PENALTY",
                "team": {"id": 516, "name": "Olympique de Marseille"},
                "scorer": {"id": 8360, "name": "Dimitri Payet"},
                "assist": None,
                "score": {"home": 0, "away": 1},
            },
            {
                "minute": 90,
                "injuryTime": None,
                "type": "REGULAR",
                "team": {"id": 531, "name": "ES Troyes AC"},
                "scorer": {"id": 519, "name": "Yoann Touzghar"},
                "assist": {"id": 811, "name": "Youssouf Koné"},
                "score": {"home": 1, "away": 1},
            },
        ],
        "penalties": [
            {
                "player": {"id": 8360, "name": "Dimitri Payet"},
                "team": {"id": None, "name": None},
                "scored": True,
            }
        ],
        "bookings": [
            {
                "minute": 11,
                "team": {"id": 516, "name": "Olympique de Marseille"},
                "player": {"id": 8695, "name": "Valentin Rongier"},
                "card": "YELLOW",
            },
            {
                "minute": 27,
                "team": {"id": 531, "name": "ES Troyes AC"},
                "player": {"id": 43707, "name": "Mama Baldé"},
                "card": "YELLOW",
            },
            {
                "minute": 36,
                "team": {"id": 531, "name": "ES Troyes AC"},
                "player": {"id": 507, "name": "Florian Tardieu"},
                "card": "YELLOW",
            },
            {
                "minute": 36,
                "team": {"id": 531, "name": "ES Troyes AC"},
                "player": {"id": 8348, "name": "Adil Rami"},
                "card": "YELLOW",
            },
            {
                "minute": 49,
                "team": {"id": 531, "name": "ES Troyes AC"},
                "player": {"id": 37728, "name": "Abdu Conté"},
                "card": "YELLOW",
            },
            {
                "minute": 55,
                "team": {"id": 516, "name": "Olympique de Marseille"},
                "player": {"id": 8360, "name": "Dimitri Payet"},
                "card": "YELLOW",
            },
            {
                "minute": 85,
                "team": {"id": 516, "name": "Olympique de Marseille"},
                "player": {"id": 32695, "name": "Pau López"},
                "card": "YELLOW",
            },
            {
                "minute": 90,
                "team": {"id": 531, "name": "ES Troyes AC"},
                "player": {"id": 99805, "name": "Giulian Biancone"},
                "card": "YELLOW",
            },
        ],
        "substitutions": [
            {
                "minute": 57,
                "team": {"id": 516, "name": "Olympique de Marseille"},
                "playerOut": {"id": 8695, "name": "Valentin Rongier"},
                "playerIn": {"id": 166642, "name": "Pol Lirola"},
            },
            {
                "minute": 57,
                "team": {"id": 516, "name": "Olympique de Marseille"},
                "playerOut": {"id": 166640, "name": "Ahmadou Bamba Dieng"},
                "playerIn": {"id": 115074, "name": "Luis Henrique"},
            },
            {
                "minute": 58,
                "team": {"id": 531, "name": "ES Troyes AC"},
                "playerOut": {"id": 6406, "name": "Iké Ugbo"},
                "playerIn": {"id": 1043, "name": "Lebo Mothiba"},
            },
            {
                "minute": 59,
                "team": {"id": 531, "name": "ES Troyes AC"},
                "playerOut": {"id": 37728, "name": "Abdu Conté"},
                "playerIn": {"id": 811, "name": "Youssouf Koné"},
            },
            {
                "minute": 77,
                "team": {"id": 531, "name": "ES Troyes AC"},
                "playerOut": {"id": 9004, "name": "Erik Palmer-Brown"},
                "playerIn": {"id": 99805, "name": "Giulian Biancone"},
            },
            {
                "minute": 77,
                "team": {"id": 531, "name": "ES Troyes AC"},
                "playerOut": {"id": 43707, "name": "Mama Baldé"},
                "playerIn": {"id": 519, "name": "Yoann Touzghar"},
            },
            {
                "minute": 78,
                "team": {"id": 516, "name": "Olympique de Marseille"},
                "playerOut": {"id": 8360, "name": "Dimitri Payet"},
                "playerIn": {"id": 2105, "name": "Arkadiusz Milik"},
            },
            {
                "minute": 86,
                "team": {"id": 516, "name": "Olympique de Marseille"},
                "playerOut": {"id": 1818, "name": "Cengiz Ünder"},
                "playerIn": {"id": 633, "name": "Pape Gueye"},
            },
            {
                "minute": 87,
                "team": {"id": 516, "name": "Olympique de Marseille"},
                "playerOut": {"id": 1086, "name": "Luan Peres"},
                "playerIn": {"id": 7786, "name": "Sead Kolašinac"},
            },
            {
                "minute": 90,
                "team": {"id": 531, "name": "ES Troyes AC"},
                "playerOut": {"id": 8415, "name": "Rominigue Kouamé"},
                "playerIn": {"id": 824, "name": "Xavier Chavalerin"},
            },
        ],
        "odds": {"homeWin": 4.25, "draw": 3.72, "awayWin": 1.81},
        "referees": [
            {
                "id": 57080,
                "name": "Cyril Mugnier",
                "type": "ASSISTANT_REFEREE_N1",
                "nationality": "France",
            },
            {
                "id": 57049,
                "name": "Mehdi Rahmouni",
                "type": "ASSISTANT_REFEREE_N2",
                "nationality": "France",
            },
            {
                "id": 57031,
                "name": "Alexandre Perreau Niel",
                "type": "FOURTH_OFFICIAL",
                "nationality": "France",
            },
            {
                "id": 43918,
                "name": "François Letexier",
                "type": "REFEREE",
                "nationality": "France",
            },
            {
                "id": 57073,
                "name": "Jérémie Pignard",
                "type": "VIDEO_ASSISTANT_REFEREE_N1",
                "nationality": "France",
            },
            {
                "id": 166622,
                "name": "Abdelali Chaoui",
                "type": "VIDEO_ASSISTANT_REFEREE_N2",
                "nationality": None,
            },
        ],
    }
]

# points = calculate_player_points(data)
# print(points)
