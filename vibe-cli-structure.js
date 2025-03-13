#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { program } = require('commander');
const chalk = require('chalk');
const inquirer = require('inquirer');
const ora = require('ora');

// Import command implementations
const init = require('./commands/init');
const generate = require('./commands/generate');
const update = require('./commands/update');
const validate = require('./commands/validate');

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
  .option('-m, --model <name>', 'LLM model to use', config.llm?.model || 'gpt-4')
  .action(async (options) => {
    try {
      await generate(options);
      console.log(chalk.green('✅ Documentation generation complete!'));
    } catch (error) {
      console.error(chalk.red('Error generating documentation:'), error.message);
      process.exit(1);
    }
  });

// vibe update command
program
  .command('update')
  .description('Update documentation as project evolves')
  .option('-i, --input <file>', 'Input file to update from', config.prdPath || './docs/prd.md')
  .option('-c, --check', 'Check for inconsistencies without updating')
  .option('-m, --model <name>', 'LLM model to use', config.llm?.model || 'gpt-4')
  .action(async (options) => {
    try {
      await update(options);
      console.log(chalk.green('✅ Documentation updated successfully!'));
    } catch (error) {
      console.error(chalk.red('Error updating documentation:'), error.message);
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
      if (results.valid) {
        console.log(chalk.green('✅ Documentation is valid and complete!'));
      } else {
        console.log(chalk.yellow('⚠️ Documentation has issues:'));
        results.issues.forEach(issue => {
          console.log(`- ${issue.file}: ${issue.message}`);
        });
        if (options.fix) {
          console.log(chalk.blue('Attempting to fix issues...'));
          // Implementation for fixing issues would go here
        }
        process.exit(1);
      }
    } catch (error) {
      console.error(chalk.red('Error validating documentation:'), error.message);
      process.exit(1);
    }
  });

// Parse arguments
program.parse(process.argv);
