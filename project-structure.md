# Vibe Docs Project Structure

```
vibe-docs/
├── index.js                 # Main CLI entry point
├── package.json             # Project metadata and dependencies
├── README.md                # Project documentation
├── LICENSE                  # MIT License
├── commands/                # Command implementations
│   ├── init.js              # Initialize documentation
│   ├── generate.js          # Generate derived documents
│   ├── update.js            # Update existing documents
│   └── validate.js          # Validate documentation completeness
├── templates/               # Document templates
│   ├── prd.md               # Product Requirements Document template
│   ├── instructions.md      # AI instructions template
│   ├── user-stories.md      # User stories template
│   ├── design-doc.md        # Design document template
│   └── readme.md            # README template for docs folder
├── lib/                     # Shared utilities
│   ├── llm.js               # LLM API integration
│   ├── file-utils.js        # File system utilities
│   └── validators.js        # Document validation functions
└── docs/                    # Documentation for the tool itself
    ├── usage.md             # Usage documentation
    └── examples/            # Example documentation sets
        └── sample-project/  # Sample project documentation
```

## Key Components

### Commands

- **init.js**: Creates the documentation folder structure with templates.
- **generate.js**: Processes the PRD and generates derived documents.
- **update.js**: Analyzes changes in the PRD and updates related documents.
- **validate.js**: Verifies that documentation is complete and consistent.

### Templates

These Markdown templates provide the starting structure for each document type:

- **prd.md**: Comprehensive product requirements document template
- **instructions.md**: Template for AI-optimized coding instructions
- **user-stories.md**: Template for structured user stories
- **design-doc.md**: Template for technical and visual design specifications

### Utilities

- **llm.js**: Handles communication with LLM APIs for document generation
- **file-utils.js**: Helper functions for file operations
- **validators.js**: Functions to validate document completeness and structure

## Implementation Notes

### LLM Integration

In the current implementation, LLM calls are simulated. In a production version, you would:

1. Connect to an actual LLM API (OpenAI, Anthropic, etc.)
2. Handle authentication, rate limiting, and error handling
3. Process and validate the LLM responses

### Document Generation

The document generation follows this process:

1. Read the PRD content
2. For each target document type:
   - Prepare a specialized prompt for the LLM
   - Include the PRD content as context
   - Request the LLM to generate the derived document
   - Save the generated content to the appropriate file

### Update Detection

The update process works by:

1. Finding a previous version of the PRD (if available)
2. Comparing the current PRD with the previous version
3. Identifying significant changes
4. For each affected document:
   - Preparing a specialized prompt for the LLM
   - Including both the changes and full PRD as context
   - Requesting the LLM to update the document
   - Saving the updated content (with backup of the original)

### Validation

The validation system:

1. Checks for required sections in each document
2. Identifies placeholder text that needs to be filled in
3. Verifies cross-document consistency
4. Reports issues with suggestions for fixing them
