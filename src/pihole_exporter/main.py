import os
import time
from typing import Iterator

from prometheus_client import REGISTRY, start_http_server
from prometheus_client.metrics_core import Metric

from .client import PiholeClient
from .config import PiholeConfig
from .logger import setup_logging
from .metrics import (
    BlockingMetrics,
    MetricsStrategy,
    SummaryMetrics,
    TopAdsDomainsMetrics,
    TopDomainsMetrics,
    UpstreamMetrics,
)


class MetricsStrategyRegistry:

    def __init__(self) -> None:
        self._strategies: list[MetricsStrategy] = []

    def register(self, strategy: MetricsStrategy) -> None:
        self._strategies.append(strategy)

    def collect_all(self) -> Iterator[Metric]:
        for strategy in self._strategies:
            try:
                yield from strategy.collect()
            except Exception as ex:
                pass


class PiholeCollector:
    def __init__(self, registry: MetricsStrategyRegistry) -> None:
        self._registry = registry

    def collect(self) -> Iterator[Metric]:
        yield from self._registry.collect_all()

if __name__ == "__main__":
    # get you ENV ready
    protocol = os.environ.get("PIHOLE_PROTOCOL", "http")
    hostname = os.environ.get("PIHOLE_HOSTNAME", "localhost")
    port = os.environ.get("PIHOLE_PORT", "8080")
    password = os.environ.get("PIHOLE_PASSWORD", "randompassword")

    # setup logging
    setup_logging()

    config = PiholeConfig(
        base_url=f"{protocol}://{hostname}:{port}/api", password=password, verify_ssl=True, session_buffer_seconds=60
    )

    client = PiholeClient(config)

    registry = MetricsStrategyRegistry()
    registry.register(SummaryMetrics(client=client))
    registry.register(BlockingMetrics(client=client))
    registry.register(TopAdsDomainsMetrics(client=client))
    registry.register(TopDomainsMetrics(client=client))
    registry.register(UpstreamMetrics(client=client))
    REGISTRY.register(PiholeCollector(registry))
    start_http_server(9617)
    while True:
        time.sleep(1)
