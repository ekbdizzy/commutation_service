import re
import time
from contextlib import contextmanager
import logging
from typing import Generator

import paramiko
from paramiko.client import SSHClient

from settings import Settings
from models.base_models import Switch
from models.vlan_models import GetMaxVlanIdData

settings = Settings()
logger = logging.getLogger(__name__)


@contextmanager
def ssh_connection(switch: Switch) -> Generator[SSHClient, None, None]:

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(
            switch.ip,
            username=switch.username,
            password=switch.password,
            look_for_keys=False,
            allow_agent=False,
        )
        logger.info("Connected to switch")
        yield ssh_client

    except paramiko.ssh_exception.AuthenticationException:
        logger.exception(
            f"Authentication failed: {switch.ip} {switch.username} {switch.password}"
        )
        raise Exception("Authentication failed")

    finally:
        ssh_client.close()


def fetch_vlan_max_id(data: GetMaxVlanIdData) -> int:
    """Get maximum VLAN id from switch."""

    with ssh_connection(data.switch) as ssh_client:

        stdin, stdout, stderr = ssh_client.exec_command(data.command)
        output = stdout.read().decode()
        logger.debug(f"output is {output}")

        max_vlan_id = 1
        for line in output.splitlines():
            match = re.match(rf"{data.pattern}", line)
            if match:
                vlan_id = int(match.group(1))
                if vlan_id > max_vlan_id:
                    max_vlan_id = vlan_id

    return max_vlan_id


def run_switch_commands(
    ssh_client: Generator[SSHClient, None, None], commands: list, sleep: int = 2
):
    shell = ssh_client.invoke_shell()
    for command in commands:
        shell.send(f"{command}\n")
        time.sleep(sleep)
    res = shell.recv(2048)
    return res
