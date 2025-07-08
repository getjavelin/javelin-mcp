## ⁠Local MCP server with the local Tools

Docker Desktop MCP Integration with their **MCP Catalog and Toolkit** provides:
1. **Centralized Discovery** - A trusted hub for discovering MCP tools integrated into Docker Hub
2. **Containerized Deployment** - Run MCP servers as containers without complex setup
3. **Secure Credential Management** - Centralized, encrypted credential handling
4. **Built-in Security** - Sandbox isolation and permissions management

The Docker MCP ecosystem includes over 100 verified tools from partners like Stripe, Elastic, Neo4j, and more, all accessible through Docker's infrastructure.

**Learn More:**
- [Docker MCP Documentation](https://docs.docker.com/ai/gordon/mcp/)
- [Docker MCP Servers Repository](https://github.com/docker/mcp-servers)
- [Introducing Docker MCP Catalog and Toolkit](https://www.docker.com/blog/introducing-docker-mcp-catalog-and-toolkit/)
- [MCP Introduction and Overview](https://www.philschmid.de/mcp-introduction)

<img width="1728" alt="Screenshot 2025-07-08 at 3 35 56 PM" src="https://github.com/user-attachments/assets/76039f18-6e03-4ae5-899d-83a6597c42bf" />

## Local MCP server with the remote tools

Claude only presently works over stdio, and we rightly ignore stdio in favor of SSE, you will need to use a layer in between.

❤️ open-source
- [fastmcp](https://github.com/jlowin/fastmcp?tab=readme-ov-file#proxy-servers)
- [mcp-proxy](https://github.com/sparfenyuk/mcp-proxy)

## Remote MCP server with remote tools

## ⁠Remote MCP server with local tools (no sure if this use case exists?)

