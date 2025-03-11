# Frontend Guidelines

## Project: {{project_name}}

## Overview
These guidelines provide recommendations for frontend clients interacting with the API.

## Authentication
- Store tokens securely (use HTTP-only cookies when possible)
- Implement token refresh logic to maintain sessions
- Handle authentication errors gracefully
- Provide clear login/logout experience

## API Interaction
- Use a consistent API client library
- Implement proper error handling for all API calls
- Handle loading and error states in the UI
- Cache responses when appropriate to improve performance

## Data Management
- Use a state management solution for complex applications
- Keep API response structures consistent with backend models
- Validate form inputs before sending to the API
- Implement optimistic updates for better user experience

## Performance
- Minimize API requests by batching when possible
- Implement pagination for large data sets
- Use appropriate caching strategies
- Lazy load data and components when applicable

## Security
- Validate all user inputs
- Sanitize data before rendering to prevent XSS
- Use HTTPS for all API requests
- Implement appropriate CSRF protections

## Testing
- Write unit tests for critical components and logic
- Implement integration tests for API interactions
- Consider end-to-end tests for critical user flows
- Test error handling and edge cases

## Documentation
- Document API client usage with examples
- Maintain a changelog for frontend changes
- Keep API integration documentation up to date
- Document state management patterns and data flow