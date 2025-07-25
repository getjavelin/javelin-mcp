<img width="2092" height="1046" alt="image" src="https://github.com/user-attachments/assets/a64d40cb-3ce3-4e46-9373-008a7e5f4167" />

[The lethal **trifecta** for AI agents: Private data, Untrusted content, and External Communication](https://simonwillison.net/tags/prompt-injection/)
1. **Prompt Injection:** Manipulating LLM behavior through malicious inputs
2. **Tool Poisoning:** Hiding malicious instructions in tool descriptions
3. **Excessive Permissions:** Exploiting overly permissive tool access
4. **Rug Pull Attacks:** Exploiting tool definition mutations
5. **Tool Shadowing:** Overriding legitimate tools with malicious ones
6. **Indirect Prompt Injection:** Injecting instructions through data sources
7. **Token Theft:** Exploiting insecure token storage
8. **Malicious Code Execution:** Executing arbitrary code through vulnerable tools
9. **Remote Access Control:** Gaining unauthorized system access
10. **Multi-Vector Attacks:** Combining multiple vulnerabilities

[**GitHub MCP Exploited:** Accessing private repositories via MCP](https://invariantlabs.ai/blog/mcp-github-vulnerability)

**Classification:** Indirect Prompt Injection (primary), enabled by Excessive Permissions, and often realized as a Multi-Vector Attack that can result in cross-repository data exfiltration (remote access/data leak). Not a Tool Poisoning case (the GitHub MCP tools themselves remain trusted/unchanged).

1. **Indirect Prompt Injection:** Attacker embeds malicious instructions in a public GitHub Issue (untrusted external data). When the user’s agent (e.g., via Claude Desktop) asks to review issues, the model ingests that issue content and follows the injected instructions—pulling data from the user’s private repos and leaking it (e.g., via an auto-created PR). This is an injection delivered through data, not via the user prompt nor via altered tool metadata—your definition of Indirect Prompt Injection.
2. **Excessive Permissions:** The exploit succeeds because the agent’s GitHub credentials (PAT) often grant broad read/write access across both public and private repositories; the injected instructions then legitimately invoke MCP GitHub tools with those privileges. Principle-of-least-privilege violations (overbroad PAT scopes, cross-repo access) are highlighted as the key enabling weakness.
3. **Multi-Vector Attack (impact chain):** The injected content triggers a sequence of tool calls—read issues → read private repos → create/write to a public PR—creating a “toxic agent flow” that chains data ingestion, privilege use, and exfiltration across trust boundaries. This chaining characteristic fits your Multi-Vector category. 

[Remote Prompt Injection in **GitLab Duo** Leads to Source Code Theft](https://www.legitsecurity.com/blog/remote-prompt-injection-in-gitlab-duo)

**Classification:** Indirect Prompt Injection (remote) – primary. Secondary contributing factors: Excessive Permissions / over-broad context access, HTML-based data exfiltration path (Remote Access Control–like impact), Malicious Code Execution potential via tainted code suggestions, culminating in a Multi-Vector Attack chain.

1. **Indirect Prompt Injection (primary):** Hidden prompts planted in user-controlled GitLab artifacts (MR descriptions/comments, commit messages, issues, even source files) were ingested by Duo and executed, allowing attacker instructions to run when a victim simply interacted with the project.
2. **Excessive Permissions:** Duo operated with the victim user’s privileges, so injected instructions could direct it to read private merge requests/projects the victim could access—breaking intended trust boundaries and enabling cross-project data exposure.
3. **HTML Injection → Data Exfil / Remote Impact:** Because Duo responses were rendered as streaming Markdown that could produce active HTML (e.g., <img> tags), attacker-planted prompts could cause the browser to beacon out base64-encoded private source code or steer users to attacker sites.
4. **Malicious Code Execution (supply-chain vector):** Injected prompts could alter Duo’s code suggestions—e.g., recommending a malicious JavaScript package or otherwise tainting code that, if accepted and run, leads to downstream execution risk.
5. **Multi-Vector Attack Chain:** The full PoC strings together hidden prompts + encoding/obfuscation tricks + HTML rendering + privileged data access to exfiltrate sensitive code and potentially phish or deliver payloads—an orchestrated, multi-stage exploitation across layers.

[PoC Attack Targeting **Atlassian’s Model Context Protocol (MCP)** Introduces New “Living Off AI” Risk](https://www.catonetworks.com/blog/cato-ctrl-poc-attack-targeting-atlassians-mcp/)

**Classification:** It’s primarily an Indirect Prompt Injection attack that’s enabled by Excessive Permissions on the MCP action path, and (in the extended scenario) chains into a Multi-Vector Attack with potential Remote Access Control / data exfiltration consequences.

1. **Indirect Prompt Injection (primary):** The malicious payload lives in an external Jira Service Management support ticket submitted by an untrusted party; when an internal user invokes an MCP-powered AI action (e.g., summarize), the model ingests that ticket content and executes the attacker’s instructions with elevated context. The injection comes through the data source, not via a direct user prompt—your definition of Indirect Prompt Injection.
2. **Excessive Permissions (contributing weakness):** The MCP integration runs with the internal agent’s privileges and can read internal Jira/Confluence items and then post back into the attacker-visible ticket, breaking the intended boundary between external and internal tenants—classic over-broad tool permissions abuse.
3. **Multi-Vector / Remote Access escalation (impact path):** Cato’s extended scenario shows how the injected instructions can be combined with additional steps (auto-comments w/ malicious links leading to C2, lateral movement, data exfiltration), illustrating chained vectors beyond the initial injection—i.e., Multi-Vector Attack with Remote Access Control implications.

[Critical Vulnerability in **Anthropic's MCP** Exposes Developer Machines to Remote Exploits](https://thehackernews.com/2025/07/critical-vulnerability-in-anthropics.html)

**Classification:** Malicious Code Execution (primary) — unauthenticated requests (incl. CSRF from a malicious web page leveraging the 0.0.0.0-day browser quirk) can command the MCP Inspector proxy to execute arbitrary OS commands on the developer’s machine. That is squarely “executing arbitrary code through vulnerable tools.”

1. **Impact extension:** Remote Access Control takeover — successful exploitation grants the attacker full control of the host running MCP Inspector (read data, drop backdoors, lateral movement).
2. **Attack surface pattern:** Multi-Vector Attack chain — combines a browser-origin vector (CSRF / 0.0.0.0-day / DNS rebinding) + exposed MCP Inspector endpoint + its “run arbitrary command” capability to pivot from mere web browsing to local RCE and further compromise.
3. **Downstream risk:** Token Theft & data exfiltration are plausible post-RCE outcomes because attackers controlling the developer box can harvest API keys, credentials, and project data accessed by MCP tools. (Discussed as practical risks of host compromise in the writeups.) 
   
[**Supabase MCP** can leak your entire SQL database](https://www.generalanalysis.com/blog/supabase-mcp-blog)

**Classification:** Indirect Prompt Injection (primary) enabled by Excessive Permissions (service_role bypassing RLS + write access), leading to Token Theft / Sensitive Data Exfiltration and demonstrating a Multi-Vector (“lethal trifecta”) Attack chain. Not Tool Poisoning. Not Rug Pull.

1. **Indirect Prompt Injection:** Attacker plants instruction text in a support ticket message (untrusted data). When a developer’s Cursor agent reviews tickets, the LLM ingests that message and treats the embedded instructions as commands—reading and then writing data via Supabase MCP.
2. **Excessive Permissions:** The agent operates the database using the Supabase service_role, which bypasses all Row-Level Security and grants full SQL over every table; this privilege boundary is highlighted as the weak link in the attack setup.
3. **Token Theft / Data Exfil:** The malicious instructions direct the agent to dump the sensitive integration_tokens table and insert the results back into the ticket thread, exposing secrets to the attacker.
4. **Multi-Vector (“lethal trifecta”) Chain:** Simon Willison calls this another lethal trifecta case: a system that combines (1) access to private data, (2) exposure to malicious instructions, and (3) a channel to exfiltrate data back out (DB writes to attacker-visible ticket). The Supabase MCP’s broad tool abilities (manage/query DB, etc.) make the chain possible when misconfigured with high privileges.
  


