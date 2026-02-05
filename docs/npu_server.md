# NPU Server Setup Guide

## Quick Start with vLLM

```bash
pip install vllm
python -m vllm.entrypoints.openai.api_server \
    --model meta-llama/Meta-Llama-3.1-8B-Instruct \
    --port 8000
```

## Docker

```bash
docker run -d --gpus all -p 8000:8000 \
    vllm/vllm-openai:latest \
    --model meta-llama/Meta-Llama-3.1-8B-Instruct
```

## Configuration

In FurnitureAI:
1. Custom Server settings
2. Endpoint: `http://your-server:8000/v1/chat/completions`
3. Test connection
