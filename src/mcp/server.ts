import { McpServer, ResourceTemplate } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import fs from 'fs/promises';
import path from 'path';
import { callAnthropicApi } from './anthropic.js';

// Define document types with proper type safety
interface DocumentType {
  filename: string;
  prompt: string;
}

// Get the package directory (where vibe-docs is installed)
import { fileURLToPath } from 'url';
import { dirname } from 'path';

// Get the directory where the vibe-docs package is installed
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const packageDir = path.resolve(__dirname, '../..');

// Current working directory (where the command is run from)
const currentDir = process.cwd();

// Function to get absolute path for a template directory
const getTemplatePath = (templateName: string): string => {
  // First priority: check in the package directory
  const packageTemplatePath = path.resolve(packageDir, 'templates', templateName);
  
  // Second priority: check in the current directory
  const currentDirTemplatePath = path.resolve(currentDir, 'templates', templateName);
  
  return packageTemplatePath;
};

// Document types and their generation prompts
const documentTypes: Record<string, DocumentType> = {
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

/**
 * Create and configure the MCP server
 */
export async function createMcpServer() {
  // Create an MCP server
  const server = new McpServer({
    name: "Vibe Docs",
    version: "1.0.0"
  });

  // Add a tool to initialize documentation structure
  server.tool(
    "init-docs",
    {
      directory: z.string().default('./docs'),
      template: z.string().default('standard')
    },
    async ({ directory, template }) => {
      console.log('======== VIBE DOCS INIT ========');
      console.log(`Initializing docs in: ${directory}`);
      console.log(`Using template: ${template}`);
      
      try {
        // SUPER SIMPLE IMPLEMENTATION
        
        // 1. Find the template directory
        const templateDir = path.join(packageDir, 'templates', template);
        console.log(`Template dir: ${templateDir}`);
        
        // 2. Make target directory absolute
        const targetDir = path.isAbsolute(directory) 
          ? directory 
          : path.join(process.cwd(), directory);
        console.log(`Target dir: ${targetDir}`);
        
        // 3. Create target directory
        console.log(`Creating directory: ${targetDir}`);
        await fs.mkdir(targetDir, { recursive: true });
        
        // 4. Check if template exists
        console.log(`Checking if template exists: ${templateDir}`);
        try {
          await fs.access(templateDir);
        } catch (error) {
          console.error(`Template not found: ${templateDir}`);
          throw new Error(`Template '${template}' not found.`);
        }
        
        // 5. List and copy files
        console.log(`Reading template directory: ${templateDir}`);
        const files = await fs.readdir(templateDir);
        console.log(`Files found: ${files.join(', ')}`);
        
        if (files.length === 0) {
          throw new Error(`Template '${template}' exists but is empty`);
        }
        
        let successCount = 0;
        
        // Copy each file
        for (const file of files) {
          // Skip hidden files
          if (file.startsWith('.')) {
            console.log(`Skipping hidden file: ${file}`);
            continue;
          }
          
          const sourcePath = path.join(templateDir, file);
          const targetPath = path.join(targetDir, file);
          
          try {
            // Skip directories
            const stats = await fs.stat(sourcePath);
            if (stats.isDirectory()) {
              console.log(`Skipping directory: ${file}`);
              continue;
            }
            
            // Copy the file
            console.log(`Copying ${file}: ${sourcePath} -> ${targetPath}`);
            await fs.copyFile(sourcePath, targetPath);
            console.log(`Successfully copied: ${file}`);
            successCount++;
          } catch (fileError) {
            console.error(`Error with file ${file}: ${fileError instanceof Error ? fileError.message : String(fileError)}`);
          }
        }
        
        console.log(`Success! Copied ${successCount} files.`);
        console.log('======== VIBE DOCS INIT COMPLETE ========');
        
        return {
          content: [{ 
            type: "text", 
            text: `Documentation structure initialized in ${targetDir} using ${template} template.\n\nCopied ${successCount} files successfully.` 
          }]
        };
      } catch (error) {
        console.error(`ERROR: ${error instanceof Error ? error.message : String(error)}`);
        console.log('======== VIBE DOCS INIT FAILED ========');
        
        return {
          content: [{ 
            type: "text", 
            text: `Error initializing documentation: ${error instanceof Error ? error.message : String(error)}` 
          }]
        };
      }
    }
  );

  // Add a tool to generate documentation from PRD
  server.tool(
    "generate-docs",
    {
      inputFile: z.string().default('./docs/prd.md'),
      outputTypes: z.array(z.string()).default(['instructions', 'user-stories', 'design-doc']),
      updateExisting: z.boolean().default(false),
      model: z.string().default('claude-3-haiku-20240307'),
      anthropicApiKey: z.string().optional()
    },
    async ({ inputFile, outputTypes, updateExisting, model, anthropicApiKey }) => {
      try {
        // Read the PRD content
        const prdContent = await fs.readFile(inputFile, 'utf8');
        const outputDir = path.dirname(inputFile);
        
        let results = [];
        
        // Process each requested document type
        for (const type of outputTypes) {
          if (!documentTypes[type]) {
            results.push(`Skipping unknown document type: ${type}`);
            continue;
          }
          
          const docType = documentTypes[type];
          const outputPath = path.join(outputDir, docType.filename);
          
          // Check if file exists and skip if not updating
          try {
            await fs.access(outputPath);
            if (!updateExisting) {
              results.push(`Skipping existing file: ${docType.filename}`);
              continue;
            }
          } catch (error) {
            // File doesn't exist, which is fine
          }
          
          // Replace placeholder in prompt
          const prompt = docType.prompt.replace('{{prdContent}}', prdContent);
          
          // Call Anthropic API
          const response = await callAnthropicApi(prompt, {
            model,
            apiKey: anthropicApiKey
          });
          
          // Write the response to the output file
          await fs.writeFile(outputPath, response);
          
          results.push(`Generated ${docType.filename}`);
        }
        
        return {
          content: [{ 
            type: "text", 
            text: results.join('\n') 
          }]
        };
      } catch (error) {
        return {
          content: [{ 
            type: "text", 
            text: `Error generating documentation: ${error instanceof Error ? error.message : String(error)}` 
          }]
        };
      }
    }
  );

  // Add a tool to validate documentation
  server.tool(
    "validate-docs",
    {
      directory: z.string().default('./docs'),
      fix: z.boolean().default(false)
    },
    async ({ directory, fix }) => {
      try {
        // Check if the directory exists
        try {
          await fs.access(directory);
        } catch (error) {
          return {
            content: [{ 
              type: "text", 
              text: `Error: Directory ${directory} does not exist.` 
            }]
          };
        }
        
        // Check for required files
        const requiredFiles = ['prd.md'];
        const missingFiles = [];
        
        for (const file of requiredFiles) {
          try {
            await fs.access(path.join(directory, file));
          } catch (error) {
            missingFiles.push(file);
          }
        }
        
        if (missingFiles.length > 0) {
          return {
            content: [{ 
              type: "text", 
              text: `Validation failed: Missing required files: ${missingFiles.join(', ')}` 
            }]
          };
        }
        
        // Read PRD and check for required sections
        const prdContent = await fs.readFile(path.join(directory, 'prd.md'), 'utf8');
        const requiredSections = ['Project Overview', 'Core Features'];
        const missingSections = [];
        
        for (const section of requiredSections) {
          if (!prdContent.includes(`# ${section}`) && !prdContent.includes(`## ${section}`)) {
            missingSections.push(section);
          }
        }
        
        if (missingSections.length > 0) {
          return {
            content: [{ 
              type: "text", 
              text: `Validation failed: PRD is missing required sections: ${missingSections.join(', ')}` 
            }]
          };
        }
        
        return {
          content: [{ 
            type: "text", 
            text: `Validation successful: All required files and sections are present.` 
          }]
        };
      } catch (error) {
        return {
          content: [{ 
            type: "text", 
            text: `Error validating documentation: ${error instanceof Error ? error.message : String(error)}` 
          }]
        };
      }
    }
  );

  // Add a tool to update documentation
  server.tool(
    "update-docs",
    {
      inputFile: z.string().default('./docs/prd.md'),
      check: z.boolean().default(false),
      model: z.string().default('claude-3-haiku-20240307'),
      anthropicApiKey: z.string().optional()
    },
    async ({ inputFile, check, model, anthropicApiKey }) => {
      try {
        // Read the PRD content
        const prdContent = await fs.readFile(inputFile, 'utf8');
        const outputDir = path.dirname(inputFile);
        
        let results = [];
        
        // Check for existing derived documents
        for (const [type, docType] of Object.entries(documentTypes)) {
          const outputPath = path.join(outputDir, docType.filename);
          
          try {
            await fs.access(outputPath);
            
            if (!check) {
              // Replace placeholder in prompt
              const prompt = docType.prompt.replace('{{prdContent}}', prdContent);
              
              // Call Anthropic API
              const response = await callAnthropicApi(prompt, {
                model,
                apiKey: anthropicApiKey
              });
              
              // Write the response to the output file
              await fs.writeFile(outputPath, response);
              
              results.push(`Updated ${docType.filename}`);
            } else {
              results.push(`Found ${docType.filename} (would update if not in check mode)`);
            }
          } catch (error) {
            results.push(`${docType.filename} not found, skipping`);
          }
        }
        
        return {
          content: [{ 
            type: "text", 
            text: results.join('\n') 
          }]
        };
      } catch (error) {
        return {
          content: [{ 
            type: "text", 
            text: `Error updating documentation: ${error instanceof Error ? error.message : String(error)}` 
          }]
        };
      }
    }
  );

  // Add a tool to set API key
  server.tool(
    "set-api-key",
    {
      apiKey: z.string()
    },
    async ({ apiKey }) => {
      try {
        // Create config directory if it doesn't exist
        const userHome = process.env.HOME || process.env.USERPROFILE || '';
        const configDir = path.join(userHome, '.vibe-docs');
        await fs.mkdir(configDir, { recursive: true });
        
        // Write config file
        const config = {
          apiKey,
          provider: 'anthropic',
          model: 'claude-3-haiku-20240307',
          temperature: 0.7
        };
        
        await fs.writeFile(
          path.join(configDir, 'config.json'),
          JSON.stringify(config, null, 2),
          'utf8'
        );
        
        return {
          content: [{ 
            type: "text", 
            text: `API key saved successfully.` 
          }]
        };
      } catch (error) {
        return {
          content: [{ 
            type: "text", 
            text: `Error setting API key: ${error instanceof Error ? error.message : String(error)}` 
          }]
        };
      }
    }
  );

  // Add a resource to access documentation templates
  server.resource(
    "templates",
    new ResourceTemplate("templates://{templateName}", { list: async () => {
      try {
        const templateDir = path.resolve(path.join(currentDir, 'templates'));
        const templates = await fs.readdir(templateDir);
        return {
          resources: templates.map(name => ({
            name,
            uri: `templates://${name}`,
            description: `Template: ${name}`
          }))
        };
      } catch (error) {
        return { resources: [] };
      }
    }}),
    async (uri, { templateName }) => {
      try {
        const templateDir = path.resolve(path.join(currentDir, 'templates'));
        const templatePath = path.join(templateDir, templateName as string);
        
        const content = await fs.readFile(templatePath, 'utf8');
        
        return {
          contents: [{
            uri: uri.href,
            text: content
          }]
        };
      } catch (error) {
        return {
          contents: [{
            uri: uri.href,
            text: `Error loading template: ${error instanceof Error ? error.message : String(error)}`
          }]
        };
      }
    }
  );

  // Add a resource to access documentation files
  server.resource(
    "docs",
    new ResourceTemplate("docs://{filePath*}", { list: async () => {
      try {
        const docsDir = path.resolve('./docs');
        const files = await fs.readdir(docsDir);
        return {
          resources: files.map(name => ({
            name,
            uri: `docs://${name}`,
            description: `Document: ${name}`
          }))
        };
      } catch (error) {
        return { resources: [] };
      }
    }}),
    async (uri, { filePath }) => {
      try {
        const docsDir = path.resolve('./docs');
        const docPath = path.join(docsDir, filePath as string);
        
        const content = await fs.readFile(docPath, 'utf8');
        
        return {
          contents: [{
            uri: uri.href,
            text: content
          }]
        };
      } catch (error) {
        return {
          contents: [{
            uri: uri.href,
            text: `Error loading document: ${error instanceof Error ? error.message : String(error)}`
          }]
        };
      }
    }
  );

  // Add a simple prompt for documentation generation guidance
  server.prompt(
    "generate-doc",
    "Generate documentation based on PRD content",
    () => {
      return {
        messages: [{
          role: "user",
          content: {
            type: "text",
            text: "Please provide the PRD content and document type to generate."
          }
        }]
      };
    }
  );

  // Add a prompt with arguments for generating specific document types
  server.prompt(
    "generate-doc-with-args",
    {
      docType: z.enum(['instructions', 'user-stories', 'design-doc']),
      prdContent: z.string()
    },
    (args) => {
      const { docType, prdContent } = args;
      const docTypeInfo = documentTypes[docType];
      if (!docTypeInfo) {
        return {
          messages: [{
            role: "user",
            content: {
              type: "text",
              text: `Unknown document type: ${docType}`
            }
          }]
        };
      }
      
      const prompt = docTypeInfo.prompt.replace('{{prdContent}}', prdContent);
      
      return {
        messages: [{
          role: "user",
          content: {
            type: "text",
            text: prompt
          }
        }]
      };
    }
  );

  return server;
}

/**
 * Start the MCP server
 */
export async function startMcpServer() {
  const server = await createMcpServer();
  
  // Start receiving messages on stdin and sending messages on stdout
  const transport = new StdioServerTransport();
  await server.connect(transport);
  
  return server;
}
