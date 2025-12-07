# Sentinel: Advanced Facial Recognition and Deep Log Analysis System

## Overview
Sentinel is a modular, scalable system designed for advanced cybersecurity investigations. It combines high-accuracy facial recognition, real-time log analysis, and internet scouting capabilities into a unified platform.

## Modules Executed
- **System Management**: JWT Authentication, User Management (Neo4j).
- **Personnel Management**: Investigator profiles, Audit Logging (Elasticsearch).
- **Facial Recognition**: Identity verification engine (FaceNet/Dlib abstraction).
- **Log Analysis**: Real-time log ingestion and search.
- **Internet Scouting**: Web scraper for OSINT.
- **Cookie Collector**: Cookie risk analysis.
- **External Empowerment**: API wrappers for external DBs.
- **Threat Dashboard**: System stats aggregator.

## Getting Started

### Prerequisites
- Docker & Docker Compose
- *Or* Python 3.9+ and local Elasticsearch/Neo4j instances.

### Quick Start (Docker)
1.  **Run with Docker Compose**:
    ```bash
    docker-compose up -d --build
    ```
2.  **Access the System**:
    - **API Documentation (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)
    - **API Root**: [http://localhost:8000](http://localhost:8000)

### API Endpoints Overview
- `POST /token`: Login to get JWT.
- `POST /users/register`: Create account.
- `POST /facial-recognition/identify`: Upload image to ID face.
- `POST /logs/upload`: Upload log file for analysis.
- `POST /scout/analyze`: Scrape a website.
- `GET /dashboard/stats`: View system threat level.

## Architecture
- **Backend**: FastAPI (Python)
- **Database**: Elasticsearch (Logs/Audit), Neo4j (Users/Relationships)
- **Containerization**: Docker
