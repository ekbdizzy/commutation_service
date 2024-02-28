import logging
from pygnmi.client import gNMIclient

from models.base_models import Switch

logger = logging.getLogger(__name__)


def _gnmi_get_max_vlan_id(switch: Switch) -> int:
    with gNMIclient(
        (switch.ip, switch.port),
        switch.username,
        switch.password,
        insecure=True,
        debug=False,
        skip_verify=True,
        gnmi_timeout=120,
    ) as gc:
        result = gc.get(path=["/vlans/vlan"])
        keys = []
        for notification in result["notification"]:
            for vlan in notification["update"]:
                val = vlan["val"]
                for key in val.keys():
                    if "id" in key:
                        keys.append(vlan["val"].get(key, 0))
        return max(keys)


def _gnmi_create_vlan(switch: Switch, vlan_id):

    with gNMIclient(
        (switch.ip, switch.port),
        switch.username,
        switch.password,
        insecure=True,
        debug=False,
        skip_verify=True,
        gnmi_timeout=120,
    ) as gc:
        create = [
            (
                "openconfig-vlan:vlans/vlan",
                {
                    "vlan-id": vlan_id,
                    "config": {
                        "name": f"VLAN{vlan_id}-test",
                        "vlan-id": vlan_id,
                    },
                },
            )
        ]
        try:
            result = gc.set(update=create)
            return result
        except Exception as e:
            logger.error(e)
            return e


def _gnmi_add_interfaces(switch: Switch, interfaces: list = None):
    interfaces = interfaces or []
    # TODO add interfaces


def _gnmi_delete_vlan(switch: Switch, vlan_id):
    with gNMIclient(
        (switch.ip, switch.port),
        switch.username,
        switch.password,
        insecure=True,
        debug=False,
        skip_verify=True,
        gnmi_timeout=120,
    ) as gc:
        delete = [(f"vlans/vlan[vlan-id={vlan_id}]")]
        try:
            result = gc.set(delete=delete)
            logger.info(result)
            return result
        except Exception as exc:
            logger.error(exc)
            return exc
