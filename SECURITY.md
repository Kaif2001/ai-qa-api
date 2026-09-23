# Security and Production Readiness

## Secrets

Secrets should never be committed to Git or baked into Docker images.

Sensitive values include:

- JWT secret
- LLM API key
- Database credentials
- Redis credentials

Production deployments should use environment variables or a dedicated secrets-management system.

## JWT Security

JWT tokens should:

- Have an expiration time
- Use a strong signing secret or asymmetric signing keys
- Be validated on protected endpoints
- Validate expiration
- Validate issuer and audience when applicable
- Be transmitted only over HTTPS

## Password Security

Passwords should never be stored as plain text.

Production authentication should use secure password hashing or delegate authentication to an established identity provider.

## API Security

The API should use:

- HTTPS/TLS
- JWT authentication
- RBAC authorization
- Request validation
- Rate limiting
- Controlled error responses

## Input Validation

The `/chat` endpoint validates the question length before processing the request.

This helps prevent unexpectedly large requests from reaching the LLM provider.

## Rate Limiting

Redis-based rate limiting protects the API from excessive requests.

Rate limits can be configured based on:

- User
- IP address
- API key
- Endpoint

Production limits should be selected based on expected traffic and business requirements.

## Database Security

Production PostgreSQL should use:

- Strong credentials
- TLS where required
- Restricted network access
- Connection pooling
- Regular backups
- Least-privilege database users

## Docker Security

Production containers should:

- Avoid storing secrets in images
- Run with only required permissions
- Use minimal base images
- Keep dependencies updated
- Avoid unnecessary packages
- Scan images for known vulnerabilities

## Logging

Logs should contain useful operational information without exposing sensitive information.

Do not log:

- Passwords
- JWT access tokens
- API keys
- Database passwords
- Sensitive user information

## Monitoring

The application exposes Prometheus-compatible metrics through `/metrics`.

Production monitoring should track:

- Request rate
- Error rate
- Response latency
- CPU
- Memory
- Database health
- Redis health
- LLM failures
- LLM latency

## Health Checks

The application provides a `/health` endpoint.

Production deployments can additionally use readiness checks that verify required dependencies such as PostgreSQL and Redis before sending traffic to an instance.

## Least Privilege

Each component should have only the permissions it requires.

Examples:

- Application database user should not have unnecessary administrative privileges.
- API containers should not require host-level privileges.
- Cloud IAM permissions should be limited to required resources.

## Production Goal

The security architecture should protect:

- User authentication
- API access
- Application secrets
- Database data
- LLM credentials
- Infrastructure
- Operational logs