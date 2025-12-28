# Deployment Guide - Android Agent Platform

**Version:** 1.0.0
**Date:** 2025-12-04
**Status:** Production Ready

---

## 📋 Overview

This guide covers deploying the Android Agent Platform using Docker containers for production environments.

### Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Internet                         │
└────────────────────┬────────────────────────────────┘
                     │
         ┌───────────▼───────────┐
         │  Nginx Reverse Proxy  │ (Port 80/443)
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────┐
         │   Frontend (Nginx)    │ (Port 80)
         └───────────┬───────────┘
                     │
         ┌───────────▼───────────┐
         │  Backend API (FastAPI)│ (Port 8000)
         └─────┬──────────┬──────┘
               │          │
       ┌───────▼───┐  ┌──▼──────┐
       │ PostgreSQL│  │  Redis  │
       └───────────┘  └─────────┘
```

---

## 🚀 Quick Start

### Prerequisites

- Docker 20.10+
- Docker Compose 2.0+
- 2GB RAM minimum
- 10GB disk space
- Android devices with Tailscale configured

### 1. Clone and Configure

```bash
# Clone repository
git clone <repository-url>
cd KUX

# Copy environment file
cp .env.docker.example .env

# Edit .env with your API keys
nano .env
```

### 2. Configure API Keys

Edit `.env` file:

```env
# Database
POSTGRES_PASSWORD=your_secure_password_here
DATABASE_URL=postgresql://agent:your_secure_password_here@postgres:5432/android_agent

# API Keys
NOTION_API_KEY=secret_xxxxx
NOTION_DATABASE_ID=xxxxx
TELEGRAM_BOT_TOKEN=123456789:ABCdef...
TELEGRAM_CHAT_ID=123456789
PUTER_API_KEY=your_puter_key
```

### 3. Configure Devices

Edit `config/devices.yaml`:

```yaml
devices:
  - id: pixel-th-1
    name: "Pixel 5 - Thailand Device 1"
    tailscale_ip: "100.x.x.x"  # Your actual Tailscale IP
    adb_port: 5555
    location: "Thailand"
    timezone: "Asia/Bangkok"
    enabled: true
```

### 4. Build and Start

```bash
# Build containers
docker-compose build

# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

### 5. Verify Deployment

```bash
# Check backend health
curl http://localhost:8000/api/health

# Check frontend
curl http://localhost/

# Check database
docker-compose exec postgres psql -U agent -d android_agent -c "\dt"
```

---

## 🔧 Production Configuration

### Database Migration

For production, use PostgreSQL instead of SQLite:

```bash
# Run database migrations
docker-compose exec backend python -m alembic upgrade head

# Verify tables
docker-compose exec postgres psql -U agent -d android_agent -c "\dt"
```

### Environment Variables

**Required:**
- `POSTGRES_PASSWORD` - Strong database password
- `NOTION_API_KEY` - Notion integration key
- `NOTION_DATABASE_ID` - Database ID
- `TELEGRAM_BOT_TOKEN` - Bot token from @BotFather
- `TELEGRAM_CHAT_ID` - Your chat ID
- `PUTER_API_KEY` - Puter.js API key

**Optional:**
- `DEBUG=false` - Disable debug mode in production
- `LOG_LEVEL=INFO` - Set logging level
- `CORS_ORIGINS` - Update with your domain

### SSL/HTTPS Setup

Add Nginx reverse proxy with Let's Encrypt:

```yaml
# docker-compose.yml additions
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    depends_on:
      - frontend
      - backend

  certbot:
    image: certbot/certbot
    volumes:
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    entrypoint: "/bin/sh -c 'trap exit TERM; while :; do certbot renew; sleep 12h & wait $${!}; done;'"
```

---

## 📊 Monitoring

### Health Checks

All services have built-in health checks:

```bash
# Backend health
curl http://localhost:8000/api/health

# Frontend health
curl http://localhost/health

# Database health
docker-compose exec postgres pg_isready

# Redis health
docker-compose exec redis redis-cli ping
```

### Logs

```bash
# View all logs
docker-compose logs -f

# View specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Container Stats

```bash
# Real-time stats
docker stats

# Disk usage
docker system df
```

---

## 🔄 Updates and Maintenance

### Update Application

```bash
# Pull latest code
git pull origin main

# Rebuild containers
docker-compose build --no-cache

# Restart services
docker-compose up -d

# Remove old images
docker image prune -f
```

### Database Backup

```bash
# Backup database
docker-compose exec postgres pg_dump -U agent android_agent > backup_$(date +%Y%m%d).sql

# Restore database
cat backup_20251204.sql | docker-compose exec -T postgres psql -U agent android_agent
```

### Cleanup

```bash
# Stop all services
docker-compose down

# Remove all data (WARNING: destructive)
docker-compose down -v

# Clean up unused resources
docker system prune -a --volumes
```

---

## 🐛 Troubleshooting

### Backend Won't Start

**Issue:** Backend container exits immediately

**Solutions:**
1. Check logs: `docker-compose logs backend`
2. Verify environment variables in `.env`
3. Ensure PostgreSQL is running: `docker-compose ps postgres`
4. Check database connection: `docker-compose exec backend python -c "from src.database.db import engine; print(engine)"`

### Frontend Can't Connect to Backend

**Issue:** API calls fail with CORS errors

**Solutions:**
1. Update `CORS_ORIGINS` in `.env`
2. Check nginx configuration in `frontend/nginx.conf`
3. Verify backend is accessible: `curl http://backend:8000/api/health`

### Database Connection Failed

**Issue:** Backend can't connect to PostgreSQL

**Solutions:**
1. Check PostgreSQL is running: `docker-compose ps postgres`
2. Verify credentials in `.env`
3. Check database logs: `docker-compose logs postgres`
4. Test connection: `docker-compose exec postgres psql -U agent -d android_agent`

### ADB Connection Issues

**Issue:** Can't connect to Android devices

**Solutions:**
1. Verify Tailscale is running on devices
2. Check device IPs in `config/devices.yaml`
3. Test ADB connection from backend container:
   ```bash
   docker-compose exec backend adb connect <tailscale_ip>:5555
   docker-compose exec backend adb devices
   ```

### Out of Memory

**Issue:** Containers crashing due to OOM

**Solutions:**
1. Increase Docker memory limit (Docker Desktop → Settings → Resources)
2. Add memory limits to `docker-compose.yml`:
   ```yaml
   services:
     backend:
       deploy:
         resources:
           limits:
             memory: 1G
   ```

---

## 🔐 Security Best Practices

### 1. Secrets Management

- **Never commit `.env` file to Git**
- Use Docker secrets in production:
  ```yaml
  secrets:
    postgres_password:
      external: true
  ```

### 2. Network Security

- Use private Docker networks
- Expose only necessary ports
- Enable firewall rules:
  ```bash
  # Allow only necessary ports
  ufw allow 80/tcp
  ufw allow 443/tcp
  ufw deny 8000/tcp  # Block direct backend access
  ```

### 3. Container Security

- Run containers as non-root user (already configured)
- Keep images updated: `docker-compose pull`
- Scan for vulnerabilities: `docker scan android-agent-backend`

### 4. Database Security

- Use strong passwords
- Limit database access to backend only
- Regular backups
- Enable SSL connections in production

---

## 📈 Performance Tuning

### Backend Optimization

```yaml
# docker-compose.yml
services:
  backend:
    environment:
      - WORKERS=4  # Adjust based on CPU cores
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

### PostgreSQL Tuning

```yaml
services:
  postgres:
    command: >
      postgres
      -c shared_buffers=256MB
      -c max_connections=200
      -c effective_cache_size=1GB
```

### Redis Configuration

```yaml
services:
  redis:
    command: redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
```

---

## 🌍 Production Deployment Checklist

### Pre-Deployment

- [ ] All API keys configured in `.env`
- [ ] Database password is strong and secure
- [ ] Device IPs updated in `config/devices.yaml`
- [ ] CORS origins updated for production domain
- [ ] SSL certificates obtained (if using HTTPS)
- [ ] Firewall rules configured
- [ ] Backup strategy in place

### Deployment

- [ ] Containers built successfully: `docker-compose build`
- [ ] All services started: `docker-compose up -d`
- [ ] Health checks passing for all services
- [ ] Database migrations completed
- [ ] Backend accessible: `curl http://localhost:8000/api/health`
- [ ] Frontend accessible: `curl http://localhost/`
- [ ] WebSocket connection working

### Post-Deployment

- [ ] Run E2E test (send WhatsApp message)
- [ ] Verify Notion sync working
- [ ] Verify Telegram notifications working
- [ ] Check logs for errors
- [ ] Setup monitoring and alerts
- [ ] Document deployment date and version

---

## 📞 Support

### Resources

- **Documentation:** See [README.md](README.md), [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Troubleshooting:** See [tests/README.md](backend/tests/README.md)
- **Issues:** GitHub Issues (if applicable)

### Common Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# Restart single service
docker-compose restart backend

# View logs
docker-compose logs -f backend

# Execute command in container
docker-compose exec backend python -m pytest

# Shell access
docker-compose exec backend bash
docker-compose exec frontend sh

# Database access
docker-compose exec postgres psql -U agent android_agent
```

---

## 🎯 Next Steps After Deployment

1. **Run E2E Test** - Follow [SETUP_GUIDE.md](SETUP_GUIDE.md) Section 8
2. **Setup Monitoring** - Configure Prometheus/Grafana
3. **Configure Alerts** - Setup Telegram alerts for errors
4. **Backup Schedule** - Automate daily database backups
5. **CI/CD Pipeline** - Setup GitHub Actions (see Phase 5 in roadmap)

---

**Android Agent Platform v1.0.0 - Production Deployment Ready** 🚀

*Last Updated: 2025-12-04*
