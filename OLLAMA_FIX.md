# Ollama ShowResponse model_info Fix

## Problem

The application was failing with a Pydantic validation error:

```
1 validation error for ShowResponse
model_info
  Field required [type=missing, input_value={'modelfile': '# Modelfil...'}
```

## Root Cause

1. When initializing the `Ollama` LLM without specifying `context_window`, LlamaIndex automatically calls the `/api/show` endpoint to retrieve model metadata
2. The `/api/show` endpoint response is validated against the `ShowResponse` Pydantic model
3. The `ShowResponse` model expects a `model_info` field (marked as required)
4. According to the official Ollama API spec, `model_info` is actually **optional**
5. Some Ollama server versions don't return this field, causing validation to fail

## Solution Implemented

**Add `context_window` parameter to bypass the metadata check entirely.**

When you manually specify `context_window`, LlamaIndex skips the `/api/show` call, avoiding the validation error.

### Changes Made

#### 1. **File: `backend/Dockerfile`**

Install packages in the correct order to avoid dependency issues:

```dockerfile
# 5. Install Python dependencies in correct order
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir huggingface_hub && \
    pip install --no-cache-dir -r requirements.txt
```

**Installation order:**
1. Upgrade pip
2. Install `huggingface_hub` first
3. Install other LlamaIndex packages

#### 2. **File: `backend/app/services/index_service.py`**

**Before:**
```python
from llama_index.llms.ollama import Ollama

Settings.llm = Ollama(
    model=settings.MODEL_NAME,
    base_url=settings.OLLAMA_BASE_URL,
    request_timeout=120.0
)
```

**After:**
```python
from llama_index.llms.ollama import Ollama

Settings.llm = Ollama(
    model=settings.MODEL_NAME,
    base_url=settings.OLLAMA_BASE_URL,
    context_window=4096,  # Bypass metadata check
    request_timeout=120.0
)
```

## Why This Works

1. **Bypasses `/api/show` endpoint**: When `context_window` is specified, LlamaIndex doesn't need to call `/api/show` to retrieve model metadata
2. **No validation issues**: The `ShowResponse` model validation is completely avoided
3. **Works with all Ollama versions**: Compatible with any Ollama server version, regardless of whether it returns `model_info` or not
4. **Simple and clean**: Just one parameter addition, no monkey-patching or complex workarounds

## Testing

After rebuilding the Docker container:
```bash
docker-compose build backend
docker-compose up -d
```

The error should be resolved and the application should successfully connect to the Ollama server.

## Package Installation Order

**Critical:** Packages must be installed in this specific order:

1. **Upgrade pip** - Ensures latest dependency resolution
2. **Install `huggingface_hub`** - Core dependency for embedding models
3. **Install other LlamaIndex packages** - Prevents dependency conflicts

This order prevents version conflicts and ensures smooth installation of all dependencies.

## References

- [Ollama API Documentation](https://docs.ollama.com/api-reference/show-model-details)
- [LlamaIndex Ollama Integration](https://docs.llamaindex.ai/en/stable/api_reference/llms/ollama/)
- Working test file: `testing_ollama_and_llamaindex/test.py`

## Alternative Solutions Considered

1. **Monkey-patching ShowResponse** - Not documented, risky, rejected
2. **Using OpenAILike client** - More complex, requires additional package
3. **Upgrading Ollama server** - Would require server maintenance
4. **Downgrading pydantic** - Caused dependency conflicts with langchain-community
5. **Adding context_window parameter** - ✅ **Selected** (simple, clean, no side effects)
