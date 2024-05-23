from pydantic import BaseModel
from typing import Optional


class Settings(BaseModel):
    api_key: str


class CreateFantasyLeague(BaseModel):
    wallet: str
    name: str
    description: Optional[str]
    competition_type: str
    competition_code: str
    competition_logo: Optional[str]
    season_start: str
    season_end: str
    buy_in: int
    fee: Optional[float] = 0.0
    first_place: Optional[float] = 0.5
    second_place: Optional[float] = 0.3
    third_place: Optional[float] = 0.2
    matchday_winner: Optional[float] = 0.1


class FantasyLeague(CreateFantasyLeague):
    id: str
    matchday: int
    num_participants: int
    has_ended: bool
    last_updated: int

    # add a property to get the total prize pool
    @property
    def total_prize_pool(self) -> float:
        return self.buy_in * self.num_participants


class CreateParticipant(BaseModel):
    fantasyleague_id: str
    wallet: str
    name: str


class Participant(CreateParticipant):
    id: str
    total_points: int
    join_date: int


class CreatePlayer(BaseModel):
    id: Optional[str]
    api_id: int
    league_id: str
    name: str
    position: str
    team: str


class Player(CreatePlayer):
    points: int


class PlayersBulk(BaseModel):
    players: list[CreatePlayer]


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
