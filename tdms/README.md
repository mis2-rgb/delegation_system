# Task Delegation Management System (TMS)

Multi-tenant SaaS for task delegation with RBAC, real-time notifications, and analytics.

## Quick Start (Local)

1. Python deps (system user install already present), set env:

Create `.env` at project root:

```
DEBUG=True
SECRET_KEY=dev-secret
ALLOWED_HOSTS=*
DATABASE_URL=sqlite:///db.sqlite3
REDIS_URL=redis://localhost:6379/0
TIME_ZONE=UTC
```

2. Migrate and create superuser:

```
python3 manage.py migrate
python3 manage.py createsuperuser
```

3. Run services:

- Dev server (with Channels):
```
daphne -b 0.0.0.0 -p 8000 config.asgi:application
```
- Celery worker and beat:
```
celery -A config worker -l info
celery -A config beat -l info
```

## Docker

Edit `docker/.env` based on sample, then:
```
docker compose up -d --build
```

Services:
- Web: Gunicorn + Daphne
- Redis
- Postgres
- Celery worker/beat

## API
- JWT: `/api/auth/login/`, `/api/auth/refresh/`
- Tasks: `/api/tasks/` with `POST {id}/complete/`, `POST {id}/verify/`
- Reports: `/api/reports/metrics/`, `/api/reports/weekly/`
- Notifications: `/api/notifications/`