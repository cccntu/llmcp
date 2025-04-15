"""CLI for llmcp."""
import typer
from typing import Optional
from rich.console import Console

from llmcp.search import search_models
from llmcp.client import test_model
from llmcp.server import start_server

app = typer.Typer(help="Interact with LLMs via LiteLLM and MCP")
console = Console()

@app.command()
def search(pattern: str = typer.Argument("*", help="Pattern to match model names")):
    """Search for models matching the pattern and check API key status."""
    search_models(pattern)

@app.command()
def serve(model_name: str = typer.Argument(..., help="Model to use for the MCP server")):
    """Start an MCP server using the specified model."""
    start_server(model_name)

@app.command()
def test(model_name: str = typer.Argument(..., help="Model to test"),
         prompt: str = typer.Argument(..., help="Prompt to send to the model")):
    """Test a model by starting a server and sending a prompt."""
    test_model(model_name, prompt)

if __name__ == "__main__":
    app()