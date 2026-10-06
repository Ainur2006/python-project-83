setup: install build-css

install:
	uv sync
	npm ci

build-css:
	npm run build:css

dev:
	uv run flask --debug --app page_analyzer:app run

setup: install

lint:
	uv run ruff check .

PORT ?= 8000

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:appuild:
	./build.sh

render-start:
	gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app