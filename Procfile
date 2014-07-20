web: env PYTHONUNBUFFERED=true python src/keybar/server.py
worker: env PYTHONUNBUFFERED=true celery worker -A keybar.core -l INFO -E
compass: compass watch --trace
