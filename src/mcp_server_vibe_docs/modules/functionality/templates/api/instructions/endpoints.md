# API Endpoints

## Project: {{project_name}}

## Authentication Endpoints
- `POST /auth/login`: User login
- `POST /auth/refresh`: Refresh access token
- `POST /auth/logout`: User logout
- `POST /auth/register`: User registration (if public registration allowed)

## User Management
- `GET /api/users`: List all users (admin only)
- `GET /api/users/{id}`: Get user details
- `POST /api/users`: Create a new user (admin only)
- `PUT /api/users/{id}`: Update user details
- `DELETE /api/users/{id}`: Delete a user

## Resource Endpoints
- `GET /api/resources`: List all resources
- `GET /api/resources/{id}`: Get resource details
- `POST /api/resources`: Create a new resource
- `PUT /api/resources/{id}`: Update resource details
- `DELETE /api/resources/{id}`: Delete a resource

## Status Endpoints
- `GET /api/status/health`: API health check
- `GET /api/status/version`: Get API version information