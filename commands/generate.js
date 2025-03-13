const fs = require('fs').promises;
const path = require('path');
const ora = require('ora');
const chalk = require('chalk');

// Document types and their generation prompts
const documentTypes = {
  'instructions': {
    filename: 'instructions.md',
    prompt: `
You are an expert at creating clear instructions for AI coding tools.
Review this PRD and extract the most important technical requirements and functionality specifications.
Create a concise, clear Instructions.md file that will guide an AI coding tool to implement this product.
Focus on what needs to be built rather than business context.
Use clear, specific language optimized for AI understanding.
Format the output as a well-structured markdown document with appropriate sections and bullet points for clarity.
Here is the PRD:

{{prdContent}}
    `
  },
  'user-stories': {
    filename: 'user-stories.md',
    prompt: `
You are an expert at creating user stories.
Review this PRD and extract all user types and their needs.
Create proper user stories in the format "As a [user type], I want [action] so that [benefit]".
Organize these by feature category and add acceptance criteria for the most important stories.
Format the output as a well-structured markdown document.
Here is the PRD:

{{prdContent}}
    `
  },
  'design-doc': {
    filename: 'design-doc.md',
    prompt: `
You are an expert system architect and designer.
Review this PRD and create a design document that outlines:
1. Visual design requirements and preferences
2. Technical architecture approach
3. Data model
4. API endpoints (if applicable)
5. Key technical considerations

Include placeholders where specific design decisions need to be made.
Format the output as a well-structured markdown document.
Here is the PRD:

{{prdContent}}
    `
  }
};

// This would be replaced with actual LLM API calls
const simulateLlmCall = async (prompt, options) => {
  // In a real implementation, this would call an LLM API
  console.log(`[SIMULATED] Calling LLM with model ${options.model}`);
  
  // For simulation, just return a template document based on the type
  if (prompt.includes('instructions for AI coding tools')) {
    return `# Project Instructions

## Project Overview
TaskFlow is a collaborative task management application designed to help teams organize, track, and complete projects efficiently with AI-powered insights.

## Core Features
- Task Management: Create, assign, prioritize, and track tasks with custom fields
- AI-Powered Insights: Analyze productivity patterns and suggest task assignments
- Real-time Collaboration: Live updates and in-context commenting
- Smart Dashboard: Personalized views with upcoming deadlines and bottlenecks
- Integration Hub: Connect with version control and communication tools

## Technical Requirements
- Frontend: React with TypeScript, Redux for state management
- Backend: Node.js with Express, GraphQL API
- Data Storage: PostgreSQL for structured data, Redis for caching
- APIs/Integrations: GitHub, Slack, Google Calendar, Microsoft Teams

## User Flows
1. Team member logs in and views personalized dashboard with prioritized tasks
2. Project manager creates new task, assigns it, and sets dependencies
3. Team members collaborate on task with real-time updates and comments
4. System provides AI insights on workload balance and potential bottlenecks

## Design Notes
Clean, minimalist interface with vibrant accent colors against a neutral background. Focus on intuitive UX with minimal training required.

## Priority Features
1. Task creation and assignment
2. Real-time collaboration
3. Dashboard with task visibility
4. AI-powered suggestions`;
  } else if (prompt.includes('user stories')) {
    return `# User Stories

## Introduction
This document contains user stories that describe the functionality of TaskFlow from the end user's perspective. Each story follows the format: "As a [user type], I want [action] so that [benefit]."

## Core User Stories

### Task Management
- As a team member, I want to create and assign tasks so that work is properly distributed.
- As a project manager, I want to set task priorities so that the team focuses on the most important work.
- As a team lead, I want to establish task dependencies so that work is completed in the proper sequence.

### Collaboration
- As a team member, I want to comment on tasks so that I can provide context and updates.
- As a reviewer, I want to approve completed work so that quality standards are maintained.
- As a stakeholder, I want to view project progress so that I stay informed without meetings.

### AI Features
- As a project manager, I want AI-suggested resource allocation so that workloads are balanced.
- As a team member, I want personalized task suggestions so that I can maximize my productivity.
- As a team lead, I want early warning of potential delays so that I can proactively address issues.

## Administrative User Stories
- As an administrator, I want to manage user permissions so that information access is appropriate.
- As an administrator, I want to configure integrations so that TaskFlow connects with other tools.

## Acceptance Criteria Example
### As a team member, I want to create and assign tasks so that work is properly distributed.
**Acceptance Criteria:**
1. User can access a task creation form from the dashboard
2. Form includes fields for title, description, assignee, due date, priority, and tags
3. Tasks can be assigned to any team member
4. Notifications are sent when tasks are assigned
5. Tasks appear in the assignee's dashboard immediately`;
  } else {
    return `# Design Document

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
| \`/api/tasks\` | GET | Retrieves tasks | Query params | JSON Array |
| \`/api/tasks/:id\` | GET | Retrieves specific task | N/A | JSON Object |
| \`/api/tasks\` | POST | Creates new task | JSON Object | JSON Object |`;
  }
};

// Function to generate a document using an LLM
async function generateDocument(type, prdContent, outputDir, options) {
  const docType = documentTypes[type];
  if (!docType) {
    throw new Error(`Unknown document type: ${type}`);
  }
  
  const outputPath = path.join(outputDir, docType.filename);
  
  // Check if file exists when in update mode
  if (options.updateExisting && !fs.existsSync(outputPath)) {
    console.warn(chalk.yellow(`Warning: Cannot update non-existent file ${outputPath}. Creating new file instead.`));
  }
  
  // Prepare prompt for LLM
  const prompt = docType.prompt.replace('{{prdContent}}', prdContent);
  
  // Call LLM to generate document
  const generatedContent = await simulateLlmCall(prompt, {
    model: options.model
  });
  
  // Write the generated content to file
  await fs.writeFile(outputPath, generatedContent);
  
  return outputPath;
}

// Main generate function
async function generate(options) {
  const spinner = ora('Preparing to generate documentation...').start();
  
  try {
    const inputFile = path.resolve(process.cwd(), options.input);
    const outputDir = path.dirname(inputFile);
    
    // Validate input file exists
    try {
      await fs.access(inputFile);
    } catch (error) {
      spinner.fail(`Input file not found: ${inputFile}`);
      throw new Error(`Input file not found: ${inputFile}`);
    }
    
    // Read the PRD content
    spinner.text = 'Reading PRD content...';
    const prdContent = await fs.readFile(inputFile, 'utf8');
    
    // Determine which documents to generate
    let documentsToGenerate = [];
    if (options.outputAll) {
      documentsToGenerate = Object.keys(documentTypes);
    } else if (options.output) {
      documentsToGenerate = options.output.split(',').filter(type => 
        Object.keys(documentTypes).includes(type)
      );
      
      if (documentsToGenerate.length === 0) {
        spinner.fail('No valid document types specified');
        throw new Error('No valid document types specified');
      }
    } else {
      // Default to just instructions if nothing specified
      documentsToGenerate = ['instructions'];
    }
    
    spinner.text = `Generating the following documents: ${documentsToGenerate.join(', ')}`;
    
    // Create backup directory for any existing documents
    if (options.updateExisting) {
      const backupDir = path.join(outputDir, '.backups', new Date().toISOString().replace(/:/g, '-'));
      await fs.mkdir(backupDir, { recursive: true });
      
      // Backup existing files
      for (const docType of documentsToGenerate) {
        const filename = documentTypes[docType].filename;
        const filePath = path.join(outputDir, filename);
        
        try {
          const content = await fs.readFile(filePath, 'utf8');
          await fs.writeFile(path.join(backupDir, filename), content);
        } catch (error) {
          if (error.code !== 'ENOENT') {
            throw error;
          }
        }
      }
    }
    
    // Generate each document
    const generatedFiles = [];
    for (const docType of documentsToGenerate) {
      spinner.text = `Generating ${docType} document...`;
      const outputPath = await generateDocument(docType, prdContent, outputDir, options);
      generatedFiles.push(outputPath);
    }
    
    spinner.succeed(`Successfully generated ${generatedFiles.length} documents`);
    
    return {
      generated: true,
      files: generatedFiles
    };
  } catch (error) {
    spinner.fail(`Error generating documentation: ${error.message}`);
    throw error;
  }
}

module.exports = generate;