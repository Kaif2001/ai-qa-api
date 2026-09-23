# Authentication and Authorization

## Current Authentication

The AI QA API currently uses JWT-based authentication.

The `/auth/login` endpoint validates the user credentials and returns a JWT access token.

```text
User
  |
  v
/auth/login
  |
  v
JWT Access Token
  |
  v
Protected API

The /chat endpoint requires a valid Bearer token.

JWT

JWT is a token format used to securely transfer claims between the client and the API.

The current application uses:

HS256 signing algorithm
JWT expiration
Username as the subject claim
Bearer authentication

The API validates the token before allowing access to protected endpoints.

OAuth2

OAuth2 is an authorization framework used to allow applications to access protected resources.

In a production system, an external identity provider can issue access tokens instead of maintaining authentication directly inside the application.

OpenID Connect

OpenID Connect (OIDC) is an authentication layer built on top of OAuth2.

A production architecture can use an OIDC provider for user authentication.

User
  |
  v
Identity Provider
  |
  v
OIDC Authentication
  |
  v
Access Token / ID Token
  |
  v
FastAPI

Examples of identity providers include enterprise identity platforms and cloud identity services.

SAML

SAML is an enterprise authentication and SSO protocol commonly used with corporate identity providers.

It can be used when an organization already has an enterprise identity system that supports SAML-based SSO.

The application can integrate with the identity provider while keeping authorization logic inside the application.

SSO

Single Sign-On allows users to authenticate through a central identity provider and access multiple applications without repeatedly entering credentials.

A production deployment can therefore use:

Corporate User
      |
      v
Enterprise Identity Provider
      |
      +---- Application A
      |
      +---- AI QA API
      |
      +---- Application C
RBAC

Role-Based Access Control assigns permissions based on user roles.

Example roles:

Admin
  - Manage users
  - View metrics
  - Use chat API

User
  - Use chat API
  - View own chat history

ReadOnly
  - View permitted information

The API can extract the user's identity and roles from validated authentication claims and enforce authorization before processing protected operations.

Production Authentication Flow

A production version can use:

User
  |
  v
SSO / Identity Provider
  |
  v
OAuth2 / OIDC
  |
  v
Access Token
  |
  v
Load Balancer
  |
  v
FastAPI
  |
  v
JWT Validation
  |
  v
RBAC Check
  |
  v
Protected Resource
Security Considerations

Production deployments should:

Use HTTPS/TLS
Store secrets outside source code
Use short-lived access tokens
Rotate signing keys when required
Validate token issuer and audience
Validate token expiration
Apply role-based authorization
Avoid storing passwords in plain text
Use an established identity provider where appropriate