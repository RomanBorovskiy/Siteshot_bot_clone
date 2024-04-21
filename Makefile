build:
	docker compose -f docker-compose.yaml build
run:
	docker compose -f docker-compose.yaml up -d

stop:
	docker compose -f docker-compose.yaml down


build-dev:
	docker compose -f docker-compose.dev.yaml build

run-dev:
	docker compose -f docker-compose.dev.yaml up -d

stop-dev:
	docker compose -f docker-compose.dev.yaml down

install:
	pip install -r requirements.txt

bot-run:
	python3 app/main.py

worker-run:
	python3 app/bot_worker.py

install-dev:
	pip install -r requirements-dev.txt

