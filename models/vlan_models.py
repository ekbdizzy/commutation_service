from pydantic import BaseModel

from models.base_models import Switch


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
    """Response from getting max vlan id."""

    max_vlan_id: int


class CreateDeleteVlanIn(BaseModel):
    """
    Model for create/delete vlan.
    :param switch: switch creds.
    :param vlan_id: VLAN id.
    :param commands: commands to run on the remote switch.
    """

    switch: Switch
    vlan_id: int
    commands: list


class CreateDeleteVlanOut(BaseModel):
    """Response from create/delete vlan."""

    status: str = "ok"
    log: str = ""


class GnmiCreateDeleteVlanIn(BaseModel):
    """
    Model for create/delete vlan via gNMI.
    :param switch: switch creds.
    :param vlan_id: VLAN id.
    """

    switch: Switch
    vlan_id: int
