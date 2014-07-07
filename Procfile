stunnel: stunnel extras/stunnel/stunnel.cnf
web: env PYTHONUNBUFFERED=true python manage.py runserver 0.0.0.0:8000
web-ssl: env PYTHONUNBUFFERED=true HTTPS=1 python manage.py runserver 0.0.0.0:8001
worker: env PYTHONUNBUFFERED=true celery worker -A keybar -l INFO -E
compass: compass watch --trace
