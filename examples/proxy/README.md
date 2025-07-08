## ⁠Local MCP server with the Local Tools

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

## Local MCP server with the Remote Tools

Claude only presently works over stdio, need to use a layer in between.

![image](https://github.com/user-attachments/assets/290299fe-221b-4ee5-8ab3-3ff02c6bbab5)

❤️ open-source
- [fastmcp](https://github.com/jlowin/fastmcp?tab=readme-ov-file#proxy-servers)
- [mcp-proxy](https://github.com/sparfenyuk/mcp-proxy)

Javelin Roadmap: https://github.com/getjavelin/javelin-rust - javelin-core++ Rust/Go Private repo Under development.

## Remote MCP server with Remote Tools

## ⁠Remote MCP server with Local (Builtin) Tools 

In the current Javelin MCP architecture, **tools are expected to be registered and executed remotely** (via an HTTP or gRPC endpoint). However, some tools (such as deterministic utilities or safe built-in actions) may be registered as **builtin tools**, which execute locally within the Javelin runtime.

While it is technically possible to have a remote MCP server route requests to local tools (co-located on the same host), this is not a typical or recommended deployment model.

### 💡 Key Notes:
- Use **remote tools** for hosted, externally managed actions (e.g., OpenAI, Anthropic).
- Use **builtin tools** for internal utilities or tightly coupled logic.
- A future enhancement may allow hybrid routing, but this is not standard today.

