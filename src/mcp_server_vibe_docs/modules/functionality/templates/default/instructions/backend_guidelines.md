# Backend Guidelines

## Project: {{project_name}}

## Technology Stack
{{backend_stack}}

## API Design
<!-- TODO: Document your API design principles. Example: -->
- Follow RESTful API design principles
- Use consistent URL structure (e.g., `/api/resources`)
- Return appropriate HTTP status codes
- Include meaningful error messages
- Version your API appropriately

## Authentication & Authorization
<!-- TODO: Document your auth approach. Example: -->
- Use JWT tokens for authentication
- Implement role-based access control
- Apply the principle of least privilege
- Secure sensitive endpoints
- Refresh token strategy for extended sessions

## Error Handling
<!-- TODO: Document your error handling approach. Example: -->
- Use consistent error response format
- Include error codes, messages, and details when appropriate
- Log errors with appropriate severity levels
- Don't expose sensitive information in error messages
- Handle unexpected errors gracefully

## Data Validation
<!-- TODO: Document your data validation approach. Example: -->
- Validate all incoming data
- Use a schema validation library (Joi, Yup, etc.)
- Apply validation at the controller/route level
- Return meaningful validation error messages
- Sanitize data to prevent injection attacks

## Database
<!-- TODO: Document your database approach. Example: -->
- Use migrations for database schema changes
- Follow naming conventions for tables and columns
- Create appropriate indexes for frequently queried fields
- Use transactions for multi-step operations
- Implement proper connection pooling

## Business Logic
<!-- TODO: Document your business logic approach. Example: -->
- Separate business logic from controllers
- Use service/repository pattern
- Write unit tests for business logic
- Document complex algorithms and flows
- Follow SOLID principles

## Security
<!-- TODO: Document your security practices. Example: -->
- Use HTTPS for all requests
- Implement proper CORS configuration
- Apply rate limiting and throttling
- Use parameterized queries to prevent SQL injection
- Validate and sanitize user input
- Set secure HTTP headers
- Follow OWASP top 10 prevention guidelines

## Performance
<!-- TODO: Document your performance considerations. Example: -->
- Use caching for frequently accessed data
- Optimize database queries
- Implement pagination for large data sets
- Use compression for responses
- Minimize response payload size
- Consider database denormalization for read-heavy operations

## Logging
<!-- TODO: Document your logging approach. Example: -->
- Log all API requests and responses
- Use structured logging format
- Include request IDs for traceability
- Apply appropriate log levels
- Don't log sensitive information