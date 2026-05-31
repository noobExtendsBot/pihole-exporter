import unittest
from unittest.mock import MagicMock, patch

from prometheus_client.metrics_core import Metric
from pihole_exporter.main import MetricsStrategyRegistry, PiholeCollector

class TestMetricsStrategyRegistry(unittest.TestCase):

    def test_register_adds_strategy(self) -> None:
        registry = MetricsStrategyRegistry()
        strategy1 = MagicMock()
        registry.register(strategy1)

        self.assertIn(strategy1, registry._strategies)


    def test_collect_all(self) -> None:
        registry = MetricsStrategyRegistry()
        metric_a = MagicMock(spec=Metric)
        metric_b = MagicMock(spec=Metric)

        strategy1 = MagicMock()
        strategy2 = MagicMock()
        strategy1.collect.return_value = iter([metric_a])
        strategy2.collect.return_value = iter([metric_b])

        registry.register(strategy1)
        registry.register(strategy2)

        all_metrics = list(registry.collect_all())
        self.assertEqual([metric_a, metric_b], all_metrics)

    def test_collect_all_empty(self) -> None:
        registry = MetricsStrategyRegistry()
        res = list(registry.collect_all())
        self.assertEqual([], res)

if __name__ == "__main__":
    unittest.main()