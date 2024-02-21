import re
from contextlib import contextmanager
import logging
from typing import Generator

import paramiko
from paramiko.client import SSHClient

from settings import Settings
from pydantic_models import Switch, GetMaxVlanIdData

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
        logger.exception("Authentication failed")
        raise Exception("Authentication failed")

    finally:
        ssh_client.close()


def get_vlan_max_id(data: GetMaxVlanIdData) -> int:
    """Get maximum VLAN id from switch.
    :param data.switch: switch creds
    :param data.command: command to show VLANs. Default for Cisco 3850.
    :param data.pattern: pattern to match VLAN id. Default for Cisco 3850."""

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
