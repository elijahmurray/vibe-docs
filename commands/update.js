const fs = require('fs').promises;
const fsSync = require('fs');
const path = require('path');
const ora = require('ora');
const chalk = require('chalk');
const diff = require('diff');

// This would be replaced with actual LLM API calls
const simulateLlmCall = async (prompt, options) => {
  // In a real implementation, this would call an LLM API
  console.log(`[SIMULATED] Calling LLM with model ${options.model}`);
  
  // For simulation, just return a placeholder response
  return `This is a simulated response from the LLM.
It would normally analyze the changes in your PRD and suggest updates to other documents.

Changes detected:
- Added new feature X
- Modified technical requirements for Y
- Updated user scenarios

Recommended updates:
1. Add feature X to instructions.md
2. Update user stories for feature Y
3. Revise design document for architectural changes`;
};

// Check for changes between current and previous version
async function checkForChanges(currentPath, previousVersionPath) {
  try {
    const currentContent = await fs.readFile(currentPath, 'utf8');
    const previousContent = await fs.readFile(previousVersionPath, 'utf8');
    
    const changes = diff.diffLines(previousContent, currentContent);
    const significantChanges = changes.filter(change => change.added || change.removed);
    
    return {
      hasChanges: significantChanges.length > 0,
      changes: significantChanges,
      changeDescription: significantChanges.map(change => {
        const prefix = change.added ? '+ ' : '- ';
        const text = change.value.split('\n').filter(line => line.trim()).slice(0, 3);
        return text.map(line => prefix + line).join('\n');
      }).join('\n')
    };
  } catch (error) {
    if (error.code === 'ENOENT') {
      return {
        hasChanges: true,
        changes: [],
        changeDescription: 'No previous version found, treating as new document'
      };
    }
    throw error;
  }
}

// Find documents that might need updates based on PRD changes
async function findAffectedDocuments(prdPath) {
  const docsDir = path.dirname(prdPath);
  const fileToCheck = ['instructions.md', 'user-stories.md', 'design-doc.md'];
  
  const results = [];
  
  for (const file of fileToCheck) {
    const filePath = path.join(docsDir, file);
    try {
      await fs.access(filePath);
      results.push(file);
    } catch (error) {
      // File doesn't exist, skip it
    }
  }
  
  return results;
}

// Make a backup of existing documents
async function backupDocuments(docsDir, files) {
  const backupDir = path.join(docsDir, '.backups', new Date().toISOString().replace(/:/g, '-'));
  await fs.mkdir(backupDir, { recursive: true });
  
  for (const file of files) {
    const sourcePath = path.join(docsDir, file);
    const destPath = path.join(backupDir, file);
    
    try {
      const content = await fs.readFile(sourcePath, 'utf8');
      await fs.writeFile(destPath, content);
    } catch (error) {
      if (error.code !== 'ENOENT') {
        throw error;
      }
    }
  }
  
  return backupDir;
}

// Get user global config
async function getUserConfig() {
  try {
    // Try to load the user's global config
    const configCommands = require('./config');
    return await configCommands.getConfig();
  } catch (error) {
    return {};
  }
}

// Main update function
async function update(options) {
  const spinner = ora('Checking for updates...').start();
  
  // Load user config for model defaults
  const userConfig = await getUserConfig();
  
  // Merge options with user config
  options.model = options.model || userConfig.model || 'claude-3-haiku-20240307';
  
  // Force provider to be anthropic unless explicitly set to something else
  // This overrides any incorrect config to ensure we're always using the right provider
  options.provider = options.provider || 'anthropic';
  
  options.temperature = options.temperature || userConfig.temperature || 0.7;
  
  try {
    const prdPath = path.resolve(process.cwd(), options.input);
    const docsDir = path.dirname(prdPath);
    
    // Check if PRD exists
    try {
      await fs.access(prdPath);
    } catch (error) {
      spinner.fail(`PRD not found: ${prdPath}`);
      throw new Error(`PRD file not found: ${prdPath}`);
    }
    
    // Find the most recent backup to compare with
    const backupsDir = path.join(docsDir, '.backups');
    let previousPrdPath = null;
    
    try {
      const backupDirs = await fs.readdir(backupsDir);
      
      if (backupDirs.length > 0) {
        const latestBackup = backupDirs.sort().pop();
        previousPrdPath = path.join(backupsDir, latestBackup, path.basename(prdPath));
        
        try {
          await fs.access(previousPrdPath);
        } catch (error) {
          previousPrdPath = null;
        }
      }
    } catch (error) {
      // No backups directory, that's fine
    }
    
    // If no previous version found, create a temporary copy to compare with current
    if (!previousPrdPath) {
      spinner.text = 'No previous version found, using current as baseline';
      previousPrdPath = path.join(docsDir, '.tmp-prd-backup.md');
      await fs.copyFile(prdPath, previousPrdPath);
    }
    
    // Check for changes
    spinner.text = 'Analyzing changes in PRD...';
    const changeResult = await checkForChanges(prdPath, previousPrdPath);
    
    spinner.text = 'Finding affected documents...';
    const affectedDocs = await findAffectedDocuments(prdPath);
    
    if (affectedDocs.length === 0) {
      spinner.succeed('No documents found that need updating');
      return {
        updated: false,
        message: 'No updates needed'
      };
    }
    
    if (!changeResult.hasChanges && !options.check) {
      spinner.succeed('No significant changes detected in PRD');
      return {
        updated: false,
        message: 'No documents to update'
      };
    }
    
    if (options.check) {
      spinner.succeed('Found documents that may need updating');
      return {
        updated: false,
        message: 'Check mode: Not making any changes',
        affectedDocs,
        changes: changeResult.changeDescription
      };
    }
    
    // Create backup of all affected documents
    spinner.text = 'Creating backup of existing documents...';
    const backupPath = await backupDocuments(docsDir, [...affectedDocs, path.basename(prdPath)]);
    
    // Process each affected document
    for (const docFile of affectedDocs) {
      const docPath = path.join(docsDir, docFile);
      spinner.text = `Updating ${docFile}...`;
      
      // Read PRD and current document
      const prdContent = await fs.readFile(prdPath, 'utf8');
      let docContent;
      try {
        docContent = await fs.readFile(docPath, 'utf8');
      } catch (error) {
        if (error.code === 'ENOENT') {
          docContent = ''; // New file
        } else {
          throw error;
        }
      }
      
      // Prepare prompt for LLM
      const prompt = `You are an expert documentation assistant.

The Product Requirements Document (PRD) for a project has been updated with the following changes:

${changeResult.changeDescription}

I need you to update the following document to reflect these changes:
Document type: ${docFile}
Current content:
${docContent}

Please provide an updated version of this document that aligns with the current PRD.
Focus on adding, modifying, or removing content to match the changes in the PRD.
Maintain the same structure and style as the original document.

Full PRD content for reference:
${prdContent}`;
      
      // Call LLM to generate updated document
      let updatedContent;
      
      // Check for API key before making the call
      if (!process.env.ANTHROPIC_API_KEY) {
        const configDir = path.join(require('os').homedir(), '.vibe-docs');
        const configPath = path.join(configDir, 'config.json');
        
        let hasApiKey = false;
        if (fsSync.existsSync(configPath)) {
          try {
            const config = JSON.parse(fsSync.readFileSync(configPath, 'utf8'));
            if (config.apiKey) {
              hasApiKey = true;
            }
          } catch (error) {
            // Failed to read config file
          }
        }
        
        if (!hasApiKey) {
          throw new Error('API key missing. Please set your Anthropic API key using "vibe config:set-api-key" command.');
        }
      }
      
      // For now, we'll simulate the call until API integration is completed
      try {
        updatedContent = await simulateLlmCall(prompt, {
          model: options.model,
        });
      } catch (error) {
        throw new Error(`LLM API call failed: ${error.message}`);
      }
      
      // In a real implementation, parse LLM response to extract the updated document
      // For now, we'll just simulate adding an update notice
      const finalContent = `${docContent}\n\n## Updated on ${new Date().toISOString()}\n\n${updatedContent}`;
      
      // Write updated document
      await fs.writeFile(docPath, finalContent);
    }
    
    spinner.succeed(`Successfully updated ${affectedDocs.length} documents`);
    return {
      updated: true,
      affectedDocs,
      backupPath
    };
  } catch (error) {
    spinner.fail(`Error updating documentation: ${error.message}`);
    throw error;
  }
}

module.exports = update;