import logging
from collections import defaultdict

logger = logging.getLogger(__name__)


def parse_eve_config(eve_config: dict) -> defaultdict[str, dict]:
    """Parse config from eve schema and return source and destinations ports for creating VLAN.
    Node_name with switch must be ended with _Switch.
    Example: Cisco_3850_Switch."""

    has_switch_in_scheme: bool = False
    switches = defaultdict(dict)
    data: dict = eve_config.get("data")

    for conn in data:
        source_name = conn.get("source_node_name")
        destination_name = conn.get("destination_node_name")
        src_port = conn["source_label"]
        dst_port = conn["destination_label"]

        if source_name.endswith("_Switch"):
            has_switch_in_scheme = True
            if source_name not in switches:

                switches[source_name] = {
                    "src_ports": [src_port],
                    "dst_ports": [],
                }
            else:
                switches[source_name]["src_ports"].append(src_port)

        if destination_name.endswith("_Switch"):
            has_switch_in_scheme = True
            if destination_name not in switches:
                switches[source_name] = {
                    "src_ports": [],
                    "dst_ports": [dst_port],
                }
            else:
                switches[destination_name]["dst_ports"].append(dst_port)
    if not has_switch_in_scheme:
        logger.warning("No switch in Eve schema or config created incorrectly.")

    return switches
