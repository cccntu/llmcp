# llmcp

A minimal CLI for interacting with LLMs via LiteLLM and MCP.

## Quickstart

```bash
# Install and test locally (recommended)
uv pip install llmcp

# Search for available models
llmcp search 'gemini-2*'

# Serve mcp server
# llmcp serve gemini-2.5-pro-exp-03-25

# Test start a mcp server and call it
llmcp test gpt-4o-mini "What is the capital of France?"
# Example output:
# Response:
# The capital of France is Paris.

# Add a gemini:ask tool to Claude Code
claude mcp add gemini uvx llmcp serve gemini-2.5-pro-exp-03-25
```

##

## MCP details:

- MCP server implements a minimalist `ask` tool. The `ask` tool schema is as follows:
  ```json
  {
    "name": "ask",
    "description": "Send a prompt to the {model_name} model and get a response.",
    "input_schema": {
      "type": "object",
      "properties": {
        "prompt": {
          "type": "string",
          "description": "The prompt to send to the {model_name} model."
        }
      },
      "required": ["prompt"]
    }
  }
  ```
- Maximum token usage by default (automatically uses the maximum available tokens for the model)



## Configuration

Set up your API keys as environment variables:

| Provider   | Environment Variable       |
|------------|---------------------------|
| OpenAI     | `OPENAI_API_KEY`          |
| Anthropic  | `ANTHROPIC_API_KEY`       |
| Gemini     | `GEMINI_API_KEY`          |
| Mistral    | `MISTRAL_API_KEY`         |
| Cohere     | `COHERE_API_KEY`          |
| Groq       | `GROQ_API_KEY`            |

Example:
```bash
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-..."
export GEMINI_API_KEY="..."
export MISTRAL_API_KEY="..."
export COHERE_API_KEY="..."
export GROQ_API_KEY="..."
```

## Acknowledgements

This tool relies on the following libraries:

- [LiteLLM](https://github.com/BerriAI/litellm) for interacting with various LLM APIs.
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk) for implementing the Model Context Protocol.

## License

MIT
