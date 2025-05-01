#!/bin/bash
export PLAYWRIGHT_BROWSERS_PATH=/mnt/data/ms-playwright
uvicorn main:app --host 0.0.0.0 --port 10000
