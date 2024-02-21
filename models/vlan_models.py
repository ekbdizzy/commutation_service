from pydantic import BaseModel

from models.base_models import EveConfig, Switch


class GetMaxVlanIdData(BaseModel):
    """
    :param data.switch: switch creds
    :param data.command:
    :param data.pattern: pattern to match VLAN id. Default for Cisco 3850.
    """

    switch: Switch
    command: str = "show vlan"
    pattern: str = r"^\s*(\d{1,4})\s+"


class GetMaxVlanIdDataOut(BaseModel):
    max_vlan_id: int


class CreateVlanIn(BaseModel):
    eve_config: EveConfig
    switch: Switch


class CreateVlansOut(BaseModel):
    vlan_ids: list[int]
    status: str
