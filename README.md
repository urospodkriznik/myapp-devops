# MyApp DevOps - Full Stack Application

A comprehensive full-stack application demonstrating modern DevOps practices, security hardening, and monitoring capabilities.

## 🚀 Features

- **FastAPI Backend** with JWT authentication and role-based access control
- **Vue.js Frontend** with TypeScript
- **PostgreSQL Database** with migrations
- **Docker Containerization** with health checks
- **Security Hardening** with security headers, CORS, and HTTPS enforcement
- **Monitoring & Observability** with Loguru, Prometheus, and Grafana

## 🏗️ Architecture

```
Frontend (Vue.js) ↔ Backend (FastAPI) ↔ Database (PostgreSQL)
                           ↓
                    Monitoring Stack
                    (Prometheus + Grafana)
```

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone https://github.com/your-username/myapp-devops.git
cd myapp-devops
cp env.template .env
# Edit .env with your configuration
```

### 2. Start Application
```bash
# Main application
docker-compose up -d

# Monitoring stack (optional)
docker-compose -f docker-compose.monitoring.yml up -d
```

### 3. Access Services
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Grafana**: http://localhost:3001 (admin/admin)
- **Prometheus**: http://localhost:9090

## 🔒 Security Features

- JWT authentication with access/refresh tokens
- Role-based access control (Admin/User)
- Security headers (XSS, CSRF protection)
- CORS configuration
- HTTPS enforcement in production
- Environment-based secret management

## 📊 Monitoring

- **Structured Logging**: Loguru with rotation
- **Metrics**: Prometheus endpoint with custom metrics
- **Dashboards**: Grafana with real-time monitoring
- **Health Checks**: Application and container monitoring

## 📚 Documentation

- [Security Documentation](SECURITY.md)
- [Monitoring Documentation](MONITORING.md)
- [Environment Template](env.template)

## 🐳 Docker Services

- `backend`: FastAPI application
- `db`: PostgreSQL database
- `prometheus`: Metrics collection
- `grafana`: Monitoring dashboards

## 🧪 Testing

```bash
# Backend tests
cd backend && pytest

# Frontend tests
cd frontend && npm test
```

## 📈 Monitoring Usage

```bash
# View logs
docker-compose logs -f backend

# Check metrics
curl http://localhost:8000/metrics

# Health check
curl http://localhost:8000/healthz
```

## 🔧 Development

1. Create feature branch
2. Implement changes with tests
3. Update documentation
4. Submit pull request

## 🚀 Production Deployment

1. Configure production environment variables
2. Set up SSL certificates
3. Configure monitoring and alerting
4. Deploy with Docker Compose or Kubernetes

---

**Built with modern DevOps practices** | **Version**: 1.0.0 