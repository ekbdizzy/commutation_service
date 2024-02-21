from pydantic import BaseModel


class Switch(BaseModel):
    ip: str
    username: str
    password: str


class GetMaxVlanIdData(BaseModel):
    switch: Switch
    command: str = "show vlan"
    pattern: str = r"^\s*(\d{1,4})\s+"


class GetMaxVlanIdDataOut(BaseModel):
    max_vlan_id: int


class EveConfig(BaseModel):
    url: str = ""
    data: list[dict]
    name: str = ""
    topology_settings: list[dict] = []


class CreateVlanIn(BaseModel):
    eve_config: EveConfig
    switch: Switch


class CreateVlansOut(BaseModel):
    vlan_ids: list[int]
    status: str
