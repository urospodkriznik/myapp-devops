include .env
export

# === COMPOSE ALIASES ===
COMPOSE_DEV=docker-compose -f docker-compose.dev.yml
COMPOSE_BASE=docker-compose -f docker-compose.yml

# === DOCKER + COMPOSE ===

dev:
	$(COMPOSE_DEV) up --build

prod:
	$(COMPOSE_BASE) up --build -d

down:
	$(COMPOSE_DEV) down -v --remove-orphans
	$(COMPOSE_BASE) down -v --remove-orphans

ps:
	docker-compose ps

restart-dev:
	$(COMPOSE_DEV) down -v --remove-orphans
	$(COMPOSE_DEV) up --build

rebuild-backend-dev:
	$(COMPOSE_DEV) build backend

logs-dev:
	$(COMPOSE_DEV) logs -f backend

# === MIGRATIONS ===

# Create new Alembic migration script from model changes
makemigrations-dev:
	$(COMPOSE_DEV) exec backend alembic revision --autogenerate -m "auto"

# Apply migrations to dev DB (inside container)
migrations-dev:
	$(COMPOSE_DEV) exec backend alembic upgrade head

# Apply migrations to local DB via built prod image (needs Cloud SQL proxy running)
migrate-local:
	docker run --rm -it \
		-e DATABASE_URL="postgresql+asyncpg://postgres:$(POSTGRES_PASSWORD)@host.docker.internal:5432/app_db" \
		-v $(PWD)/backend:/app \
		europe-central2-docker.pkg.dev/$(GCP_PROJECT_ID)/$(GCP_BACKEND_REPO)/backend:latest \
		alembic upgrade head

# Apply to remote DB via local proxy
migrate-prod:
	docker run --rm -it \
		-e DATABASE_URL="postgresql+asyncpg://postgres:$(POSTGRES_PASSWORD)@host.docker.internal:$(SQL_PROXY_PORT)/app_db" \
		-v $(PWD)/backend:/app \
		europe-central2-docker.pkg.dev/$(GCP_PROJECT_ID)/$(GCP_BACKEND_REPO)/backend:latest \
		alembic upgrade head

# === CLOUD SQL PROXY ===

SQL_INSTANCE=myapp-devops:europe-central2:myapp-postgres
SQL_PROXY_PORT=5433
SQL_PROXY_PROD_PORT=9999

run-proxy:
	./cloud-sql-proxy --port=$(SQL_PROXY_PORT) $(SQL_INSTANCE)

proxy-prod:
	./cloud-sql-proxy --port=$(SQL_PROXY_PROD_PORT) $(SQL_INSTANCE)

# === BACKEND PROD ===

build-prod:
	docker build --platform linux/amd64 -f backend/Dockerfile \
		-t europe-central2-docker.pkg.dev/myapp-devops/myapp-backend-repo/backend:latest ./backend

build-prod-nocache:
	docker build --platform linux/amd64 --no-cache -f backend/Dockerfile \
		-t europe-central2-docker.pkg.dev/myapp-devops/myapp-backend-repo/backend:latest ./backend

push-prod:
	docker push europe-central2-docker.pkg.dev/myapp-devops/myapp-backend-repo/backend:latest

deploy-prod:
	gcloud run deploy myapp-backend \
		--image europe-central2-docker.pkg.dev/myapp-devops/myapp-backend-repo/backend:latest \
		--platform managed \
		--region europe-central2 \
		--allow-unauthenticated \
		--port 8000 \
		--add-cloudsql-instances=$(SQL_INSTANCE) \
		--update-secrets "DATABASE_URL=DATABASE_URL_PROD:latest"

# === FRONTEND PROD ===

build-frontend:
	docker build --platform linux/amd64 -f frontend/Dockerfile \
		-t europe-central2-docker.pkg.dev/myapp-devops/myapp-frontend-repo/frontend:latest ./frontend

push-frontend:
	docker push europe-central2-docker.pkg.dev/myapp-devops/myapp-frontend-repo/frontend:latest

deploy-frontend:
	gcloud run deploy myapp-frontend \
		--image europe-central2-docker.pkg.dev/myapp-devops/myapp-frontend-repo/frontend:latest \
		--platform managed \
		--region europe-central2 \
		--allow-unauthenticated \
		--port 80