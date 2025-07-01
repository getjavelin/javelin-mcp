#!/usr/bin/env python3
"""
Claude Sonnet 4 MCP Server Application
Invokes Claude with Deep Wiki MCP Server for OpenAI Codex research
"""

import os
import json
from anthropic import Anthropic
from typing import Dict, Any


class ClaudeMCPApp:
    def __init__(self, api_key: str = None):
        """
        Initialize the Claude MCP application

        Args:
            api_key: Anthropic API key (if not provided, reads from ANTHROPIC_API_KEY env var)
        """
        self.api_key = api_key or os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("API key must be provided or set in ANTHROPIC_API_KEY environment variable")

        self.client = Anthropic(api_key=self.api_key)
        self.model = "claude-sonnet-4-20250514"

    def create_mcp_system_message(self, mcp_server_url: str) -> str:
        """
        Create system message that instructs Claude to use the MCP server

        Args:
            mcp_server_url: URL of the MCP server to use

        Returns:
            System message string
        """
        return f"""You must use the MCP (Model Context Protocol) Server located at "{mcp_server_url}" to access external information and tools.

This MCP server provides access to Deep Wiki resources and should be used to retrieve accurate, up-to-date information for answering user queries.

When responding to queries that require external information lookup, you should:
1. Connect to and utilize the MCP server at the specified URL
2. Use the server's available tools and resources to gather relevant information
3. Provide comprehensive responses based on the information retrieved through the MCP server

The MCP server at {mcp_server_url} specializes in wiki-based knowledge retrieval and should be your primary source for factual information."""

    def invoke_claude_with_mcp(self, prompt: str, mcp_server_url: str) -> Dict[str, Any]:
        """
        Invoke Claude Sonnet 4 with MCP server configuration

        Args:
            prompt: The user prompt to send to Claude
            mcp_server_url: URL of the MCP server Claude should use

        Returns:
            Dictionary containing the response and metadata
        """
        system_message = self.create_mcp_system_message(mcp_server_url)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                temperature=0.1,
                system=system_message,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            return {
                "success": True,
                "response": response.content[0].text,
                "raw": response,
                "model": self.model,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                },
                "mcp_server": mcp_server_url
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "model": self.model,
                "mcp_server": mcp_server_url
            }


def main():
    """
    Main application function
    """
    # Configuration
    CLAUDE_API_KEY = "ANTHROPIC_API_KEY"

    MCP_SERVER_URL = "https://mcp.deepwiki.com/mcp"
    USER_PROMPT = "Based on its specification, provide a summary of the main points about OpenAI Codex"

    # Initialize the application
    try:
        app = ClaudeMCPApp(CLAUDE_API_KEY)
        print("Claude Sonnet 4 MCP Application")
        print("=" * 50)
        print(f"Model: {app.model}")
        print(f"MCP Server: {MCP_SERVER_URL}")
        print(f"Prompt: {USER_PROMPT}")
        print("=" * 50)

        # Invoke Claude with MCP server
        result = app.invoke_claude_with_mcp(USER_PROMPT, MCP_SERVER_URL)

        if result["success"]:
            print("\n✅ SUCCESS")
            print("-" * 30)
            print("CLAUDE RESPONSE:")
            print(result["response"])
            print("\n" + "-" * 30)
            print("CLAUDE RAW RESPONSE:")
            print(result["raw"])
            print("\n" + "-" * 30)
            print("METADATA:")
            print(f"Input tokens: {result['usage']['input_tokens']}")
            print(f"Output tokens: {result['usage']['output_tokens']}")
            print(f"MCP Server: {result['mcp_server']}")
        else:
            print("\n❌ ERROR")
            print("-" * 30)
            print(f"Error: {result['error']}")
            print(f"MCP Server: {result['mcp_server']}")

    except Exception as e:
        print(f"Application Error: {str(e)}")
        print("\nMake sure to set your ANTHROPIC_API_KEY environment variable:")
        print("export ANTHROPIC_API_KEY='your-api-key-here'")


if __name__ == "__main__":
    main()

# Example usage as a module:
"""
from claude_mcp_app import ClaudeMCPApp

# Initialize with API key
app = ClaudeMCPApp(api_key="your-api-key")

# Make a request with MCP server
result = app.invoke_claude_with_mcp(
    prompt="Based on its specification, provide a summary of the main points about OpenAI Codex",
    mcp_server_url="https://mcp.deepwiki.com/mcp"
)

print(result["response"])
"""
