#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { program } = require('commander');
const chalk = require('chalk');

// Import command implementations
const init = require('./commands/init');
const generate = require('./commands/generate');
const update = require('./commands/update');
const validate = require('./commands/validate');
const configCommands = require('./commands/config');

// Load config if exists
let config = {};
try {
  const configPath = path.join(process.cwd(), 'vibe.config.js');
  if (fs.existsSync(configPath)) {
    config = require(configPath);
  }
} catch (error) {
  console.warn(chalk.yellow('Warning: Error loading vibe.config.js, using defaults'));
}

// Define CLI
program
  .name('vibe')
  .description('Vibe Docs - Documentation scaffolding for vibe coding')
  .version('1.0.0');

// vibe init command
program
  .command('init')
  .description('Initialize documentation structure')
  .option('-d, --dir <directory>', 'Target directory', config.docsDir || './docs')
  .option('-t, --template <template>', 'Template to use', 'standard')
  .action(async (options) => {
    try {
      await init(options);
      console.log(chalk.green('✅ Documentation structure initialized successfully!'));
      console.log(chalk.blue('Next steps:'));
      console.log('1. Fill in the PRD template with your project requirements');
      console.log('2. Run "vibe validate" to check for completeness');
      console.log('3. Run "vibe generate" to create derived documents');
    } catch (error) {
      console.error(chalk.red('Error initializing documentation:'), error.message);
      process.exit(1);
    }
  });

// vibe generate command
program
  .command('generate')
  .description('Generate documentation from PRD')
  .option('-i, --input <file>', 'Input PRD file path', config.prdPath || './docs/prd.md')
  .option('-a, --output-all', 'Generate all document types')
  .option('-o, --output <types>', 'Specific document types to generate (comma-separated)')
  .option('-u, --update-existing', 'Update existing documents')
  .option('-m, --model <n>', 'LLM model to use', config.llm?.model || 'claude-3-haiku-20240307')
  .action(async (options) => {
    try {
      await generate(options);
      console.log(chalk.green('✅ Documentation generation complete!'));
    } catch (error) {
      if (error.message.includes('API key') || error.message.includes('401')) {
        console.error(chalk.red('\n❌ API Key Error: ') + 
          chalk.yellow('Missing or invalid API key. Please set up your Anthropic API key:'));
        console.error(chalk.blue('\n    vibe config:set-api-key\n'));
        console.error(chalk.gray('You can get an API key from https://console.anthropic.com/\n'));
      } else {
        console.error(chalk.red('Error generating documentation:'), error.message);
      }
      process.exit(1);
    }
  });

// vibe update command
program
  .command('update')
  .description('Update documentation as project evolves')
  .option('-i, --input <file>', 'Input file to update from', config.prdPath || './docs/prd.md')
  .option('-c, --check', 'Check for inconsistencies without updating')
  .option('-m, --model <n>', 'LLM model to use', config.llm?.model || 'claude-3-haiku-20240307')
  .action(async (options) => {
    try {
      await update(options);
      console.log(chalk.green('✅ Documentation updated successfully!'));
    } catch (error) {
      if (error.message.includes('API key') || error.message.includes('401')) {
        console.error(chalk.red('\n❌ API Key Error: ') + 
          chalk.yellow('Missing or invalid API key. Please set up your Anthropic API key:'));
        console.error(chalk.blue('\n    vibe config:set-api-key\n'));
        console.error(chalk.gray('You can get an API key from https://console.anthropic.com/\n'));
      } else {
        console.error(chalk.red('Error updating documentation:'), error.message);
      }
      process.exit(1);
    }
  });

// vibe validate command
program
  .command('validate')
  .description('Validate documentation for completeness')
  .option('-d, --dir <directory>', 'Directory to validate', config.docsDir || './docs')
  .option('-f, --fix', 'Attempt to fix issues automatically')
  .action(async (options) => {
    try {
      const results = await validate(options);
      // No additional console output needed as validate() now handles all the display
      
      if (!results.valid && options.fix) {
        console.log(chalk.blue('\nAttempting to fix issues...'));
        // Implementation for fixing issues would go here
      }
      
      if (!results.valid) {
        process.exit(1);
      }
    } catch (error) {
      console.error(chalk.red('Error validating documentation:'), error.message);
      process.exit(1);
    }
  });

// vibe config command
program
  .command('config')
  .description('Configure Vibe Docs settings')
  .action(async () => {
    try {
      await configCommands.showConfig();
    } catch (error) {
      console.error(chalk.red('Error showing configuration:'), error.message);
      process.exit(1);
    }
  });

program
  .command('config:set-api-key')
  .description('Set the API key for LLM calls')
  .option('-k, --key <key>', 'API key')
  .option('-p, --provider <provider>', 'API provider (openai, anthropic)', 'openai')
  .action(async (options) => {
    try {
      await configCommands.setApiKey(options);
      console.log(chalk.green('✅ API key set successfully!'));
    } catch (error) {
      console.error(chalk.red('Error setting API key:'), error.message);
      process.exit(1);
    }
  });

program
  .command('config:set-model')
  .description('Set the default LLM model to use')
  .argument('<model>', 'Model name (e.g. gpt-4, claude-3)')
  .action(async (model, options) => {
    try {
      await configCommands.setModel({ model, ...options });
      console.log(chalk.green(`✅ Default model set to ${model}!`));
    } catch (error) {
      console.error(chalk.red('Error setting model:'), error.message);
      process.exit(1);
    }
  });

// Parse arguments
program.parse(process.argv);