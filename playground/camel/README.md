# 🐪 CaMeL: Defeating Prompt Injections by Design

[Guardrails won’t protect you](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/#guardrails)
> Here’s the really bad news: we still don’t know how to 100% reliably prevent this from happening.
>
> Plenty of vendors will sell you “guardrail” products that claim to be able to detect and prevent these attacks. I am deeply suspicious of these: If you look closely they’ll almost always carry confident claims that they > capture “95% of attacks” or similar... but in web application security 95% is very much a failing grade.
> 
> I’ve written recently about a couple of papers that describe approaches application developers can take to help mitigate this class of attacks:
> 
> Design Patterns for Securing LLM Agents against Prompt Injections reviews a paper that describes six patterns that can help. That paper also includes this succinct summary if the core problem: “once an LLM agent has > ingested untrusted input, it must be constrained so that it is impossible for that input to trigger any consequential actions.”
> CaMeL offers a promising new direction for mitigating prompt injection attacks describes the Google DeepMind CaMeL paper in depth.
Sadly neither of these are any help to end users who are mixing and matching tools together. The only way to stay safe there is to avoid that lethal trifecta combination entirely.

Implementation of the CaMeL (short for **CA**pabilities for **M**achin**E** **L**earning) system from the paper (_125 Pages_) ["Defeating Prompt Injections by Design" by Debenedetti et al. (2025).](https://arxiv.org/pdf/2503.18813)

- CaMeL is short for CApabilities for MachinE Learning.
- Here the term **capability** refers to the standard security definition, and not the standard machine learning measurement of how capable models are.

**So, are prompt injections solved now?**
**No, prompt injection attacks are not fully solved.** While CaMeL significantly improves the security
of LLM agents against prompt injection attacks and allows for fine-grained policy enforcement, it
is not without limitations. Importantly, CaMeL suffers from users needing to codify and specify
security policies and maintain them. CaMeL also comes with a user burden. At the same time, it is
well known that balancing security with user experience, especially with de-classification and user
fatigue, is challenging. We also explicitly acknowledge the potential for side-channel vulnerabilities in
CaMeL; however, we do note that their successful exploitation is significantly hindered by bandwidth
limitations and the involved attack complexity.

**And is [AgentDojo](https://agentdojo.spylab.ai/) fully solved now? Not exactly.** While CaMeL offers robust security guarantees
and demonstrates resilience against existing prompt injection attacks within AgentDojo benchmark, it
would be inaccurate to claim a complete resolution. Rather, our approach diverges from prior efforts,
focusing on building model scaffolding rather than improving the model. Furthermore, existing
research predominantly aims to optimize utility while mitigating attack success rates. In contrast,
our focus is on establishing verifiable security guarantees while concurrently maximizing utility. We
firmly believe that by adopting CaMeL as a fundamental design paradigm, future research will unlock
substantial enhancements in utility.

## Architecture

```
User Query → P-LLM → Python Code → CaMeL Interpreter → Secure Execution
                                        ↓
                                  Q-LLM (for untrusted data)
```

## Installation

## Usage

## Security Guarantees

- **Control Flow Isolation**: Untrusted data cannot affect control flow
- **Data Exfiltration Prevention**: Capabilities prevent unauthorized data exfiltration  
- **Policy Enforcement**: Custom interpreter enforces security policies
- **LLM Isolation**: Dual LLM pattern isolates planning from data processing
- **Lethal Trifecta Protection**: Defends against attacks combining private data access, untrusted content, and external communication


-- 

**More Papers:**
- [Design Patterns for Securing LLM Agents against Prompt Injections](https://arxiv.org/pdf/2506.08837)
