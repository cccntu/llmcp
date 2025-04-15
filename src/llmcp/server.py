"""Minimal MCP server implementation for llmcp."""
import os
import logging
from pydantic import Field
from mcp.server.fastmcp import FastMCP
from mcp.types import CallToolResult, TextContent
import litellm

# Configure logging
logging.basicConfig(level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_server(model_name: str) -> FastMCP:
    """Create an MCP server for the specified model."""
    from llmcp import __version__
    
    mcp = FastMCP(
        "llmcp",
        version=__version__,
        description=f"Minimal MCP server for {model_name}",
    )

    @mcp.tool(
        name="ask",
        description=f"Send a prompt to the {model_name} model and get a response."
    )
    async def ask_tool(
        prompt: str = Field(description=f"The text prompt to send to the {model_name} model")
    ) -> CallToolResult:
        """MCP Tool implementation for asking the LLM."""
        try:
            # Get maximum available tokens for the model
            try:
                max_tokens = litellm.get_max_tokens(model=model_name) - 1
                logger.info(f"Using maximum available tokens: {max_tokens}")
            except Exception:
                max_tokens = 1000
                logger.warning(f"Using default max tokens: {max_tokens}")

            # Call the model
            completion = await litellm.acompletion(
                model=model_name,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
            )

            # Process successful response
            response_text = completion.choices[0].message.content
            if response_text is None:
                response_text = "LLM returned no text content."
            return CallToolResult(content=[TextContent(type="text", text=response_text)])

        except Exception as e:
            error_msg = f"Error: {str(e)}"
            logger.error(error_msg)
            return CallToolResult(isError=True, content=[TextContent(type="text", text=error_msg)])

    return mcp

def start_server(model_name: str) -> None:
    """Start an MCP server for the specified model."""
    mcp = create_server(model_name)
    print(f"Starting MCP server for model: {model_name}")
    mcp.run()

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        start_server(sys.argv[1])
    else:
        print("Usage: python server.py <model_name>")