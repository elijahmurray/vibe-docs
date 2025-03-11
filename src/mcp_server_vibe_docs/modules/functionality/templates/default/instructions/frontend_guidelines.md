# Frontend Guidelines

## Project: {{project_name}}

## Technology Stack
{{frontend_stack}}

## Component Architecture
<!-- TODO: Document your component architecture approach. Example: -->
- Use atomic design principles (atoms, molecules, organisms, templates, pages)
- Keep components small and focused on a single responsibility
- Separate logic from presentation when possible
- Use container/presentational pattern for complex components

## State Management
<!-- TODO: Document your state management approach. Example: -->
- Use local state for component-specific state
- Use context API for shared state between related components
- Use Redux/Zustand/etc. for global application state
- Consider server state management tools for API data

## Styling Approach
<!-- TODO: Document your styling approach. Example: -->
- Use CSS-in-JS, CSS Modules, or Tailwind CSS
- Follow a consistent naming convention
- Use design tokens for colors, spacing, typography, etc.
- Ensure responsive design with mobile-first approach

## Form Handling
<!-- TODO: Document your form handling approach. Example: -->
- Use Formik, React Hook Form, or similar library
- Implement proper validation with Yup or Zod
- Show clear error messages
- Handle submission and error states appropriately

## Routing
<!-- TODO: Document your routing approach. Example: -->
- Use React Router or Next.js routing
- Implement route guards for protected routes
- Handle query parameters consistently
- Implement loading states during navigation

## API Integration
<!-- TODO: Document your API integration approach. Example: -->
- Use axios, fetch, or React Query
- Implement proper error handling
- Show loading states during requests
- Handle caching appropriately

## Testing
<!-- TODO: Document your testing approach. Example: -->
- Write unit tests for critical components
- Add integration tests for complex flows
- Use Jest, React Testing Library, or similar tools
- Test accessibility with axe or similar tools

## Performance Optimizations
<!-- TODO: Document your performance optimizations. Example: -->
- Use code splitting for large applications
- Implement virtualization for long lists
- Optimize images and assets
- Use memoization for expensive calculations

## Accessibility (a11y)
<!-- TODO: Document your accessibility approach. Example: -->
- Follow WCAG 2.1 guidelines
- Use semantic HTML elements
- Implement proper focus management
- Ensure keyboard navigation works
- Add appropriate ARIA attributes