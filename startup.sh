#!/usr/bin/env bash
uv sync --frozen --no-cache
/app/.venv/bin/fastapi run app/main.py --port 80 --host 0.0.0.0
