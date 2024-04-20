build:
	docker compose -f docker-compose.yaml build
run:
	docker compose -f docker-compose.yaml up -d

stop:
	docker compose -f docker-compose.yaml down


build-dev:
	docker compose -f docker-compose.dev.yaml build db_bot redis_bot

run-dev:
	docker compose -f docker-compose.dev.yaml up -d db_bot redis_bot

stop-dev:
	docker compose -f docker-compose.dev.yaml down

install:
	pip install -r requirements.txt

bot-run:
	python3 app/main.py

install-dev:
	pip install -r requirements-dev.txt

