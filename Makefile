start_dev:
	.venv/bin/uvicorn main:app --host 127.0.0.1 --port $(PORT) --reload
create_env:
	cp sample.env .env