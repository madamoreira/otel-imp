from contextlib import asynccontextmanager
import logging
import uvicorn

from fastapi import FastAPI
from metrics_study.routes import cookies_router
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor
from opentelemetry import metrics
# from opentelemetry.exporter.prometheus import PrometheusMetricReader
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
# from prometheus_client import start_http_server

log = logging.getLogger("uvicorn")

@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("---------- up ------------")

    yield

    log.info("---------- down ------------")

app = FastAPI(docs_url="/swagger", lifespan=lifespan)
app.include_router(cookies_router)

FastAPIInstrumentor.instrument_app(app)

configuration = {
    "system.memory.usage": ["used", "free", "cached"],
    "system.cpu.time": ["idle", "user", "system", "irq"],
    "process.runtime.memory": ["rss", "vms"],
    "process.runtime.cpu.time": ["user", "system"],
    "process.runtime.context_switches": ["involuntary", "voluntary"],
}

SystemMetricsInstrumentor(config=configuration).instrument()

# Service name is required for most backends
# resource = Resource(attributes={SERVICE_NAME: "cookies"})

# Start Prometheus client
# start_http_server(port=9464)
# Initialize PrometheusMetricReader which pulls metrics from the SDK
# on-demand to respond to scrape requests
# reader = PrometheusMetricReader()
# provider = MeterProvider(resource=resource, metric_readers=[reader])
# metrics.set_meter_provider(provider)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8008)
