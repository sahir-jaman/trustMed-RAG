#!/bin/sh
# 1) Start the API in the background (it downloads the database on first start)
uvicorn app.api:app --app-dir src --host 127.0.0.1 --port 8000 &

# 2) Wait until the API is ready
echo "Waiting for the TrustMed API to start..."
until python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/')" 2>/dev/null; do
  sleep 3
done
echo "API is ready."

# 3) Start the website on the public port
streamlit run src/app/ui.py --server.port 7860 --server.address 0.0.0.0