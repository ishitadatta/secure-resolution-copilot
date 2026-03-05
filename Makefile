.PHONY: api web test eval seed up down

api:
	cd apps/api && uvicorn app.main:app --reload --port 8000

web:
	cd apps/web && python -m http.server 3000

test:
	cd apps/api && pytest -q

eval:
	curl -s -X POST http://localhost:8000/v1/evals/run | python -m json.tool

seed:
	cd apps/api && python ../../scripts/seed_synthetic_data.py

up:
	docker compose up --build

down:
	docker compose down
