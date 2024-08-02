#!/bin/sh

# --metrics_exporter console

exec opentelemetry-instrument uvicorn metrics_study.webserver:app --host 0.0.0.0 --port 8008