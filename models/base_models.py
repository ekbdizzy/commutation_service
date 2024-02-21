from pydantic import BaseModel


class Switch(BaseModel):
    ip: str
    username: str
    password: str


class EveConfig(BaseModel):
    url: str = ""
    data: list[dict]
    name: str = ""
    topology_settings: list[dict] = []
