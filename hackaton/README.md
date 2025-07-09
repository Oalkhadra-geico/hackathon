# Context Injection LLM Client

This is an enhanced Python script that allows you to inject various types of context into prompts before sending them to an LLM API.

## Features

- **Multiple Context Types**: Support for system context, domain knowledge, file content, conversation history, and custom contexts
- **Flexible Context Management**: Add, clear, and selectively include different types of context
- **Configuration-based Context**: Load context from JSON configuration files
- **Context Filtering**: Include only specific context types in prompts
- **File Context**: Automatically load file contents as context
- **Conversation History**: Maintain and inject conversation history

## Usage

### Basic Usage (No Context)
```python
response = call_llm("Say hi")
```

### With Context Injection
```python
# Create context injector
context_injector = ContextInjector()

# Add various types of context
context_injector.add_system_context("You are a helpful coding assistant")
context_injector.add_domain_knowledge("python", "Python best practices...")
context_injector.add_file_context("path/to/file.py")

# Make LLM call with context
response = call_llm("Explain this code", context_injector)
```

### Configuration-based Context
```python
context_injector = ContextInjector()
context_injector.load_context_from_config("context_config.json")
response = call_llm("Your prompt", context_injector)
```

### Selective Context Inclusion
```python
# Only include specific context types
response = call_llm(
    "Your prompt", 
    context_injector, 
    include_context_types=["system", "domain_knowledge"]
)
```

## Context Types

1. **System Context**: Instructions for the LLM's behavior
2. **Domain Knowledge**: Specific knowledge about domains/topics
3. **File Context**: Content from files
4. **Conversation History**: Previous conversation messages
5. **Custom Context**: Any other type of context you define

## Configuration File Format

```json
{
  "system_contexts": [
    {
      "content": "You are an expert software engineer...",
      "metadata": {"priority": "high"}
    }
  ],
  "domain_knowledge": [
    {
      "domain": "python",
      "content": "Python best practices...",
      "metadata": {"source": "Python Style Guide"}
    }
  ]
}
```

## Running the Examples

```bash
python test.py
```

This will run several demonstration scenarios showing different ways to use context injection.

## Requirements

Install dependencies with:
```bash
pip install -r requirements.txt
```
