from pydantic import BaseModel
from typing import Optional


class Settings(BaseModel):
    api_key: str
    first_prize: float
    second_prize: float
    third_prize: float
    weekly_prize: Optional[float]
    monthly_prize: Optional[float]
    matchday_prize: Optional[float]
    finals_prize: Optional[float]


class CreateFantasyLeague(BaseModel):
    wallet: str
    name: str
    description: Optional[str]
    competition_type: str
    competition_code: str
    season_start: str
    season_end: str
    buy_in: int
    budget: Optional[int]


class FantasyLeague(CreateFantasyLeague):
    id: str
    matchday: int
    has_ended: bool
    last_updated: int


class CreateParticipant(BaseModel):
    fantasyleague_id: str
    wallet: str
    name: str


class Participant(CreateParticipant):
    id: str
    total_points: int
    join_date: int


class CreatePlayer(BaseModel):
    api_id: int
    league_id: str
    name: str
    position: str
    team: str


class Player(CreatePlayer):
    id: str
    price: float
    points: int


class Players(BaseModel):
    players: list[Player]


class CreatePrizeDistribution(BaseModel):
    league_id: str
    participant_id: str
    prize_type: str
    prize_amount: int


class PrizeDistribution(CreatePrizeDistribution):
    id: str
    distributed_at: int
