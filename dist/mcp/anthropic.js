import fs from 'fs/promises';
import path from 'path';
import axios from 'axios';
import dotenv from 'dotenv';
// Load environment variables
dotenv.config();
/**
 * Call the Anthropic API with the given prompt
 */
export async function callAnthropicApi(prompt, options) {
    // Get API key from options, environment variable, or config file
    let apiKey = options.apiKey || process.env.ANTHROPIC_API_KEY;
    // If no API key provided, try to load from config file
    if (!apiKey) {
        try {
            const userHome = process.env.HOME || process.env.USERPROFILE || '';
            const configPath = path.join(userHome, '.vibe-docs', 'config.json');
            const configData = await fs.readFile(configPath, 'utf8');
            const config = JSON.parse(configData);
            apiKey = config.apiKey;
        }
        catch (error) {
            // Failed to read config file
        }
    }
    // Check if we have an API key
    if (!apiKey) {
        throw new Error('Anthropic API key not found. Please set ANTHROPIC_API_KEY environment variable or run "vibe config:set-api-key"');
    }
    try {
        const requestBody = {
            model: options.model,
            messages: [{ role: 'user', content: prompt }],
            max_tokens: options.maxTokens || 4000,
            temperature: options.temperature || 0.7
        };
        const response = await axios.post('https://api.anthropic.com/v1/messages', requestBody, {
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': apiKey,
                'anthropic-version': '2023-06-01'
            }
        });
        // Safely extract text from the response
        if (response.data.content && response.data.content.length > 0) {
            return response.data.content[0].text;
        }
        throw new Error('Unexpected response format from Anthropic API');
    }
    catch (error) {
        if (axios.isAxiosError(error) && error.response) {
            // Handle API errors
            if (error.response.status === 401) {
                throw new Error('Invalid Anthropic API key. Please check your API key and try again.');
            }
            else {
                throw new Error(`Anthropic API error: ${error.response.status} - ${error.response.data?.error?.message || error.message}`);
            }
        }
        else {
            // Handle network errors
            throw new Error(`Error calling Anthropic API: ${error instanceof Error ? error.message : String(error)}`);
        }
    }
}
