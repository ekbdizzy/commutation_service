from pydantic import BaseModel


class Switch(BaseModel):
    ip: str
    username: str
    password: str


class GetMaxVlanIdData(BaseModel):
    switch: Switch
    command: str = "show vlan"
    pattern: str = r"^\s*(\d{1,4})\s+"
