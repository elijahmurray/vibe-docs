# Vibe Docs: Installation and Usage Guide

## Installation

### Option 1: Global Installation (Recommended)

```bash
npm install -g vibe-docs
```

After installation, the `vibe` command will be available globally.

### Option 2: Local Installation

```bash
npm install vibe-docs --save-dev
```

With local installation, use npx to run the commands:

```bash
npx vibe init
```

### Option 3: Clone and Install from Source

```bash
git clone https://github.com/yourusername/vibe-docs.git
cd vibe-docs
npm install
npm link
```

## Usage

### Basic Workflow

1. **Initialize documentation structure**:
   ```bash
   vibe init
   ```
   This creates an `docs` directory with template files for PRD, instructions, user stories, and design documents.

2. **Fill out the PRD**:
   Open `docs/prd.md` and fill in your project requirements.

3. **Validate your documentation**:
   ```bash
   vibe validate
   ```
   This checks for completeness and highlights any missing sections.

4. **Generate derived documents**:
   ```bash
   vibe generate
   ```
   This creates/updates instructions.md based on your PRD.

5. **Update documentation as your project evolves**:
   ```bash
   vibe update
   ```
   This checks for changes in your PRD and updates related documents accordingly.

### Command Reference

#### `vibe init`

Initializes a new documentation structure.

```bash
vibe init [options]
```

Options:
- `--dir <directory>` - Target directory (default: './docs')
- `--template <template>` - Template to use (default: 'standard')

Example:
```bash
vibe init --dir ./documentation
```

#### `vibe validate`

Validates your documentation for completeness.

```bash
vibe validate [options]
```

Options:
- `--dir <directory>` - Directory to validate (default: './docs')
- `--fix` - Attempt to fix issues automatically

Example:
```bash
vibe validate --fix
```

#### `vibe generate`

Generates derived documentation from your PRD.

```bash
vibe generate [options]
```

Options:
- `--input <file>` - Input PRD file path (default: './docs/prd.md')
- `--output-all` - Generate all document types
- `--output <types>` - Specific document types (comma-separated)
- `--update-existing` - Update existing documents
- `--model <n>` - LLM model to use (default: 'gpt-4')

Examples:
```bash
# Generate just instructions
vibe generate

# Generate all document types
vibe generate --output-all

# Generate specific documents
vibe generate --output user-stories,design-doc
```

#### `vibe update`

Updates documentation as your project evolves.

```bash
vibe update [options]
```

Options:
- `--input <file>` - Input file to update from (default: './docs/prd.md')
- `--check` - Check for inconsistencies without updating
- `--model <n>` - LLM model to use (default: 'gpt-4')

Example:
```bash
vibe update --check
```

## Configuration

You can customize Vibe Docs by creating a `vibe.config.js` file in your project root:

```javascript
module.exports = {
  docsDir: './documentation',
  templates: {
    prd: './custom-templates/prd.md',
    // other custom templates...
  },
  llm: {
    model: 'gpt-4',
    temperature: 0.7
  },
  validation: {
    requiredSections: ['Project Overview', 'Core Features', 'Technical Requirements']
  }
};
```

## Workflow Tips

1. **Start with a clear product vision**: Before running any commands, have a clear understanding of what you want to build.

2. **Be thorough with your PRD**: The more detailed your PRD, the better the derived documents will be.

3. **Iterative updates**: As your project evolves, update your PRD first, then run `vibe update` to keep all documentation in sync.

4. **Version control**: Commit your documentation alongside your code to track its evolution.

5. **AI collaboration**: Use the generated `instructions.md` when working with AI coding tools for best results.
