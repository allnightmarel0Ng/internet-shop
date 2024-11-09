.PHONY: all build run down

all: build run

build:
	docker compose --env-file .env -f deployments/docker-compose.yml build

run:
	docker compose --env-file .env -f deployments/docker-compose.yml up -d

down:
	docker compose --env-file .env -f deployments/docker-compose.yml down