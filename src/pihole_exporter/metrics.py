from abc import ABC, abstractmethod
from typing import Iterator
import time
import logging

from prometheus_client.metrics_core import GaugeMetricFamily, Metric


from .client import PiholeClient
from .config import PiholeConfig
from .models import (
    SummaryResponse,
    BlockingResponse,
    TopDomainsResponse,
    UpstreamsResponse,
)


logger = logging.getLogger(__name__)

class MetricsStrategy(ABC):

    def __init__(self, client: PiholeClient):
        self._client = client
        # self._instance_label = instance_label

    @abstractmethod
    def collect(self):
        raise NotImplementedError


class SummaryMetrics(MetricsStrategy):
    def __init__(self, client: PiholeClient):
        self._api_path = "/stats/summary"
        super().__init__(client)

    def _collect(self):
        try:
            data = self._client.get(self._api_path)
            data = SummaryResponse.model_validate(data)
        except Exception as ex:
            logger.error(f"When collecting data following exception occured: {ex}")
            return 

        yield GaugeMetricFamily(
            "pihole_dns_queries_today",
            "Total DNS queries (24h)",
            value=data.queries.total
        )
        
        yield GaugeMetricFamily(
            "pihole_ads_blocked_today",
            "Total ADs blocked (24h)",
            value=data.queries.blocked
        )

        yield GaugeMetricFamily(
            "pihole_ads_percentage_today",
            "Total Ads percentage (24h)",
            value=data.queries.percent_blocked
        )

        yield GaugeMetricFamily(
            "pihole_unique_domains",
            "Total unique domains (24h)",
            value=data.queries.unique_domains
        )

        yield GaugeMetricFamily(
            "pihole_gravity_domains_being_blocked",
            "Current value of gravity list",
            value=data.gravity.domains_being_blocked
        )

        yield GaugeMetricFamily(
            "pihole_queries_cached",
            "Total number of queries fetched from cached (24h)",
            value=data.queries.cached,
        )

        yield GaugeMetricFamily(
            "pihole_queries_forwarded",
            "Total number of queries forwarded (24h)",
            value=data.queries.forwarded,
        )

        yield GaugeMetricFamily(
            "pihole_clients_ever_seen",
            "Total number of clients recorded",
            value=data.clients.total
        )

        qtype = GaugeMetricFamily(
            "pihole_query_type",
            "Number of DNS queries by record type (A, AAAA, MX, etc.) in the last 24h",
            labels=["query_type"]
        )

        for pqtype, value in data.queries.types.model_dump().items():
            qtype.add_metric([pqtype], value)

        yield qtype

        rtype = GaugeMetricFamily(
            "pihole_reply_type",
            "Number of DNS queries by reply type (IP, NXDOMAIN, SERVFAIL, etc.) in the last 24h",
            labels=["reply_type"]
        )
        for prtype, value in data.queries.replies.model_dump().items():
            rtype.add_metric([prtype], value)

        yield rtype

    def collect(self):
        try:
            yield from self._collect()
        except Exception as ex:
            logger.exception(f"Unhandled error in SummaryMetrics collect: {ex}")
            return

class BlockingMetrics(MetricsStrategy):
    
    def __init__(self, client: PiholeClient):
        self._api_path = "/dns/blocking"
        super().__init__(client)


    def _collect(self):
        try:
            data = self._client.get(self._api_path)
            data = BlockingResponse.model_validate(data)
        except Exception as ex:
            logger.error(f"When fetching BlockingMetrics data from pihole following error occured: {ex}")
            return
        
        yield GaugeMetricFamily(
            "pihole_status",
            "Pi-hole blocking status (1=enabled, 0=disabled)",
            value=1 if data.blocking == "enabled" else 0
        )


    def collect(self):
        try:
            yield from self._collect()
        except Exception as ex:
            logger.error(f"Unhandled error in BlockingMetrics collect: {ex}")
            return

class TopAdsDomainsMetrics(MetricsStrategy):

    def __init__(self, client: PiholeClient):
        self._api_path = "/stats/top_domains?blocked=true"
        super().__init__(client)
    
    def _collect(self):
        try:
            data = self._client.get(self._api_path)
            data = TopDomainsResponse.model_validate(data)
        except Exception as ex:
            logger.error(f"When fetching TopDomainsMetrics data from pihole following error occured: {ex}")
            return
        
        top_queries = GaugeMetricFamily(
            "pihole_top_ads",
            "Top blocked Ads domains",
            labels=["domain"]
        )

        for entry in data.domains:
            top_queries.add_metric([entry.domain], entry.count)
        
        yield top_queries

    def collect(self):
        try:
            yield from self._collect()
        except Exception as ex:
            logger.error(f"Unhandled error in TopDomainsMetrics collect: {ex}")
            return

class TopDomainsMetrics(MetricsStrategy):

    def __init__(self, client: PiholeClient):
        self._api_path = "/stats/top_domains"
        super().__init__(client)
    
    def _collect(self):
        try:
            data = self._client.get(self._api_path)
            data = TopDomainsResponse.model_validate(data)
        except Exception as ex:
            logger.error(f"When fetching TopDomainsMetrics data from pihole following error occured: {ex}")
            return
        
        top_queries = GaugeMetricFamily(
            "pihole_top_queries",
            "Top queries in last 24h",
            labels=["domain"]
        )

        for entry in data.domains:
            top_queries.add_metric([entry.domain], entry.count)
        
        yield top_queries

    def collect(self):
        try:
            yield from self._collect()
        except Exception as ex:
            logger.error(f"Unhandled error in TopDomainsMetrics collect: {ex}")
            return

class UpstreamMetrics(MetricsStrategy):

    def __init__(self, client: PiholeClient):
        self._api_path = "/stats/upstreams"
        super().__init__(client)
    
    def _collect(self):
        try:
            data = self._client.get(self._api_path)
            data = UpstreamsResponse.model_validate(data)
        except Exception as ex:
            logger.error(f"When fetching UpstreamMetrics data from pihole following error occured: {ex}")
            return

        upstream_queries = GaugeMetricFamily(
            "pihole_upstream_queries",
            "Number of queries sent to each upstream DNS server",
            labels=["upstream"]
        )

        for upstream in data.upstreams:
            label = upstream.name or upstream.ip or "unknown"
            upstream_queries.add_metric([label], upstream.count)
        
        yield upstream_queries

    def collect(self) -> None:
        try:
            yield from self._collect()
        except Exception as ex:
            logger.error(f"Unhandled error in UpstreamMetrics collect: {ex}")
            return