"""Search functionality for llmcp."""
import os
import sys
import fnmatch
from typing import Dict

import litellm

def get_models() -> Dict[str, str]:
    """Get available models from LiteLLM."""
    # Use context manager for stdout redirection
    with open(os.devnull, 'w') as devnull:
        original_stdout = sys.stdout
        sys.stdout = devnull
        
        try:
            models = {}
            # Add models from LiteLLM cost map
            for model_name, _ in litellm.model_cost.items():
                try:
                    _, provider, _, _ = litellm.get_llm_provider(model=model_name)
                    models[model_name] = provider.title() 
                except Exception:
                    pass
            
            return models
        finally:
            sys.stdout = original_stdout

def check_api_key(provider: str) -> bool:
    """Check if API key for the provider is set."""
    key_map = {
        "openai": "OPENAI_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "gemini": "GEMINI_API_KEY",
        "vertex_ai": "GEMINI_API_KEY",
        "mistral": "MISTRAL_API_KEY",
        "cohere": "COHERE_API_KEY",
        "groq": "GROQ_API_KEY",
    }
    env_var = key_map.get(provider.lower())
    return env_var and os.environ.get(env_var, "").strip() != ""

def search_models(pattern: str) -> None:
    """Search models matching pattern and check API keys."""
    models = get_models()
    matching = {name: provider for name, provider in models.items() 
               if fnmatch.fnmatch(name.lower(), pattern.lower())}
    
    if not matching:
        print(f"No models found matching: {pattern}")
        return
    
    # Group by provider
    by_provider = {}
    for name, provider in matching.items():
        if provider not in by_provider:
            by_provider[provider] = []
        by_provider[provider].append(name)
    
    # Print results
    print(f"Models matching: {pattern}")
    print("-" * 50)
    
    provider_keys = {}
    for provider in by_provider:
        provider_keys[provider] = check_api_key(provider.lower())
    
    for provider, models_list in sorted(by_provider.items()):
        has_key = provider_keys[provider]
        key_status = "✓" if has_key else "✗"
        print(f"{provider} [{key_status}]")
        for model in sorted(models_list):
            print(f"  {model}")
        print()
    
    print("API Key: ✓ = available, ✗ = missing")