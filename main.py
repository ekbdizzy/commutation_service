import logging
from fastapi import FastAPI, status


logging.basicConfig(
    level=logging.DEBUG,
    filename="commutation.log",
    filemode="w",
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
