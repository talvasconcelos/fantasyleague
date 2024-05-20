async def m001_initial(db):
    await db.execute(
        """
        CREATE TABLE fantasyleague.settings (
            api_key TEXT NOT NULL,
            first_prize FLOAT NOT NULL,
            second_prize FLOAT NOT NULL,
            third_prize FLOAT NOT NULL,
            weekly_prize FLOAT,
            monthly_prize FLOAT,
            matchday_prize FLOAT,
            finals_prize FLOAT,
        );
        """
    )

    await db.execute(
        f"""
        CREATE TABLE fantasyleague.fantasyleague (
            id TEXT PRIMARY KEY,
            wallet TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            buy_in INTEGER NOT NULL,
            competition_type TEXT NOT NULL,
            competition_code TEXT NOT NULL,
            matchday INTEGER DEFAULT 1,
            season_start TEXT NOT NULL,
            season_end TEXT NOT NULL,
            budget INTEGER DEFAULT 1000000,
            has_ended BOOLEAN DEFAULT FALSE,
            last_updated TIMESTAMP NOT NULL DEFAULT {db.timestamp_now}
        );
        """
    )

    await db.execute(
        f"""
        CREATE TABLE fantasyleague.participants (
            id TEXT PRIMARY KEY,
            fantasyleague_id TEXT NOT NULL,
            wallet TEXT NOT NULL,
            name TEXT NOT NULL,
            total_points INTEGER DEFAULT 0,
            join_date TIMESTAMP NOT NULL DEFAULT {db.timestamp_now}
        );
        """
    )

    await db.execute(
        f"""
        CREATE TABLE fantasyleague.players (
            id TEXT PRIMARY KEY,
            league_id TEXT,
            api_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            price REAL DEFAULT 0.0,
            team TEXT NOT NULL,
            points INTEGER DEFAULT 0,
            FOREIGN KEY (league_id) REFERENCES {db.references_schema}fantasyleague(id),
        );
        """
    )

    await db.execute(
        f"""
        CREATE TABLE fantasyleague.participant_players (
            participant_id TEXT,
            player_id TEXT,
            FOREIGN KEY (participant_id) REFERENCES {db.references_schema}participants(id),
            FOREIGN KEY (player_id) REFERENCES {db.references_schema}players(id),
            PRIMARY KEY (participant_id, player_id)
        );
        """
    )

    await db.execute(
        f"""
        CREATE TABLE fantasyleague.gameweeks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            gameweek INTEGER NOT NULL,
            player_id TEXT,
            points INTEGER NOT NULL,
            FOREIGN KEY (player_id) REFERENCES {db.references_schema}players(id)
        );
        """
    )

    await db.execute(
        f"""
        CREATE TABLE prize_distributions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            league_id TEXT,
            participant_id TEXT,
            prize_type TEXT,
            prize_amount INTEGER,
            distributed_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now},
            FOREIGN KEY (league_id) REFERENCES {db.references_schema}fantasyleague(id),
            FOREIGN KEY (participant_id) {db.references_schema}REFERENCES participants(id)
        );
        """
    )
