# Rate Limiting

## Project: {{project_name}}

## Rate Limiting Policy
To ensure fair usage and prevent abuse, the API implements rate limiting with the following default limits:

| Authentication Level | Request Limit          | Window    |
|----------------------|------------------------|-----------|
| Unauthenticated      | 30 requests            | per minute |
| Authenticated Users  | 100 requests           | per minute |
| Premium Users        | 300 requests           | per minute |
| Admin Users          | 1000 requests          | per minute |

## Rate Limit Headers
The API includes rate limiting information in the response headers:

- `X-RateLimit-Limit`: Maximum number of requests allowed in the window
- `X-RateLimit-Remaining`: Number of requests remaining in the current window
- `X-RateLimit-Reset`: Time (in UTC epoch seconds) when the rate limit window resets

## Rate Limit Exceeded Response
When rate limits are exceeded, the API returns:

- Status code: `429 Too Many Requests`
- Response body:
  ```json
  {
    "error": "rate_limit_exceeded",
    "message": "Rate limit exceeded. Please try again in X seconds.",
    "retry_after": 30
  }
  ```

## Best Practices
1. Implement exponential backoff when receiving 429 responses
2. Cache responses when appropriate to reduce API calls
3. Use batch operations when possible instead of multiple single operations
4. Monitor your usage via the rate limit headers