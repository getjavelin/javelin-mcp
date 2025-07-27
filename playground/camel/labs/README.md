
[Guardrails won’t protect you](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/#guardrails)
> Here’s the really bad news: we still don’t know how to 100% reliably prevent this from happening.
>
> Plenty of vendors will sell you “guardrail” products that claim to be able to detect and prevent these attacks. I am deeply suspicious of these: If you look closely they’ll almost always carry confident claims that they > capture “95% of attacks” or similar... but in web application security 95% is very much a failing grade.
> 
> I’ve written recently about a couple of papers that describe approaches application developers can take to help mitigate this class of attacks:
> 
> [Design Patterns for Securing LLM Agents against Prompt Injections](https://simonwillison.net/2025/Jun/13/prompt-injection-design-patterns/) reviews a paper that describes six patterns that can help. That paper also includes this succinct summary if the core problem: “once an LLM agent has > ingested untrusted input, it must be constrained so that it is impossible for that input to trigger any consequential actions.”
> 
> [CaMeL offers a promising new direction for mitigating prompt injection attacks](https://simonwillison.net/2025/Apr/11/camel/) describes the Google DeepMind CaMeL paper in depth.
>
>
> Sadly neither of these are any help to end users who are mixing and matching tools together. The only way to stay safe there is to avoid that lethal trifecta combination entirely.
