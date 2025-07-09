# Solving the Agent Identity Problem in OAuth/OIDC Systems

## Executive Summary

Identity standards such as OpenID Connect (OIDC) and OAuth 2.0 provide robust mechanisms for
authentication and authorization in traditional user-centric scenarios. However, the emergence
of agentic systems has revealed critical gaps in these protocols when AI agents need to access
user data.

This document presents a comprehensive but high level solution to address the unique challenges of
agent identity management, building upon the security considerations outlined in the [Model
Context Protocol (MCP) Security Best Practices Specification](https://modelcontextprotocol.io/specification/2025-06-18/basic/security_best_practices).

## Problem Statement

### Functional Requirements

The introduction of AI agents into existing identity workflows creates two fundamental requirements:

1. **Agent to Client Relationship**: Agents must never operate autonomously. Every agent action
must be traceable to a human supervisor who explicitly instructed the agent to perform
specific tasks under defined circumstances. This establishes a clear chain of responsibility
for all agent-initiated activities through the declaration of relationships between agents
and clients.
2. **Agent to User Relationship**: When agents require access to user data, explicit consent
must be obtained from the data owner. This consent must encompass both the agent's access
requirements and the identity of the human controller directing the agent's actions.

### Security Requirements

The MCP specification identifies three critical attack vectors that must be addressed:

1. **Confused Deputy Problem**: Attackers may exploit agents, mcp clients, and mcp servers as
intermediaries to gain unauthorized access to user data without proper authentication flows.
2. **Token Passthrough Vulnerabilities**: Improper token validation can allow unauthorized
parties to bypass security controls by presenting tokens not intended for specific services.
3. **Session Hijacking**: Malicious actors may intercept or manipulate session identifiers to
impersonate legitimate users or inject unauthorized commands into agent workflows.

## Solution Overview

### Overview

The solution implements a proxy layer architecture that enhances existing identity providers
without requiring modifications to established OAuth/OIDC implementations. This approach
provides immediate compatibility with major identity providers (Microsoft, Google, etc.) while
addressing agent-specific security requirements.

![oauth2_security_pattern_complete_responsibility_segregation](https://github.com/user-attachments/assets/922da2a2-7015-4cd2-b891-941ee5327c5b)

### Core Components

### 1. Proxy Identity Provider

- Manages the relationship between users, agents, and MCP servers
- Provides enhanced consent flows that explicitly identify all entities involved in data access
- Maps proxy tokens to actual OAuth tokens while maintaining security boundaries

### 2. Gateway Service

- Enforces token validation and exchange mechanisms
- Prevents direct token passthrough by validating proxy tokens before accessing downstream services
- Implements comprehensive audit logging for all token exchanges

### 3. Session Management Layer

- Maintains secure linkage between application sessions, agent sessions, and MCP server sessions
- Implements non-deterministic session identifiers with proper binding to user-specific information
- Provides protection against session hijacking through cryptographic state validation

### Detailed Workflow

The solution implements a multi-stage authentication and authorization flow:

### Initial Setup (Steps 8.1-8.2)

- MCP Server identifies the need to access user data
- Gateway attempts data access and fails due to missing permissions, triggering the
authentication flow

### Discovery Phase (Steps 9-10)

- Gateway discovers the appropriate authorization server for the requested user data
- System prepares for dual-consent flow implementation

### Proxy Authentication Setup (Steps 14.1-14.2)

- MCP Server retrieves authentication delegation parameters
- Proxy Identity Provider configures parameters to route initial authentication through the
proxy layer

### User Consent Flow (Steps 17.1-24)

- Browser opens popup at Proxy Identity Provider's authorization endpoint
- **First Consent Screen**: User explicitly consents to data access by the complete entity
chain (Proxy, Agent, MCP Client, MCP Server, LLM)
- User is redirected to actual Authorization Server
- **Second Consent Screen**: User consents to proxy layer accessing their data (Authorization
Server remains unaware of underlying agent infrastructure)

### Code to Token Exchange (Steps 26-32)

- Proxy Identity Provider receives authorization code from actual Authorization Server
- System exchanges code for access token and creates corresponding proxy token mapping
- MCP Server obtains proxy access token (unaware of underlying token architecture)

### Secure Data Access (Steps 39-45)

- MCP Server selects appropriate proxy token based on maintained session context
- Gateway validates proxy token and exchanges for actual access token
- Data retrieval proceeds through validated token chain

### Agent Processing (Step 51)

- Agent receives context data and invokes LLM for output generation
- Complete audit trail maintained throughout the process

## Implementation Details

### Entity Relationship Management

### Agent-Client Relationships

- **Scope**: Lifecycle management for Agent-MCP Server relationships
- **Implementation**: Portal and API infrastructure for relationship registration and management
- **Responsibilities**: Integration with Proxy Authorization Servers and Identity Providers

### Agent-User Relationships

- **Scope**: Lifecycle management for User-{Agent, MCP Server} tuple relationships
- **Implementation**: User consent management portals and APIs
- **Responsibilities**: Ensuring explicit user consent for agent data access

### Agent-Client-User Relationships

- **Scope**: Consent lifecycle management for {User, Agent, MCP Server} tuples
- **Implementation**: Comprehensive consent applications and supporting APIs
- **Responsibilities**: Maintaining consent state across all entity relationships

### Security Architecture

### Tuple-Based Access Control

The Proxy system implements a tuple-based access model using `{User, Agent, MCP Server}` as the
fundamental access control unit:

- **Unique User Association**: Each tuple must include a user identifier to prevent cross-user
access violations
- **Consent Mapping**: One proxy access token maps to exactly one actual access token per tuple
- **Scalability**: Single actual access tokens may support multiple proxy tokens for different
tuple combinations

### Token Security

- **Proxy Token Isolation**: Proxy tokens never expose actual access tokens to agents or MCP servers
- **Validation Enforcement**: Gateway validates every proxy token before downstream access
- **Audit Compliance**: Complete token usage audit trails maintained for security and compliance

### Attack Mitigation Strategies

### Confused Deputy Protection

- **Universal Consent Verification**: Every data access request triggers consent validation for
the specific `{User, Agent, MCP Server}` tuple
- **Authentication Coupling**: Proxy consent acceptance is invalid without corresponding
successful authentication
- **Entity Registration**: All agents and MCP servers must be registered with established
relationships in the proxy layer

### Token Passthrough Prevention

- **Gateway Enforcement**: All data server interactions must include validated proxy and
actual tokens
- **Token Validation**: Invalid or missing proxy or actual tokens trigger user authentication flows
- **Access Control**: Direct access to actual access tokens is prevented through architectural
isolation

### Session Hijacking Mitigation

The solution addresses session security through comprehensive session linkage. The following is
an example of a potential solution:

1. **Application-Agent Session**: Application provides agent with ID token containing user
identifier and session ID
2. **Agent-MCP Client Session**: Agent passes session identifier to MCP client with proper
validation
3. **MCP Client-Server Session**: One-to-one mapping maintained between application session ID
and MCP session ID
4. **MCP Server-Proxy Session**: OAuth2 state field implemented as token containing MCP session ID
5. **Proxy-Identity Provider Session**: New OAuth2 state field preserves MCP server state while
maintaining proxy validation

### Session Security Requirements

- **Session Identifier Privacy**: Session IDs must remain private between involved parties or
require authenticated communication channels
- **Server Authentication**: Servers must authenticate all incoming communications and maintain
client-session mappings
- **State Token Security**: OAuth2 state values must be single-use with proper code_verifier
validation

## Deployment Considerations

### Integration Requirements

- **Identity Provider Compatibility**: Solution works with existing OAuth/OIDC providers without
requiring vendor modifications
- **Scalability**: Architecture supports multiple concurrent agent-user relationships
- **Audit Compliance**: Comprehensive logging and audit trail capabilities built into all components

### Security Best Practices

- **Least Privilege**: Agents receive minimal necessary permissions for specified tasks
- **Regular Token Rotation**: Implement automated token refresh and rotation policies
- **Monitoring and Alerting**: Real-time detection of anomalous access patterns or potential
security violations

## Conclusion

This solution provides a comprehensive approach to agent identity management that preserves the
security guarantees of existing OAuth/OIDC systems while extending them to support agentic
workflows. By implementing a proxy layer architecture with dual consent flows and comprehensive
session management, organizations can safely deploy AI agents with clear accountability chains
and robust security controls.

The architecture's compatibility with existing identity providers ensures immediate
implementability while providing a foundation for future enhancements as the agent ecosystem
continues to evolve.
