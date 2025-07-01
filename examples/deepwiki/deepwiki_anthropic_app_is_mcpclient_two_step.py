#!/usr/bin/env python3
"""
Claude Sonnet 4 with Deep Wiki MCP Integration
Demonstrates the complete flow:
1. Claude requests tool execution
2. App executes MCP client to get information
3. App sends results back to Claude
4. Display final response
"""

import asyncio
import json
import logging
import uuid
from typing import Dict, Any, Optional, List
import aiohttp
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
ANTHROPIC_API_KEY = "your-anthropic-api-key-here"  # Replace with your API key
ANTHROPIC_API_URL = "https://api.anthropic.com/v1/messages"
DEEPWIKI_MCP_URL = "https://mcp.deepwiki.com/mcp"


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
    """MCP Client for Deep Wiki server using HTTP Streaming"""

    def __init__(self, server_url: str = DEEPWIKI_MCP_URL):
        self.server_url = server_url
        self.session: Optional[aiohttp.ClientSession] = None
        self.server_capabilities: Dict[str, Any] = {}
        self.client_capabilities: Dict[str, Any] = {
            "roots": {"listChanged": True},
            "sampling": {}
        }
        self.mcp_session_id = ""
        self.initialized = False

    async def __aenter__(self):
        connector = aiohttp.TCPConnector(ssl=False)
        self.session = aiohttp.ClientSession(connector=connector)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def generate_request_id(self) -> str:
        return str(uuid.uuid4())

    def create_request(self, method: str, params: Optional[Dict[str, Any]] = None) -> MCPMessage:
        return MCPMessage(
            jsonrpc="2.0",
            id=self.generate_request_id(),
            method=method,
            params=params or {}
        )

    def create_notification(self, method: str, params: Optional[Dict[str, Any]] = None) -> MCPMessage:
        return MCPMessage(
            jsonrpc="2.0",
            method=method,
            params=params or {}
        )

    async def send_streaming_request(self, message: MCPMessage) -> Dict[str, Any]:
        """Send request using HTTP Streaming transport"""
        if not self.session:
            raise RuntimeError("Session not initialized.")

        message_data = {
            "jsonrpc": message.jsonrpc,
            "method": message.method,
            "params": message.params or {}
        }

        if message.id:
            message_data["id"] = message.id

        logger.info(f"MCP Request: {message.method}")

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

                # Parse response lines
                response_lines = [line.strip() for line in full_response.split('\n') if line.strip()]

                final_response = None
                for line in response_lines:
                    line = line.replace("data: ", "")
                    print(line)
                    try:
                        parsed_line = json.loads(line)
                        if message.id and parsed_line.get("id") == message.id:
                            final_response = parsed_line
                            break
                        elif "result" in parsed_line or "error" in parsed_line:
                            final_response = parsed_line
                    except json.JSONDecodeError:
                        continue

                if final_response is None:
                    try:
                        final_response = json.loads(full_response)
                    except json.JSONDecodeError:
                        raise RuntimeError(f"Could not parse response: {full_response}")

                logger.info(f"MCP Response received for: {message.method}")
                return final_response

        except Exception as e:
            logger.error(f"MCP request error: {e}")
            raise

    async def send_notification(self, message: MCPMessage) -> None:
        """Send notification using streaming transport"""
        if not self.session:
            raise RuntimeError("Session not initialized.")

        message_data = {
            "jsonrpc": message.jsonrpc,
            "method": message.method,
            "params": message.params or {}
        }

        logger.info(f"MCP Notification: {message.method}")

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
                    logger.warning(f"Notification HTTP {response.status}")

                # Consume response
                async for chunk in response.content.iter_chunked(1024):
                    pass

        except Exception as e:
            logger.error(f"MCP notification error: {e}")
            raise

    async def initialize(self) -> Dict[str, Any]:
        """Initialize MCP connection"""
        logger.info("Initializing MCP connection...")

        init_request = self.create_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": self.client_capabilities,
            "clientInfo": {
                "name": "claude-deepwiki-integration",
                "version": "1.0.0"
            }
        })

        response = await self.send_streaming_request(init_request)

        if "error" in response:
            raise RuntimeError(f"Initialize failed: {response['error']}")

        result = response.get("result", {})
        self.server_capabilities = result.get("capabilities", {})

        # Send initialized notification
        await self.send_notification(self.create_notification("notifications/initialized"))

        self.initialized = True
        logger.info("MCP connection initialized")
        return result

    async def list_tools(self) -> Dict[str, Any]:
        """List available tools"""
        if not self.initialized:
            raise RuntimeError("Client not initialized")

        tools_request = self.create_request("tools/list")
        response = await self.send_streaming_request(tools_request)

        if "error" in response:
            raise RuntimeError(f"List tools failed: {response['error']}")

        return response.get("result", {})

    async def ask_question(self, repository: str, question: str) -> Dict[str, Any]:
        """Ask question using the ask_question tool"""
        if not self.initialized:
            raise RuntimeError("Client not initialized")

        tool_request = self.create_request("tools/call", {
            "name": "ask_question",
            "arguments": {
                "repoName": repository,
                "question": question
            }
        })

        response = await self.send_streaming_request(tool_request)

        if "error" in response:
            raise RuntimeError(f"Tool call failed: {response['error']}")

        return response.get("result", {})


class ClaudeClient:
    """Client for Claude Sonnet 4 API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def send_message(self, messages: List[Dict[str, Any]], tools: Optional[List[Dict[str, Any]]] = None) -> Dict[
        str, Any]:
        """Send message to Claude API"""
        if not self.session:
            raise RuntimeError("Session not initialized")

        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01"
        }

        payload = {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 4000,
            "messages": messages
        }

        if tools:
            payload["tools"] = tools

        logger.info("Sending request to Claude...")

        try:
            async with self.session.post(ANTHROPIC_API_URL, json=payload, headers=headers, ssl=False) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise RuntimeError(f"Claude API error {response.status}: {error_text}")

                result = await response.json()
                logger.info("Claude response received")
                return result

        except Exception as e:
            logger.error(f"Claude API error: {e}")
            raise


async def get_deepwiki_info(repository: str, question: str) -> str:
    """Get information from Deep Wiki MCP server"""
    logger.info(f"Querying Deep Wiki for: {repository}")

    async with MCPClient() as mcp_client:
        # Initialize MCP connection
        await mcp_client.initialize()

        # List available tools
        tools = await mcp_client.list_tools()
        logger.info(f"Available MCP tools: {[tool.get('name') for tool in tools.get('tools', [])]}")

        # Ask the question
        result = await mcp_client.ask_question(repository, question)

        # Extract text content from result
        content_text = ""
        if "content" in result:
            for content_item in result["content"]:
                if content_item.get("type") == "text":
                    content_text += content_item.get("text", "")

        return content_text or str(result)


async def main():
    """Main application flow"""
    if ANTHROPIC_API_KEY == "your-anthropic-api-key-here":
        print("ERROR: Please set your Anthropic API key in the ANTHROPIC_API_KEY variable")
        return

    print("Claude Sonnet 4 + Deep Wiki MCP Integration")
    print("=" * 60)

    # Define the tool that Claude can use
    deepwiki_tool = {
        "name": "get_openai_codex_info",
        "description": "Get detailed information about OpenAI Codex from Deep Wiki",
        "input_schema": {
            "type": "object",
            "properties": {
                "repoName": {
                    "type": "string",
                    "description": "The repository to query (e.g., 'openai/codex')"
                },
                "question": {
                    "type": "string",
                    "description": "The question to ask about the repository"
                }
            },
            "required": ["repoName", "question"]
        }
    }

    async with ClaudeClient(ANTHROPIC_API_KEY) as claude:
        # Step 1: Initial request to Claude with tool definition
        print("\n1. Sending initial request to Claude with tool definition...")

        initial_messages = [{
            "role": "user",
            "content": "Based on its specification, provide a summary of the main points about OpenAI Codex"
        }]

        response1 = await claude.send_message(initial_messages, tools=[deepwiki_tool])

        print("Claude's initial response:")
        print(json.dumps(response1, indent=2))

        # Check if Claude wants to use the tool
        if response1.get("stop_reason") == "tool_use":
            tool_use = None
            for content in response1.get("content", []):
                if content.get("type") == "tool_use":
                    tool_use = content
                    break

            if tool_use:
                print("\n2. Claude requested tool execution:")
                print(f"Tool: {tool_use['name']}")
                print(f"Arguments: {tool_use['input']}")

                # Step 2: Execute the MCP query
                print("\n3. Executing MCP query to Deep Wiki...")

                repository = tool_use['input'].get('repoName', 'openai/codex')
                question = tool_use['input'].get('question', 'What is OpenAI Codex?')

                try:
                    deepwiki_result = await get_deepwiki_info(repository, question)
                    print(f"Deep Wiki result obtained ({len(deepwiki_result)} characters)")

                    # Step 3: Send results back to Claude
                    print("\n4. Sending Deep Wiki results back to Claude...")

                    followup_messages = initial_messages + [{
                        "role": "assistant",
                        "content": response1["content"]
                    }, {
                        "role": "user",
                        "content": [{
                            "type": "tool_result",
                            "tool_use_id": tool_use["id"],
                            "content": deepwiki_result
                        }]
                    }]

                    final_response = await claude.send_message(followup_messages)

                    # Step 4: Display final results
                    print("\n5. Final Results:")
                    print("=" * 60)

                    print("\nClaude's Final Text Response:")
                    print("-" * 40)
                    for content in final_response.get("content", []):
                        if content.get("type") == "text":
                            print(content.get("text", ""))

                    print("\nRaw Response Object:")
                    print("-" * 40)
                    print(final_response)

                    print("\nRaw Response as JSON:")
                    print("-" * 40)
                    print(json.dumps(final_response, indent=2))

                except Exception as e:
                    print(f"Error executing MCP query: {e}")
            else:
                print("No tool use found in Claude's response")
        else:
            print("Claude did not request tool execution")
            print("Response content:")
            for content in response1.get("content", []):
                if content.get("type") == "text":
                    print(content.get("text", ""))


if __name__ == "__main__":
    print("Required dependencies:")
    print("pip install aiohttp")
    print("\nMake sure to set your Anthropic API key!")
    print("=" * 60)

    asyncio.run(main())
