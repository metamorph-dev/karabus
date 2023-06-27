up:
	docker compose up

up-d:
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
