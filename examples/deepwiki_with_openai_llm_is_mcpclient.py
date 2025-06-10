from openai import OpenAI

client = OpenAI()

resp = client.responses.create(
    #model="gpt-4.1",
    model="gpt-4o-mini",
    tools=[
        {
            "type": "mcp",
            "server_label": "deepwiki",
            "server_url": "https://mcp.deepwiki.com/mcp",
            "require_approval": "never",
        },
    ],
    #input="What transport protocols are supported in the 2025-03-26 version of the MCP spec?",
    input="What is OpenAI Codex?"
)

print("SUMMARY\n---\n")
print(resp.output_text)
print("\n\n\nDETAILS\n---\n")
print(resp)
