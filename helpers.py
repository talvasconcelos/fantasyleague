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
        stats = player_entry["statistics"][0]["goals"]
        if stats["total"] is not None:
            player_position = player_entry["statistics"][0]["games"]["position"]
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
        stats = player_entry["statistics"][0]["goals"]
        if stats["assists"] is not None:
            points[player_id] += 3 * stats["assists"]


def _calculate_points_for_cards(player_data, points):
    for player_entry in player_data:
        player_id = player_entry["player"]["id"]
        cards = player_entry["statistics"][0]["cards"]
        points[player_id] -= 1 * cards["yellow"]
        points[player_id] -= 3 * cards["red"]


def _calculate_points_for_playing_time(player_data, points):
    for player_entry in player_data:
        player_id = player_entry["player"]["id"]
        minutes_played = player_entry["statistics"][0]["games"]["minutes"] or 0
        if minutes_played >= 60:
            points[player_id] += 2
        elif minutes_played > 0:
            points[player_id] += 1


def _calculate_points_for_saves(player_data, points):
    for player_entry in player_data:
        player_id = player_entry["player"]["id"]
        stats = player_entry["statistics"][0]
        if stats["games"]["position"] == "G":  # Check if the player is a goalkeeper
            points[player_id] += stats["goals"]["saves"] or 0


# Example usage
data = [
    {
        "player": {
            "id": 10298,
            "name": "Marcos Felipe",
            "photo": "https://media.api-sports.io/football/players/10298.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 22,
                    "position": "G",
                    "rating": "8.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": 5},
                "passes": {"total": 38, "key": None, "accuracy": "28"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": 0,
                },
            }
        ],
    },
    {
        "player": {
            "id": 30,
            "name": "Santiago Arias",
            "photo": "https://media.api-sports.io/football/players/30.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 13,
                    "position": "D",
                    "rating": "7.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 23, "key": None, "accuracy": "15"},
                "tackles": {"total": 1, "blocks": 1, "interceptions": None},
                "duels": {"total": 11, "won": 5},
                "dribbles": {"attempts": None, "success": None, "past": 2},
                "fouls": {"drawn": 2, "committed": 2},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 353728,
            "name": "Gabriel Xavier",
            "photo": "https://media.api-sports.io/football/players/353728.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 3,
                    "position": "D",
                    "rating": "8.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 50, "key": None, "accuracy": "40"},
                "tackles": {"total": 5, "blocks": 2, "interceptions": 4},
                "duels": {"total": 14, "won": 12},
                "dribbles": {"attempts": None, "success": None, "past": 1},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10059,
            "name": "Kanu",
            "photo": "https://media.api-sports.io/football/players/10059.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 4,
                    "position": "D",
                    "rating": "7.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 31, "key": None, "accuracy": "27"},
                "tackles": {"total": None, "blocks": None, "interceptions": 1},
                "duels": {"total": 6, "won": 5},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 197383,
            "name": "Luciano Juba",
            "photo": "https://media.api-sports.io/football/players/197383.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 46,
                    "position": "D",
                    "rating": "7.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 41, "key": 1, "accuracy": "29"},
                "tackles": {"total": None, "blocks": 1, "interceptions": 2},
                "duels": {"total": 2, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10168,
            "name": "Everton Ribeiro",
            "photo": "https://media.api-sports.io/football/players/10168.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 77,
                    "number": 10,
                    "position": "M",
                    "rating": "7",
                    "captain": True,
                    "substitute": False,
                },
                "offsides": 1,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 38, "key": 1, "accuracy": "31"},
                "tackles": {"total": 2, "blocks": None, "interceptions": 3},
                "duels": {"total": 10, "won": 3},
                "dribbles": {"attempts": 1, "success": None, "past": 1},
                "fouls": {"drawn": 1, "committed": 2},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 180236,
            "name": "Caio Alexandre",
            "photo": "https://media.api-sports.io/football/players/180236.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 77,
                    "number": 19,
                    "position": "M",
                    "rating": "7.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 40, "key": 1, "accuracy": "36"},
                "tackles": {"total": 4, "blocks": None, "interceptions": 1},
                "duels": {"total": 11, "won": 6},
                "dribbles": {"attempts": 1, "success": 1, "past": 3},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9994,
            "name": "Jean Lucas",
            "photo": "https://media.api-sports.io/football/players/9994.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 6,
                    "position": "M",
                    "rating": "6.7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": 1,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 34, "key": 1, "accuracy": "26"},
                "tackles": {"total": 2, "blocks": None, "interceptions": 1},
                "duels": {"total": 21, "won": 10},
                "dribbles": {"attempts": 4, "success": 2, "past": 3},
                "fouls": {"drawn": 3, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 25272,
            "name": "Cauly",
            "photo": "https://media.api-sports.io/football/players/25272.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 85,
                    "number": 8,
                    "position": "M",
                    "rating": "7.7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": 1, "saves": None},
                "passes": {"total": 36, "key": 4, "accuracy": "31"},
                "tackles": {"total": 2, "blocks": None, "interceptions": None},
                "duels": {"total": 7, "won": 3},
                "dribbles": {"attempts": 2, "success": None, "past": 1},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10492,
            "name": "Thaciano",
            "photo": "https://media.api-sports.io/football/players/10492.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 77,
                    "number": 16,
                    "position": "F",
                    "rating": "7.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": 1,
                "shots": {"total": 3, "on": 1},
                "goals": {"total": 1, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 19, "key": None, "accuracy": "14"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 7, "won": 3},
                "dribbles": {"attempts": None, "success": None, "past": 1},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10222,
            "name": "Everaldo",
            "photo": "https://media.api-sports.io/football/players/10222.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 69,
                    "number": 9,
                    "position": "F",
                    "rating": "6.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": 1,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 18, "key": None, "accuracy": "14"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 8, "won": 2},
                "dribbles": {"attempts": None, "success": None, "past": 2},
                "fouls": {"drawn": 2, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 305817,
            "name": "Biel",
            "photo": "https://media.api-sports.io/football/players/305817.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 21,
                    "number": 11,
                    "position": "F",
                    "rating": "6.2",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 4, "key": None, "accuracy": "2"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 6, "won": 1},
                "dribbles": {"attempts": 2, "success": 1, "past": None},
                "fouls": {"drawn": None, "committed": 3},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 2173,
            "name": "Carlos De Pena",
            "photo": "https://media.api-sports.io/football/players/2173.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 13,
                    "number": 14,
                    "position": "M",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 7, "key": None, "accuracy": "6"},
                "tackles": {"total": None, "blocks": None, "interceptions": 1},
                "duels": {"total": 2, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": 1},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 157359,
            "name": "Rezende",
            "photo": "https://media.api-sports.io/football/players/157359.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 13,
                    "number": 5,
                    "position": "M",
                    "rating": "6.7",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 1, "key": None, "accuracy": "1"},
                "tackles": {"total": 1, "blocks": None, "interceptions": 1},
                "duels": {"total": 3, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 61159,
            "name": "Rafael Ratão",
            "photo": "https://media.api-sports.io/football/players/61159.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 13,
                    "number": 21,
                    "position": "F",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 5, "key": None, "accuracy": "4"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 3, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": 1},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9854,
            "name": "Ademir",
            "photo": "https://media.api-sports.io/football/players/9854.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 10,
                    "number": 7,
                    "position": "F",
                    "rating": "6.6",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 2, "key": None, "accuracy": "2"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 2, "won": 2},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 2, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10374,
            "name": "Danilo Fernandes",
            "photo": "https://media.api-sports.io/football/players/10374.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 1,
                    "position": "G",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10351,
            "name": "David Duarte",
            "photo": "https://media.api-sports.io/football/players/10351.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 33,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10305,
            "name": "Gilberto",
            "photo": "https://media.api-sports.io/football/players/10305.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 2,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10377,
            "name": "Víctor Cuesta",
            "photo": "https://media.api-sports.io/football/players/10377.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 15,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 1057,
            "name": "Cicinho",
            "photo": "https://media.api-sports.io/football/players/1057.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 40,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10348,
            "name": "Yago Felipe",
            "photo": "https://media.api-sports.io/football/players/10348.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 20,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 63968,
            "name": "Óscar Estupiñán",
            "photo": "https://media.api-sports.io/football/players/63968.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 29,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9862,
            "name": "Cleiton",
            "photo": "https://media.api-sports.io/football/players/9862.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 1,
                    "position": "G",
                    "rating": "7",
                    "captain": True,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 1, "assists": None, "saves": 2},
                "passes": {"total": 17, "key": None, "accuracy": "12"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 2, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": 0,
                },
            }
        ],
    },
    {
        "player": {
            "id": 311518,
            "name": "Nathan Mendes",
            "photo": "https://media.api-sports.io/football/players/311518.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 45,
                    "position": "D",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": 1,
                "shots": {"total": 2, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 39, "key": None, "accuracy": "34"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 9, "won": 5},
                "dribbles": {"attempts": 1, "success": 1, "past": 1},
                "fouls": {"drawn": 2, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10235,
            "name": "Pedro Henrique",
            "photo": "https://media.api-sports.io/football/players/10235.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 14,
                    "position": "D",
                    "rating": "7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 61, "key": 1, "accuracy": "44"},
                "tackles": {"total": 4, "blocks": None, "interceptions": 1},
                "duels": {"total": 11, "won": 6},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 41544,
            "name": "Eduardo Santos",
            "photo": "https://media.api-sports.io/football/players/41544.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 3,
                    "position": "D",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 61, "key": None, "accuracy": "55"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 7, "won": 4},
                "dribbles": {"attempts": 2, "success": 1, "past": None},
                "fouls": {"drawn": 2, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9906,
            "name": "Luan Cândido",
            "photo": "https://media.api-sports.io/football/players/9906.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 36,
                    "position": "D",
                    "rating": "7.7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 36, "key": None, "accuracy": "31"},
                "tackles": {"total": 7, "blocks": 1, "interceptions": 3},
                "duels": {"total": 12, "won": 10},
                "dribbles": {"attempts": 1, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 403951,
            "name": "Gustavo Neves",
            "photo": "https://media.api-sports.io/football/players/403951.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 45,
                    "number": 22,
                    "position": "M",
                    "rating": "6.7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 10, "key": None, "accuracy": "9"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 10, "won": 6},
                "dribbles": {"attempts": 6, "success": 4, "past": 1},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 80539,
            "name": "Jadsom",
            "photo": "https://media.api-sports.io/football/players/80539.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 64,
                    "number": 5,
                    "position": "M",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 31, "key": None, "accuracy": "28"},
                "tackles": {"total": 3, "blocks": None, "interceptions": None},
                "duels": {"total": 4, "won": 3},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 21095,
            "name": "Lucas Evangelista",
            "photo": "https://media.api-sports.io/football/players/21095.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 57,
                    "number": 8,
                    "position": "M",
                    "rating": "7.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 2, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 22, "key": 1, "accuracy": "16"},
                "tackles": {"total": 1, "blocks": 1, "interceptions": 2},
                "duels": {"total": 10, "won": 4},
                "dribbles": {"attempts": None, "success": None, "past": 2},
                "fouls": {"drawn": 2, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9965,
            "name": "Helinho",
            "photo": "https://media.api-sports.io/football/players/9965.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 11,
                    "position": "F",
                    "rating": "8",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 2, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 40, "key": 3, "accuracy": "28"},
                "tackles": {"total": None, "blocks": None, "interceptions": 2},
                "duels": {"total": 8, "won": 7},
                "dribbles": {"attempts": 5, "success": 5, "past": None},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 197513,
            "name": "Thiago Borbas",
            "photo": "https://media.api-sports.io/football/players/197513.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 77,
                    "number": 18,
                    "position": "F",
                    "rating": "6.5",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 7, "key": 1, "accuracy": "3"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 8, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 3},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10147,
            "name": "Vitinho",
            "photo": "https://media.api-sports.io/football/players/10147.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 45,
                    "number": 28,
                    "position": "F",
                    "rating": "6.6",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 12, "key": None, "accuracy": "8"},
                "tackles": {"total": 2, "blocks": None, "interceptions": 1},
                "duels": {"total": 13, "won": 5},
                "dribbles": {"attempts": 3, "success": 1, "past": None},
                "fouls": {"drawn": 1, "committed": 3},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10027,
            "name": "Eric Ramires",
            "photo": "https://media.api-sports.io/football/players/10027.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 45,
                    "number": 7,
                    "position": "M",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 22, "key": 1, "accuracy": "21"},
                "tackles": {"total": 3, "blocks": None, "interceptions": None},
                "duels": {"total": 4, "won": 3},
                "dribbles": {"attempts": 1, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 350927,
            "name": "Henry Mosquera",
            "photo": "https://media.api-sports.io/football/players/350927.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 45,
                    "number": 30,
                    "position": "F",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 11, "key": None, "accuracy": "9"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 9, "won": 4},
                "dribbles": {"attempts": 5, "success": 4, "past": None},
                "fouls": {"drawn": None, "committed": 2},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9925,
            "name": "Matheus Fernandes",
            "photo": "https://media.api-sports.io/football/players/9925.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 33,
                    "number": 35,
                    "position": "M",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 16, "key": None, "accuracy": "12"},
                "tackles": {"total": 1, "blocks": None, "interceptions": 1},
                "duels": {"total": 6, "won": 3},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 2, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10497,
            "name": "Lincoln",
            "photo": "https://media.api-sports.io/football/players/10497.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 26,
                    "number": 10,
                    "position": "M",
                    "rating": "6.6",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": 1,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 10, "key": None, "accuracy": "7"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 1, "won": None},
                "dribbles": {"attempts": 1, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 403950,
            "name": "Talisson",
            "photo": "https://media.api-sports.io/football/players/403950.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 13,
                    "number": 21,
                    "position": "F",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": 1,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 3, "key": None, "accuracy": "1"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 2, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 140450,
            "name": "Lucão",
            "photo": "https://media.api-sports.io/football/players/140450.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 40,
                    "position": "G",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 41092,
            "name": "Lucas Cunha",
            "photo": "https://media.api-sports.io/football/players/41092.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 4,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 16370,
            "name": "Leonardo Realpe",
            "photo": "https://media.api-sports.io/football/players/16370.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 2,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10481,
            "name": "Juninho Capixaba",
            "photo": "https://media.api-sports.io/football/players/10481.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 29,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 195976,
            "name": "Guilherme Lopes",
            "photo": "https://media.api-sports.io/football/players/195976.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 31,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 51464,
            "name": "Ignacio Laquintana",
            "photo": "https://media.api-sports.io/football/players/51464.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 33,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 306181,
            "name": "Everton",
            "photo": "https://media.api-sports.io/football/players/306181.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 55,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 11756,
            "name": "Agustín Rossi",
            "photo": "https://media.api-sports.io/football/players/11756.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 95,
                    "number": 1,
                    "position": "G",
                    "rating": "7.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": 3},
                "passes": {"total": 41, "key": None, "accuracy": "29"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 1, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": 0,
                },
            }
        ],
    },
    {
        "player": {
            "id": 1290,
            "name": "Guillermo Varela",
            "photo": "https://media.api-sports.io/football/players/1290.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 95,
                    "number": 2,
                    "position": "D",
                    "rating": "7.7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 59, "key": 2, "accuracy": "55"},
                "tackles": {"total": 2, "blocks": None, "interceptions": 1},
                "duels": {"total": 10, "won": 7},
                "dribbles": {"attempts": 1, "success": 1, "past": 1},
                "fouls": {"drawn": 3, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10089,
            "name": "Fabrício Bruno",
            "photo": "https://media.api-sports.io/football/players/10089.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 95,
                    "number": 15,
                    "position": "D",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 55, "key": None, "accuracy": "49"},
                "tackles": {"total": None, "blocks": 1, "interceptions": None},
                "duels": {"total": 1, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10124,
            "name": "Léo Pereira",
            "photo": "https://media.api-sports.io/football/players/10124.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 95,
                    "number": 4,
                    "position": "D",
                    "rating": "7.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 56, "key": None, "accuracy": "49"},
                "tackles": {"total": 2, "blocks": 2, "interceptions": 1},
                "duels": {"total": 11, "won": 4},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": 2},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 1771,
            "name": "Ayrton Lucas",
            "photo": "https://media.api-sports.io/football/players/1771.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 95,
                    "number": 6,
                    "position": "D",
                    "rating": "7.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 51, "key": 2, "accuracy": "39"},
                "tackles": {"total": 2, "blocks": None, "interceptions": None},
                "duels": {"total": 14, "won": 9},
                "dribbles": {"attempts": 6, "success": 4, "past": None},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 5995,
            "name": "Nicolás de la Cruz",
            "photo": "https://media.api-sports.io/football/players/5995.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 92,
                    "number": 18,
                    "position": "M",
                    "rating": "8.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 69, "key": 3, "accuracy": "62"},
                "tackles": {"total": 4, "blocks": 1, "interceptions": 1},
                "duels": {"total": 17, "won": 10},
                "dribbles": {"attempts": 3, "success": 2, "past": 1},
                "fouls": {"drawn": 3, "committed": 2},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10319,
            "name": "Allan",
            "photo": "https://media.api-sports.io/football/players/10319.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 95,
                    "number": 21,
                    "position": "M",
                    "rating": "7.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 43, "key": 1, "accuracy": "35"},
                "tackles": {"total": 1, "blocks": 1, "interceptions": 1},
                "duels": {"total": 11, "won": 5},
                "dribbles": {"attempts": 1, "success": 1, "past": None},
                "fouls": {"drawn": 1, "committed": 5},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 30408,
            "name": "Gerson",
            "photo": "https://media.api-sports.io/football/players/30408.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 95,
                    "number": 8,
                    "position": "M",
                    "rating": "8.5",
                    "captain": True,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": 1, "saves": None},
                "passes": {"total": 48, "key": 6, "accuracy": "48"},
                "tackles": {"total": 4, "blocks": None, "interceptions": None},
                "duels": {"total": 11, "won": 7},
                "dribbles": {"attempts": 1, "success": None, "past": None},
                "fouls": {"drawn": 3, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 403300,
            "name": "Lorran",
            "photo": "https://media.api-sports.io/football/players/403300.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 88,
                    "number": 19,
                    "position": "M",
                    "rating": "8.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 3, "on": 2},
                "goals": {"total": 1, "conceded": 0, "assists": 1, "saves": None},
                "passes": {"total": 40, "key": 2, "accuracy": "27"},
                "tackles": {"total": 3, "blocks": None, "interceptions": 1},
                "duels": {"total": 15, "won": 9},
                "dribbles": {"attempts": 6, "success": 5, "past": None},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 2414,
            "name": "Everton",
            "photo": "https://media.api-sports.io/football/players/2414.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 88,
                    "number": 11,
                    "position": "M",
                    "rating": "7.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": 1,
                "shots": {"total": 3, "on": 3},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 21, "key": None, "accuracy": "16"},
                "tackles": {"total": 2, "blocks": None, "interceptions": 1},
                "duels": {"total": 14, "won": 5},
                "dribbles": {"attempts": 5, "success": 2, "past": 2},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10321,
            "name": "Pedro",
            "photo": "https://media.api-sports.io/football/players/10321.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 45,
                    "number": 9,
                    "position": "F",
                    "rating": "7.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 3, "on": 2},
                "goals": {"total": 1, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 6, "key": None, "accuracy": "4"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 4, "won": 2},
                "dribbles": {"attempts": 1, "success": 1, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10174,
            "name": "Gabriel Barbosa",
            "photo": "https://media.api-sports.io/football/players/10174.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 50,
                    "number": 10,
                    "position": "F",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 4, "key": None, "accuracy": "4"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 2, "won": 1},
                "dribbles": {"attempts": 1, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9458,
            "name": "Léo Ortiz",
            "photo": "https://media.api-sports.io/football/players/9458.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 7,
                    "number": 3,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 3, "key": None, "accuracy": "1"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 22238,
            "name": "Luiz Araújo",
            "photo": "https://media.api-sports.io/football/players/22238.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 7,
                    "number": 7,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 352371,
            "name": "Victor Hugo",
            "photo": "https://media.api-sports.io/football/players/352371.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 3,
                    "number": 29,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 1, "key": None, "accuracy": "1"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 1, "won": None},
                "dribbles": {"attempts": 1, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 306210,
            "name": "Matheus Cunha",
            "photo": "https://media.api-sports.io/football/players/306210.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 25,
                    "position": "G",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 349001,
            "name": "Wesley França",
            "photo": "https://media.api-sports.io/football/players/349001.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 43,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 51572,
            "name": "Matías Viña",
            "photo": "https://media.api-sports.io/football/players/51572.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 17,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 2, "key": None, "accuracy": "2"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 2283,
            "name": "David Luiz",
            "photo": "https://media.api-sports.io/football/players/2283.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 23,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 2612,
            "name": "Giorgian De Arrascaeta",
            "photo": "https://media.api-sports.io/football/players/2612.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 14,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 322067,
            "name": "Igor Jesus",
            "photo": "https://media.api-sports.io/football/players/322067.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 48,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 311158,
            "name": "Werton",
            "photo": "https://media.api-sports.io/football/players/311158.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 26,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 70297,
            "name": "Carlinhos",
            "photo": "https://media.api-sports.io/football/players/70297.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 22,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10373,
            "name": "Carlos Miguel",
            "photo": "https://media.api-sports.io/football/players/10373.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 95,
                    "number": 22,
                    "position": "G",
                    "rating": "8.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 2, "assists": None, "saves": 8},
                "passes": {"total": 20, "key": None, "accuracy": "17"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": 0,
                },
            }
        ],
    },
    {
        "player": {
            "id": 63964,
            "name": "Félix Torres",
            "photo": "https://media.api-sports.io/football/players/63964.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 95,
                    "number": 3,
                    "position": "D",
                    "rating": "7.5",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 61, "key": 1, "accuracy": "54"},
                "tackles": {"total": 5, "blocks": 1, "interceptions": 1},
                "duels": {"total": 14, "won": 8},
                "dribbles": {"attempts": None, "success": None, "past": 2},
                "fouls": {"drawn": None, "committed": 3},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9992,
            "name": "Gustavo Henrique",
            "photo": "https://media.api-sports.io/football/players/9992.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 95,
                    "number": 13,
                    "position": "D",
                    "rating": "7.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 3, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 33, "key": None, "accuracy": "29"},
                "tackles": {"total": None, "blocks": None, "interceptions": 2},
                "duels": {"total": 9, "won": 7},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10085,
            "name": "Cacá",
            "photo": "https://media.api-sports.io/football/players/10085.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 75,
                    "number": 25,
                    "position": "D",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 2, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 20, "key": None, "accuracy": "20"},
                "tackles": {"total": None, "blocks": 2, "interceptions": None},
                "duels": {"total": 8, "won": 2},
                "dribbles": {"attempts": None, "success": None, "past": 1},
                "fouls": {"drawn": 1, "committed": 2},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 2411,
            "name": "Fagner",
            "photo": "https://media.api-sports.io/football/players/2411.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 82,
                    "number": 23,
                    "position": "M",
                    "rating": "7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 25, "key": 2, "accuracy": "18"},
                "tackles": {"total": 2, "blocks": None, "interceptions": 1},
                "duels": {"total": 7, "won": 4},
                "dribbles": {"attempts": 1, "success": 1, "past": 2},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 12719,
            "name": "Paulinho",
            "photo": "https://media.api-sports.io/football/players/12719.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 45,
                    "number": 8,
                    "position": "M",
                    "rating": "6.9",
                    "captain": True,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 23, "key": None, "accuracy": "21"},
                "tackles": {"total": 3, "blocks": None, "interceptions": None},
                "duels": {"total": 10, "won": 6},
                "dribbles": {"attempts": None, "success": None, "past": 2},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 363693,
            "name": "Breno Bidon",
            "photo": "https://media.api-sports.io/football/players/363693.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 95,
                    "number": 27,
                    "position": "M",
                    "rating": "6.6",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 35, "key": None, "accuracy": "29"},
                "tackles": {"total": 1, "blocks": 1, "interceptions": 1},
                "duels": {"total": 6, "won": 3},
                "dribbles": {"attempts": None, "success": None, "past": 2},
                "fouls": {"drawn": 2, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 54093,
            "name": "Hugo",
            "photo": "https://media.api-sports.io/football/players/54093.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 95,
                    "number": 46,
                    "position": "M",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 27, "key": 1, "accuracy": "21"},
                "tackles": {"total": 2, "blocks": None, "interceptions": 1},
                "duels": {"total": 12, "won": 6},
                "dribbles": {"attempts": None, "success": None, "past": 2},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 2521,
            "name": "Ángel Romero",
            "photo": "https://media.api-sports.io/football/players/2521.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 75,
                    "number": 11,
                    "position": "F",
                    "rating": "6.7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 23, "key": 1, "accuracy": "17"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 12, "won": 5},
                "dribbles": {"attempts": 3, "success": 1, "past": 1},
                "fouls": {"drawn": 2, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 5794,
            "name": "Rodrigo Garro",
            "photo": "https://media.api-sports.io/football/players/5794.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 82,
                    "number": 10,
                    "position": "F",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 30, "key": 2, "accuracy": "22"},
                "tackles": {"total": 2, "blocks": None, "interceptions": None},
                "duels": {"total": 11, "won": 3},
                "dribbles": {"attempts": 2, "success": None, "past": 2},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 365287,
            "name": "Wesley",
            "photo": "https://media.api-sports.io/football/players/365287.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 95,
                    "number": 36,
                    "position": "F",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 14, "key": 2, "accuracy": "11"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 15, "won": 5},
                "dribbles": {"attempts": 5, "success": 2, "past": 2},
                "fouls": {"drawn": 3, "committed": 2},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10007,
            "name": "Yuri Alberto",
            "photo": "https://media.api-sports.io/football/players/10007.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 50,
                    "number": 9,
                    "position": "F",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": 1,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 13, "key": 1, "accuracy": "11"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 4, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 50268,
            "name": "Igor Coronado",
            "photo": "https://media.api-sports.io/football/players/50268.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 20,
                    "number": 77,
                    "position": "M",
                    "rating": "6.6",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 16, "key": None, "accuracy": "10"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 3, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9620,
            "name": "Gustavo Silva",
            "photo": "https://media.api-sports.io/football/players/9620.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 20,
                    "number": 19,
                    "position": "F",
                    "rating": "6.7",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 7, "key": 1, "accuracy": "6"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 361665,
            "name": "Léo Mana",
            "photo": "https://media.api-sports.io/football/players/361665.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 13,
                    "number": 35,
                    "position": "D",
                    "rating": "6.7",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 10, "key": None, "accuracy": "6"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 306853,
            "name": "Guilherme Biro",
            "photo": "https://media.api-sports.io/football/players/306853.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 13,
                    "number": 26,
                    "position": "M",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 5, "key": None, "accuracy": "4"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 1, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10229,
            "name": "Cássio",
            "photo": "https://media.api-sports.io/football/players/10229.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 12,
                    "position": "G",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9742,
            "name": "Matheus Bidú",
            "photo": "https://media.api-sports.io/football/players/9742.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 21,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 14390,
            "name": "Raul Gustavo",
            "photo": "https://media.api-sports.io/football/players/14390.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 34,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 80534,
            "name": "Caetano",
            "photo": "https://media.api-sports.io/football/players/80534.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 4,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 403953,
            "name": "Ryan Gustavo",
            "photo": "https://media.api-sports.io/football/players/403953.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 37,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 312615,
            "name": "Giovane",
            "photo": "https://media.api-sports.io/football/players/312615.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 17,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9329,
            "name": "Pedro Raul",
            "photo": "https://media.api-sports.io/football/players/9329.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 20,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 41169,
            "name": "Léo Jardim",
            "photo": "https://media.api-sports.io/football/players/41169.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 1,
                    "position": "G",
                    "rating": "7.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 1, "assists": None, "saves": 4},
                "passes": {"total": 27, "key": None, "accuracy": "21"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": 0,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10225,
            "name": "João Victor",
            "photo": "https://media.api-sports.io/football/players/10225.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 80,
                    "number": 38,
                    "position": "D",
                    "rating": "7.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 33, "key": 1, "accuracy": "27"},
                "tackles": {"total": 3, "blocks": 1, "interceptions": None},
                "duels": {"total": 12, "won": 7},
                "dribbles": {"attempts": 1, "success": None, "past": 1},
                "fouls": {"drawn": 2, "committed": 2},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 44304,
            "name": "Maicon",
            "photo": "https://media.api-sports.io/football/players/44304.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 4,
                    "position": "D",
                    "rating": "7.6",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": 1, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 55, "key": None, "accuracy": "50"},
                "tackles": {"total": 1, "blocks": None, "interceptions": 2},
                "duels": {"total": 9, "won": 7},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 2, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9951,
            "name": "Léo",
            "photo": "https://media.api-sports.io/football/players/9951.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 3,
                    "position": "D",
                    "rating": "6.9",
                    "captain": True,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 62, "key": None, "accuracy": "55"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 5, "won": 3},
                "dribbles": {"attempts": None, "success": None, "past": 2},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10234,
            "name": "Lucas Piton",
            "photo": "https://media.api-sports.io/football/players/10234.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 6,
                    "position": "D",
                    "rating": "7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 38, "key": 1, "accuracy": "38"},
                "tackles": {"total": 7, "blocks": None, "interceptions": 2},
                "duels": {"total": 13, "won": 7},
                "dribbles": {"attempts": 1, "success": None, "past": 3},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 6057,
            "name": "Pablo Galdames",
            "photo": "https://media.api-sports.io/football/players/6057.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 80,
                    "number": 27,
                    "position": "M",
                    "rating": "7.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 53, "key": 1, "accuracy": "48"},
                "tackles": {"total": None, "blocks": None, "interceptions": 2},
                "duels": {"total": 5, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": 1},
                "fouls": {"drawn": None, "committed": 2},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 237089,
            "name": "Juan Sforza",
            "photo": "https://media.api-sports.io/football/players/237089.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 20,
                    "position": "M",
                    "rating": "7.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 81, "key": None, "accuracy": "75"},
                "tackles": {"total": 2, "blocks": 1, "interceptions": 1},
                "duels": {"total": 7, "won": 4},
                "dribbles": {"attempts": 1, "success": 1, "past": 1},
                "fouls": {"drawn": None, "committed": 2},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10578,
            "name": "Rossi",
            "photo": "https://media.api-sports.io/football/players/10578.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 45,
                    "number": 31,
                    "position": "M",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 13, "key": None, "accuracy": "9"},
                "tackles": {"total": 2, "blocks": None, "interceptions": 1},
                "duels": {"total": 3, "won": 2},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 1912,
            "name": "Dimitri Payet",
            "photo": "https://media.api-sports.io/football/players/1912.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 67,
                    "number": 10,
                    "position": "M",
                    "rating": "8.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": 2, "saves": None},
                "passes": {"total": 46, "key": 4, "accuracy": "41"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 8, "won": 3},
                "dribbles": {"attempts": 3, "success": 1, "past": None},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10105,
            "name": "David",
            "photo": "https://media.api-sports.io/football/players/10105.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 7,
                    "position": "M",
                    "rating": "7.5",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 3, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 34, "key": 1, "accuracy": "28"},
                "tackles": {"total": 3, "blocks": None, "interceptions": None},
                "duels": {"total": 17, "won": 8},
                "dribbles": {"attempts": 5, "success": 3, "past": 1},
                "fouls": {"drawn": 1, "committed": 2},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 5804,
            "name": "Pablo Vegetti",
            "photo": "https://media.api-sports.io/football/players/5804.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 99,
                    "position": "F",
                    "rating": "7.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": 1,
                "shots": {"total": 2, "on": 2},
                "goals": {"total": 1, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 21, "key": 1, "accuracy": "14"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 17, "won": 10},
                "dribbles": {"attempts": None, "success": None, "past": 2},
                "fouls": {"drawn": 3, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 306261,
            "name": "Adson",
            "photo": "https://media.api-sports.io/football/players/306261.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 44,
                    "number": 28,
                    "position": "M",
                    "rating": "7.2",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 20, "key": 1, "accuracy": "17"},
                "tackles": {"total": 3, "blocks": None, "interceptions": None},
                "duels": {"total": 8, "won": 7},
                "dribbles": {"attempts": 3, "success": 3, "past": 1},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 197533,
            "name": "Bruno Praxedes",
            "photo": "https://media.api-sports.io/football/players/197533.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 23,
                    "number": 21,
                    "position": "M",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 14, "key": 3, "accuracy": "12"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 7, "won": 4},
                "dribbles": {"attempts": 3, "success": 2, "past": 2},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 133910,
            "name": "Paulo Henrique",
            "photo": "https://media.api-sports.io/football/players/133910.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 10,
                    "number": 96,
                    "position": "D",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 9, "key": 1, "accuracy": "9"},
                "tackles": {"total": 1, "blocks": 1, "interceptions": None},
                "duels": {"total": 3, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 2},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 375565,
            "name": "Mateus Carvalho",
            "photo": "https://media.api-sports.io/football/players/375565.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 10,
                    "number": 85,
                    "position": "M",
                    "rating": "3.6",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 17, "key": None, "accuracy": "15"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 5, "won": 1},
                "dribbles": {"attempts": 1, "success": None, "past": 1},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 51426,
            "name": "Puma Rodríguez",
            "photo": "https://media.api-sports.io/football/players/51426.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 1,
                    "number": 2,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 4, "key": None, "accuracy": "4"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10370,
            "name": "Keiller",
            "photo": "https://media.api-sports.io/football/players/10370.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 13,
                    "position": "G",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9907,
            "name": "Victor Luis",
            "photo": "https://media.api-sports.io/football/players/9907.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 12,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 2504,
            "name": "Robert Rojas",
            "photo": "https://media.api-sports.io/football/players/2504.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 32,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 1982,
            "name": "Gary Medel",
            "photo": "https://media.api-sports.io/football/players/1982.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 17,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 125677,
            "name": "Zé Gabriel",
            "photo": "https://media.api-sports.io/football/players/125677.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 23,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 195580,
            "name": "Clayton",
            "photo": "https://media.api-sports.io/football/players/195580.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 9,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 407806,
            "name": "Rayan",
            "photo": "https://media.api-sports.io/football/players/407806.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 77,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9510,
            "name": "Lucas Arcanjo",
            "photo": "https://media.api-sports.io/football/players/9510.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 1,
                    "position": "G",
                    "rating": "7.5",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 2, "assists": None, "saves": 6},
                "passes": {"total": 7, "key": None, "accuracy": "2"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": 0,
                },
            }
        ],
    },
    {
        "player": {
            "id": 80523,
            "name": "Willean Lepo",
            "photo": "https://media.api-sports.io/football/players/80523.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 45,
                    "number": 97,
                    "position": "D",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 19, "key": 1, "accuracy": "16"},
                "tackles": {"total": 3, "blocks": None, "interceptions": None},
                "duels": {"total": 12, "won": 6},
                "dribbles": {"attempts": 3, "success": 1, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 54692,
            "name": "Camutanga",
            "photo": "https://media.api-sports.io/football/players/54692.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 13,
                    "position": "D",
                    "rating": "6.5",
                    "captain": True,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 27, "key": None, "accuracy": "25"},
                "tackles": {"total": 3, "blocks": 2, "interceptions": None},
                "duels": {"total": 12, "won": 4},
                "dribbles": {"attempts": None, "success": None, "past": 2},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 1},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 54230,
            "name": "Reynaldo",
            "photo": "https://media.api-sports.io/football/players/54230.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 40,
                    "position": "D",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 31, "key": None, "accuracy": "28"},
                "tackles": {"total": 2, "blocks": 2, "interceptions": None},
                "duels": {"total": 4, "won": 2},
                "dribbles": {"attempts": None, "success": None, "past": 1},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 353394,
            "name": "Janderson",
            "photo": "https://media.api-sports.io/football/players/353394.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 79,
                    "number": 39,
                    "position": "M",
                    "rating": "7.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 29, "key": 2, "accuracy": "19"},
                "tackles": {"total": 2, "blocks": None, "interceptions": None},
                "duels": {"total": 12, "won": 8},
                "dribbles": {"attempts": 5, "success": 3, "past": None},
                "fouls": {"drawn": 2, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9957,
            "name": "Luan Santos",
            "photo": "https://media.api-sports.io/football/players/9957.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 58,
                    "number": 8,
                    "position": "M",
                    "rating": "6.5",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 27, "key": None, "accuracy": "25"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 5, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": 2},
                "fouls": {"drawn": None, "committed": 2},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 156942,
            "name": "Dudu",
            "photo": "https://media.api-sports.io/football/players/156942.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 21,
                    "position": "M",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 67, "key": 1, "accuracy": "49"},
                "tackles": {"total": 5, "blocks": None, "interceptions": None},
                "duels": {"total": 19, "won": 9},
                "dribbles": {"attempts": 3, "success": 1, "past": 3},
                "fouls": {"drawn": 2, "committed": 3},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 53985,
            "name": "Patric Calmon",
            "photo": "https://media.api-sports.io/football/players/53985.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 14,
                    "position": "M",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 39, "key": None, "accuracy": "29"},
                "tackles": {"total": 1, "blocks": None, "interceptions": 5},
                "duels": {"total": 10, "won": 4},
                "dribbles": {"attempts": 4, "success": 1, "past": 1},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 114436,
            "name": "Matheuzinho",
            "photo": "https://media.api-sports.io/football/players/114436.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 66,
                    "number": 30,
                    "position": "F",
                    "rating": "7.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 2, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 16, "key": None, "accuracy": "15"},
                "tackles": {"total": None, "blocks": None, "interceptions": 2},
                "duels": {"total": 9, "won": 6},
                "dribbles": {"attempts": 4, "success": 3, "past": None},
                "fouls": {"drawn": 3, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9533,
            "name": "Rodrigo Andrade",
            "photo": "https://media.api-sports.io/football/players/9533.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 32,
                    "position": "F",
                    "rating": "6.6",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 42, "key": None, "accuracy": "39"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 5, "won": 1},
                "dribbles": {"attempts": 1, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9893,
            "name": "Alerrandro",
            "photo": "https://media.api-sports.io/football/players/9893.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 66,
                    "number": 9,
                    "position": "F",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 21, "key": 1, "accuracy": "13"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 8, "won": 2},
                "dribbles": {"attempts": 1, "success": None, "past": 1},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10376,
            "name": "Zeca",
            "photo": "https://media.api-sports.io/football/players/10376.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 45,
                    "number": 2,
                    "position": "D",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 20, "key": None, "accuracy": "17"},
                "tackles": {"total": 1, "blocks": 2, "interceptions": None},
                "duels": {"total": 4, "won": 2},
                "dribbles": {"attempts": 1, "success": 1, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 44675,
            "name": "Iury Castilho",
            "photo": "https://media.api-sports.io/football/players/44675.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 32,
                    "number": 7,
                    "position": "F",
                    "rating": "7.2",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": 3, "on": 2},
                "goals": {"total": 1, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 14, "key": 1, "accuracy": "12"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 13, "won": 6},
                "dribbles": {"attempts": 3, "success": 1, "past": None},
                "fouls": {"drawn": 3, "committed": 3},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 317049,
            "name": "Zé Hugo",
            "photo": "https://media.api-sports.io/football/players/317049.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 24,
                    "number": 17,
                    "position": "F",
                    "rating": "7.2",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 10, "key": 2, "accuracy": "8"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 6, "won": 4},
                "dribbles": {"attempts": 4, "success": 4, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9997,
            "name": "Jean Mota",
            "photo": "https://media.api-sports.io/football/players/9997.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 24,
                    "number": 10,
                    "position": "M",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 12, "key": 1, "accuracy": "11"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 1793,
            "name": "Luiz Adriano",
            "photo": "https://media.api-sports.io/football/players/1793.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 11,
                    "number": 12,
                    "position": "F",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 3, "key": None, "accuracy": "3"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 2, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 41227,
            "name": "Muriel",
            "photo": "https://media.api-sports.io/football/players/41227.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 22,
                    "position": "G",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 44305,
            "name": "Bruno Uvini",
            "photo": "https://media.api-sports.io/football/players/44305.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 25,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 1634,
            "name": "Cristián Zapata",
            "photo": "https://media.api-sports.io/football/players/1634.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 3,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9911,
            "name": "Lucas Esteves",
            "photo": "https://media.api-sports.io/football/players/9911.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 16,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9208,
            "name": "Willian Oliveira",
            "photo": "https://media.api-sports.io/football/players/9208.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 29,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 299089,
            "name": "Leo Naldi",
            "photo": "https://media.api-sports.io/football/players/299089.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 5,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 80171,
            "name": "Mateus Gonçalves",
            "photo": "https://media.api-sports.io/football/players/80171.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 23,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 2410,
            "name": "Weverton",
            "photo": "https://media.api-sports.io/football/players/2410.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 98,
                    "number": 21,
                    "position": "G",
                    "rating": "7.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 2, "assists": None, "saves": 5},
                "passes": {"total": 26, "key": None, "accuracy": "24"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": 0,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9917,
            "name": "Mayke",
            "photo": "https://media.api-sports.io/football/players/9917.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 98,
                    "number": 12,
                    "position": "D",
                    "rating": "7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 58, "key": 1, "accuracy": "49"},
                "tackles": {"total": 4, "blocks": None, "interceptions": 4},
                "duels": {"total": 8, "won": 7},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 2502,
            "name": "Gustavo Gómez",
            "photo": "https://media.api-sports.io/football/players/2502.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 98,
                    "number": 15,
                    "position": "D",
                    "rating": "7.2",
                    "captain": True,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 2, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 71, "key": 1, "accuracy": "59"},
                "tackles": {"total": 4, "blocks": None, "interceptions": None},
                "duels": {"total": 19, "won": 13},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9913,
            "name": "Luan",
            "photo": "https://media.api-sports.io/football/players/9913.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 58,
                    "number": 13,
                    "position": "D",
                    "rating": "6.6",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 22, "key": None, "accuracy": "20"},
                "tackles": {"total": 1, "blocks": 2, "interceptions": None},
                "duels": {"total": 3, "won": 2},
                "dribbles": {"attempts": 1, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 51466,
            "name": "Joaquín Piquerez",
            "photo": "https://media.api-sports.io/football/players/51466.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 98,
                    "number": 22,
                    "position": "D",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 2, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 26, "key": 2, "accuracy": "23"},
                "tackles": {"total": None, "blocks": None, "interceptions": 1},
                "duels": {"total": 5, "won": 4},
                "dribbles": {"attempts": 2, "success": 1, "past": None},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9932,
            "name": "Zé Rafael",
            "photo": "https://media.api-sports.io/football/players/9932.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 82,
                    "number": 8,
                    "position": "M",
                    "rating": "7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 33, "key": 2, "accuracy": "27"},
                "tackles": {"total": 2, "blocks": 1, "interceptions": 1},
                "duels": {"total": 4, "won": 4},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 195111,
            "name": "Gabriel Menino",
            "photo": "https://media.api-sports.io/football/players/195111.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 65,
                    "number": 25,
                    "position": "M",
                    "rating": "6.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 55, "key": None, "accuracy": "51"},
                "tackles": {"total": 1, "blocks": None, "interceptions": 1},
                "duels": {"total": 13, "won": 5},
                "dribbles": {"attempts": 3, "success": 1, "past": 2},
                "fouls": {"drawn": 2, "committed": 3},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 425733,
            "name": "Estêvão",
            "photo": "https://media.api-sports.io/football/players/425733.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 65,
                    "number": 41,
                    "position": "M",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 3, "on": 2},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 26, "key": 1, "accuracy": "22"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 8, "won": 3},
                "dribbles": {"attempts": 4, "success": 1, "past": None},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9920,
            "name": "Raphael Veiga",
            "photo": "https://media.api-sports.io/football/players/9920.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 98,
                    "number": 23,
                    "position": "M",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 3, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 34, "key": None, "accuracy": "29"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 3, "won": 1},
                "dribbles": {"attempts": 1, "success": 1, "past": 1},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 1,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10143,
            "name": "Rony",
            "photo": "https://media.api-sports.io/football/players/10143.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 58,
                    "number": 10,
                    "position": "M",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 2, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 10, "key": None, "accuracy": "5"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 3, "won": 2},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 2, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 377122,
            "name": "Endrick",
            "photo": "https://media.api-sports.io/football/players/377122.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 98,
                    "number": 9,
                    "position": "F",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 16, "key": None, "accuracy": "12"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 20, "won": 10},
                "dribbles": {"attempts": 6, "success": 2, "past": None},
                "fouls": {"drawn": 6, "committed": 4},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": 1,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 237103,
            "name": "Lázaro",
            "photo": "https://media.api-sports.io/football/players/237103.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 40,
                    "number": 17,
                    "position": "F",
                    "rating": "6.6",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": 1,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 9, "key": None, "accuracy": "8"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 4, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": 1},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 295513,
            "name": "José López",
            "photo": "https://media.api-sports.io/football/players/295513.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 40,
                    "number": 42,
                    "position": "F",
                    "rating": "6.6",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 4, "key": 1, "accuracy": "2"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 6, "won": 2},
                "dribbles": {"attempts": 1, "success": 1, "past": 1},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 195104,
            "name": "Richard Ríos",
            "photo": "https://media.api-sports.io/football/players/195104.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 33,
                    "number": 27,
                    "position": "M",
                    "rating": "6.6",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 1, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 404574,
            "name": "Luis Guilherme",
            "photo": "https://media.api-sports.io/football/players/404574.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 33,
                    "number": 31,
                    "position": "M",
                    "rating": "7.3",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 9, "key": 4, "accuracy": "9"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 5, "won": 3},
                "dribbles": {"attempts": 3, "success": 1, "past": None},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 290868,
            "name": "Rômulo",
            "photo": "https://media.api-sports.io/football/players/290868.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 16,
                    "number": 20,
                    "position": "M",
                    "rating": "7",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 10, "key": 2, "accuracy": "9"},
                "tackles": {"total": 1, "blocks": None, "interceptions": 1},
                "duels": {"total": 3, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10372,
            "name": "Marcelo Lomba",
            "photo": "https://media.api-sports.io/football/players/10372.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 14,
                    "position": "G",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 348896,
            "name": "Kaiky Naves",
            "photo": "https://media.api-sports.io/football/players/348896.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 34,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9916,
            "name": "Marcos Rocha",
            "photo": "https://media.api-sports.io/football/players/9916.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 2,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 279800,
            "name": "Vanderlan",
            "photo": "https://media.api-sports.io/football/players/279800.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 6,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10527,
            "name": "Caio Paulista",
            "photo": "https://media.api-sports.io/football/players/10527.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 16,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 279805,
            "name": "Fabinho",
            "photo": "https://media.api-sports.io/football/players/279805.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 35,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 306800,
            "name": "Jhon Jhon",
            "photo": "https://media.api-sports.io/football/players/306800.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 40,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10111,
            "name": "Bento",
            "photo": "https://media.api-sports.io/football/players/10111.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 98,
                    "number": 1,
                    "position": "G",
                    "rating": "8",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": 5},
                "passes": {"total": 34, "key": None, "accuracy": "19"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 2, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": 1},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": 1,
                    "scored": 0,
                    "missed": 0,
                    "saved": 1,
                },
            }
        ],
    },
    {
        "player": {
            "id": 6228,
            "name": "Leonardo Godoy",
            "photo": "https://media.api-sports.io/football/players/6228.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 58,
                    "number": 29,
                    "position": "D",
                    "rating": "6.7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 15, "key": None, "accuracy": "10"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 4, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 3},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9990,
            "name": "Kaique Rocha",
            "photo": "https://media.api-sports.io/football/players/9990.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 98,
                    "number": 4,
                    "position": "D",
                    "rating": "7.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 15, "key": None, "accuracy": "14"},
                "tackles": {"total": 2, "blocks": 2, "interceptions": 1},
                "duels": {"total": 7, "won": 2},
                "dribbles": {"attempts": None, "success": None, "past": 1},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 69142,
            "name": "Mateo Gamarra",
            "photo": "https://media.api-sports.io/football/players/69142.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 98,
                    "number": 15,
                    "position": "D",
                    "rating": "7.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 22, "key": 1, "accuracy": "17"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 7, "won": 5},
                "dribbles": {"attempts": None, "success": None, "past": 1},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 288704,
            "name": "Lucas Esquivel",
            "photo": "https://media.api-sports.io/football/players/288704.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 67,
                    "number": 37,
                    "position": "D",
                    "rating": "6.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 18, "key": None, "accuracy": "14"},
                "tackles": {"total": 2, "blocks": None, "interceptions": 1},
                "duels": {"total": 5, "won": 3},
                "dribbles": {"attempts": 1, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 2, "red": 1},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 640,
            "name": "Fernandinho",
            "photo": "https://media.api-sports.io/football/players/640.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 98,
                    "number": 5,
                    "position": "M",
                    "rating": "7.3",
                    "captain": True,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 24, "key": 2, "accuracy": "18"},
                "tackles": {"total": 3, "blocks": None, "interceptions": None},
                "duels": {"total": 16, "won": 11},
                "dribbles": {"attempts": 2, "success": 1, "past": None},
                "fouls": {"drawn": 3, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10130,
            "name": "Erick",
            "photo": "https://media.api-sports.io/football/players/10130.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 98,
                    "number": 26,
                    "position": "M",
                    "rating": "6.7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 21, "key": None, "accuracy": "14"},
                "tackles": {"total": 2, "blocks": None, "interceptions": 1},
                "duels": {"total": 8, "won": 3},
                "dribbles": {"attempts": 2, "success": 1, "past": 1},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10133,
            "name": "Nikão",
            "photo": "https://media.api-sports.io/football/players/10133.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 61,
                    "number": 11,
                    "position": "M",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 20, "key": None, "accuracy": "18"},
                "tackles": {"total": 2, "blocks": None, "interceptions": None},
                "duels": {"total": 4, "won": 2},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 152931,
            "name": "Bruno Zapelli",
            "photo": "https://media.api-sports.io/football/players/152931.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 58,
                    "number": 10,
                    "position": "M",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 19, "key": 2, "accuracy": "17"},
                "tackles": {"total": 2, "blocks": None, "interceptions": None},
                "duels": {"total": 11, "won": 5},
                "dribbles": {"attempts": 2, "success": 1, "past": 2},
                "fouls": {"drawn": 2, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 6031,
            "name": "Tomás Cuello",
            "photo": "https://media.api-sports.io/football/players/6031.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 72,
                    "number": 28,
                    "position": "M",
                    "rating": "7.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 21, "key": 2, "accuracy": "18"},
                "tackles": {"total": 1, "blocks": None, "interceptions": 2},
                "duels": {"total": 11, "won": 4},
                "dribbles": {"attempts": 4, "success": 1, "past": None},
                "fouls": {"drawn": 2, "committed": 2},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9976,
            "name": "Pablo",
            "photo": "https://media.api-sports.io/football/players/9976.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 72,
                    "number": 92,
                    "position": "F",
                    "rating": "7.6",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 2, "on": 1},
                "goals": {"total": 1, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 19, "key": 1, "accuracy": "13"},
                "tackles": {"total": None, "blocks": 1, "interceptions": None},
                "duels": {"total": 9, "won": 2},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 3},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10117,
            "name": "Madson",
            "photo": "https://media.api-sports.io/football/players/10117.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 40,
                    "number": 22,
                    "position": "D",
                    "rating": "7",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 6, "key": None, "accuracy": "3"},
                "tackles": {"total": None, "blocks": 2, "interceptions": None},
                "duels": {"total": 2, "won": 2},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 288230,
            "name": "Zé Vitor",
            "photo": "https://media.api-sports.io/football/players/288230.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 40,
                    "number": 30,
                    "position": "M",
                    "rating": "6.2",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 11, "key": None, "accuracy": "7"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 7, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": 1},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 51603,
            "name": "Agustín Canobbio",
            "photo": "https://media.api-sports.io/football/players/51603.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 37,
                    "number": 14,
                    "position": "F",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": 1,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 4, "key": 1, "accuracy": "4"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 3, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": 1},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 182015,
            "name": "Fernando",
            "photo": "https://media.api-sports.io/football/players/182015.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 26,
                    "number": 6,
                    "position": "D",
                    "rating": "6.6",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 2, "key": None, "accuracy": "1"},
                "tackles": {"total": 2, "blocks": None, "interceptions": None},
                "duels": {"total": 4, "won": 2},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 2},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9661,
            "name": "Julimar",
            "photo": "https://media.api-sports.io/football/players/9661.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 26,
                    "number": 20,
                    "position": "F",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 10, "key": None, "accuracy": "5"},
                "tackles": {"total": None, "blocks": 1, "interceptions": None},
                "duels": {"total": 4, "won": 2},
                "dribbles": {"attempts": 1, "success": 1, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 292166,
            "name": "Léo Linck",
            "photo": "https://media.api-sports.io/football/players/292166.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 24,
                    "position": "G",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 445727,
            "name": "Marcos André",
            "photo": "https://media.api-sports.io/football/players/445727.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 46,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10247,
            "name": "Gabriel Girotto",
            "photo": "https://media.api-sports.io/football/players/10247.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 3,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10067,
            "name": "Alex Santana",
            "photo": "https://media.api-sports.io/football/players/10067.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 80,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 140507,
            "name": "Felipinho",
            "photo": "https://media.api-sports.io/football/players/140507.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 23,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 16265,
            "name": "Lucas Di Yorio",
            "photo": "https://media.api-sports.io/football/players/16265.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 7,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 16669,
            "name": "Gonzalo Mastriani",
            "photo": "https://media.api-sports.io/football/players/16669.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 9,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10081,
            "name": "Rafael",
            "photo": "https://media.api-sports.io/football/players/10081.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 23,
                    "position": "G",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 1, "assists": None, "saves": 2},
                "passes": {"total": 22, "key": None, "accuracy": "16"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": 0,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9949,
            "name": "Igor Vinícius",
            "photo": "https://media.api-sports.io/football/players/9949.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 2,
                    "position": "D",
                    "rating": "7.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 53, "key": 1, "accuracy": "47"},
                "tackles": {"total": 4, "blocks": None, "interceptions": None},
                "duels": {"total": 9, "won": 7},
                "dribbles": {"attempts": 1, "success": 1, "past": 1},
                "fouls": {"drawn": 2, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 2571,
            "name": "Robert Arboleda",
            "photo": "https://media.api-sports.io/football/players/2571.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 5,
                    "position": "D",
                    "rating": "7.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": 1,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": 1, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 58, "key": None, "accuracy": "51"},
                "tackles": {"total": 1, "blocks": 1, "interceptions": 1},
                "duels": {"total": 3, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": 2},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 6083,
            "name": "Alan Franco",
            "photo": "https://media.api-sports.io/football/players/6083.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 28,
                    "position": "D",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 55, "key": None, "accuracy": "49"},
                "tackles": {"total": 1, "blocks": None, "interceptions": 1},
                "duels": {"total": 5, "won": 3},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 180921,
            "name": "Patryck",
            "photo": "https://media.api-sports.io/football/players/180921.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 89,
                    "number": 36,
                    "position": "D",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 38, "key": None, "accuracy": "36"},
                "tackles": {"total": 1, "blocks": None, "interceptions": 2},
                "duels": {"total": 9, "won": 3},
                "dribbles": {"attempts": 2, "success": 1, "past": 3},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10501,
            "name": "Alisson",
            "photo": "https://media.api-sports.io/football/players/10501.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 25,
                    "position": "M",
                    "rating": "7.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 40, "key": None, "accuracy": "37"},
                "tackles": {"total": 5, "blocks": None, "interceptions": 1},
                "duels": {"total": 13, "won": 7},
                "dribbles": {"attempts": 1, "success": 1, "past": 3},
                "fouls": {"drawn": 1, "committed": 3},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 195107,
            "name": "Damián Bobadilla",
            "photo": "https://media.api-sports.io/football/players/195107.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 61,
                    "number": 21,
                    "position": "M",
                    "rating": "8",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 2, "on": 1},
                "goals": {"total": 1, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 37, "key": 2, "accuracy": "30"},
                "tackles": {"total": 6, "blocks": None, "interceptions": None},
                "duels": {"total": 10, "won": 7},
                "dribbles": {"attempts": None, "success": None, "past": 1},
                "fouls": {"drawn": None, "committed": 2},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 41188,
            "name": "André Silva",
            "photo": "https://media.api-sports.io/football/players/41188.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 79,
                    "number": 17,
                    "position": "M",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": 1,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 20, "key": 1, "accuracy": "16"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 2, "won": 1},
                "dribbles": {"attempts": 1, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9954,
            "name": "Rodrigo Nestor",
            "photo": "https://media.api-sports.io/football/players/9954.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 61,
                    "number": 11,
                    "position": "M",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": 1,
                "shots": {"total": 2, "on": 2},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 16, "key": 1, "accuracy": "14"},
                "tackles": {"total": 2, "blocks": None, "interceptions": None},
                "duels": {"total": 8, "won": 4},
                "dribbles": {"attempts": 4, "success": 1, "past": None},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 180916,
            "name": "Juan",
            "photo": "https://media.api-sports.io/football/players/180916.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 61,
                    "number": 31,
                    "position": "M",
                    "rating": "7.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 2, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": 1, "saves": None},
                "passes": {"total": 8, "key": 1, "accuracy": "6"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 5, "won": 3},
                "dribbles": {"attempts": 1, "success": 1, "past": None},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10323,
            "name": "Luciano",
            "photo": "https://media.api-sports.io/football/players/10323.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 10,
                    "position": "F",
                    "rating": "7",
                    "captain": True,
                    "substitute": False,
                },
                "offsides": 1,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 25, "key": 2, "accuracy": "18"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 13, "won": 7},
                "dribbles": {"attempts": 1, "success": 1, "past": 2},
                "fouls": {"drawn": 2, "committed": 3},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 363689,
            "name": "Rodriguinho",
            "photo": "https://media.api-sports.io/football/players/363689.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 29,
                    "number": 18,
                    "position": "M",
                    "rating": "7.2",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 7, "key": 1, "accuracy": "7"},
                "tackles": {"total": 4, "blocks": None, "interceptions": None},
                "duels": {"total": 8, "won": 5},
                "dribbles": {"attempts": 1, "success": None, "past": 2},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 6379,
            "name": "Giuliano Galoppo",
            "photo": "https://media.api-sports.io/football/players/6379.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 29,
                    "number": 8,
                    "position": "M",
                    "rating": "7",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 5, "key": None, "accuracy": "5"},
                "tackles": {"total": None, "blocks": None, "interceptions": 3},
                "duels": {"total": 5, "won": 2},
                "dribbles": {"attempts": None, "success": None, "past": 1},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9549,
            "name": "Erick",
            "photo": "https://media.api-sports.io/football/players/9549.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 29,
                    "number": 33,
                    "position": "F",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 11, "key": 2, "accuracy": "9"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 8, "won": 4},
                "dribbles": {"attempts": 5, "success": 3, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 106510,
            "name": "Ferreira",
            "photo": "https://media.api-sports.io/football/players/106510.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 11,
                    "number": 47,
                    "position": "F",
                    "rating": "6.7",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 5, "key": None, "accuracy": "5"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 1, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 180919,
            "name": "Welington",
            "photo": "https://media.api-sports.io/football/players/180919.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 1,
                    "number": 6,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 1, "key": None, "accuracy": "1"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 30763,
            "name": "Jandrei",
            "photo": "https://media.api-sports.io/football/players/30763.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 93,
                    "position": "G",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9340,
            "name": "Sabino",
            "photo": "https://media.api-sports.io/football/players/9340.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 35,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 2440,
            "name": "Nahuel Ferraresi",
            "photo": "https://media.api-sports.io/football/players/2440.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 32,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 352994,
            "name": "Moreira",
            "photo": "https://media.api-sports.io/football/players/352994.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 30,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 143363,
            "name": "Diego Costa",
            "photo": "https://media.api-sports.io/football/players/143363.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 4,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 1909,
            "name": "Luiz Gustavo",
            "photo": "https://media.api-sports.io/football/players/1909.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 16,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 449243,
            "name": "William",
            "photo": "https://media.api-sports.io/football/players/449243.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 39,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10080,
            "name": "Fábio",
            "photo": "https://media.api-sports.io/football/players/10080.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 1,
                    "position": "G",
                    "rating": "6.9",
                    "captain": True,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 2, "assists": None, "saves": 6},
                "passes": {"total": 24, "key": None, "accuracy": "18"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": 0,
                },
            }
        ],
    },
    {
        "player": {
            "id": 311520,
            "name": "Marquinhos",
            "photo": "https://media.api-sports.io/football/players/311520.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 77,
                    "position": "D",
                    "rating": "5.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 30, "key": None, "accuracy": "24"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 14, "won": 6},
                "dribbles": {"attempts": 7, "success": 3, "past": 1},
                "fouls": {"drawn": 2, "committed": 2},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10237,
            "name": "Manoel",
            "photo": "https://media.api-sports.io/football/players/10237.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 45,
                    "number": 26,
                    "position": "D",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 16, "key": None, "accuracy": "14"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 2, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9908,
            "name": "Antônio Carlos",
            "photo": "https://media.api-sports.io/football/players/9908.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 25,
                    "position": "D",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 52, "key": 1, "accuracy": "47"},
                "tackles": {"total": 1, "blocks": 2, "interceptions": 1},
                "duels": {"total": 7, "won": 3},
                "dribbles": {"attempts": 2, "success": 1, "past": 1},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9905,
            "name": "Diogo Barbosa",
            "photo": "https://media.api-sports.io/football/players/9905.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 85,
                    "number": 6,
                    "position": "D",
                    "rating": "6.7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 29, "key": 1, "accuracy": "23"},
                "tackles": {"total": 1, "blocks": None, "interceptions": 2},
                "duels": {"total": 5, "won": 2},
                "dribbles": {"attempts": None, "success": None, "past": 1},
                "fouls": {"drawn": 1, "committed": 2},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 363323,
            "name": "Alexsander",
            "photo": "https://media.api-sports.io/football/players/363323.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 5,
                    "position": "M",
                    "rating": "7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 52, "key": None, "accuracy": "47"},
                "tackles": {"total": 4, "blocks": 1, "interceptions": 2},
                "duels": {"total": 16, "won": 8},
                "dribbles": {"attempts": 4, "success": 3, "past": 2},
                "fouls": {"drawn": 1, "committed": 2},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 280245,
            "name": "Matheus Martinelli",
            "photo": "https://media.api-sports.io/football/players/280245.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 45,
                    "number": 8,
                    "position": "M",
                    "rating": "6.7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 36, "key": None, "accuracy": "32"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 3, "won": 2},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 13708,
            "name": "Jhon Arias",
            "photo": "https://media.api-sports.io/football/players/13708.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 21,
                    "position": "M",
                    "rating": "7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 2, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 31, "key": None, "accuracy": "31"},
                "tackles": {"total": 2, "blocks": None, "interceptions": 1},
                "duels": {"total": 12, "won": 7},
                "dribbles": {"attempts": 3, "success": 1, "past": 1},
                "fouls": {"drawn": 3, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 50532,
            "name": "Lima",
            "photo": "https://media.api-sports.io/football/players/50532.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 45,
                    "position": "M",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 50, "key": None, "accuracy": "43"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 7, "won": 4},
                "dribbles": {"attempts": 1, "success": 1, "past": None},
                "fouls": {"drawn": 2, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 16847,
            "name": "Keno",
            "photo": "https://media.api-sports.io/football/players/16847.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 79,
                    "number": 11,
                    "position": "M",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 2, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 23, "key": 1, "accuracy": "17"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 5, "won": 2},
                "dribbles": {"attempts": 1, "success": 1, "past": 1},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 414358,
            "name": "Kauã Elias",
            "photo": "https://media.api-sports.io/football/players/414358.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 79,
                    "number": 19,
                    "position": "F",
                    "rating": "6.5",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 18, "key": 1, "accuracy": "16"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 11, "won": 2},
                "dribbles": {"attempts": 5, "success": 1, "past": 1},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 306581,
            "name": "Felipe Andrade",
            "photo": "https://media.api-sports.io/football/players/306581.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 45,
                    "number": 13,
                    "position": "D",
                    "rating": "6.5",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 25, "key": None, "accuracy": "23"},
                "tackles": {"total": None, "blocks": None, "interceptions": 1},
                "duels": {"total": 7, "won": 3},
                "dribbles": {"attempts": 2, "success": 1, "past": None},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 297522,
            "name": "John Kennedy",
            "photo": "https://media.api-sports.io/football/players/297522.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 45,
                    "number": 9,
                    "position": "F",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 12, "key": None, "accuracy": "9"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 6, "won": 2},
                "dribbles": {"attempts": 5, "success": 2, "past": 1},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9874,
            "name": "Guga",
            "photo": "https://media.api-sports.io/football/players/9874.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 11,
                    "number": 23,
                    "position": "D",
                    "rating": "6.5",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 9, "key": 1, "accuracy": "9"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 1, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9891,
            "name": "David Terans",
            "photo": "https://media.api-sports.io/football/players/9891.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 11,
                    "number": 80,
                    "position": "M",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 6, "key": None, "accuracy": "5"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 3, "won": 3},
                "dribbles": {"attempts": 1, "success": 1, "past": None},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 743,
            "name": "Marcelo",
            "photo": "https://media.api-sports.io/football/players/743.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 13,
                    "number": 12,
                    "position": "D",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 8, "key": None, "accuracy": "6"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10408,
            "name": "Felipe Alves",
            "photo": "https://media.api-sports.io/football/players/10408.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 27,
                    "position": "G",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 133194,
            "name": "Calegari",
            "photo": "https://media.api-sports.io/football/players/133194.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 31,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9929,
            "name": "Felipe Melo",
            "photo": "https://media.api-sports.io/football/players/9929.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 30,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 306580,
            "name": "Arthur Wenderroscky",
            "photo": "https://media.api-sports.io/football/players/306580.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 28,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 303136,
            "name": "Jan Franc Lucumi",
            "photo": "https://media.api-sports.io/football/players/303136.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 17,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 404536,
            "name": "Isaac",
            "photo": "https://media.api-sports.io/football/players/404536.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 32,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 13523,
            "name": "Germán Cano",
            "photo": "https://media.api-sports.io/football/players/13523.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 14,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10186,
            "name": "João Ricardo",
            "photo": "https://media.api-sports.io/football/players/10186.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 99,
                    "number": 1,
                    "position": "G",
                    "rating": "7.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 1, "assists": None, "saves": 4},
                "passes": {"total": 18, "key": None, "accuracy": "15"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 1, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": 0,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10413,
            "name": "Tinga",
            "photo": "https://media.api-sports.io/football/players/10413.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 99,
                    "number": 2,
                    "position": "D",
                    "rating": "7",
                    "captain": True,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 37, "key": 1, "accuracy": "32"},
                "tackles": {"total": 3, "blocks": None, "interceptions": 1},
                "duels": {"total": 13, "won": 6},
                "dribbles": {"attempts": 1, "success": None, "past": 1},
                "fouls": {"drawn": None, "committed": 2},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 11365,
            "name": "Benjamin Kuscevic",
            "photo": "https://media.api-sports.io/football/players/11365.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 99,
                    "number": 13,
                    "position": "D",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": 1,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 41, "key": None, "accuracy": "37"},
                "tackles": {"total": 1, "blocks": 1, "interceptions": 1},
                "duels": {"total": 7, "won": 3},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 50166,
            "name": "Titi",
            "photo": "https://media.api-sports.io/football/players/50166.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 99,
                    "number": 4,
                    "position": "D",
                    "rating": "6",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 39, "key": None, "accuracy": "35"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 8, "won": 2},
                "dribbles": {"attempts": None, "success": None, "past": 1},
                "fouls": {"drawn": 1, "committed": 3},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9989,
            "name": "Felipe Jonatan",
            "photo": "https://media.api-sports.io/football/players/9989.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 99,
                    "number": 36,
                    "position": "D",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 43, "key": None, "accuracy": "33"},
                "tackles": {"total": 1, "blocks": None, "interceptions": 1},
                "duels": {"total": 6, "won": 4},
                "dribbles": {"attempts": 1, "success": 1, "past": 1},
                "fouls": {"drawn": 2, "committed": 2},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 266267,
            "name": "Hércules",
            "photo": "https://media.api-sports.io/football/players/266267.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 83,
                    "number": 35,
                    "position": "M",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 36, "key": None, "accuracy": "29"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 10, "won": 4},
                "dribbles": {"attempts": 1, "success": 1, "past": 1},
                "fouls": {"drawn": 1, "committed": 3},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10138,
            "name": "Matheus Rossetto",
            "photo": "https://media.api-sports.io/football/players/10138.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 99,
                    "number": 16,
                    "position": "M",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 50, "key": 1, "accuracy": "43"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 6, "won": 3},
                "dribbles": {"attempts": 1, "success": None, "past": 1},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10506,
            "name": "Marinho",
            "photo": "https://media.api-sports.io/football/players/10506.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 64,
                    "number": 11,
                    "position": "M",
                    "rating": "7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": 3,
                "shots": {"total": 2, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 20, "key": 1, "accuracy": "14"},
                "tackles": {"total": 3, "blocks": None, "interceptions": None},
                "duels": {"total": 13, "won": 6},
                "dribbles": {"attempts": 4, "success": 1, "past": 2},
                "fouls": {"drawn": 2, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 6242,
            "name": "Tomás Pochettino",
            "photo": "https://media.api-sports.io/football/players/6242.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 72,
                    "number": 7,
                    "position": "M",
                    "rating": "7.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 2, "on": 1},
                "goals": {"total": 1, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 20, "key": 1, "accuracy": "16"},
                "tackles": {"total": 3, "blocks": None, "interceptions": None},
                "duels": {"total": 6, "won": 4},
                "dribbles": {"attempts": 1, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 53966,
            "name": "Breno Lopes",
            "photo": "https://media.api-sports.io/football/players/53966.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 72,
                    "number": 26,
                    "position": "M",
                    "rating": "7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": 1, "saves": None},
                "passes": {"total": 13, "key": 1, "accuracy": "9"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 21, "won": 12},
                "dribbles": {"attempts": 4, "success": 3, "past": 1},
                "fouls": {"drawn": 6, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9726,
            "name": "Renato Kayzer",
            "photo": "https://media.api-sports.io/football/players/9726.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 64,
                    "number": 79,
                    "position": "F",
                    "rating": "6",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 9, "key": None, "accuracy": "4"},
                "tackles": {"total": 2, "blocks": None, "interceptions": None},
                "duels": {"total": 9, "won": 4},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10581,
            "name": "Yago Pikachu",
            "photo": "https://media.api-sports.io/football/players/10581.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 35,
                    "number": 22,
                    "position": "M",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 7, "key": 1, "accuracy": "5"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 3, "won": 3},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 2, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 6326,
            "name": "Juan Martín Lucero",
            "photo": "https://media.api-sports.io/football/players/6326.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 35,
                    "number": 9,
                    "position": "F",
                    "rating": "6.6",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": 1,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 1, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 1, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 6121,
            "name": "Imanol Machuca",
            "photo": "https://media.api-sports.io/football/players/6121.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 27,
                    "number": 39,
                    "position": "F",
                    "rating": "6.5",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 6, "key": None, "accuracy": "4"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 4, "won": 1},
                "dribbles": {"attempts": 1, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 153454,
            "name": "Moisés",
            "photo": "https://media.api-sports.io/football/players/153454.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 27,
                    "number": 21,
                    "position": "F",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 5, "key": None, "accuracy": "2"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 4, "won": 3},
                "dribbles": {"attempts": 1, "success": 1, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9882,
            "name": "Zé Welison",
            "photo": "https://media.api-sports.io/football/players/9882.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 16,
                    "number": 17,
                    "position": "M",
                    "rating": "6.6",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 10, "key": None, "accuracy": "9"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 1, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10112,
            "name": "Santos",
            "photo": "https://media.api-sports.io/football/players/10112.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 23,
                    "position": "G",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10192,
            "name": "Bruno Pacheco",
            "photo": "https://media.api-sports.io/football/players/10192.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 6,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 6078,
            "name": "Emanuel Brítez",
            "photo": "https://media.api-sports.io/football/players/6078.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 19,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10381,
            "name": "Dudu",
            "photo": "https://media.api-sports.io/football/players/10381.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 20,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 16637,
            "name": "Emmanuel Martínez",
            "photo": "https://media.api-sports.io/football/players/16637.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 8,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 311785,
            "name": "Kervin Andrade",
            "photo": "https://media.api-sports.io/football/players/311785.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 77,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 396358,
            "name": "Kauan Rodrigues",
            "photo": "https://media.api-sports.io/football/players/396358.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 37,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 70366,
            "name": "John Victor",
            "photo": "https://media.api-sports.io/football/players/70366.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 99,
                    "number": 12,
                    "position": "G",
                    "rating": "6.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 1, "assists": None, "saves": 2},
                "passes": {"total": 48, "key": None, "accuracy": "36"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": 0,
                },
            }
        ],
    },
    {
        "player": {
            "id": 297687,
            "name": "Mateo Ponte",
            "photo": "https://media.api-sports.io/football/players/297687.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 72,
                    "number": 4,
                    "position": "D",
                    "rating": "6.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 19, "key": None, "accuracy": "16"},
                "tackles": {"total": 3, "blocks": None, "interceptions": None},
                "duels": {"total": 13, "won": 5},
                "dribbles": {"attempts": 1, "success": 1, "past": 3},
                "fouls": {"drawn": None, "committed": 3},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 1845,
            "name": "Bastos",
            "photo": "https://media.api-sports.io/football/players/1845.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 99,
                    "number": 15,
                    "position": "D",
                    "rating": "6.6",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 67, "key": None, "accuracy": "64"},
                "tackles": {"total": None, "blocks": 1, "interceptions": None},
                "duels": {"total": 2, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": 1},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 5933,
            "name": "Alexander Barboza",
            "photo": "https://media.api-sports.io/football/players/5933.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 99,
                    "number": 20,
                    "position": "D",
                    "rating": "7.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 2, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 67, "key": None, "accuracy": "56"},
                "tackles": {"total": None, "blocks": 1, "interceptions": None},
                "duels": {"total": 4, "won": 2},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 353034,
            "name": "Cuiabano",
            "photo": "https://media.api-sports.io/football/players/353034.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 99,
                    "number": 66,
                    "position": "D",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 30, "key": None, "accuracy": "26"},
                "tackles": {"total": 3, "blocks": None, "interceptions": 1},
                "duels": {"total": 13, "won": 7},
                "dribbles": {"attempts": 1, "success": 1, "past": None},
                "fouls": {"drawn": 2, "committed": 3},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 22167,
            "name": "Danilo Barbosa",
            "photo": "https://media.api-sports.io/football/players/22167.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 64,
                    "number": 5,
                    "position": "M",
                    "rating": "7.5",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": 1, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 42, "key": None, "accuracy": "36"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 9, "won": 6},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": 3},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10031,
            "name": "Gregore",
            "photo": "https://media.api-sports.io/football/players/10031.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 99,
                    "number": 26,
                    "position": "M",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 66, "key": 1, "accuracy": "60"},
                "tackles": {"total": 5, "blocks": None, "interceptions": None},
                "duels": {"total": 17, "won": 8},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 3},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 2515,
            "name": "Óscar Romero",
            "photo": "https://media.api-sports.io/football/players/2515.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 57,
                    "number": 70,
                    "position": "M",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": 1, "saves": None},
                "passes": {"total": 28, "key": 1, "accuracy": "18"},
                "tackles": {"total": 2, "blocks": None, "interceptions": 1},
                "duels": {"total": 7, "won": 4},
                "dribbles": {"attempts": 1, "success": 1, "past": None},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9958,
            "name": "Tchê Tchê",
            "photo": "https://media.api-sports.io/football/players/9958.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 99,
                    "number": 6,
                    "position": "M",
                    "rating": "6.7",
                    "captain": True,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 44, "key": None, "accuracy": "40"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 5, "won": 2},
                "dribbles": {"attempts": 1, "success": 1, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 238391,
            "name": "Jeffinho",
            "photo": "https://media.api-sports.io/football/players/238391.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 57,
                    "number": 47,
                    "position": "M",
                    "rating": "6.6",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 15, "key": None, "accuracy": "11"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 13, "won": 6},
                "dribbles": {"attempts": 3, "success": 2, "past": 1},
                "fouls": {"drawn": 2, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 265785,
            "name": "Luiz Henrique",
            "photo": "https://media.api-sports.io/football/players/265785.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 57,
                    "number": 7,
                    "position": "F",
                    "rating": "6.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 6, "key": None, "accuracy": "3"},
                "tackles": {"total": None, "blocks": None, "interceptions": 1},
                "duels": {"total": 12, "won": 5},
                "dribbles": {"attempts": 3, "success": 1, "past": 1},
                "fouls": {"drawn": 2, "committed": 2},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 269374,
            "name": "Diego Hernández",
            "photo": "https://media.api-sports.io/football/players/269374.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 42,
                    "number": 77,
                    "position": "F",
                    "rating": "6.6",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 4, "key": None, "accuracy": "4"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 4, "won": 2},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 2, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 51214,
            "name": "Jefferson Savarino",
            "photo": "https://media.api-sports.io/football/players/51214.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 42,
                    "number": 10,
                    "position": "F",
                    "rating": "7.2",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 17, "key": 2, "accuracy": "14"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 2, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10432,
            "name": "Júnior Santos",
            "photo": "https://media.api-sports.io/football/players/10432.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 42,
                    "number": 11,
                    "position": "F",
                    "rating": "7.2",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": 4, "on": 2},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 11, "key": 1, "accuracy": "10"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 4, "won": 4},
                "dribbles": {"attempts": 1, "success": 1, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9218,
            "name": "Marlon Freitas",
            "photo": "https://media.api-sports.io/football/players/9218.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 35,
                    "number": 17,
                    "position": "M",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 15, "key": 1, "accuracy": "14"},
                "tackles": {"total": None, "blocks": None, "interceptions": 1},
                "duels": {"total": 2, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 47257,
            "name": "Damián Suárez",
            "photo": "https://media.api-sports.io/football/players/47257.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 27,
                    "number": 22,
                    "position": "D",
                    "rating": "6.6",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 8, "key": 1, "accuracy": "6"},
                "tackles": {"total": 2, "blocks": None, "interceptions": None},
                "duels": {"total": 5, "won": 2},
                "dribbles": {"attempts": None, "success": None, "past": 1},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 2497,
            "name": "Gatito Fernández",
            "photo": "https://media.api-sports.io/football/players/2497.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 1,
                    "position": "G",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10120,
            "name": "Lucas Halter",
            "photo": "https://media.api-sports.io/football/players/10120.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 3,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 197317,
            "name": "Hugo",
            "photo": "https://media.api-sports.io/football/players/197317.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 16,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 195109,
            "name": "Patrick de Paula",
            "photo": "https://media.api-sports.io/football/players/195109.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 8,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 103121,
            "name": "Jacob Montes",
            "photo": "https://media.api-sports.io/football/players/103121.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 32,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 460177,
            "name": "Yarlen",
            "photo": "https://media.api-sports.io/football/players/460177.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 67,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 415631,
            "name": "Fabiano",
            "photo": "https://media.api-sports.io/football/players/415631.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 79,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9512,
            "name": "Ronaldo",
            "photo": "https://media.api-sports.io/football/players/9512.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 1,
                    "position": "G",
                    "rating": "6.9",
                    "captain": True,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 1, "assists": None, "saves": 3},
                "passes": {"total": 23, "key": None, "accuracy": "16"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 1, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": 0,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9468,
            "name": "Bruno Tubarão",
            "photo": "https://media.api-sports.io/football/players/9468.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 2,
                    "position": "D",
                    "rating": "6.7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 40, "key": 1, "accuracy": "32"},
                "tackles": {"total": 2, "blocks": None, "interceptions": 2},
                "duels": {"total": 8, "won": 4},
                "dribbles": {"attempts": 2, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 196887,
            "name": "Adriano Martins",
            "photo": "https://media.api-sports.io/football/players/196887.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 3,
                    "position": "D",
                    "rating": "7.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 46, "key": 1, "accuracy": "35"},
                "tackles": {"total": None, "blocks": 2, "interceptions": 1},
                "duels": {"total": 1, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": 1},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 297893,
            "name": "Alix Vinicius",
            "photo": "https://media.api-sports.io/football/players/297893.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 4,
                    "position": "D",
                    "rating": "8",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 3, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 50, "key": 2, "accuracy": "46"},
                "tackles": {"total": 4, "blocks": 1, "interceptions": None},
                "duels": {"total": 12, "won": 8},
                "dribbles": {"attempts": 1, "success": 1, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9675,
            "name": "Guilherme Romão",
            "photo": "https://media.api-sports.io/football/players/9675.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 6,
                    "position": "D",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 48, "key": None, "accuracy": "37"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 5, "won": 3},
                "dribbles": {"attempts": 3, "success": 1, "past": None},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9460,
            "name": "Gabriel Baralhas",
            "photo": "https://media.api-sports.io/football/players/9460.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 8,
                    "position": "M",
                    "rating": "7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 31, "key": None, "accuracy": "23"},
                "tackles": {"total": 4, "blocks": 2, "interceptions": 2},
                "duels": {"total": 14, "won": 5},
                "dribbles": {"attempts": None, "success": None, "past": 3},
                "fouls": {"drawn": None, "committed": 2},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9952,
            "name": "Lucas Kal",
            "photo": "https://media.api-sports.io/football/players/9952.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 83,
                    "number": 5,
                    "position": "M",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 28, "key": None, "accuracy": "23"},
                "tackles": {"total": 1, "blocks": None, "interceptions": 1},
                "duels": {"total": 5, "won": 4},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 2, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 199324,
            "name": "Gabriel Barros",
            "photo": "https://media.api-sports.io/football/players/199324.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 63,
                    "number": 7,
                    "position": "M",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 16, "key": None, "accuracy": "13"},
                "tackles": {"total": 2, "blocks": None, "interceptions": 1},
                "duels": {"total": 11, "won": 6},
                "dribbles": {"attempts": 2, "success": 2, "past": 3},
                "fouls": {"drawn": 1, "committed": 2},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10025,
            "name": "Shaylon",
            "photo": "https://media.api-sports.io/football/players/10025.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 72,
                    "number": 10,
                    "position": "M",
                    "rating": "7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 25, "key": 3, "accuracy": "17"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 5, "won": 1},
                "dribbles": {"attempts": 1, "success": None, "past": 1},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10073,
            "name": "Luiz Fernando",
            "photo": "https://media.api-sports.io/football/players/10073.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 11,
                    "position": "M",
                    "rating": "6.5",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 3, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 17, "key": None, "accuracy": "10"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 17, "won": 5},
                "dribbles": {"attempts": 4, "success": 1, "past": 2},
                "fouls": {"drawn": 2, "committed": 3},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 157361,
            "name": "Derek Freitas",
            "photo": "https://media.api-sports.io/football/players/157361.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 72,
                    "number": 9,
                    "position": "F",
                    "rating": "7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 3, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 17, "key": 3, "accuracy": "14"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 9, "won": 3},
                "dribbles": {"attempts": 1, "success": None, "past": 1},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10328,
            "name": "Yony González",
            "photo": "https://media.api-sports.io/football/players/10328.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 27,
                    "number": 19,
                    "position": "F",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 8, "key": 1, "accuracy": "7"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 3, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": 2},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10320,
            "name": "Danielzinho",
            "photo": "https://media.api-sports.io/football/players/10320.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 18,
                    "number": 17,
                    "position": "M",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 18, "key": None, "accuracy": "14"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 2, "won": 1},
                "dribbles": {"attempts": 1, "success": 1, "past": 1},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 354077,
            "name": "Emiliano Rodriguez",
            "photo": "https://media.api-sports.io/football/players/354077.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 18,
                    "number": 21,
                    "position": "F",
                    "rating": "6.5",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 4, "key": 1, "accuracy": "3"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 4, "won": None},
                "dribbles": {"attempts": 1, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10261,
            "name": "Vágner Love",
            "photo": "https://media.api-sports.io/football/players/10261.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 14,
                    "number": 20,
                    "position": "F",
                    "rating": "6.7",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 2, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 293555,
            "name": "Pedro Rangel",
            "photo": "https://media.api-sports.io/football/players/293555.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 12,
                    "position": "G",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 32948,
            "name": "Maguinho",
            "photo": "https://media.api-sports.io/football/players/32948.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 13,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 41147,
            "name": "Pedro Henrique",
            "photo": "https://media.api-sports.io/football/players/41147.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 15,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 454813,
            "name": "Luiz Gustavo",
            "photo": "https://media.api-sports.io/football/players/454813.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 14,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 13467,
            "name": "Yeferson Rodallega",
            "photo": "https://media.api-sports.io/football/players/13467.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 16,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 288763,
            "name": "Alejo Cruz",
            "photo": "https://media.api-sports.io/football/players/288763.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 18,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 454454,
            "name": "Max",
            "photo": "https://media.api-sports.io/football/players/454454.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 22,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 80173,
            "name": "Anderson",
            "photo": "https://media.api-sports.io/football/players/80173.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 98,
                    "position": "G",
                    "rating": "7.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": 5},
                "passes": {"total": 25, "key": None, "accuracy": "18"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": 0,
                },
            }
        ],
    },
    {
        "player": {
            "id": 25398,
            "name": "William",
            "photo": "https://media.api-sports.io/football/players/25398.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 12,
                    "position": "D",
                    "rating": "8.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 40, "key": 2, "accuracy": "31"},
                "tackles": {"total": 5, "blocks": 1, "interceptions": 2},
                "duels": {"total": 14, "won": 9},
                "dribbles": {"attempts": 2, "success": 2, "past": 2},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10114,
            "name": "Zé Ivaldo",
            "photo": "https://media.api-sports.io/football/players/10114.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 5,
                    "position": "D",
                    "rating": "8.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 3, "on": 2},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 41, "key": None, "accuracy": "33"},
                "tackles": {"total": 2, "blocks": 1, "interceptions": 1},
                "duels": {"total": 10, "won": 9},
                "dribbles": {"attempts": 1, "success": 1, "past": None},
                "fouls": {"drawn": 2, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 54866,
            "name": "João Marcelo",
            "photo": "https://media.api-sports.io/football/players/54866.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 43,
                    "position": "D",
                    "rating": "7.7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": 1, "saves": None},
                "passes": {"total": 40, "key": 1, "accuracy": "35"},
                "tackles": {"total": None, "blocks": 3, "interceptions": None},
                "duels": {"total": 7, "won": 2},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10309,
            "name": "Marlon",
            "photo": "https://media.api-sports.io/football/players/10309.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 3,
                    "position": "D",
                    "rating": "7.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 49, "key": 1, "accuracy": "40"},
                "tackles": {"total": 2, "blocks": 1, "interceptions": 1},
                "duels": {"total": 9, "won": 5},
                "dribbles": {"attempts": 1, "success": 1, "past": 2},
                "fouls": {"drawn": 1, "committed": 2},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10102,
            "name": "Lucas Silva",
            "photo": "https://media.api-sports.io/football/players/10102.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 89,
                    "number": 16,
                    "position": "M",
                    "rating": "7",
                    "captain": True,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 41, "key": 2, "accuracy": "34"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 3, "won": 2},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10100,
            "name": "Lucas Romero",
            "photo": "https://media.api-sports.io/football/players/10100.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 29,
                    "position": "M",
                    "rating": "7.5",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 66, "key": None, "accuracy": "56"},
                "tackles": {"total": None, "blocks": None, "interceptions": 1},
                "duels": {"total": 14, "won": 11},
                "dribbles": {"attempts": 4, "success": 3, "past": None},
                "fouls": {"drawn": 2, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 6052,
            "name": "Álvaro Barreal",
            "photo": "https://media.api-sports.io/football/players/6052.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 66,
                    "number": 21,
                    "position": "M",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 29, "key": None, "accuracy": "20"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 7, "won": 2},
                "dribbles": {"attempts": 3, "success": 2, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 13063,
            "name": "Rafael Silva",
            "photo": "https://media.api-sports.io/football/players/13063.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 67,
                    "number": 8,
                    "position": "F",
                    "rating": "7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": 1,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 14, "key": 1, "accuracy": "11"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 6, "won": 4},
                "dribbles": {"attempts": 2, "success": 2, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 25618,
            "name": "Matheus Pereira",
            "photo": "https://media.api-sports.io/football/players/25618.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 89,
                    "number": 10,
                    "position": "F",
                    "rating": "7.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": 1, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 46, "key": 3, "accuracy": "34"},
                "tackles": {"total": 1, "blocks": None, "interceptions": 1},
                "duels": {"total": 12, "won": 6},
                "dribbles": {"attempts": 1, "success": None, "past": None},
                "fouls": {"drawn": 3, "committed": 3},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10006,
            "name": "Arthur Gomes",
            "photo": "https://media.api-sports.io/football/players/10006.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 79,
                    "number": 11,
                    "position": "F",
                    "rating": "7",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": 1,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 26, "key": None, "accuracy": "21"},
                "tackles": {"total": 2, "blocks": None, "interceptions": None},
                "duels": {"total": 9, "won": 5},
                "dribbles": {"attempts": 3, "success": 1, "past": None},
                "fouls": {"drawn": 2, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 456213,
            "name": "Vitor Hugo Amorim de Assis",
            "photo": "https://media.api-sports.io/football/players/456213.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 24,
                    "number": 22,
                    "position": "M",
                    "rating": "6.6",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 7, "key": None, "accuracy": "6"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 2, "won": 2},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9896,
            "name": "Rafael Elias",
            "photo": "https://media.api-sports.io/football/players/9896.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 23,
                    "number": 19,
                    "position": "F",
                    "rating": "6.6",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 8, "key": None, "accuracy": "7"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 4, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": 2},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 180235,
            "name": "Gabriel Veron",
            "photo": "https://media.api-sports.io/football/players/180235.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 11,
                    "number": 30,
                    "position": "F",
                    "rating": "6.7",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 6, "key": 1, "accuracy": "5"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 1, "won": None},
                "dribbles": {"attempts": 1, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10249,
            "name": "Ramiro",
            "photo": "https://media.api-sports.io/football/players/10249.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 1,
                    "number": 17,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 3, "key": None, "accuracy": "1"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 16776,
            "name": "José Cifuentes",
            "photo": "https://media.api-sports.io/football/players/16776.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 1,
                    "number": 18,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": 1, "key": None, "accuracy": "1"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 1, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 309634,
            "name": "Gabriel Grando",
            "photo": "https://media.api-sports.io/football/players/309634.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 81,
                    "position": "G",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 309792,
            "name": "Kaiki",
            "photo": "https://media.api-sports.io/football/players/309792.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 6,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 41299,
            "name": "Neris",
            "photo": "https://media.api-sports.io/football/players/41299.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 27,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 2486,
            "name": "Helibelton Palacios",
            "photo": "https://media.api-sports.io/football/players/2486.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 28,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 6268,
            "name": "Lucas Villalba",
            "photo": "https://media.api-sports.io/football/players/6268.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 25,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 422779,
            "name": "Robert",
            "photo": "https://media.api-sports.io/football/players/422779.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 80,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 359600,
            "name": "Jhosefer",
            "photo": "https://media.api-sports.io/football/players/359600.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 20,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9303,
            "name": "Gustavo",
            "photo": "https://media.api-sports.io/football/players/9303.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 1,
                    "position": "G",
                    "rating": "5.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 5, "assists": 0, "saves": 2},
                "passes": {"total": 15, "key": None, "accuracy": "14"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": 0,
                },
            }
        ],
    },
    {
        "player": {
            "id": 135136,
            "name": "Claudinho",
            "photo": "https://media.api-sports.io/football/players/135136.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 44,
                    "number": 27,
                    "position": "D",
                    "rating": "6.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": 29, "key": 2, "accuracy": "22"},
                "tackles": {"total": 1, "blocks": None, "interceptions": 1},
                "duels": {"total": 4, "won": 1},
                "dribbles": {"attempts": 1, "success": None, "past": 1},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9484,
            "name": "Rodrigo Fagundes",
            "photo": "https://media.api-sports.io/football/players/9484.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 3,
                    "position": "D",
                    "rating": "6.9",
                    "captain": True,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": 71, "key": None, "accuracy": "64"},
                "tackles": {"total": 1, "blocks": 2, "interceptions": 4},
                "duels": {"total": 9, "won": 6},
                "dribbles": {"attempts": 1, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 19293,
            "name": "Tobias Figueiredo",
            "photo": "https://media.api-sports.io/football/players/19293.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 29,
                    "position": "D",
                    "rating": "7.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": 1, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": 71, "key": None, "accuracy": "65"},
                "tackles": {"total": 4, "blocks": None, "interceptions": 1},
                "duels": {"total": 9, "won": 8},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10340,
            "name": "Marcelo Hermes",
            "photo": "https://media.api-sports.io/football/players/10340.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 66,
                    "number": 22,
                    "position": "D",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": 1, "saves": None},
                "passes": {"total": 39, "key": 3, "accuracy": "29"},
                "tackles": {"total": 1, "blocks": None, "interceptions": 2},
                "duels": {"total": 7, "won": 3},
                "dribbles": {"attempts": None, "success": None, "past": 2},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9849,
            "name": "Matheusinho",
            "photo": "https://media.api-sports.io/football/players/9849.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 17,
                    "position": "M",
                    "rating": "7.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 2, "on": 1},
                "goals": {"total": 1, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": 39, "key": 4, "accuracy": "31"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 5, "won": 2},
                "dribbles": {"attempts": 1, "success": None, "past": None},
                "fouls": {"drawn": 2, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9212,
            "name": "Higor Meritão",
            "photo": "https://media.api-sports.io/football/players/9212.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 44,
                    "number": 5,
                    "position": "M",
                    "rating": "5.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": 30, "key": None, "accuracy": "27"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 2, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9461,
            "name": "Barreto",
            "photo": "https://media.api-sports.io/football/players/9461.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 86,
                    "number": 88,
                    "position": "M",
                    "rating": "7.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": 49, "key": 1, "accuracy": "45"},
                "tackles": {"total": 2, "blocks": None, "interceptions": None},
                "duels": {"total": 9, "won": 6},
                "dribbles": {"attempts": 1, "success": 1, "past": 1},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10096,
            "name": "Marquinhos Gabriel",
            "photo": "https://media.api-sports.io/football/players/10096.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 44,
                    "number": 10,
                    "position": "M",
                    "rating": "6.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": 1,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": 19, "key": None, "accuracy": "16"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 6, "won": 1},
                "dribbles": {"attempts": 2, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 12795,
            "name": "Éder",
            "photo": "https://media.api-sports.io/football/players/12795.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 23,
                    "position": "F",
                    "rating": "7.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": 1,
                "shots": {"total": 3, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": 32, "key": 3, "accuracy": "29"},
                "tackles": {"total": 1, "blocks": None, "interceptions": None},
                "duels": {"total": 8, "won": 4},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 2, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 1432,
            "name": "Yannick Bolasie",
            "photo": "https://media.api-sports.io/football/players/1432.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 11,
                    "position": "F",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": 3,
                "shots": {"total": 7, "on": 3},
                "goals": {"total": None, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": 17, "key": 1, "accuracy": "11"},
                "tackles": {"total": None, "blocks": None, "interceptions": 1},
                "duels": {"total": 7, "won": 3},
                "dribbles": {"attempts": 1, "success": None, "past": None},
                "fouls": {"drawn": 2, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9312,
            "name": "Jonathan",
            "photo": "https://media.api-sports.io/football/players/9312.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 46,
                    "number": 13,
                    "position": "D",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": 1, "saves": None},
                "passes": {"total": 32, "key": 2, "accuracy": "29"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 4, "won": 1},
                "dribbles": {"attempts": 1, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 64363,
            "name": "Ronald",
            "photo": "https://media.api-sports.io/football/players/64363.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 46,
                    "number": 6,
                    "position": "M",
                    "rating": "7.3",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": 29, "key": 1, "accuracy": "27"},
                "tackles": {"total": 4, "blocks": None, "interceptions": None},
                "duels": {"total": 10, "won": 8},
                "dribbles": {"attempts": 1, "success": 1, "past": None},
                "fouls": {"drawn": 3, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10039,
            "name": "Arthur Caíke",
            "photo": "https://media.api-sports.io/football/players/10039.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 46,
                    "number": 45,
                    "position": "F",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": 10, "key": None, "accuracy": "8"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 9, "won": 3},
                "dribbles": {"attempts": None, "success": None, "past": 1},
                "fouls": {"drawn": 2, "committed": 3},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 2424,
            "name": "Miguel Trauco",
            "photo": "https://media.api-sports.io/football/players/2424.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 13,
                    "number": 14,
                    "position": "D",
                    "rating": "5.7",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": 10, "key": None, "accuracy": "8"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 3, "won": 2},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 1},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 277169,
            "name": "Newton",
            "photo": "https://media.api-sports.io/football/players/277169.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 12,
                    "number": 8,
                    "position": "M",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": 11, "key": None, "accuracy": "9"},
                "tackles": {"total": None, "blocks": None, "interceptions": 1},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9410,
            "name": "Alisson",
            "photo": "https://media.api-sports.io/football/players/9410.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 25,
                    "position": "G",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9347,
            "name": "Walisson Maia",
            "photo": "https://media.api-sports.io/football/players/9347.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 33,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 371579,
            "name": "Eliédson",
            "photo": "https://media.api-sports.io/football/players/371579.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 15,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 311795,
            "name": "Baltasar Barcia",
            "photo": "https://media.api-sports.io/football/players/311795.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 30,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 50243,
            "name": "Allano",
            "photo": "https://media.api-sports.io/football/players/50243.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 2,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 197073,
            "name": "Eduardo Melo",
            "photo": "https://media.api-sports.io/football/players/197073.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 99,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 197074,
            "name": "João Carlos",
            "photo": "https://media.api-sports.io/football/players/197074.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 21,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10226,
            "name": "Walter",
            "photo": "https://media.api-sports.io/football/players/10226.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 1,
                    "position": "G",
                    "rating": "7.5",
                    "captain": True,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 2, "assists": 0, "saves": 6},
                "passes": {"total": 23, "key": None, "accuracy": "13"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 1, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": 0,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9709,
            "name": "Matheus Alexandre",
            "photo": "https://media.api-sports.io/football/players/9709.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 2,
                    "position": "D",
                    "rating": "6.5",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": 28, "key": None, "accuracy": "20"},
                "tackles": {"total": 2, "blocks": None, "interceptions": 2},
                "duels": {"total": 7, "won": 4},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10232,
            "name": "Marllon",
            "photo": "https://media.api-sports.io/football/players/10232.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 4,
                    "position": "D",
                    "rating": "6.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": 26, "key": None, "accuracy": "22"},
                "tackles": {"total": None, "blocks": 1, "interceptions": 1},
                "duels": {"total": 6, "won": 2},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 3},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 30925,
            "name": "Alan Empereur",
            "photo": "https://media.api-sports.io/football/players/30925.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 33,
                    "position": "D",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": 41, "key": None, "accuracy": "36"},
                "tackles": {"total": 1, "blocks": 1, "interceptions": None},
                "duels": {"total": 4, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 67944,
            "name": "Ramon",
            "photo": "https://media.api-sports.io/football/players/67944.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 23,
                    "position": "D",
                    "rating": "7.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": 1, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": 25, "key": 2, "accuracy": "17"},
                "tackles": {"total": 6, "blocks": None, "interceptions": 3},
                "duels": {"total": 11, "won": 8},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 2, "committed": 2},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10565,
            "name": "Lucas Mineiro",
            "photo": "https://media.api-sports.io/football/players/10565.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 90,
                    "number": 30,
                    "position": "M",
                    "rating": "7.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": None, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": 42, "key": 1, "accuracy": "34"},
                "tackles": {"total": 4, "blocks": 1, "interceptions": None},
                "duels": {"total": 8, "won": 5},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 276452,
            "name": "Denilson",
            "photo": "https://media.api-sports.io/football/players/276452.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 70,
                    "number": 27,
                    "position": "M",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": 1, "saves": None},
                "passes": {"total": 21, "key": 1, "accuracy": "18"},
                "tackles": {"total": 2, "blocks": None, "interceptions": None},
                "duels": {"total": 5, "won": 3},
                "dribbles": {"attempts": None, "success": None, "past": 1},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 306213,
            "name": "Max",
            "photo": "https://media.api-sports.io/football/players/306213.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 69,
                    "number": 10,
                    "position": "M",
                    "rating": "7.5",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 1, "on": 1},
                "goals": {"total": 1, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": 30, "key": 1, "accuracy": "22"},
                "tackles": {"total": 2, "blocks": None, "interceptions": 1},
                "duels": {"total": 5, "won": 3},
                "dribbles": {"attempts": 1, "success": 1, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 350,
            "name": "Jonathan Cafú",
            "photo": "https://media.api-sports.io/football/players/350.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 89,
                    "number": 7,
                    "position": "F",
                    "rating": "8.3",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": 2, "saves": None},
                "passes": {"total": 20, "key": 3, "accuracy": "15"},
                "tackles": {"total": 5, "blocks": None, "interceptions": None},
                "duels": {"total": 20, "won": 10},
                "dribbles": {"attempts": 6, "success": 3, "past": 1},
                "fouls": {"drawn": 1, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 70670,
            "name": "Isidro Pitta",
            "photo": "https://media.api-sports.io/football/players/70670.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 89,
                    "number": 9,
                    "position": "F",
                    "rating": "8",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 2, "on": 1},
                "goals": {"total": 1, "conceded": 0, "assists": 1, "saves": None},
                "passes": {"total": 15, "key": 2, "accuracy": "12"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 8, "won": 2},
                "dribbles": {"attempts": 1, "success": None, "past": None},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10258,
            "name": "Clayson",
            "photo": "https://media.api-sports.io/football/players/10258.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 69,
                    "number": 25,
                    "position": "F",
                    "rating": "8.2",
                    "captain": False,
                    "substitute": False,
                },
                "offsides": None,
                "shots": {"total": 3, "on": 3},
                "goals": {"total": 2, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": 22, "key": None, "accuracy": "17"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 5, "won": 2},
                "dribbles": {"attempts": 3, "success": 1, "past": None},
                "fouls": {"drawn": 1, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 80187,
            "name": "Fernando Sobral",
            "photo": "https://media.api-sports.io/football/players/80187.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 21,
                    "number": 88,
                    "position": "M",
                    "rating": "6.7",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": 12, "key": None, "accuracy": "9"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 2, "won": 1},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 374922,
            "name": "Eliel",
            "photo": "https://media.api-sports.io/football/players/374922.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 21,
                    "number": 11,
                    "position": "F",
                    "rating": "6.7",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": 2, "key": None, "accuracy": "1"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 237906,
            "name": "Guilherme Madruga",
            "photo": "https://media.api-sports.io/football/players/237906.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 20,
                    "number": 8,
                    "position": "D",
                    "rating": "6.9",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": 1, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": 1, "saves": None},
                "passes": {"total": 10, "key": 1, "accuracy": "9"},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": 7, "won": 2},
                "dribbles": {"attempts": 1, "success": None, "past": None},
                "fouls": {"drawn": 2, "committed": 2},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 10256,
            "name": "André Luís",
            "photo": "https://media.api-sports.io/football/players/10256.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 9,
                    "number": 97,
                    "position": "F",
                    "rating": "6.6",
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": 1, "key": None, "accuracy": "1"},
                "tackles": {"total": None, "blocks": 1, "interceptions": None},
                "duels": {"total": 3, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": 1},
                "cards": {"yellow": 1, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 294033,
            "name": "Luciano Giménez",
            "photo": "https://media.api-sports.io/football/players/294033.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": 1,
                    "number": 19,
                    "position": "F",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": 0, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 458374,
            "name": "Rhyan",
            "photo": "https://media.api-sports.io/football/players/458374.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 12,
                    "position": "G",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9663,
            "name": "Mateus Pasinato",
            "photo": "https://media.api-sports.io/football/players/9663.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 14,
                    "position": "G",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 111324,
            "name": "Allyson",
            "photo": "https://media.api-sports.io/football/players/111324.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 3,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 334620,
            "name": "Juan Tavares",
            "photo": "https://media.api-sports.io/football/players/334620.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 63,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 160594,
            "name": "Railan",
            "photo": "https://media.api-sports.io/football/players/160594.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 21,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 304824,
            "name": "Rikelme",
            "photo": "https://media.api-sports.io/football/players/304824.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 20,
                    "position": "M",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
    {
        "player": {
            "id": 9945,
            "name": "Bruno Alves",
            "photo": "https://media.api-sports.io/football/players/9945.png",
        },
        "statistics": [
            {
                "games": {
                    "minutes": None,
                    "number": 34,
                    "position": "D",
                    "rating": None,
                    "captain": False,
                    "substitute": True,
                },
                "offsides": None,
                "shots": {"total": None, "on": None},
                "goals": {"total": None, "conceded": 0, "assists": None, "saves": None},
                "passes": {"total": None, "key": None, "accuracy": None},
                "tackles": {"total": None, "blocks": None, "interceptions": None},
                "duels": {"total": None, "won": None},
                "dribbles": {"attempts": None, "success": None, "past": None},
                "fouls": {"drawn": None, "committed": None},
                "cards": {"yellow": 0, "red": 0},
                "penalty": {
                    "won": None,
                    "commited": None,
                    "scored": 0,
                    "missed": 0,
                    "saved": None,
                },
            }
        ],
    },
]

# points = calculate_player_points(data)
# print(points)
