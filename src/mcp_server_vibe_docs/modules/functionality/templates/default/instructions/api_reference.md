# API Reference

## Project: {{project_name}}

## API Overview
{{api_description}}

## Authentication
<!-- TODO: Document your authentication methods. Example: -->
```
# Bearer Token Authentication
Authorization: Bearer <token>

# API Key Authentication
X-API-Key: <api_key>
```

## Common Headers
<!-- TODO: Document common request/response headers. Example: -->
- `Content-Type: application/json`
- `Accept: application/json`
- `X-Request-ID: <request_id>` - For request tracking

## Error Handling
<!-- TODO: Document your error response format. Example: -->
```json
{
  "error": {
    "code": "invalid_request",
    "message": "Required field missing",
    "details": {
      "field": "email",
      "issue": "cannot be empty"
    }
  }
}
```

## Endpoints

### Resource Endpoints
<!-- TODO: Document your resource endpoints. Example: -->

#### Get All Resources
```
GET /api/resources
```

**Query Parameters:**
- `page` (optional): Page number for pagination
- `limit` (optional): Items per page (default: 20)
- `sort` (optional): Field to sort by (default: 'createdAt')

**Response:**
```json
{
  "data": [
    {
      "id": "1",
      "type": "resource",
      "attributes": {
        "name": "Example Resource",
        "created_at": "2023-05-01T12:00:00Z",
        "updated_at": "2023-05-01T12:00:00Z"
      }
    }
  ],
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 20
  }
}
```

#### Get Resource by ID
```
GET /api/resources/:id
```

**Response:**
```json
{
  "data": {
    "id": "1",
    "type": "resource",
    "attributes": {
      "name": "Example Resource",
      "description": "This is an example resource",
      "created_at": "2023-05-01T12:00:00Z",
      "updated_at": "2023-05-01T12:00:00Z"
    },
    "relationships": {
      "owner": {
        "data": { "type": "user", "id": "1" }
      }
    }
  }
}
```

#### Create Resource
```
POST /api/resources
```

**Request Body:**
```json
{
  "name": "New Resource",
  "description": "This is a new resource"
}
```

**Response:**
```json
{
  "data": {
    "id": "2",
    "type": "resource",
    "attributes": {
      "name": "New Resource",
      "description": "This is a new resource",
      "created_at": "2023-05-01T12:00:00Z",
      "updated_at": "2023-05-01T12:00:00Z"
    }
  }
}
```

### User Endpoints
<!-- TODO: Document your user endpoints -->

## Data Models
<!-- TODO: Document your data models -->

## Pagination
<!-- TODO: Document your pagination approach -->

## Rate Limiting
<!-- TODO: Document rate limiting policies -->