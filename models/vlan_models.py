from pydantic import BaseModel

from models.base_models import EveConfig, Switch


class GetMaxVlanIdData(BaseModel):
    """
    :param switch: switch creds
    :param command: command to show VLANs. Default for Cisco.
    :param pattern: pattern to match VLAN id. Default for Cisco.
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
