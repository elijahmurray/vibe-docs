# Architecture

## Project: {{project_name}}

## Overview
{{architecture_description}}

## Components
The system is comprised of the following key components:

{{key_components}}

## Data Flow
1. User initializes a project with `vibe init`
2. Documentation templates are created and populated
3. Features are tracked in a SQLite database
4. Status can be queried with `vibe status`
5. Documentation can be updated with `vibe update`

## Database Schema
- Projects table: Stores project metadata
- Features table: Tracks feature implementation status
- Sections table: Stores documentation sections
- Templates table: Defines available templates