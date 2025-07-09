#!/usr/bin/env python3
"""
MCP Client for Deep Wiki Server
Implements Model Context Protocol client to communicate with Deep Wiki MCP server.
"""

import asyncio
import json
import logging
import uuid
from typing import Dict, Any, Optional, AsyncGenerator
import aiohttp
from dataclasses import dataclass
from enum import Enum
from anthropic import Anthropic

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MCPMessageType(Enum):
    """MCP message types according to the specification"""
    REQUEST = "request"
    RESPONSE = "response"
    NOTIFICATION = "notification"


@dataclass
class MCPMessage:
    """MCP message structure following JSON-RPC 2.0"""
    jsonrpc: str = "2.0"
    id: Optional[str] = None
    method: Optional[str] = None
    params: Optional[Dict[str, Any]] = None
    result: Optional[Any] = None
    error: Optional[Dict[str, Any]] = None


class MCPClient:
    """MCP Client implementation for Deep Wiki server"""

    #def __init__(self, server_url: str = "https://mcp.deepwiki.com/mcp"):
    def __init__(self, server_url: str):
        self.server_url = server_url
        self.session: Optional[aiohttp.ClientSession] = None
        self.server_capabilities: Dict[str, Any] = {}
        self.client_capabilities: Dict[str, Any] = {
            "roots": {
                "listChanged": True
            },
            "sampling": {}
        }
        self.initialized = False
        self.mcp_session_id = ""

    async def __aenter__(self):
        """Async context manager entry"""
        connector = aiohttp.TCPConnector(ssl=False)
        self.session = aiohttp.ClientSession(connector=connector)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()

    def generate_request_id(self) -> str:
        """Generate unique request ID"""
        return str(uuid.uuid4())

    def create_request(self, method: str, params: Optional[Dict[str, Any]] = None) -> MCPMessage:
        """Create MCP request message"""
        return MCPMessage(
            jsonrpc="2.0",
            id=self.generate_request_id(),
            method=method,
            params=params or {}
        )

    def create_notification(self, method: str, params: Optional[Dict[str, Any]] = None) -> MCPMessage:
        """Create MCP notification message"""
        return MCPMessage(
            jsonrpc="2.0",
            method=method,
            params=params or {}
        )

    async def send_streaming_request(self, message: MCPMessage) -> Dict[str, Any]:
        """Send request using HTTP Streaming transport"""
        if not self.session:
            raise RuntimeError("Session not initialized. Use async context manager.")

        # Convert message to JSON
        message_data = {
            "jsonrpc": message.jsonrpc,
            "method": message.method,
            "params": message.params or {}
        }

        if message.id:
            message_data["id"] = message.id

        logger.info(f"Sending streaming request: {message.method}")
        logger.debug(f"Request data: {json.dumps(message_data, indent=2)}")

        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json, text/event-stream"  # New-line delimited JSON for streaming
        }
        if self.mcp_session_id != "":
            headers["Mcp-Session-Id"] = self.mcp_session_id

        try:
            async with self.session.post(
                    self.server_url,
                    json=message_data,
                    headers=headers,
                    # headers={
                    #     "Content-Type": "application/json",
                    #     "Accept": "application/json, text/event-stream",  # New-line delimited JSON for streaming
                    #     #"Accept": "application/x-ndjson"  # New-line delimited JSON for streaming
                    #     #text/event-stream
                    #     #"Mcp-Session-Id": self.mcp_session_id
                    # },
                    ssl=False
            ) as response:
                if response.status != 200:
                    raise RuntimeError(f"HTTP {response.status}: {await response.text()}")

                self.mcp_session_id = response.headers["Mcp-Session-Id"]

                # Handle streaming response
                full_response = ""
                async for chunk in response.content.iter_chunked(1024):
                    chunk_text = chunk.decode('utf-8')
                    full_response += chunk_text

                # Parse the response - it might be multiple JSON objects separated by newlines
                response_lines = [line.strip() for line in full_response.split('\n') if line.strip()]

                # For most MCP responses, we expect a single JSON object
                # But streaming responses might have multiple parts
                final_response = None
                for line in response_lines:
                    line = line.replace("data: ", "")
                    print(line)
                    try:
                        parsed_line = json.loads(line)
                        # Look for the response with matching ID or the final result
                        if message.id and parsed_line.get("id") == message.id:
                            final_response = parsed_line
                            break
                        elif "result" in parsed_line or "error" in parsed_line:
                            final_response = parsed_line
                    except json.JSONDecodeError:
                        continue

                if final_response is None:
                    # If no structured response found, try parsing the whole thing
                    try:
                        final_response = json.loads(full_response)
                    except json.JSONDecodeError:
                        raise RuntimeError(f"Could not parse streaming response: {full_response}")

                logger.info(f"Received streaming response for: {message.method}")
                logger.debug(f"Response data: {json.dumps(final_response, indent=2)}")

                return final_response

        except Exception as e:
            logger.error(f"Error sending streaming request: {e}")
            raise

    async def send_notification(self, message: MCPMessage) -> None:
        """Send notification to MCP server using streaming transport"""
        if not self.session:
            raise RuntimeError("Session not initialized. Use async context manager.")

        # Convert message to JSON
        message_data = {
            "jsonrpc": message.jsonrpc,
            "method": message.method,
            "params": message.params or {}
        }

        logger.info(f"Sending streaming notification: {message.method}")
        logger.debug(f"Notification data: {json.dumps(message_data, indent=2)}")

        try:
            async with self.session.post(
                    self.server_url,
                    json=message_data,
                    headers={
                        "Content-Type": "application/json",
                        #"Accept": "application/x-ndjson"
                        "Accept": "application/json, text/event-stream",
                        "Mcp-Session-Id": self.mcp_session_id
                    },
                    ssl=False
            ) as response:
                if response.status != 200:
                    logger.warning(f"Notification HTTP {response.status}: {await response.text()}")

                # Consume the response even for notifications
                async for chunk in response.content.iter_chunked(1024):
                    pass  # Just consume the stream

        except Exception as e:
            logger.error(f"Error sending streaming notification: {e}")
            raise

    async def initialize(self) -> Dict[str, Any]:
        """Initialize MCP connection with capabilities negotiation"""
        logger.info("Initializing MCP connection...")

        # Send initialize request
        init_request = self.create_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": self.client_capabilities,
            "clientInfo": {
                "name": "deep-wiki-mcp-client",
                "version": "1.0.0"
            }
        })

        response = await self.send_streaming_request(init_request)

        if "error" in response:
            raise RuntimeError(f"Initialize failed: {response['error']}")

        # Store server capabilities
        result = response.get("result", {})
        self.server_capabilities = result.get("capabilities", {})

        logger.info("Server capabilities received:")
        logger.info(json.dumps(self.server_capabilities, indent=2))

        # Send initialized notification
        await self.send_notification(self.create_notification("notifications/initialized"))

        self.initialized = True
        logger.info("MCP connection initialized successfully")

        return result

    async def list_tools(self) -> Dict[str, Any]:
        """List available tools from the server"""
        if not self.initialized:
            raise RuntimeError("Client not initialized. Call initialize() first.")

        logger.info("Requesting tools list...")

        tools_request = self.create_request("tools/list")
        response = await self.send_streaming_request(tools_request)

        if "error" in response:
            raise RuntimeError(f"List t¡ools failed: {response['error']}")

        return response.get("result", {})

    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        """Call a specific tool with given arguments"""
        if not self.initialized:
            raise RuntimeError("Client not initialized. Call initialize() first.")

        logger.info(f"Calling tool: {tool_name}")
        logger.debug(f"Tool arguments: {json.dumps(arguments, indent=2)}")

        tool_request = self.create_request("tools/call", {
            "name": tool_name,
            "arguments": arguments
        })

        response = await self.send_streaming_request(tool_request)

        if "error" in response:
            raise RuntimeError(f"Tool call failed: {response['error']}")

        return response.get("result", {})

    async def ask_question(self, repository: str, question: str) -> Dict[str, Any]:
        """Ask a question about a GitHub repository using the ask_question tool"""
        return await self.call_tool("ask_question", {
            "repoName": repository,
            "question": question
        })


class ClaudeClient:
    """Client for interacting with Claude Sonnet 4"""

    def __init__(self, api_key: str):
        self.client = Anthropic(api_key=api_key)
        self.model = "claude-sonnet-4-20250514"

    #    async def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
    async def generate_response(self, prompt: str, context: Optional[str] = None):
        """Generate a response using Claude Sonnet 4"""
        try:
            full_prompt = prompt
            if context:
                full_prompt = f"Context: {context}\n\nQuery: {prompt}"

            message = self.client.messages.create(
                model=self.model,
                max_tokens=4000,
                messages=[
                    {"role": "user", "content": full_prompt}
                ]
            )

            # return message.content[0].text
            return message

        except Exception as e:
            logger.error(f"Claude API error: {e}")
            return f"Error generating response: {e}"


async def main():
    """Main function demonstrating the MCP client usage"""
    logger.info("Starting MCP Deep Wiki Client...")

    CLAUDE_API_KEY = "ANTRHOPIC_API_KEY"
    DEEP_WIKI_URL = "https://mcp.deepwiki.com/mcp"  # Adjust to your Deep Wiki MCP server URL


    async with MCPClient(DEEP_WIKI_URL) as client:
        try:
            # Initialize the connection
            init_result = await client.initialize()
            logger.info("✓ MCP connection initialized")

            # List available tools
            tools = await client.list_tools()
            logger.info("✓ Available tools:")
            for tool in tools.get("tools", []):
                logger.info(f"  - {tool.get('name', 'Unknown')}: {tool.get('description', 'No description')}")

            # Ask the required question about OpenAI Codex
            logger.info("✓ Asking question about OpenAI Codex...")
            result = await client.ask_question(
                repository="openai/codex",
                question="What is OpenAI Codex?"
            )

            logger.info("✓ Question answered successfully!")

            claude = ClaudeClient(CLAUDE_API_KEY)
            response = await claude.generate_response(prompt="Based on its specification, provide a summary of the main points about OpenAI Codex", context=result['content'][0]['text'])

            logger.info("Answer:")

            print("\n" + "-" * 80)
            print("RESULT:")
            print("\n" + "-" * 80)
            print(response.content[0].text)
            print("-" * 80)
            print("\n\n\n")
            print("DETAIL:")
            print("\n" + "-" * 80)
            print(response)
            print("-" * 80)

        except Exception as e:
            logger.error(f"Error: {e}")
            raise


if __name__ == "__main__":
    # Install required dependencies
    print("Required dependencies:")
    print("pip install aiohttp")
    print("\nRunning MCP client with HTTP Streaming transport...")
    print("-" * 50)

    # Run the client
    asyncio.run(main())
