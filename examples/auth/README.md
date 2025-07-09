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

![oauth2_security_pattern_complete_responsibility_segregation.svg](attachment:41ff060f-bc24-40e0-ba51-0621d493f88d:oauth2_security_pattern_complete_responsibility_segregation.svg)
