up:
	docker compose up

build:
	docker compose up --build

start:
	docker compose up -d

down:
	docker compose down

bash:
	docker compose exec web bash

install:
	poetry install

test:
	pytest -v

coverage:
	pytest -v --cov=app/

chown:
	sudo chown -R $(USER) .
