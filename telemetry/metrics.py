"""metrics.py - OpenTelemetry metrics instrumentation for IOE EdTech Platform.

Exposes named instruments for all four pipeline planes:
  - Ingestion (Prefect flows)
  - Retrieval (query router -> reranker -> composer)
  - Agent (LangGraph student/teacher graphs)
  - Governance (safety and alignment checks)

Usage:
    from telemetry.metrics import (
        record_token_usage, record_retrieval_latency,
        record_student_accuracy, record_ingestion_document,
        record_governance_check, record_embedding_latency,
    )
"""

from __future__ import annotations

from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

# ---------------------------------------------------------------------------
# Provider bootstrap (call once at application startup)
# ---------------------------------------------------------------------------

def configure_metrics(otlp_endpoint: str = "http://localhost:4317") -> None:
    """Initialize MeterProvider with OTLP + Console exporters."""
    otlp_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=otlp_endpoint, insecure=True),
        export_interval_millis=15_000,
    )
    console_reader = PeriodicExportingMetricReader(
        ConsoleMetricExporter(),
        export_interval_millis=60_000,
    )
    provider = MeterProvider(metric_readers=[otlp_reader, console_reader])
    metrics.set_meter_provider(provider)


# ---------------------------------------------------------------------------
# Meter and instruments
# ---------------------------------------------------------------------------

_meter = metrics.get_meter("ioe_edtech", version="1.0.0")

# -- Agent plane --
_token_usage_counter = _meter.create_counter(
    name="ioe_edtech_token_usage_total",
    description="Total LLM tokens consumed by agents",
    unit="tokens",
)

# -- Retrieval plane --
_retrieval_latency_histogram = _meter.create_histogram(
    name="ioe_edtech_retrieval_latency_ms",
    description="End-to-end retrieval latency in milliseconds",
    unit="ms",
)

# -- Student accuracy (business KPI) --
_student_accuracy_gauge = _meter.create_observable_gauge(
    name="ioe_edtech_student_response_accuracy",
    description="Rolling accuracy of student agent responses (0.0-1.0)",
    unit="ratio",
)

# -- Ingestion plane --
_ingestion_docs_counter = _meter.create_counter(
    name="ioe_edtech_ingestion_docs_total",
    description="Documents processed by ingestion pipeline",
    unit="documents",
)

# -- Governance plane --
_governance_checks_counter = _meter.create_counter(
    name="ioe_edtech_governance_checks_total",
    description="Total governance/safety validation checks performed",
    unit="checks",
)

# -- Embedding latency --
_embedding_latency_histogram = _meter.create_histogram(
    name="ioe_edtech_embedding_latency_ms",
    description="Time to embed a document chunk",
    unit="ms",
)


# ---------------------------------------------------------------------------
# Public helper functions
# ---------------------------------------------------------------------------

def record_token_usage(tokens: int, agent_role: str = "student", model: str = "ollama") -> None:
    """Record token consumption for an agent response."""
    _token_usage_counter.add(tokens, {"agent_role": agent_role, "model": model})


def record_retrieval_latency(latency_ms: float, query_type: str = "semantic", grade: str = "") -> None:
    """Record retrieval latency after a retrieval pipeline call."""
    _retrieval_latency_histogram.record(latency_ms, {"query_type": query_type, "grade": grade})


def record_student_accuracy(accuracy: float, subject: str = "", grade: str = "") -> None:
    """Update student response accuracy gauge (call after evaluation)."""
    # Observable gauges use callbacks; this is a simple wrapper for direct recording
    # Use a UpDownCounter if live updates are needed
    _meter.create_observable_gauge(
        name="ioe_edtech_student_response_accuracy_sample",
        callbacks=[lambda options: [(accuracy, {"subject": subject, "grade": grade})]],
    )


def record_ingestion_document(count: int = 1, source: str = "github", status: str = "success") -> None:
    """Increment ingestion document counter."""
    _ingestion_docs_counter.add(count, {"source": source, "status": status})


def record_governance_check(result: str = "passed") -> None:
    """Increment governance check counter with result label."""
    _governance_checks_counter.add(1, {"result": result})


def record_embedding_latency(latency_ms: float, model: str = "all-minilm") -> None:
    """Record embedding time per chunk."""
    _embedding_latency_histogram.record(latency_ms, {"model": model})
