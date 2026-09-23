# Scaling Strategy

## Traffic Scenario

The AI QA API should support approximately 100 requests per second during normal traffic and handle spikes up to 500 requests per second.

## Normal Traffic - 100 RPS

For normal traffic, multiple FastAPI instances can run behind a load balancer.

```text
Users
   |
   v
Load Balancer
   |
   +---- FastAPI Instance 1
   |
   +---- FastAPI Instance 2
   |
   +---- FastAPI Instance 3

The load balancer distributes requests across the available API instances.

Peak Traffic - 500 RPS

When traffic increases, the API can scale horizontally by adding more FastAPI instances.

Users
   |
   v
Load Balancer
   |
   +---- FastAPI Instance 1
   +---- FastAPI Instance 2
   +---- FastAPI Instance 3
   +---- FastAPI Instance 4
   +---- FastAPI Instance 5
   +---- Additional Instances

The actual number of instances should be determined through load testing and application performance measurements rather than using a fixed server count.

Redis

Redis is used for distributed rate limiting.

It prevents a single user from sending excessive requests and protects the API and downstream LLM service during traffic spikes.

Redis can also be used for caching frequently requested data when appropriate.

PostgreSQL

PostgreSQL stores chat history and application data.

For higher traffic, the database can use:

Connection pooling
Proper database indexes
Read replicas when required
Automated backups
Managed PostgreSQL services
LLM Gateway

The LLM Gateway separates the application from the external LLM provider.

FastAPI
   |
   v
LLM Gateway
   |
   +---- Rate Limiting
   +---- Timeout
   +---- Retry
   +---- Error Handling
   +---- Fallback Provider
   |
   v
LLM Provider

This allows the API to handle LLM provider rate limits and temporary failures without exposing provider-specific logic throughout the application.

Queue for Traffic Spikes

For workloads that do not require an immediate response, a queue can be introduced.

FastAPI
   |
   v
Queue
   |
   v
Worker
   |
   v
LLM Gateway
   |
   v
LLM Provider

The queue helps absorb temporary traffic spikes and prevents downstream services from being overloaded.

Monitoring and Autoscaling

The application exposes Prometheus-compatible metrics through /metrics.

Production deployment can use monitoring and autoscaling to increase or decrease FastAPI instances based on:

Request rate
CPU usage
Memory usage
Request latency
Error rate
Queue depth
Summary

The scaling approach is based on horizontal scaling, distributed rate limiting, database connection management, LLM gateway protection, optional asynchronous queues, and monitoring.

The system can start with multiple FastAPI instances for approximately 100 RPS and add additional instances as traffic approaches 500 RPS. Actual capacity should be validated through load testing.