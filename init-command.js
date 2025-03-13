// commands/init.js

const fs = require('fs').promises;
const path = require('path');
const ora = require('ora');
const chalk = require('chalk');

// Template content - these would normally be in separate files
const templates = {
  prd: `# Product Requirements Document (PRD)

## Project Overview
**Project Name**: [Name]
**Purpose**: [Brief description of what the product does and why it exists]
**Target Audience**: [Who will use this product]

## Problem Statement
[Describe the problem your software aims to solve]

## User Needs
[Describe what users need and how your product will help them]

## Core Features
- **[Feature 1]**: [Detailed description of the feature]
- **[Feature 2]**: [Detailed description of the feature]
- **[Feature 3]**: [Detailed description of the feature]

## User Types & Scenarios
- **[User Type 1]**
  - [Describe how this type of user will use the product]
  - [Key tasks they need to accomplish]
- **[User Type 2]**
  - [Describe how this type of user will use the product]
  - [Key tasks they need to accomplish]

## Technical Requirements
- **Frontend**: [Technologies, frameworks, etc.]
- **Backend**: [Technologies, frameworks, etc.]
- **Data Storage**: [Requirements]
- **APIs/Integrations**: [External services to connect with]
- **Performance Requirements**: [Speed, load capacity, etc.]
- **Security Requirements**: [Authentication, data protection, etc.]

## Design Preferences
- **Visual Style**: [Clean/minimal, colorful, professional, playful, etc.]
- **UI Components**: [Any specific UI elements you want]
- **References**: [Any examples or inspiration]
- **Brand Guidelines**: [If applicable]

## Non-Functional Requirements
- **Accessibility**: [Requirements]
- **Usability**: [Requirements]
- **Scalability**: [Requirements]
- **Reliability**: [Requirements]
- **Compliance**: [Any regulations or standards to meet]

## Project Constraints
- **Timeline**: [Important dates or milestones]
- **Budget**: [Any financial constraints]
- **Resources**: [Team size, available skills, etc.]
- **Technical Limitations**: [Any technical constraints]

## Success Criteria
[Measurable outcomes that will indicate the project is successful]

## Future Considerations
[Features or improvements planned for future versions]

## Additional Notes
[Any other relevant information]`,

  instructions: `# Project Instructions

## Project Overview
[Provide a high-level description of what your software should do]

## Core Features
- [Feature 1: Brief description]
- [Feature 2: Brief description]
- [Feature 3: Brief description]

## Technical Requirements
- **Frontend**: [Specify technologies/frameworks]
- **Backend**: [Specify technologies/frameworks]
- **Other Requirements**: [Any other technical constraints or preferences]

## User Flows
1. [Describe key user flow 1]
2. [Describe key user flow 2]
3. [Describe key user flow 3]

## Examples
[Provide concrete examples of how the software should work or behave]

## Design Notes
[Brief notes about visual style, UI/UX preferences, or specific design elements]

## Priority Features
[Identify which features are most important to implement first]

## Additional Context
[Any other information that would help AI tools understand your needs]`,

  userStories: `# User Stories

## Introduction
This document contains user stories that describe the functionality of the application from the end user's perspective. Each story follows the format: "As a [user type], I want [action] so that [benefit]."

## Core User Stories

### User Registration and Authentication
- **US-1**: As a new user, I want to create an account so that I can access the application's features.
- **US-2**: As a registered user, I want to log in securely so that I can access my personal data.
- **US-3**: As a user, I want to reset my password if I forget it so that I can regain access to my account.

### [Feature Category 1]
- **US-4**: As a [user type], I want to [action] so that [benefit].
- **US-5**: As a [user type], I want to [action] so that [benefit].

### [Feature Category 2]
- **US-6**: As a [user type], I want to [action] so that [benefit].
- **US-7**: As a [user type], I want to [action] so that [benefit].

## Administrative User Stories
- **US-8**: As an administrator, I want to [action] so that [benefit].
- **US-9**: As an administrator, I want to [action] so that [benefit].

## Error Handling User Stories
- **US-10**: As a user, I want to receive clear error messages when something goes wrong so that I can understand the issue and take appropriate action.

## Acceptance Criteria Example
### US-1: As a new user, I want to create an account so that I can access the application's features.
**Acceptance Criteria:**
1. User can access a registration form from the home page
2. Form requires: username, email, password, password confirmation
3. System validates email format
4. System ensures password meets security requirements
5. System prevents duplicate email/username registrations
6. User receives confirmation email after successful registration
7. User can click on a link in the email to verify their account
8. User is redirected to login page after successful verification

## Priority
- **High**: US-1, US-2, US-4
- **Medium**: US-3, US-5, US-6
- **Low**: US-7, US-8, US-9, US-10`,

  designDoc: `# Design Document

## Visual Design

### Brand Guidelines
- **Color Palette**: 
  - Primary: [Hex Code]
  - Secondary: [Hex Code]
  - Accent: [Hex Code]
  - Background: [Hex Code]
  - Text: [Hex Code]
- **Typography**:
  - Headings: [Font name, size range]
  - Body Text: [Font name, size range]
  - Special Text: [Font name, size range]
- **Logo Usage**: [Guidelines for logo placement and sizing]

### UI Components
- **Navigation**: [Description of navigation structure]
- **Buttons**: [Style and behavior description]
- **Forms**: [Style and validation behavior]
- **Cards/Panels**: [Style description]
- **Tables**: [Style description]
- **Modals/Dialogs**: [Style and behavior description]

### Wireframes
[Include links to wireframes or descriptions of key screens]

## Technical Architecture

### System Architecture
[Diagram or description of overall system architecture]

### Frontend Architecture
- **Framework**: [Framework name and version]
- **State Management**: [Approach]
- **Routing**: [Approach]
- **Key Libraries**: [List of important libraries]
- **Directory Structure**: [Overview of organization]

### Backend Architecture
- **Framework**: [Framework name and version]
- **API Design**: [RESTful, GraphQL, etc.]
- **Authentication**: [Approach]
- **Database**: [Type and design approach]
- **Directory Structure**: [Overview of organization]

### Data Model
[Description of key data entities and relationships]

### API Endpoints
| Endpoint | Method | Purpose | Request Format | Response Format |
|----------|--------|---------|----------------|-----------------|
| \`/api/resource\` | GET | Retrieves resources | N/A | JSON Array |
| \`/api/resource/:id\` | GET | Retrieves specific resource | N/A | JSON Object |
| \`/api/resource\` | POST | Creates new resource | JSON Object | JSON Object |

## Performance Considerations
- [Key performance requirements]
- [Caching strategy]
- [Load handling approach]

## Security Considerations
- [Authentication approach]
- [Authorization model]
- [Data protection strategy]
- [Other security measures]

## Accessibility Guidelines
- [Target compliance level (e.g., WCAG 2.1 AA)]
- [Specific accessibility requirements]

## Responsive Design
- [Breakpoints for different device sizes]
- [Layout changes at different breakpoints]

## Testing Strategy
- [Unit testing approach]
- [Integration testing approach]
- [UI testing approach]

## Implementation Notes
- [Any specific implementation details or considerations]
- [Known technical challenges]
- [Third-party integration details]`,

  readme: `# Documentation Guide

## Overview
This folder contains documentation for the project. These documents help provide structure and guidance for development, especially when using AI-assisted coding methods like vibe coding.

## Files

### PRD (prd.md)
The Product Requirements Document (PRD) is the primary document that captures all project requirements. This serves as the source of truth for your project.

### Instructions (instructions.md)
AI-optimized guidance for code generation tools. This is what you'll refer to when using AI coding assistants.

### User Stories (user-stories.md)
Structured user narratives that clarify how users will interact with your software.

### Design Document (design-doc.md)
Technical architecture and visual design specifications.

## Workflow

1. Fill in your PRD with project requirements
2. Run \`vibe validate\` to ensure your PRD is complete
3. Run \`vibe generate\` to create derived documents
4. As your project evolves, update your PRD and run \`vibe update\`

## Maintenance

Keep these documents updated as your project evolves. The PRD should always reflect the current state of your project requirements.`
};

// Main init function
async function init(options) {
  const spinner = ora('Initializing Vibe Docs structure...').start();
  
  try {
    // Create docs directory if it doesn't exist
    const docsDir = path.resolve(process.cwd(), options.dir);
    await fs.mkdir(docsDir, { recursive: true });
    spinner.text = `Created directory: ${docsDir}`;
    
    // Create each template file
    const files = {
      'prd.md': templates.prd,
      'instructions.md': templates.instructions,
      'user-stories.md': templates.userStories,
      'design-doc.md': templates.designDoc,
      'README.md': templates.readme
    };
    
    for (const [filename, content] of Object.entries(files)) {
      const filePath = path.join(docsDir, filename);
      await fs.writeFile(filePath, content);
      spinner.text = `Created file: ${filePath}`;
    }
    
    spinner.succeed('Documentation structure initialized successfully');
    
    return {
      docsDir,
      files: Object.keys(files).map(f => path.join(docsDir, f))
    };
  } catch (error) {
    spinner.fail(`Failed to initialize documentation structure: ${error.message}`);
    throw error;
  }
}

module.exports = init;
