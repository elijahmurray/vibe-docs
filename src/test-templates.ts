import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

// Get the directory where this script is located
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const packageDir = path.resolve(__dirname, '..');

async function testTemplates() {
  try {
    console.log('Testing template access...');
    console.log(`Package directory: ${packageDir}`);
    
    // Check if templates directory exists
    const templatesDir = path.join(packageDir, 'templates');
    console.log(`Templates directory: ${templatesDir}`);
    
    try {
      await fs.access(templatesDir);
      console.log('✅ Templates directory exists');
    } catch (error) {
      console.error('❌ Templates directory does not exist:', error);
      return;
    }
    
    // List templates
    const templates = await fs.readdir(templatesDir);
    console.log(`Available templates: ${templates.join(', ')}`);
    
    // Check standard template
    const standardTemplateDir = path.join(templatesDir, 'standard');
    try {
      await fs.access(standardTemplateDir);
      console.log('✅ Standard template directory exists');
    } catch (error) {
      console.error('❌ Standard template directory does not exist:', error);
      return;
    }
    
    // List files in standard template
    const files = await fs.readdir(standardTemplateDir);
    console.log(`Files in standard template: ${files.join(', ')}`);
    
    if (files.length === 0) {
      console.error('❌ Standard template directory is empty');
      return;
    }
    
    console.log('✅ Template test completed successfully');
  } catch (error) {
    console.error('Error testing templates:', error);
  }
}

testTemplates();
