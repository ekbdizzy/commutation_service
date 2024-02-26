import logging

from fastapi import APIRouter, status

from models.vlan_models import (
    GetMaxVlanIdData,
    GetMaxVlanIdDataOut,
    CreateDeleteVlanIn,
    CreateDeleteVlanOut,
)
from utils.ssh_utils import fetch_vlan_max_id, ssh_connection, run_switch_commands

logger = logging.getLogger(__name__)


vlan_router = APIRouter(
    prefix="/vlans",
    tags=["Vlans"],
)


@vlan_router.post(
    "/max_id",
    status_code=status.HTTP_200_OK,
    response_model=GetMaxVlanIdDataOut,
)
async def get_max_vlan_id(data: GetMaxVlanIdData) -> GetMaxVlanIdDataOut:
    max_vlan_id = fetch_vlan_max_id(data)
    return GetMaxVlanIdDataOut(max_vlan_id=max_vlan_id)


@vlan_router.post(
    "/",
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
    return CreateDeleteVlanIn(status="ok", log=switch_logs)


@vlan_router.delete(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=CreateDeleteVlanOut,
)
async def delete_vlan(data: CreateDeleteVlanIn):
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
