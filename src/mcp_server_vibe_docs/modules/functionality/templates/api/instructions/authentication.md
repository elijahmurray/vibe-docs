# Authentication

## Project: {{project_name}}

## Authentication Methods
The API supports the following authentication methods:

1. **JWT (JSON Web Tokens)**
   - Used for user authentication
   - Tokens expire after 30 minutes
   - Refresh tokens valid for 7 days

2. **API Keys**
   - Used for service-to-service authentication
   - No expiration by default
   - Can be revoked at any time

## Authentication Flow
1. User provides credentials via `/auth/login`
2. API returns an access token and refresh token
3. Access token is included in the Authorization header for subsequent requests
4. When the access token expires, use the refresh token to get a new one via `/auth/refresh`

## Example Login Request
```json
POST /auth/login
{
  "username": "user@example.com",
  "password": "securepassword"
}
```

## Example Login Response
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

## Using Authentication
Include the token in the Authorization header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```