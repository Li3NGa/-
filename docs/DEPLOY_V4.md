# Anonymous Chat V4 Production Deployment

## Requirements

- Docker
- Docker Compose
- Linux server recommended

## Configure environment

Copy production environment template:

```
cp config/production.env.example .env
```

Update:

- SECRET_KEY
- DATABASE_URL
- REDIS_URL

## Deploy

Run:

```
cd deploy
chmod +x deploy.sh
./deploy.sh
```

## Services

- Flask Socket.IO application
- Redis message queue
- PostgreSQL database
- Nginx reverse proxy

## Health Check

```
GET /health
```
