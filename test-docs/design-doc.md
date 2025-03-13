# Design Document

## Visual Design

### Brand Guidelines
- **Color Palette**: 
  - Primary: #0052CC (Blue)
  - Secondary: #FF5630 (Orange)
  - Accent: #36B37E (Green)
  - Background: #F4F5F7 (Light Gray)
  - Text: #172B4D (Dark Blue)
- **Typography**:
  - Headings: Inter, 16-32px
  - Body Text: Inter, 14-16px
  - Special Text: Inter Medium, 14px
- **Logo Usage**: TaskFlow logo should have adequate padding, minimum size 32px

### UI Components
- **Navigation**: Side navigation with collapsible sections
- **Buttons**: Rounded with subtle hover effects
- **Forms**: Inline validation with clear error messages
- **Cards**: Task cards with color-coded priority indicators
- **Modals**: Centered with overlay background and clear dismiss action

## Technical Architecture

### System Architecture
Microservices architecture with separate services for task management, user authentication, and AI insights.

### Frontend Architecture
- **Framework**: React 18 with TypeScript
- **State Management**: Redux Toolkit
- **Routing**: React Router v6
- **Key Libraries**: React Query for data fetching, DnD Kit for drag-and-drop
- **Directory Structure**: Feature-based organization with shared components

### Backend Architecture
- **Framework**: Node.js with Express
- **API Design**: GraphQL with Apollo Server
- **Authentication**: JWT with refresh tokens
- **Database**: PostgreSQL with Prisma ORM
- **Caching**: Redis for performance optimization

### Data Model
- **Users**: User profiles and authentication
- **Projects**: Collection of related tasks
- **Tasks**: Core work items with metadata
- **Comments**: Communication attached to tasks
- **Teams**: Groups of users with shared access

### API Endpoints
| Endpoint | Method | Purpose | Request Format | Response Format |
|----------|--------|---------|----------------|-----------------|
| `/api/tasks` | GET | Retrieves tasks | Query params | JSON Array |
| `/api/tasks/:id` | GET | Retrieves specific task | N/A | JSON Object |
| `/api/tasks` | POST | Creates new task | JSON Object | JSON Object |