// commands/validate.js

const fs = require('fs').promises;
const path = require('path');
const ora = require('ora');
const chalk = require('chalk');

// Required sections for each document type
const requiredSections = {
  prd: [
    'Project Overview',
    'Problem Statement',
    'Core Features',
    'User Types & Scenarios',
    'Technical Requirements'
  ],
  instructions: [
    'Project Overview',
    'Core Features',
    'Technical Requirements'
  ],
  userStories: [
    'Introduction',
    'Core User Stories'
  ],
  designDoc: [
    'Visual Design',
    'Technical Architecture'
  ]
};

// Function to check if a section exists in content
function hasSection(content, section) {
  // This is a simple check - in a real implementation you might want to use
  // a more robust method to detect sections (e.g., regex or markdown parser)
  return content.includes(`## ${section}`) || content.includes(`# ${section}`);
}

// Function to check document completeness
async function checkDocumentCompleteness(filePath, docType) {
  try {
    const content = await fs.readFile(filePath, 'utf8');
    const required = requiredSections[docType];
    
    if (!required) {
      return { valid: true, issues: [] }; // No validation rules for this type
    }
    
    const missingRequiredSections = required.filter(section => !hasSection(content, section));
    
    // Check for placeholder text
    const containsPlaceholders = content.includes('[') && content.includes(']');
    
    const issues = [];
    
    if (missingRequiredSections.length > 0) {
      issues.push({
        type: 'missing_sections',
        sections: missingRequiredSections,
        message: `Missing required sections: ${missingRequiredSections.join(', ')}`
      });
    }
    
    if (containsPlaceholders) {
      issues.push({
        type: 'contains_placeholders',
        message: 'Document contains placeholder text that needs to be filled in'
      });
    }
    
    return {
      valid: issues.length === 0,
      issues
    };
  } catch (error) {
    if (error.code === 'ENOENT') {
      return {
        valid: false,
        issues: [{
          type: 'file_missing',
          message: 'File does not exist'
        }]
      };
    }
    throw error;
  }
}

// Main validate function
async function validate(options) {
  const spinner = ora('Validating documentation...').start();
  
  try {
    const docsDir = path.resolve(process.cwd(), options.dir);
    
    // Check if directory exists
    try {
      await fs.access(docsDir);
    } catch (error) {
      spinner.fail(`Documentation directory not found: ${docsDir}`);
      return {
        valid: false,
        issues: [{
          file: docsDir,
          message: 'Documentation directory does not exist'
        }]
      };
    }
    
    // Map file names to doc types
    const fileToDocType = {
      'prd.md': 'prd',
      'instructions.md': 'instructions',
      'user-stories.md': 'userStories',
      'design-doc.md': 'designDoc'
    };
    
    const allIssues = [];
    
    // Check each document
    for (const [fileName, docType] of Object.entries(fileToDocType)) {
      const filePath = path.join(docsDir, fileName);
      spinner.text = `Checking ${fileName}...`;
      
      const result = await checkDocumentCompleteness(filePath, docType);
      
      if (!result.valid) {
        result.issues.forEach(issue => {
          allIssues.push({
            file: fileName,
            ...issue
          });
        });
      }
    }
    
    // Check for inter-document consistency
    // This would be more complex in a real implementation
    
    const isValid = allIssues.length === 0;
    
    if (isValid) {
      spinner.succeed('All documentation is valid and complete');
    } else {
      spinner.warn(`Found ${allIssues.length} issues in documentation`);
    }
    
    return {
      valid: isValid,
      issues: allIssues
    };
  } catch (error) {
    spinner.fail(`Error validating documentation: ${error.message}`);
    throw error;
  }
}

module.exports = validate;
