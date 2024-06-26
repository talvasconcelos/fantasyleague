async def m001_initial(db):
    await db.execute(
        """
        CREATE TABLE fantasyleague.api_settings (
            api_key TEXT NOT NULL PRIMARY KEY
        );
        """
    )

    await db.execute(
        f"""
        CREATE TABLE fantasyleague.competitions (
            id TEXT PRIMARY KEY,
            wallet TEXT NOT NULL,
            name TEXT NOT NULL,
            description TEXT,
            buy_in INTEGER NOT NULL,
            competition_type TEXT NOT NULL,
            competition_code TEXT NOT NULL,
            competition_logo TEXT,
            season INTEGER NOT NULL,
            matchday TEXT,
            season_start TEXT NOT NULL,
            season_end TEXT NOT NULL,
            has_ended BOOLEAN DEFAULT FALSE,
            fee FLOAT NOT NULL DEFAULT 0.0,
            num_participants INTEGER DEFAULT 0,
            first_place FLOAT NOT NULL,
            second_place FLOAT NOT NULL,
            third_place FLOAT NOT NULL,
            matchday_winner FLOAT NOT NULL,
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
            formation TEXT DEFAULT '4-4-2',
            lineup TEXT,
            total_points INTEGER DEFAULT 0,
            join_date TIMESTAMP NOT NULL DEFAULT {db.timestamp_now}
        );
        """
    )

    await db.execute(
        """
        CREATE TABLE fantasyleague.players (
            id TEXT PRIMARY KEY,
            league_id TEXT,
            api_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            position TEXT NOT NULL,
            team TEXT NOT NULL,
            photo TEXT,
            points INTEGER DEFAULT 0
        );
        """
    )

    await db.execute(
        """
        CREATE TABLE fantasyleague.participant_players (
            participant_id TEXT,
            player_id TEXT,
            PRIMARY KEY (participant_id, player_id)
        );
        """
    )

    await db.execute(
        f"""
        CREATE TABLE prize_distributions (
            id {db.serial_primary_key},
            league_id TEXT,
            participant_id TEXT,
            prize_type TEXT,
            prize_amount INTEGER,
            distributed_at TIMESTAMP NOT NULL DEFAULT {db.timestamp_now}
        );
        """
    )

async def m002_add_transfers(db):
    await db.execute("ALTER TABLE fantasyleague.competitions ADD COLUMN transfer_window_close INTEGER;")
    await db.execute(
        f"""
        CREATE TABLE fantasyleague.participant_transfers (
            id TEXT PRIMARY KEY,
            participant_id TEXT NOT NULL,
            player_out_id TEXT,
            player_in_id TEXT,
            gameweek TEXT NOT NULL,
            transfer_date TIMESTAMP NOT NULL DEFAULT {db.timestamp_now},
            cost INTEGER DEFAULT 0
        );
        """
    )

    await db.execute(
        """
        CREATE TABLE fantasyleague.participant_free_transfers (
            participant_id TEXT PRIMARY KEY,
            free_transfers INTEGER DEFAULT 1,
            saved_transfers INTEGER DEFAULT 0
        );
        """
    )

async def m003_initiate_free_transfers(db):
    participants = await db.fetchall("SELECT id FROM fantasyleague.participants")
    for participant in participants:
        await db.execute(
            """
            INSERT INTO fantasyleague.participant_free_transfers (participant_id, free_transfers, saved_transfers)
            VALUES (?, 1, 0)
            ON CONFLICT (participant_id) DO NOTHING;
            """,
            (participant["id"],),
        )