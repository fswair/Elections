from typing import Union
from datetime import datetime
from dataclasses import dataclass
from mento import BaseModel, PrimaryKey

@dataclass
class SessionModel(BaseModel):
    id: int
    session_chat: PrimaryKey(int)
    party_name: str


@dataclass
class CandidateModel(BaseModel):
    candidate_id: int
    candidate_name: str
    candidate_age: int
    candidate_party: int
    candidate_requested_laws: int

@dataclass
class LawModel(BaseModel):
    law_id: Union[int, str]
    law_name: str
    law_description: str
    law_released_date: Union[float, datetime]
    law_requested_by: int

@dataclass
class VoterModel(BaseModel):
    voter_id: int
    voter_name: str
    voter_party: str
    voter_voted_laws: list[int]
