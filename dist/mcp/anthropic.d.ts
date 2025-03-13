interface AnthropicOptions {
    model: string;
    apiKey?: string;
    temperature?: number;
    maxTokens?: number;
}
/**
 * Call the Anthropic API with the given prompt
 */
export declare function callAnthropicApi(prompt: string, options: AnthropicOptions): Promise<string>;
export {};
