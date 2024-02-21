import logging

from fastapi import FastAPI, status

from pydantic_models import GetMaxVlanIdData
from utils.ssh_utils import get_vlan_max_id


logging.basicConfig(
    level=logging.DEBUG,
    filename="commutation.log",
    filemode="a",
    format="%(asctime)s %(name)s %(levelname)s:%(message)s",
)

logger = logging.getLogger(__name__)
consoleHandler = logging.StreamHandler()
logFormatter = logging.Formatter(
    "%(levelname)s: %(asctime)s | %(threadName)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

app = FastAPI()


@app.get("/status/", status_code=status.HTTP_200_OK)
async def healthcheck():
    logger.info("Healthcheck")
    return {"status": "ok"}


@app.post("/max_vlan_id", status_code=status.HTTP_200_OK)
async def get_max_vlan_id(data: GetMaxVlanIdData):
    max_vlan_id = get_vlan_max_id(data)
    return {"max_vlan": max_vlan_id}
