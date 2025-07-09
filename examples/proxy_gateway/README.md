> 🧵 This [thread on X](https://x.com/solomonstre/status/1940470145505431674) by Solomon Hykes, founder of Docker, highlights an emerging conflict: developers driving adoption vs. enterprise gatekeeping and control.  
> 
> As the MCP protocol gains traction, enterprise vendors are increasingly incentivized to **block** rather than **enable** open developer usage—shifting focus from innovation to control.
>
> 

![image](https://github.com/user-attachments/assets/290299fe-221b-4ee5-8ab3-3ff02c6bbab5)

Applications like Claude only presently works over stdio, need to use a layer in between.

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

**Javelin Roadmap:** 
- https://github.com/getjavelin/javelin-rust - javelin-core++ Private repo Rust/Go Under development.

## Remote MCP server with Remote Tools

Listing servers we are testing with ...
1. [Remote GitHub MCP Server](https://github.blog/changelog/2025-06-12-remote-github-mcp-server-is-now-available-in-public-preview/)
      - [Architecture](https://github.com/github/github-mcp-server/blob/main/docs/host-integration.md)
2. [Sentry MCP Server](https://mcp.sentry.dev/)
3. [DeepWiki MCP Server](https://docs.devin.ai/work-with-devin/deepwiki-mcp)
4. [Hugging Face](https://huggingface.co/settings/mcp)
   
**Remote MCP server Catalog:**
- [List of MCP servers](https://github.com/modelcontextprotocol/servers)

## ⁠Remote MCP server with Local (Builtin) Tools 

In the current Javelin MCP architecture, **tools are expected to be registered and executed remotely** (via an HTTP or gRPC endpoint). However, some tools (such as deterministic utilities or safe built-in actions) may be registered as **builtin tools**, which execute locally within the Javelin runtime.

While it is technically possible to have a remote MCP server route requests to local tools (co-located on the same host), this is not a typical or recommended deployment model.

### 💡 Key Notes:
- Use **remote tools** for hosted, externally managed actions (e.g., OpenAI, Anthropic).
- Use **builtin tools** for internal utilities or tightly coupled logic.
- A future enhancement may allow hybrid routing, but this is not standard today.

## Alternatives:** ❤️ open-source
- [fastmcp](https://github.com/jlowin/fastmcp?tab=readme-ov-file#proxy-servers)
- [mcp-proxy](https://github.com/sparfenyuk/mcp-proxy)
