import { startMcpServer } from './mcp/server.js';
// Start the MCP server
startMcpServer().catch(error => {
    console.error('Error starting MCP server:', error);
    process.exit(1);
});
