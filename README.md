# ⛅ Weather CI/CD App
## https://techcode.online/

A production-grade Flask weather application deployed via a **3-stage CI/CD pipeline** using GitHub Actions, Docker Hub, and AWS EC2.

---

## 🏗️ Architecture

```
GitHub Push → GitHub Actions CI/CD → Docker Hub → AWS EC2
                  │
          ┌───────┴────────┐
          │                │
    Stage 1          Stage 2          Stage 3
  Build & Test    Docker Build     Deploy to EC2
   (Python)         & Push          (SSH + Run)
```

---

## 📁 Project Structure

```
weather-cicd-app/
├── app.py                        # Flask application
├── requirements.txt              # Python dependencies
├── Dockerfile                    # Multi-stage Docker build
├── .dockerignore
├── .gitignore
├── templates/
│   └── index.html                # Weather UI
└── .github/
    └── workflows/
        └── ci-cd.yml             # 3-stage CI/CD pipeline
```

---

## 🚀 Quick Start (Local)

### Option A — Run with Python
```bash
git clone https://github.com/YOUR_USERNAME/weather-cicd-app.git
cd weather-cicd-app

pip install -r requirements.txt

export WEATHER_API_KEY=your_openweathermap_api_key
python app.py
# → Visit http://localhost:5000
```

### Option B — Run with Docker
```bash
docker build -t weather-cicd-app .

docker run -d \
  -p 5000:5000 \
  -e WEATHER_API_KEY=your_api_key \
  --name weather-cicd-app \
  weather-cicd-app

# → Visit http://localhost:5000
```

---

## 🔑 Get a Free API Key

1. Go to [openweathermap.org](https://openweathermap.org/api)
2. Sign up (free)
3. Copy your API key from the dashboard
4. API key activates within ~10 minutes

---

## ⚙️ GitHub Actions — CI/CD Pipeline

The pipeline has **3 stages** and triggers on every push to `main`:

| Stage | Name | What it does |
|-------|------|-------------|
| 1 | Build & Test | Installs deps, runs health & route tests |
| 2 | Docker Build & Push | Builds multi-stage image, pushes to Docker Hub with SHA tag + `latest` |
| 3 | Deploy to EC2 | SSH into EC2, pulls image, replaces container, validates health |

### Required GitHub Secrets

Go to **Settings → Secrets → Actions** and add:

| Secret | Description |
|--------|-------------|
| `DOCKER_USERNAME` | Your Docker Hub username |
| `DOCKER_PASSWORD` | Docker Hub password or access token |
| `EC2_HOST` | EC2 public IP (e.g. `13.234.56.78`) |
| `EC2_USER` | SSH user (`ubuntu` for Ubuntu AMIs) |
| `EC2_SSH_KEY` | Contents of your `.pem` private key file |
| `WEATHER_API_KEY` | OpenWeatherMap API key |

---

## 🖥️ AWS EC2 Setup

### 1. Launch EC2 Instance
- **AMI**: Ubuntu Server 24.04 LTS
- **Instance type**: t2.micro (Free Tier)
- **Security Group inbound rules**:
  - Port 22 (SSH) — your IP
  - Port 80 (HTTP) — 0.0.0.0/0

### 2. Install Docker on EC2
```bash
ssh -i your-key.pem ubuntu@YOUR_EC2_IP

# Install Docker
sudo apt update && sudo apt install -y docker.io
sudo systemctl enable --now docker
sudo usermod -aG docker ubuntu

# Log out and back in for group changes
exit
```

### 3. Add Secrets to GitHub
```bash
# Copy your .pem key contents for EC2_SSH_KEY:
cat your-key.pem
```

### 4. Push to main — pipeline runs automatically!
```bash
git add .
git commit -m "Initial deployment"
git push origin main
```

---

## 🌐 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page with search form |
| `/` | POST | Fetch weather for city |
| `/health` | GET | Health check → `{"status": "ok"}` |

---

## 🐳 Docker Details

- **Base image**: `python:3.12-alpine` (minimal, ~50MB)
- **Multi-stage build**: builder stage installs deps; production stage is lean
- **Non-root user**: `appuser` for security
- **HEALTHCHECK**: polls `/health` every 30s
- **WSGI server**: Gunicorn with 2 workers

---

## 🔄 Rolling Deployment Strategy

The pipeline uses a **stop → pull → start** rolling strategy:
1. Pull new image (zero downtime during pull)
2. Stop old container
3. Start new container immediately
4. Health check validates before marking success

---

## 🛠️ Tech Stack

| Technology | Role |
|------------|------|
| Python + Flask | Web framework |
| Gunicorn | Production WSGI server |
| Docker (Alpine) | Containerization |
| GitHub Actions | CI/CD orchestration |
| Docker Hub | Container registry |
| AWS EC2 | Cloud hosting |
| OpenWeatherMap API | Weather data |

# Deployed via CI/CD Pipeline
End ..

