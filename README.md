## Commutation Service

Managing VLANs on Cisco/Microtic routers.

## How to start

1. To start project you have to create `.env` file with options:

```
SWITCH_IP=IP
SWITCH_USERNAME=username
SWITCH_PASSWORD=password
```

Run command `make create_env` to create default `.env` file.

2. Create virtualenv in .venv folder:

```shell
python3 -m virtualenv .venv
```

3. Run command:

```shell
make PORT=8000 start_dev
```

Alternative way:

```shell
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

