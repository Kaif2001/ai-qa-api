# AI QA API

A production-oriented AI Question & Answer API built with FastAPI, Google Gemini, PostgreSQL, Redis, Docker, JWT authentication, and Prometheus metrics.

## Project Overview

This project provides a secure REST API for authenticated AI question answering.

The API includes:

- JWT-based authentication
- AI question answering using Google Gemini
- PostgreSQL chat history storage
- Redis-based rate limiting
- Prometheus metrics
- Health checks for PostgreSQL and Redis
- Docker and Docker Compose support
- Automated API tests
- Production scaling and security documentation

## Architecture

```text
Users
  |
  v
Load Balancer / Reverse Proxy
  |
  v
FastAPI Application
  |
  +----> Redis
  |       |
  |       +---- Rate Limiting
  |
  +----> PostgreSQL
  |       |
  |       +---- Chat History
  |
  +----> LLM Gateway
          |
          +---- Google Gemini

For the detailed architecture and production scaling approach, see:

SCALING.md
MIGRATION.md
LLM_PRODUCTION.md
Tech Stack
Python 3.10
FastAPI
Google Gemini API
PostgreSQL 16
Redis 7
SQLAlchemy
JWT
Docker
Docker Compose
Prometheus
Pytest
Project Structure
ai-qa-api/
│
├── app/
│   ├── auth.py
│   ├── database.py
│   ├── llm_gateway.py
│   ├── main.py
│   ├── models.py
│   └── redis_client.py
│
├── tests/
│   ├── test_auth.py
│   ├── test_health.py
│   └── test_metrics.py
│
├── .dockerignore
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
│
├── AUTHENTICATION.md
├── LLM_PRODUCTION.md
├── MIGRATION.md
├── SCALING.md
└── SECURITY.md
API Endpoints
Login
POST /auth/login

Form data:

username=admin
password=admin123

Returns a JWT access token.

The credentials above are demo credentials for this assessment implementation. Production applications should use database-backed users, secure password hashing, and an external identity provider where appropriate.

Chat
POST /chat

Requires:

Authorization: Bearer <JWT_TOKEN>

Request:

{
  "question": "What is DevOps?"
}

The response contains the generated answer and stored chat ID.

Health
GET /health

Checks:

FastAPI application
PostgreSQL
Redis

Example:

{
  "status": "healthy",
  "database": "connected",
  "redis": "connected"
}
Metrics
GET /metrics

Exposes Prometheus metrics including:

chat_requests_total
chat_errors_total
chat_request_duration_seconds
llm_input_tokens_total
llm_output_tokens_total

Environment Variables

Create a .env file in the project root.

Example:

JWT_SECRET=your_jwt_secret_here
GEMINI_API_KEY=your_gemini_api_key_here
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_qa_api
REDIS_HOST=localhost
REDIS_PORT=6379

Never commit .env or real API keys to Git.

Use .env.example as the configuration template.

Running Locally
1. Create virtual environment
python -m venv venv

Activate it:

.\venv\Scripts\Activate.ps1
2. Install dependencies
pip install -r requirements.txt
3. Start PostgreSQL and Redis

The easiest option is Docker Compose:

docker compose up -d postgres redis
4. Start the API
uvicorn app.main:app --reload

API:

http://localhost:8000

Swagger documentation:

http://localhost:8000/docs
Running with Docker Compose

Build the API image:

docker compose build api

Start all services:

docker compose up -d

Check containers:

docker compose ps

Check API health:

Invoke-RestMethod http://localhost:8000/health

Expected result:

status    database   redis
------    --------   -----
healthy   connected  connected
Testing

Run the complete test suite:

python -m pytest -v

Current test coverage includes:

Successful login
Invalid login
Unauthorized chat request
PostgreSQL and Redis health check
Prometheus metrics endpoint

The current test suite passes all 6 tests.

The real Gemini /chat endpoint should not be repeatedly called during testing because external LLM API quotas and rate limits apply.

Rate Limiting

The API uses Redis to limit authenticated chat requests.

The current implementation allows up to 10 chat requests per user within a 60-second window.

When the limit is exceeded:

429 Too Many Requests

is returned.

For production, the rate limiter can be improved using atomic Redis operations or Lua scripts.

LLM Gateway

The application uses a dedicated LLM gateway module:

app/llm_gateway.py

The gateway provides:

LLM API integration
Retry handling for temporary failures
Exponential backoff
LLM rate-limit handling

Production LLM strategies are documented in:

LLM_PRODUCTION.md

This includes discussion of:

Provider fallback
Token optimization
Cost controls
Rate limiting
Retry strategies
Model selection
Authentication

The current API uses JWT authentication.

Authentication documentation covers:

JWT
OAuth2
OIDC
SAML
SSO
RBAC

See:

AUTHENTICATION.md
Security

Security considerations are documented in:

SECURITY.md

The Docker image does not copy the .env file into the container image.

.env is excluded using .dockerignore and .gitignore.

Production deployments should additionally use:

Secret management
HTTPS/TLS
Secure password storage
External identity providers
Least-privilege IAM
Network isolation
Container image scanning
Centralized logging
Monitoring and alerting
Scaling

The application can be scaled horizontally by running multiple FastAPI instances behind a load balancer.

Example:

                  Load Balancer
                       |
          +------------+------------+
          |            |            |
      FastAPI 1    FastAPI 2    FastAPI 3
          |            |            |
          +------------+------------+
                       |
              Redis / PostgreSQL
                       |
                  LLM Gateway

The scaling strategy for approximately 100 RPS to 500 RPS is documented in:

SCALING.md
EC2 to Large-Scale Deployment

The migration approach from a single EC2 deployment toward a larger production environment is documented in:

MIGRATION.md

The document covers:

Horizontal scaling
Load balancing
Database scaling
Redis
Monitoring
Container orchestration
High availability
Monitoring

Prometheus metrics are available at:

GET /metrics

Important application metrics include:

chat_requests_total
chat_errors_total

These metrics can be collected by Prometheus and visualized using Grafana.

Production Considerations

This assessment implementation is designed to demonstrate production-oriented concepts.

Before a real production deployment, the following should be strengthened:

Replace demo credentials with database-backed authentication
Use a production identity provider where required
Store secrets in a secret manager
Use HTTPS
Add centralized logging
Add distributed tracing
Add stronger Redis rate limiting
Add LLM provider fallback
Add queue-based asynchronous processing for long-running workloads
Add database migrations
Add container vulnerability scanning
Add CI/CD deployment automation
Add alerting and SLO monitoring
Documentation

Additional design documents:

Document	Purpose
AUTHENTICATION.md	Authentication, OAuth2, OIDC, SAML, SSO and RBAC
LLM_PRODUCTION.md	LLM reliability, fallback, cost and token strategies
MIGRATION.md	EC2 to larger-scale production migration
SCALING.md	Scaling from approximately 100 RPS to 500 RPS
SECURITY.md	Production security considerations
Docker Services

Docker Compose runs:

Service	Port	Purpose
API	8000	FastAPI application
PostgreSQL	5432	Chat history database
Redis	6379	Rate limiting and caching
Current Verification

The project has been verified with:

6/6 automated tests passing
Docker API container running
PostgreSQL connected
Redis connected
Health endpoint healthy
Metrics endpoint working
Git working tree clean
License

This project was created as a technical assessment project.
