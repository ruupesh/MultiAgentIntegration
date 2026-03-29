# PostgreSQL Setup

This guide explains how to run PostgreSQL in Docker with persistent storage.

## 1. Prerequisites

- Docker
- Docker Compose (optional, recommended)

Check installation:

```bash
docker --version
docker compose version
```

## 2. Pull the PostgreSQL Image

```bash
docker pull postgres:latest
```

## 3. Create a Persistent Volume

```bash
docker volume create postgres_data
docker volume ls
```

## 4. Run the Container

```bash
docker run -d \
  --name postgres_db \
  -e POSTGRES_USER=admin \
  -e POSTGRES_PASSWORD=admin \
  -e POSTGRES_DB=my_db \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  postgres:latest
```

## 5. Verify It Is Running

```bash
docker ps
```

## 6. Connect

From host:

```bash
psql -h localhost -U admin -d my_db
```

From container:

```bash
docker exec -it postgres_db psql -U admin -d my_db
```

## 7. Stop and Start

```bash
docker stop postgres_db
docker start postgres_db
```

Data persists because it is stored in `postgres_data` volume.

## 8. Remove Container Without Data Loss

```bash
docker rm -f postgres_db
```

Recreate with the same `-v postgres_data:/var/lib/postgresql/data` mount.

## 9. Optional Compose Setup

`docker-compose.yml`:

```yaml
version: "3.9"

services:
  postgres:
    image: postgres:latest
    container_name: postgres_db
    restart: always
    environment:
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: admin
      POSTGRES_DB: my_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

```bash
docker compose up -d
docker compose down
```

## 10. Match Backend Configuration

`backend_service/.env` should align with your DB credentials:

```env
DATABASE_URL=postgresql+asyncpg://admin:admin@localhost:5432/my_db
```

If you change user/password/database/port in Docker, update `DATABASE_URL` accordingly.

## 11. Useful Commands

```bash
docker logs postgres_db
docker exec -it postgres_db bash
docker volume inspect postgres_data
```

## 12. Port Notes

Default PostgreSQL port is `5432`. If in use:

```bash
-p 5433:5432
```

Then update backend env and any `psql` command to use `5433`.

## 13. Cleanup

```bash
docker rm -f postgres_db
docker volume rm postgres_data
```

Warning: removing the volume deletes DB data permanently.
