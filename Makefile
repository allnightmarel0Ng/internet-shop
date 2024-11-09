.PHONY: all build run down lint

all: build run

build:
	docker compose --env-file .env -f deployments/docker-compose.yml build

run:
	docker compose --env-file .env -f deployments/docker-compose.yml up -d

down:
	docker compose --env-file .env -f deployments/docker-compose.yml down

lint:
	autopep8 --in-place -r .
