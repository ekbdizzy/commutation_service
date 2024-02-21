import logging
from fastapi import APIRouter, status

from models.vlan_models import GetMaxVlanIdData, GetMaxVlanIdDataOut, CreateVlanIn
from utils.ssh_utils import get_vlan_max_id

logger = logging.getLogger(__name__)


vlan_router = APIRouter(
    prefix="/vlans",
    tags=["Vlans"],
    # responses={404: {"description": "Not found"}},
)


@vlan_router.post("/max_id", status_code=status.HTTP_200_OK)
async def get_max_vlan_id(data: GetMaxVlanIdData) -> GetMaxVlanIdDataOut:
    max_vlan_id = get_vlan_max_id(data)
    return GetMaxVlanIdDataOut(max_vlan_id=max_vlan_id)


@vlan_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_vlan(create_vlan_in: CreateVlanIn):  # TODO add ->
    logger.info("Creating vlan")

    return {}


@vlan_router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
async def delete_vlan():
    pass
