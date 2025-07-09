![image](https://github.com/user-attachments/assets/290299fe-221b-4ee5-8ab3-3ff02c6bbab5)

## ⁠Local MCP server ⬄ Local Tools

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


**sidenote:** Apps like Anthropic Claude currently **work only over stdio**, so a lightweight proxy layer is needed to expose them as MCP-compatible endpoints.

## Local MCP server ⬄ Remote Tools

**Javelin Roadmap:** 
- https://github.com/getjavelin/javelin-rust - javelin-core++ Private repo Rust/Go Under development.

## Remote MCP server ⬄ Remote Tools

**Remote MCP server Catalog:** [List of MCP servers](https://github.com/modelcontextprotocol/servers)
  
Listing servers we are testing with ...

1. [DeepWiki MCP Server](https://docs.devin.ai/work-with-devin/deepwiki-mcp)
2. [Remote GitHub MCP Server](https://github.blog/changelog/2025-06-12-remote-github-mcp-server-is-now-available-in-public-preview/)
      - [Architecture](https://github.com/github/github-mcp-server/blob/main/docs/host-integration.md)
3. [Hugging Face](https://huggingface.co/settings/mcp)
4. [Sentry MCP Server](https://mcp.sentry.dev/)


![Screenshot 2025-07-09 at 3 03 01 PM](https://github.com/user-attachments/assets/8a975110-e341-454b-8266-9a86925ca501)

![screenshot_2025-07-09_at_9 35 28___pm](https://github.com/user-attachments/assets/4de4f94b-67b8-42a9-b27f-36931bc49b14)

![Screenshot 2025-07-09 at 3 04 48 PM](https://github.com/user-attachments/assets/573fe7ba-0439-4cc9-b595-0b9ba457f9a1)

**Register First Tool Server** (AKA MCP Server)

1. **DeepWiki**

```bash
curl https://your-javelin-domain.com/v1/admin/tools/deepwiki \
  -H "Content-Type: application/json" \
  -H "x-javelin-apikey: $JAVELIN_API_KEY" \
  -d '{
    "name": "deepwiki",
    "type": "streamable-http",
    "version": "1.0.0",
    "description": "DeepWiki MCP integration",
    "endpoint": "https://mcp.deepwiki.com/mcp",
    "is_active": true,
    "config": {}
  }'
```

**GET Tool Server**

```bash
curl https://your-javelin-domain.com/v1/admin/tools/deepwiki \
  -H "Content-Type: application/json" \
  -H "x-javelin-apikey: $JAVELIN_API_KEY" | jq .
```

**GET Tools**

```bash
curl https://your-javelin-domain.com/v1/admin/tools \
  -H "Content-Type: application/json" \
  -H "x-javelin-apikey: $JAVELIN_API_KEY" | jq .
```

**GET Tool Definitions**

```bash
curl "https://your-javelin-domain.com/v1/admin/tool-definitions/deepwiki" \
  -H "Content-Type: application/json" \
  -H "x-javelin-apikey: $JAVELIN_API_KEY" | jq .
```

```bash
curl https://your-javelin-domain.com/v1/admin/tool-definitions \
  -H "Content-Type: application/json" \
  -H "x-javelin-apikey: $JAVELIN_API_KEY" | jq .
```

```bash
 curl "https://your-javelin-domain.com/v1/admin/tool-definitions?enabled=true" \
  -H "Content-Type: application/json" \
  -H "x-javelin-apikey: $JAVELIN_API_KEY" | jq .
```

**Register** **Second & Third Tool Servers** ...

2. **GitHub**

```bash
curl https://your-javelin-domain.com/v1/admin/tools/github \
  -H "Content-Type: application/json" \
  -H "x-javelin-apikey: $JAVELIN_API_KEY" \
  -d '{
    "name": "github",
    "type": "streamable-http",
    "version": "1.0.0",
    "description": "GitHub Copilot MCP integration",
    "endpoint": "https://api.githubcopilot.com/mcp/",
    "is_active": true,
    "config": {
      "authorization_token": "Bearer ghp_xxxxxxxxxxxx"
    },
    "policy": {
      "rate_limit": "100/min",
      "timeout": "30s"
    }
  }'
```

3. **HuggingFace**

```bash
curl https://your-javelin-domain.com/v1/admin/tools/huggingface \
  -H "Content-Type: application/json" \
  -H "x-javelin-apikey: $JAVELIN_API_KEY" \
  -d '{
    "name": "huggingface",
    "type": "streamable-http",
    "version": "1.0.0",
    "description": "Hugging Face MCP integration",
    "endpoint": "https://huggingface.co/mcp",
    "is_active": true,
    "config": {
      "authorization_token": "Bearer hf_xxxxxxxxxxxx"
    }
  }'
```

**UnRegister Tool Server**

```bash
curl -X DELETE https://your-javelin-domain.com/v1/admin/tools/huggingface \
  -H "Content-Type: application/json" \
  -H "x-javelin-apikey: $JAVELIN_API_KEY" | jq .
```

## ⁠Remote MCP server ⬄ Local (Builtin) Tools 

In the current Javelin MCP architecture, **tools are expected to be registered and executed remotely** (via an HTTP or gRPC endpoint). However, some tools (such as deterministic utilities or safe built-in actions) may be registered as **builtin tools**, which execute locally within the Javelin runtime.

While it is technically possible to have a remote MCP server route requests to local tools (co-located on the same host), this is not a typical or recommended deployment model.

### 💡 Key Notes:
- Use **remote tools** for hosted, externally managed actions (e.g., OpenAI, Anthropic).
- Use **builtin tools** for internal utilities or tightly coupled logic.
- A future enhancement may allow hybrid routing, but this is not standard today.

## Alternatives ❤️ open-source
- [fastmcp](https://github.com/jlowin/fastmcp?tab=readme-ov-file#proxy-servers)
- [mcp-proxy](https://github.com/sparfenyuk/mcp-proxy)
