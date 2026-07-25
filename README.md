# 🚗 CV Vehicle Analytics Service

An asynchronous REST API service built with **FastAPI** for vehicle detection and counting on images using **YOLOv8**, with results saved to **PostgreSQL** in a fully containerized **Docker** environment.

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat&logo=postgresql)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0_(Async)-red?style=flat)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat&logo=docker)
![YOLOv8](https://img.shields.io/badge/Ultralytics-YOLOv8-00FFFF?style=flat)

---

## 📌 Key Features

* **Computer Vision Inference:** Processes incoming images using YOLOv8 models to detect vehicles, buses, trucks, and other object classes.
* **Asynchronous Backend:** High-performance request processing built on FastAPI and `asyncpg`.
* **Data Storage & ORM:** Leverages SQLAlchemy 2.0 (Async Engine) for relational mappings in PostgreSQL (`DetectionTask` $\rightarrow$ `DetectedObject`).
* **Containerization & Orchestration:** Isolated Docker builds for both the application service and database, complete with health check dependencies.

---

## 🏗 Architecture & Project Structure

```cv-analytics-service/
├── app/
│   ├── ml/
│   │   ├── __init__.py
│   │   └── detector.py      # YOLOv8 inference & object detection logic
│   ├── __init__.py
│   ├── config.py          # Application configuration & env settings
│   ├── database.py        # Async engine & SQLAlchemy session setup
│   ├── main.py            # FastAPI entry point, lifespan management & routes
│   ├── models.py          # SQLAlchemy ORM models (DetectionTask, DetectedObject)
│   └── schemas.py         # Pydantic validation schemas
├── uploads/               # Directory for temporary uploaded images
├── .dockerignore
├── .env
├── .env.example
├── .gitignore
├── docker-compose.yaml    # Service orchestration (FastAPI + PostgreSQL)
├── Dockerfile             # Container build instructions for FastAPI
├── README.md              # Project documentation
├── requirements.txt       # Python dependencies
└── yolov8n.pt             # Pre-trained YOLOv8 weights file

🛠 Tech Stack
Language: Python 3.11+

Framework: FastAPI, Uvicorn

ML / CV: Ultralytics YOLOv8, OpenCV, Pillow

Database: PostgreSQL 15, asyncpg, SQLAlchemy 2.0

DevOps: Docker, Docker Compose

🚀 Quick Start
1. Clone the repository
Bash
git clone [https://github.com/your-username/cv-analytics-service.git](https://github.com/your-username/cv-analytics-service.git)
cd cv-analytics-service
2. Configure Environment Variables
Create a .env file in the root directory:

Фрагмент коду
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgrespassword
POSTGRES_DB=cv_analytics_db
POSTGRES_PORT=5433

DATABASE_URL=postgresql+asyncpg://postgres:postgrespassword@db:5432/cv_analytics_db
3. Run with Docker Compose
Build and launch the containers with a single command:

Bash
docker-compose up --build
The application will wait for the database health check to pass and launch the API at http://localhost:8000.

📡 API Endpoints
Once running, interactive Swagger/OpenAPI documentation is available at:

👉 http://localhost:8000/docs