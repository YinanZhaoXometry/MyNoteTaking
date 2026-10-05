#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
if [[ -x venv/bin/python ]]; then
  PY=venv/bin/python
else
  PY=python3
fi
exec "$PY" -c "import sys; sys.path.insert(0,'.'); from src.main import app; print('OK:', app.name)"
