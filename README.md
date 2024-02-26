## Commutation Service

Managing VLANs on Cisco/Microtic routers.

## How to start

Run command:

```shell
make PORT=8000 start_dev
```
Alternative way:

```shell
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```


## Request body samples

### Get max VLAN id on Cisco:
```json
{
  "switch": {
    "ip": "192.168.100.101",
    "username": "cisco_username",
    "password": "cisco_password"
  },
  "command": "show vlan",
  "pattern": "^\\s*(\\d{1,4})\\s+"
}
```

### Create VLAN with `id=2000` on Cisco and interfaces: `Te1/0/2, Te1/0/4`:

```json  
  {
  "switch": {
    "ip": "192.168.100.101",
    "username": "cisco_username",
    "password": "cisco_password"
  },
  "vlan_id": 2000,  // using for logging
  "commands": [
    "enable",
    "conf t",
    "vlan 2009",  // create VLAN
    
    "interface Te1/0/2", // add interface
    "switchport mode access",
    "switchport access vlan 2009",
    "exit",
    
    "interface Te1/0/4",
    "switchport mode access",
    "switchport access vlan 2009",
    "exit"
  ]
}
```

### Delete VLAN with `id=2000` on Cisco:

```json
  {
  "switch": {
    "ip": "192.168.100.101",
    "username": "cisco_username",
    "password": "cisco_password"
  },
  "vlan_id": 2000,  // using for logging
  "commands": [
    "enable",
    "conf t",
    "no vlan 2000",  // delete vlan
    "end",
    "write memory"  // save settings
  ]
}
```