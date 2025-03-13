const fs = require('fs').promises;
const path = require('path');
const ora = require('ora');
const chalk = require('chalk');
const inquirer = require('inquirer');

// Config directory
const getConfigDir = () => {
  const userHome = require('os').homedir();
  return path.join(userHome, '.vibe-docs');
};

// Config file path
const getConfigPath = () => {
  return path.join(getConfigDir(), 'config.json');
};

// Get current config
async function getConfig() {
  try {
    const configPath = getConfigPath();
    const configData = await fs.readFile(configPath, 'utf8');
    return JSON.parse(configData);
  } catch (error) {
    // Return default config if file doesn't exist
    return {
      apiKey: '',
      provider: 'anthropic',
      model: 'claude-3-haiku-20240307',
      temperature: 0.7
    };
  }
}

// Save config
async function saveConfig(config) {
  const configDir = getConfigDir();
  const configPath = getConfigPath();
  
  // Create config directory if it doesn't exist
  try {
    await fs.mkdir(configDir, { recursive: true });
  } catch (error) {
    if (error.code !== 'EEXIST') {
      throw error;
    }
  }
  
  // Write config file
  await fs.writeFile(configPath, JSON.stringify(config, null, 2), 'utf8');
}

// Set API key
async function setApiKey(options) {
  const spinner = ora('Setting API key...').start();
  
  try {
    // Get current config
    const config = await getConfig();
    
    // If key is provided in options, use it
    if (options.key) {
      config.apiKey = options.key;
    } else {
      // Otherwise prompt for it
      spinner.stop();
      const answers = await inquirer.prompt([
        {
          type: 'input',
          name: 'apiKey',
          message: 'Enter your API key:',
          validate: input => input.trim() !== '' || 'API key cannot be empty'
        }
      ]);
      
      config.apiKey = answers.apiKey;
      spinner.start();
    }
    
    // Set provider if provided
    if (options.provider) {
      config.provider = options.provider;
    } else {
      // Default to anthropic if not specified
      config.provider = 'anthropic';
    }
    
    // Save config
    await saveConfig(config);
    
    spinner.succeed('API key saved');
    return { success: true };
  } catch (error) {
    spinner.fail(`Failed to set API key: ${error.message}`);
    throw error;
  }
}

// Set model
async function setModel(options) {
  const spinner = ora('Setting model...').start();
  
  try {
    // Get current config
    const config = await getConfig();
    
    // Set model
    config.model = options.model;
    
    // Save config
    await saveConfig(config);
    
    spinner.succeed(`Model set to ${options.model}`);
    return { success: true };
  } catch (error) {
    spinner.fail(`Failed to set model: ${error.message}`);
    throw error;
  }
}

// Set provider
async function setProvider(options) {
  const spinner = ora('Setting provider...').start();
  
  try {
    // Get current config
    const config = await getConfig();
    
    // Check if valid provider
    if (!['anthropic', 'openai'].includes(options.provider)) {
      spinner.fail(`Invalid provider: ${options.provider}. Valid options are: anthropic, openai`);
      throw new Error(`Invalid provider: ${options.provider}`);
    }
    
    // Set provider
    config.provider = options.provider;
    
    // Save config
    await saveConfig(config);
    
    spinner.succeed(`Provider set to ${options.provider}`);
    return { success: true };
  } catch (error) {
    spinner.fail(`Failed to set provider: ${error.message}`);
    throw error;
  }
}

// Reset config to defaults
async function resetConfig() {
  const spinner = ora('Resetting configuration...').start();
  
  try {
    // Default config
    const defaultConfig = {
      apiKey: '',
      provider: 'anthropic',
      model: 'claude-3-haiku-20240307',
      temperature: 0.7
    };
    
    // Save config
    await saveConfig(defaultConfig);
    
    spinner.succeed('Configuration reset to defaults');
    return { success: true };
  } catch (error) {
    spinner.fail(`Failed to reset configuration: ${error.message}`);
    throw error;
  }
}

// Show current config
async function showConfig() {
  const spinner = ora('Loading configuration...').start();
  
  try {
    const config = await getConfig();
    spinner.succeed('Configuration loaded');
    
    console.log('\nCurrent configuration:');
    console.log(`API Key: ${config.apiKey ? '****' + config.apiKey.slice(-4) : 'Not set'}`);
    console.log(`Provider: ${config.provider || 'anthropic'}`);
    console.log(`Model: ${config.model || 'claude-3-haiku-20240307'}`);
    console.log(`Temperature: ${config.temperature || 0.7}`);
    
    return { config };
  } catch (error) {
    spinner.fail(`Failed to load configuration: ${error.message}`);
    throw error;
  }
}

module.exports = {
  setApiKey,
  setModel,
  setProvider,
  resetConfig,
  showConfig,
  getConfig
};