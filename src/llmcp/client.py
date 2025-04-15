"""Client functions for llmcp."""
import os
import sys
import time
import asyncio
import logging
from pathlib import Path
from pprint import pprint
import json

# Disable all logging output below critical
logging.basicConfig(level=logging.CRITICAL)

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

def print_tool_schema(tools):
    """Print available tools and their schemas in a clean format."""
    for tool in tools:
        print(f"\nTool: {tool.name}")
        print(f"Description: {tool.description}")
        if hasattr(tool, "inputSchema") and "properties" in tool.inputSchema:
            print("Parameters:")
            for param_name, param_info in tool.inputSchema["properties"].items():
                desc = param_info.get("description", "No description")
                print(f"  - {param_name}: {desc}")

def extract_llm_answer(response_text):
    """Extract the actual LLM answer from a JSON string if needed."""
    try:
        maybe_json = json.loads(response_text)
        if isinstance(maybe_json, dict) and "content" in maybe_json:
            content_list = maybe_json["content"]
            if (
                isinstance(content_list, list) and
                len(content_list) > 0 and
                isinstance(content_list[0], dict) and
                "text" in content_list[0]
            ):
                return content_list[0]["text"]
    except Exception:
        pass  # Not JSON, just use as is
    return response_text

async def test_model_async(model_name: str, prompt: str) -> None:
    """Test a model by starting an MCP server and sending a prompt."""
    # Prepare server parameters
    module_dir = Path(__file__).parent
    server_script = str(module_dir / "server.py")
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[server_script, model_name],
        env=os.environ.copy()
    )

    print(f"Testing model: {model_name}")
    print(f"Prompt: \"{prompt}\"")

    try:
        start_time = time.time()
        async with stdio_client(server_params) as (read, write):
            print("Server started")
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = await session.list_tools()
                print_tool_schema(tools.tools)

                # Ensure 'ask' tool is available
                if "ask" not in [t.name for t in tools.tools]:
                    print("\nError: 'ask' tool not available")
                    return

                print("\nSending prompt...")
                result = await session.call_tool("ask", arguments={"prompt": prompt})

                # Explain protocol structure to user
                print("\n[INFO] The result you see below is a CallToolResult object, which contains a list of TextContent objects.")
                print("[INFO] This is the expected and standards-compliant protocol behavior for MCP. The 'text' field inside TextContent holds the model's response.\n")
                print("[CallToolResult object]:")
                pprint(result)
                print("[End CallToolResult object]\n")

                # Extract the LLM's answer as a string
                response_text = None
                for content in getattr(result, 'content', []):
                    if getattr(content, 'type', None) == "text":
                        response_text = getattr(content, 'text', None)
                        break

                if not response_text:
                    print("Error: No response received")
                    return

                llm_answer = extract_llm_answer(response_text)
                duration = time.time() - start_time
                print("Response:")
                print(llm_answer)
                print(f"\nTime: {duration:.2f}s")
    except Exception as e:
        print(f"Error: {str(e)}")

def test_model(model_name: str, prompt: str) -> None:
    """Entry point for testing a model."""
    asyncio.run(test_model_async(model_name, prompt))