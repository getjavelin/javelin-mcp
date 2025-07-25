# Javelin MCP: Model Context Protocol & Agentic Systems Playground

Welcome to the Javelin MCP project! This repository is a comprehensive playground and resource hub for exploring, prototyping, and documenting best practices around the **Model Context Protocol (MCP)**, agentic AI systems, and secure, auditable agent-to-server communication.

## What is MCP?
**Model Context Protocol (MCP)** is an emerging standard for enabling secure, flexible, and auditable communication between AI agents, clients, and servers. MCP is designed to address the unique challenges of agent identity, authentication, authorization, and trust in modern cloud and enterprise environments.

[blog post that answers the most common questions i've been getting from developers, partners and enterprises](https://vercel.com/blog/model-context-protocol-mcp-explained)

## Project Purpose
This project brings together:
- **Research & Documentation** on agent identity, trust, and security in OAuth/OIDC systems
- **Integration Patterns** for LLMs, agents, and MCP clients/servers
- **Curated Resources** for MCP tools, SDKs, and agentic development
- **Experimental Code & Labs** for new architectures and security models

## Repository Structure

### Core Components
- [**playground/agents/**](playground/agents/): Integration patterns and resources for building AI agents with MCP
  - Example agent implementations
  - Best practices for OpenAI and Anthropic integration
  - Documentation on agent design patterns in [`README.md`](playground/agents/README.md)

- [**playground/proxy_gateway/**](playground/proxy_gateway/): Gateway and proxy implementations for secure MCP communication
  - [`openai_agents/`](playground/proxy_gateway/openai_agents/): Transport implementations for OpenAI agents
  - [`proxy_go/`](playground/proxy_gateway/proxy_go/): Go-based MCP proxy implementation using the official Go SDK
  - Examples of SSE and Streamable HTTP transports in [`transports.py`](playground/proxy_gateway/openai_agents/transports.py)

### Security & Authentication
- [**playground/auth/**](playground/auth/): Comprehensive documentation on agent security architecture
  - [`agent_identity.md`](playground/auth/agent_identity.md): Detailed solution for agent identity in OAuth/OIDC systems
  - [`identity_trust.md`](playground/auth/identity_trust.md): In-depth analysis of trust frameworks for agentic systems

- [**playground/vulnerabilities/**](playground/vulnerabilities/): Security research and vulnerability analysis
  - Documentation of known MCP vulnerabilities in [`README.md`](playground/vulnerabilities/README.md)
  - Analysis of attack vectors (prompt injection, token theft, etc.)
  - Security best practices and mitigation strategies

### Integration Patterns
- [**playground/deepwiki/**](playground/deepwiki/): Reference implementations for MCP integration patterns
  - Examples of LLM as MCP Client in [`deepwiki_with_openai_llm_is_mcpclient.py`](playground/deepwiki/deepwiki_with_openai_llm_is_mcpclient.py)
  - Implementations with Anthropic's Claude in [`deepwiki_with_anthropic_llm_is_mcpclient.py`](playground/deepwiki/deepwiki_with_anthropic_llm_is_mcpclient.py)
  - One-step and two-step integration approaches in:
    - [`deepwiki_anthropic_app_is_mcpclient_one_step.py`](playground/deepwiki/deepwiki_anthropic_app_is_mcpclient_one_step.py)
    - [`deepwiki_anthropic_app_is_mcpclient_two_step.py`](playground/deepwiki/deepwiki_anthropic_app_is_mcpclient_two_step.py)

- [**playground/camel/**](playground/camel/): CaMeL (CApabilities for MachinE Learning) implementation
  - [`labs/`](playground/camel/labs/): Experimental research and threat analysis
  - Implementation of secure prompt injection prevention detailed in [`README.md`](playground/camel/README.md)
  - Security research documented in [`labs/Threat Research.md`](playground/camel/labs/Threat%20Research.md)

### Resources & Tools
- [**playground/awesome/**](playground/awesome/): Curated collection of MCP ecosystem tools
  - Official SDKs and client libraries
  - Development tools and frameworks
  - UI components and visualization tools
  - Comprehensive resource list in [`README.md`](playground/awesome/README.md)

## Start Here
- For a deep dive into agent identity and trust, see:
  - `playground/auth/agent_identity.md`
  - `playground/auth/identity_trust.md`
- For integration patterns, see:
  - `playground/deepwiki/README.md`
- For curated tools and resources, see:
  - `playground/awesome/README.md`

## License
See [LICENSE](LICENSE) for details.

---

*This project is a living knowledge base and experimental ground for the future of agentic AI and secure, context-aware communication. Dive in, explore, and help shape the next generation of agent protocols!*
