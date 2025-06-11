include .env
export

# Variables
COMPOSE_DEV=docker-compose -f docker-compose.dev.yml
COMPOSE_BASE=docker-compose -f docker-compose.yml

# Targets
.PHONY: dev down prod migrations logs ps restart build-prod build-prod-nocache push-prod deploy-prod run-proxy migrate-local

# Dev
dev:
	$(COMPOSE_DEV) up --build

# Prod (base)
prod:
	$(COMPOSE_BASE) up --build -d

# Stop all and cleanup volumes
down:
	$(COMPOSE_DEV) down -v --remove-orphans
	$(COMPOSE_BASE) down -v --remove-orphans

# Run Alembic migrations (dev)
migrations-dev:
	$(COMPOSE_DEV) exec backend alembic upgrade head

# Follow backend logs (dev)
logs-dev:
	$(COMPOSE_DEV) logs -f backend

# Rebuild backend only (dev)
rebuild-backend-dev:
	$(COMPOSE_DEV) build backend

# Show running containers
ps:
	docker-compose ps

# Restart dev (quick cycle)
restart-dev:
	$(COMPOSE_DEV) down -v --remove-orphans
	$(COMPOSE_DEV) up --build

# Build production image
build-prod:
	docker build --platform linux/amd64 -f backend/Dockerfile -t europe-central2-docker.pkg.dev/myapp-devops/myapp-backend-repo/backend:latest ./backend

build-prod-nocache:
	docker build --platform linux/amd64 --no-cache -f backend/Dockerfile -t europe-central2-docker.pkg.dev/myapp-devops/myapp-backend-repo/backend:latest ./backend

# Push production image
push-prod:
	docker push europe-central2-docker.pkg.dev/myapp-devops/myapp-backend-repo/backend:latest

# Deploy to Cloud Run
deploy-prod:
	gcloud run deploy myapp-backend \
		--image europe-central2-docker.pkg.dev/myapp-devops/myapp-backend-repo/backend:latest \
		--platform managed \
		--region europe-central2 \
		--allow-unauthenticated \
		--port 8000 \
		--add-cloudsql-instances=myapp-devops:europe-central2:myapp-postgres \
		--update-secrets "DATABASE_URL=DATABASE_URL_PROD:latest"

# Cloud SQL instance name
SQL_INSTANCE=myapp-devops:europe-central2:myapp-postgres

# Local DB (dev)
SQL_PROXY_PORT=5433

# Prod DB (pgAdmin)
SQL_PROXY_PROD_PORT=9999

# Run Cloud SQL Proxy for local dev (used by LOCAL_DATABASE_URL and migrate-local)
run-proxy:
	./cloud-sql-proxy --port=$(SQL_PROXY_PORT) $(SQL_INSTANCE)

# Run Cloud SQL Proxy for pgAdmin → NO conflict
proxy-prod:
	./cloud-sql-proxy --port=$(SQL_PROXY_PROD_PORT) $(SQL_INSTANCE)

# Run Alembic migrations → LOCAL DB (docker-compose db)
migrate-local:
	docker run --rm -it \
		-e DATABASE_URL="postgresql+asyncpg://postgres:$(POSTGRES_PASSWORD)@host.docker.internal:5432/app_db" \
		-v $(PWD)/backend:/app \
		europe-central2-docker.pkg.dev/myapp-devops/myapp-backend-repo/backend:latest \
		alembic upgrade head

# Run Alembic migrations → CLOUD DB (via Cloud SQL Proxy)
migrate-prod:
	docker run --rm -it \
		-e DATABASE_URL="postgresql+asyncpg://postgres:$(POSTGRES_PASSWORD)@host.docker.internal:$(SQL_PROXY_PORT)/app_db" \
		-v $(PWD)/backend:/app \
		europe-central2-docker.pkg.dev/myapp-devops/myapp-backend-repo/backend:latest \
		alembic upgrade head


# FRONTEND TARGETS
build-frontend:
	docker build --platform linux/amd64 -f frontend/Dockerfile -t europe-central2-docker.pkg.dev/myapp-devops/myapp-frontend-repo/frontend:latest ./frontend

push-frontend:
	docker push europe-central2-docker.pkg.dev/myapp-devops/myapp-frontend-repo/frontend:latest

deploy-frontend:
	gcloud run deploy myapp-frontend \
		--image europe-central2-docker.pkg.dev/myapp-devops/myapp-frontend-repo/frontend:latest \
		--platform managed \
		--region europe-central2 \
		--allow-unauthenticated \
		--port 80