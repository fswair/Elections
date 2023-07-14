from typing import Union, Any
from datetime import datetime
from discord import Bot, Intents, Message
from pydantic import BaseModel
from models import CandidateModel, VoterModel, LawModel, SessionModel
from mento import Mento, PrimaryKey, Column, Lambda
from mento.connection import MentoConnection
from os import remove


DEFAULT_CONTEXT: Any = id(__name__)

class DiscordIntents:
    def __new__(cls) -> Intents:
        intents = Intents.all()
        intents.guild_messages = True
        intents.message_content = True
        return intents

sessions = {1: dict(party=dict())}

def get_session(ctx: Message):
    db = Database()
    sessions = db.select("sessions")
    if sessions:
        session = sessions[0]
        return session
    return dict()



class Cord(Bot):
    async def on_ready(self):
        print("Ready")
    
    async def on_message(self, ctx: Message):
        session = get_session(ctx)
        if session and not session.get("party_name"):
            party = session.get("party_name", "")
            if not party.strip():
                    core = Core(1)
                    party_name = ctx.content
                    if core.db.select("sessions", where=dict(party_name="")):
                        core.db.update("sessions", data=dict(id=ctx.author.id, party_name=party_name), where=dict(id=ctx.author.id))
                    return await ctx.reply("Parti başarıyla oluşturuldu.: %s " %party_name)
                    



class Core(object):
    def __init__(self, discord_token: str, database_name: str = None, database_model: BaseModel = None, *args, **kwargs):
        self.db = Database(default_table=database_name, check_model=database_model)
        self.db.create("candidates", CandidateModel)
        self.db.create("voters", VoterModel)
        self.db.create("laws", LawModel)
        self.db.create("sessions", SessionModel)
        assert discord_token
        self.discord_token = discord_token
        self.cord = Cord(intents=DiscordIntents())
    
    def run(self):
        return self.cord.run(self.discord_token)

class _Reload(Core):
    __doc__ = "Reload the database"


class Database(Mento):
    def __init__(self, connection = MentoConnection(), default_table = None, check_model = None, error_logging = False):
        super().__init__(connection, default_table, check_model, error_logging)
    
    def reload(self) -> _Reload:
        remove("database.db")
        return Core(DEFAULT_CONTEXT)


class Session(BaseModel):
    id: int
    session_chat: PrimaryKey(int)
    party_name: str

    @staticmethod
    def select(core: Core, where: dict = None, order_by: Column = None, limit: int = 0, filter: Lambda = None, model: BaseModel = None):
        response = core.db.select(from_table="sessions", where=where, order_by=order_by, limit=limit, filter=filter, model=model) 
        return SessionContext(response=response)
    @staticmethod
    def insert(core: Core, data: dict, check_model: BaseModel = None):
        response = core.db.i(table="sessions", data=data, check_model=check_model)
        return SessionContext(response=response)
    @staticmethod
    def update(core: Core, data: dict, where: dict = None, *args, **kwargs):
        response = core.db.update(table="sessions", data=data, where=where, *args, **kwargs)
        if not response: return dict()
        return SessionContext(response=response)
    @staticmethod
    def delete(core: Core, where: dict = None, *args, **kwargs):
        response = core.db.delete(table="sessions", where=where, *args, **kwargs)
        if not response: return dict()
        return SessionContext(response=response)
    @staticmethod
    def drop(core: Core):
        response = core.db.drop(table="sessions")
        if not response: return dict()
        return SessionContext(response=response)

class Candidate(BaseModel):
    candidate_id: int
    candidate_name: str
    candidate_age: int
    candidate_party: int
    candidate_requested_laws: int

    @staticmethod
    def select(core: Core, where: dict = None, order_by: Column = None, limit: int = 0, filter: Lambda = None, model: BaseModel = None):
        response = core.db.select(from_table="candidates", where=where, order_by=order_by, limit=limit, filter=filter, model=model)
        if not response: return dict()
        return CandidateContext(response=response)
    @staticmethod
    def insert(core: Core, data: dict, check_model: BaseModel = None):
        response = core.db.i(table="candidates", data=data, check_model=check_model)
        if not response: return dict()
        return CandidateContext(response=response)
    @staticmethod
    def update(core: Core, data: dict, where: dict = None, *args, **kwargs):
        response = core.db.update(table="candidates", data=data, where=where, *args, **kwargs)
        if not response: return dict()
        return CandidateContext(response=response)
    @staticmethod
    def delete(core: Core, where: dict = None, *args, **kwargs):
        response = core.db.delete(table="candidates", where=where, *args, **kwargs)
        if not response: return dict()
        return CandidateContext(response=response)
    @staticmethod
    def drop(core: Core):
        response = core.db.drop(table="candidates")
        if not response: return dict()
        return CandidateContext(response=response)

class Law(BaseModel):
    law_id: Union[int, str]
    law_name: str
    law_description: str
    law_released_date: Union[float, datetime]
    law_requested_by: int

    @staticmethod
    def select(core: Core, where: dict = None, order_by: Column = None, limit: int = 0, filter: Lambda = None, model: BaseModel = None):
        response = core.db.select(from_table="laws", where=where, order_by=order_by, limit=limit, filter=filter, model=model)
        if not response: return dict()
        return LawContext(response=response)
    @staticmethod
    def insert(core: Core, data: dict, check_model: BaseModel = None):
        response = core.db.i(table="laws", data=data, check_model=check_model)
        if not response: return dict()
        return LawContext(response=response)
    @staticmethod
    def update(core: Core, data: dict, where: dict = None, *args, **kwargs):
        response = core.db.update(table="laws", data=data, where=where, *args, **kwargs)
        if not response: return dict()
        return LawContext(response=response)
    @staticmethod
    def delete(core: Core, where: dict = None, *args, **kwargs):
        response = core.db.delete(table="laws", where=where, *args, **kwargs)
        if not response: return dict()
        return LawContext(response=response)
    @staticmethod
    def drop(core: Core):
        response = core.db.drop(table="laws")
        if not response: return dict()
        return LawContext(response=response)

class Voter(BaseModel):
    voter_id: int
    voter_name: str
    voter_party: str
    voter_voted_laws: list[int]

    @staticmethod
    def select(core: Core, where: dict = None, order_by: Column = None, limit: int = 0, filter: Lambda = None, model: BaseModel = None):
        response = core.db.select(from_table="voters", where=where, order_by=order_by, limit=limit, filter=filter, model=model)
        if not response: return dict()
        return VoterContext(response=response)
    @staticmethod
    def insert(core: Core, data: dict, check_model: BaseModel = None):
        response = core.db.insert(table="voters", data=data, check_model=check_model)
        if not response: return dict()
        return VoterContext(response=response)
    @staticmethod
    def update(core: Core, data: dict, where: dict = None, *args, **kwargs):
        response = core.db.update(table="voters", data=data, where=where, *args, **kwargs)
        if not response: return dict()
        return VoterContext(response=response)
    @staticmethod
    def delete(core: Core, where: dict = None, *args, **kwargs):
        response = core.db.delete(table="voters", where=where, *args, **kwargs)
        if not response: return dict()
        return VoterContext(response=response)
    @staticmethod
    def drop(core: Core):
        response = core.db.drop(table="voters")
        if not response: return dict()
        return VoterContext(response=response)


class Context:
    __doc__: str = "Context for your base classes"

class LawContext(Context):
    def __new__(self, response: dict | list[dict], first: bool = True) -> Law | list[Law]:
        assert response
        if isinstance(response, list):
            if not first:
                return list(map(lambda kw: Law(**kw), response))
        return Law(**response)

class CandidateContext(Context):
    def __new__(self, response: dict | list[dict], first: bool = True) -> Candidate | list[Candidate]:
        assert response
        if isinstance(response, list):
            if not first:
                return list(map(lambda kw: Candidate(**kw), response))
        return Candidate(**response)
    
class VoterContext(Context):
    def __new__(self, response: dict | list[dict], first: bool = True) -> Voter | list[Voter]:
        assert response
        if isinstance(response, list):
            if not first:
                return list(map(lambda kw: Voter(**kw), response))
        return Voter(**response)

class SessionContext(Context):
    def __new__(self, response: dict | list[dict], first: bool = True) -> Session | list[Session]:
        assert response
        if isinstance(response, list):
            if not first:
                return list(map(lambda kw: Session(**kw), response))
        return Session(**response)
