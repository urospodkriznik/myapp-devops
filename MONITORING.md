# Monitoring & Observability Documentation

## Overview

This document describes the monitoring and observability setup for the MyApp DevOps project, including logging, metrics, and alerting capabilities.

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   MyApp API     │    │   Prometheus    │    │     Grafana     │
│   (FastAPI)     │───▶│   (Metrics)     │───▶│   (Dashboard)   │
│                 │    │                 │    │                 │
│ • Loguru Logs   │    │ • HTTP Metrics  │    │ • Visualizations│
│ • Prometheus    │    │ • Custom Metrics│    │ • Alerts        │
│   Metrics       │    │ • Health Checks │    │ • Dashboards    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Components

### 1. Application Logging (Loguru)

#### Configuration
- **Log Level**: Configurable via `LOG_LEVEL` environment variable
- **Log File**: `logs/app.log` with automatic rotation
- **Rotation**: 10MB files, 7 days retention
- **Format**: Structured logging with timestamps and context

#### Log Types
- **Request Logs**: All HTTP requests with timing and status codes
- **Authentication Logs**: Login attempts, successes, and failures
- **Authorization Logs**: Access to protected resources
- **Error Logs**: Detailed error information for debugging
- **Performance Logs**: Request timing and database operations

#### Example Log Output
```
2024-12-19 10:30:15 | INFO | Request started | method=POST | url=/login | client_ip=192.168.1.100
2024-12-19 10:30:15 | INFO | Login attempt for user: user@example.com
2024-12-19 10:30:15 | INFO | Successful login for user: user@example.com
2024-12-19 10:30:15 | INFO | Request completed | method=POST | url=/login | status_code=200 | process_time=0.0456
```

### 2. Metrics Collection (Prometheus)

#### Available Metrics

##### HTTP Metrics
- `http_requests_total`: Total number of HTTP requests
- `http_request_duration_seconds`: Request duration histogram
- `http_request_size_bytes`: Request size in bytes
- `http_response_size_bytes`: Response size in bytes

##### Custom Application Metrics
- `login_attempts_total`: Total login attempts
- `login_failures_total`: Failed login attempts
- `user_registrations_total`: New user registrations
- `database_connections_active`: Active database connections

##### System Metrics
- `process_cpu_seconds_total`: CPU usage
- `process_resident_memory_bytes`: Memory usage
- `process_open_fds`: Open file descriptors

#### Metrics Endpoint
- **URL**: `http://localhost:8000/metrics`
- **Format**: Prometheus text format
- **Access**: Public (for monitoring)

### 3. Visualization (Grafana)

#### Dashboard Features
- **Request Rate**: Requests per second over time
- **Total Requests**: Cumulative request count
- **Response Times**: Average and percentile response times
- **Error Rates**: 4xx and 5xx error rates
- **Authentication Events**: Login attempts and failures
- **System Resources**: CPU, memory, and disk usage

#### Access
- **URL**: `http://localhost:3001`
- **Username**: `admin`
- **Password**: `admin`
- **Default Dashboard**: MyApp Monitoring Dashboard

## Setup Instructions

### 1. Development Environment

#### Start Monitoring Stack
```bash
# Start the main application
docker-compose up -d

# Start monitoring services
docker-compose -f docker-compose.monitoring.yml up -d
```

#### Verify Setup
```bash
# Check application health
curl http://localhost:8000/healthz

# Check metrics endpoint
curl http://localhost:8000/metrics

# Check Prometheus
curl http://localhost:9090/-/healthy

# Check Grafana
curl http://localhost:3001/api/health
```

### 2. Production Environment

#### Environment Variables
```bash
# Required for production
ENVIRONMENT=production
JWT_SECRET=your-super-secret-jwt-key
CORS_ORIGINS=https://yourdomain.com
ALLOWED_HOSTS=yourdomain.com
FORCE_HTTPS=true
```

#### Security Considerations
- Change default Grafana credentials
- Use HTTPS for all monitoring endpoints
- Restrict access to monitoring ports
- Use strong passwords for all services

## Usage Guide

### 1. Viewing Logs

#### Application Logs
```bash
# View real-time logs
docker-compose logs -f backend

# View log file directly
docker exec -it myapp-devops-backend-1 tail -f logs/app.log
```

#### Container Logs
```bash
# View all container logs
docker-compose logs

# View specific service logs
docker-compose logs backend
docker-compose logs db
```

### 2. Monitoring Metrics

#### Prometheus Queries
```promql
# Request rate over 5 minutes
rate(http_requests_total[5m])

# Total requests by status code
http_requests_total

# 95th percentile response time
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# Error rate
rate(http_requests_total{status=~"5.."}[5m])
```

#### Grafana Dashboard
1. Open Grafana at `http://localhost:3001`
2. Login with `admin/admin`
3. Navigate to "MyApp Monitoring Dashboard"
4. Explore different panels and time ranges

### 3. Setting Up Alerts

#### Prometheus Alert Rules
Create `monitoring/alerts.yml`:
```yaml
groups:
  - name: myapp_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors per second"

      - alert: HighResponseTime
        expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High response time detected"
          description: "95th percentile response time is {{ $value }} seconds"
```

#### Grafana Alerts
1. Go to Alerting in Grafana
2. Create new alert rule
3. Set conditions and thresholds
4. Configure notification channels

## Troubleshooting

### Common Issues

#### 1. Metrics Not Showing
```bash
# Check if metrics endpoint is accessible
curl http://localhost:8000/metrics

# Check Prometheus targets
curl http://localhost:9090/api/v1/targets

# Check Prometheus logs
docker-compose -f docker-compose.monitoring.yml logs prometheus
```

#### 2. Grafana Not Loading
```bash
# Check Grafana health
curl http://localhost:3001/api/health

# Check Grafana logs
docker-compose -f docker-compose.monitoring.yml logs grafana

# Reset Grafana data (if needed)
docker-compose -f docker-compose.monitoring.yml down
docker volume rm myapp-devops_grafana_data
docker-compose -f docker-compose.monitoring.yml up -d
```

#### 3. Logs Not Appearing
```bash
# Check log file permissions
docker exec -it myapp-devops-backend-1 ls -la logs/

# Check application logs
docker-compose logs backend

# Restart application
docker-compose restart backend
```

### Performance Tuning

#### Prometheus Configuration
```yaml
global:
  scrape_interval: 15s  # Adjust based on needs
  evaluation_interval: 15s

scrape_configs:
  - job_name: 'backend'
    scrape_interval: 10s  # More frequent for critical metrics
    scrape_timeout: 5s
```

#### Grafana Configuration
```ini
[server]
http_port = 3000
domain = localhost

[security]
admin_user = admin
admin_password = your-secure-password

[users]
allow_sign_up = false
```

## Best Practices

### 1. Logging
- Use structured logging with consistent fields
- Include correlation IDs for request tracing
- Log at appropriate levels (DEBUG, INFO, WARNING, ERROR)
- Rotate logs to prevent disk space issues
- Never log sensitive information (passwords, tokens)

### 2. Metrics
- Use descriptive metric names
- Include appropriate labels for filtering
- Avoid high-cardinality labels
- Set reasonable scrape intervals
- Monitor metric cardinality

### 3. Alerting
- Set meaningful thresholds
- Use different severity levels
- Include helpful alert descriptions
- Test alert conditions
- Have escalation procedures

### 4. Security
- Use strong passwords for all services
- Enable authentication for monitoring endpoints
- Use HTTPS in production
- Restrict access to monitoring ports
- Regularly update monitoring tools

## Future Enhancements

### Planned Features
- **Distributed Tracing**: Jaeger or Zipkin integration
- **Log Aggregation**: ELK stack or Loki
- **Advanced Alerting**: AlertManager with multiple channels
- **Custom Dashboards**: Business-specific metrics
- **Performance Profiling**: Application performance monitoring

### Monitoring Roadmap
- **Q1**: Distributed tracing implementation
- **Q2**: Advanced alerting and notification
- **Q3**: Business metrics and dashboards
- **Q4**: Performance optimization and tuning

## Resources

### Documentation
- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Loguru Documentation](https://loguru.readthedocs.io/)

### Tools
- [Prometheus Query Language](https://prometheus.io/docs/prometheus/latest/querying/)
- [Grafana Dashboard Templates](https://grafana.com/grafana/dashboards/)
- [Prometheus Alert Rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/)

---

**Last Updated**: December 2024  
**Version**: 1.0  
**Maintainer**: DevOps Team 