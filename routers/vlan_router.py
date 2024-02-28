import logging

from fastapi import APIRouter, status

from models.vlan_models import (
    GetMaxVlanIdData,
    GetMaxVlanIdDataOut,
    CreateDeleteVlanIn,
    CreateDeleteVlanOut,
    GnmiCreateDeleteVlanIn,
)
from utils.gnmi_utils import _gnmi_create_vlan, _gnmi_get_max_vlan_id, _gnmi_delete_vlan
from utils.ssh_utils import fetch_vlan_max_id, ssh_connection, run_switch_commands

logger = logging.getLogger(__name__)


vlan_router = APIRouter(
    prefix="/vlans",
    tags=["Vlans"],
)


@vlan_router.post(
    "/ssh/max_id",
    status_code=status.HTTP_200_OK,
    response_model=GetMaxVlanIdDataOut,
)
async def ssh_get_max_vlan_id(data: GetMaxVlanIdData) -> GetMaxVlanIdDataOut:
    max_vlan_id = fetch_vlan_max_id(data)
    return GetMaxVlanIdDataOut(max_vlan_id=max_vlan_id)


@vlan_router.post(
    "/ssh",
    status_code=status.HTTP_201_CREATED,
    response_model=CreateDeleteVlanOut,
)
async def create_vlan(data: CreateDeleteVlanIn):
    """Create vlan on switch."""
    logger.info(f"Creating vlan {data.switch.ip} {data.vlan_id}")

    with ssh_connection(data.switch) as ssh_client:
        switch_logs = run_switch_commands(ssh_client, data.commands, sleep=2)
        logger.info(
            f"""*** Create VLAN {data.vlan_id} log ***:
            {switch_logs}
            *** *** ***"""
        )
    return CreateDeleteVlanOut(status="ok", log=switch_logs)


@vlan_router.delete(
    "/ssh",
    status_code=status.HTTP_200_OK,
    response_model=CreateDeleteVlanOut,
)
async def ssh_delete_vlan(data: CreateDeleteVlanIn):
    """Delete vlan from switch."""
    logger.info(f"Delete VLAN {data.switch.ip} {data.vlan_id}")

    with ssh_connection(data.switch) as ssh_client:
        switch_logs = run_switch_commands(ssh_client, data.commands, sleep=2)
        logger.info(
            f"""*** Delete VLAN {data.vlan_id} log ***:
            {switch_logs}
            *** *** ***"""
        )
    return CreateDeleteVlanOut(status="ok", log=switch_logs)


@vlan_router.post("/gnmi/max_id")
async def gnmi_get_vlan_max_id(data: GetMaxVlanIdData) -> GetMaxVlanIdDataOut:
    max_vlan_id = _gnmi_get_max_vlan_id(data.switch)
    return GetMaxVlanIdDataOut(max_vlan_id=max_vlan_id)


@vlan_router.post("/gnmi/")
async def gnmi_create_vlan(data: GnmiCreateDeleteVlanIn):
    """Create vlan within gNMI."""
    gnmi_logs = _gnmi_create_vlan(data.switch, data.vlan_id)
    logger.info(
        f"""*** Create VLAN {data.vlan_id} log ***:
                {gnmi_logs}
                *** *** ***"""
    )
    return CreateDeleteVlanOut(status="ok", log=str(gnmi_logs))


@vlan_router.delete("/gnmi/")
async def delete_vlan_gnmi(data: GnmiCreateDeleteVlanIn):
    """Delete vlan within gNMI."""
    gnmi_logs = _gnmi_delete_vlan(data.switch, data.vlan_id)
    logger.info(
        f"""*** Delete VLAN {data.vlan_id} log ***:
        {gnmi_logs}
        *** *** ***"""
    )
    print(gnmi_logs)
    if isinstance(gnmi_logs, dict):
        gnmi_logs = str(gnmi_logs)
    return CreateDeleteVlanOut(status="ok", log=gnmi_logs)
