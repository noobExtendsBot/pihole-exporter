import os
import unittest
from unittest.mock import MagicMock, patch

from prometheus_client.metrics_core import Metric

from pihole_exporter.main import MetricsStrategyRegistry, PiholeCollector, main


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
        result = list(registry.collect_all())
        self.assertEqual([], result)


class TestPiholeCollector(unittest.TestCase):

    def test_collect(self) -> None:
        registry = MagicMock()
        collector = PiholeCollector(registry)

        metric_a = MagicMock(spec=Metric)
        registry.collect_all.return_value = iter([metric_a])

        result = list(collector.collect())
        self.assertEqual([metric_a], result)


class TestMain(unittest.TestCase):

    @patch("pihole_exporter.main.time.sleep", side_effect=KeyboardInterrupt)
    @patch("pihole_exporter.main.start_http_server")
    @patch("pihole_exporter.main.REGISTRY")
    @patch("pihole_exporter.main.PiholeClient")
    @patch("pihole_exporter.main.setup_logging")
    def test_main_registers_collectors_and_starts_server(
        self, m_logging, m_client, m_prom_registry, m_start_server, m_sleep
    ) -> None:

        with self.assertRaises(KeyboardInterrupt):
            main()

        m_logging.assert_called_once()
        m_client.assert_called_once()
        m_start_server.assert_called_once_with(9617)
        m_prom_registry.register.assert_called_once()

    @patch("pihole_exporter.main.time.sleep", side_effect=KeyboardInterrupt)
    @patch("pihole_exporter.main.start_http_server")
    @patch("pihole_exporter.main.REGISTRY")
    @patch("pihole_exporter.main.PiholeClient")
    @patch("pihole_exporter.main.setup_logging")
    def test_main_uses_default_env_vars(self, m_logging, m_client, m_prom_registry, m_start_server, m_sleep) -> None:
        keys = ["PIHOLE_PROTOCOL", "PIHOLE_HOSTNAME", "PIHOLE_PORT", "PIHOLE_PASSWORD"]
        env_without_keys = {k: v for k, v in os.environ.items() if k not in keys}
        with patch.dict(os.environ, env_without_keys, clear=True):
            with self.assertRaises(KeyboardInterrupt):
                main()

        config = m_client.call_args[0][0]
        self.assertEqual(config.base_url, "http://localhost:8080/api")
        self.assertEqual(config.password, "randompassword")


if __name__ == "__main__":
    unittest.main()
