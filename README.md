# MyApp DevOps – Full Stack Application

A modern, production-ready full-stack application demonstrating advanced DevOps, security, and monitoring practices. This project showcases expertise in building scalable, secure, and observable systems using FastAPI, Vue 3, and a robust cloud-native toolchain. Designed to meet the standards of professional software teams, it is ready for real-world deployment and extensibility.

---

## 🚀 Project Overview

This application exemplifies:
- **End-to-end full stack development** with FastAPI (Python) and Vue 3 (TypeScript)
- **Enterprise-grade DevOps workflows** including CI/CD, Docker, and cloud deployment
- **Comprehensive security and monitoring** for production environments
- **Clean, maintainable code** and modern development practices

---

## 🏆 Key Features

- **FastAPI Backend**
  - Secure JWT authentication and refresh tokens
  - Role-based access control (Admin/User)
  - User registration, login, and management
  - Hardened API endpoints with input validation and password hashing
  - Structured logging (Loguru), Prometheus metrics, and health checks
  - Database migrations (Alembic) and environment-based configuration

- **Vue 3 + TypeScript Frontend**
  - Modern, responsive UI with Vuetify
  - Authentication flows and protected routes
  - Role-based UI and CRUD operations
  - Seamless integration with backend API
  - Automated testing (Vitest) and linting (ESLint)

- **DevOps & CI/CD**
  - Fully containerized stack (Docker, Docker Compose)
  - Automated build, test, and deployment pipelines (GitHub Actions, GCP Cloud Run)
  - Health checks and environment management
  - Makefile for streamlined developer operations

- **Monitoring & Observability**
  - Prometheus metrics and custom application monitoring
  - Grafana dashboards for real-time insights
  - Loguru for structured, actionable logs

- **Security**
  - Industry best practices: HTTPS, security headers, secret management, environment separation, and production hardening
  - Detailed [Security Documentation](SECURITY.md)

- **Testing**
  - Backend: pytest
  - Frontend: Vitest

- **Documentation**
  - Clear setup, security, monitoring, and environment configuration guides

---

## 🏗️ Architecture

```
Frontend (Vue 3) ↔ Backend (FastAPI) ↔ Database (PostgreSQL)
                           ↓
                    Monitoring Stack
                    (Prometheus + Grafana)
```

---

## ⚡ Development Quick Start

### 1. Backend, Database, and Monitoring (Dev Mode)
Start all backend services, database, and monitoring stack using Docker Compose (dev configuration):

```bash
make dev
```
- This will launch the FastAPI backend, PostgreSQL database, Prometheus, and Grafana using `docker-compose.dev.yml`.

### 2. Frontend (Dev Mode)
The frontend is developed and run separately for optimal developer experience:

```bash
cd frontend
npm install
npm run dev
```
- This starts the Vue 3 development server with hot reload at http://localhost:5173

### 3. Access Services
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Grafana**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9090

---

## 🐳 Services
- `backend`: FastAPI application
- `frontend`: Vue 3 application
- `db`: PostgreSQL database
- `prometheus`: Metrics collection
- `grafana`: Monitoring dashboards

---

## 🔒 Security Highlights
- JWT authentication and refresh tokens
- Role-based access control (Admin/User)
- Security headers, CORS, HTTPS enforcement
- Environment-based secret management
- Input validation and password hashing (bcrypt)
- See [SECURITY.md](SECURITY.md) for full details

---

## 📊 Monitoring & Observability
- Structured logging (Loguru, rotation)
- Prometheus metrics endpoint (`/metrics`)
- Grafana dashboards (real-time monitoring)
- Health checks for application and containers
- See [MONITORING.md](MONITORING.md) for full details

---

## 🧪 Testing
```bash
# Backend tests
cd backend && pytest

# Frontend tests
cd frontend && npm test
```

---

## ⚙️ DevOps & CI/CD
- **Dockerized**: All services containerized for consistency and portability
- **Docker Compose**: Local orchestration for full stack
- **GitHub Actions**: CI/CD pipelines for build, push, and deploy (GCP Cloud Run)
- **Makefile**: Build and deploy automation
- **Health checks**: Docker and application level

---

## 🛠️ Development Workflow
1. Create a feature branch
2. Implement changes with tests
3. Update documentation
4. Submit a pull request

---

## 📚 Documentation
- [Security Documentation](SECURITY.md)
- [Monitoring Documentation](MONITORING.md)
- [Environment Template](env.template)
- API docs: http://localhost:8000/docs

---

Developed by Uroš Podrkižnik.

**Built with modern DevOps practices | Version: 1.0.0** 