#!/usr/bin/env bash
set -e

export STREAMLIT_SERVER_HEADLESS=true
export STREAMLIT_SERVER_ENABLE_CORS=false
export STREAMLIT_SERVER_ENABLE_STATIC_SERVING=true

python -m streamlit run app.py --server.address 0.0.0.0 --server.port ${PORT:-8080}
