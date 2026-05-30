![CI](https://github.com/noobExtendsBot/pihole-exporter/workflows/CI/badge.svg)
[![Python](https://img.shields.io/badge/python-3.14-blue)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# pihole-exporter for Prometheus

![Dashboard](https://raw.githubusercontent.com/noobExtendsBot/pihole-exporter/master/dashboard.jpg)

This project is inspired by [eko/pihole-exporter](https://github.com/eko/pihole-exporter) to support new version of pihole.

## Usage

### Docker

```bash
docker run -e PIHOLE_HOSTNAME=192.168.1.2 -e PIHOLE_PASSWORD=yourpassword -p 9617:9617 ghcr.io/noobextendsbot/pihole-exporter
```

### Docker Compose

```yaml
services:
  pihole-exporter:
    image: ghcr.io/noobextendsbot/pihole-exporter
    ports:
      - "9617:9617"
    environment:
      PIHOLE_PROTOCOL: http
      PIHOLE_HOSTNAME: 192.168.1.2
      PIHOLE_PORT: 8080
      PIHOLE_PASSWORD: yourpassword
```

| Variable | Default | Description |
|---|---|---|
| `PIHOLE_PROTOCOL` | `http` | `http` or `https` |
| `PIHOLE_HOSTNAME` | `localhost` | Pi-hole address |
| `PIHOLE_PORT` | `8080` | Pi-hole port |
| `PIHOLE_PASSWORD` | — | Pi-hole web password |

Metrics are exposed on port `9617`.

## Available Metrics

| Metric | Description |
|---|---|
| `pihole_status` | Pi-hole blocking status (1 = enabled, 0 = disabled) |
| `pihole_dns_queries_today` | Total DNS queries in the last 24h |
| `pihole_ads_blocked_today` | Total ads/domains blocked in the last 24h |
| `pihole_ads_percentage_today` | Percentage of queries blocked in the last 24h |
| `pihole_unique_domains` | Number of unique domains queried in the last 24h |
| `pihole_queries_cached` | Number of queries answered from cache in the last 24h |
| `pihole_queries_forwarded` | Number of queries forwarded to upstream in the last 24h |
| `pihole_clients_ever_seen` | Total number of clients ever recorded |
| `pihole_gravity_domains_being_blocked` | Number of domains in the current gravity blocklist |
| `pihole_query_type` | DNS query count by record type in the last 24h |
| `pihole_reply_type` | DNS query count by reply type in the last 24h |
| `pihole_top_queries` | Top queried domains in the last 24h |
| `pihole_top_ads` | Top blocked ad domains in the last 24h |
| `pihole_upstream_queries` | Number of queries sent to each upstream DNS server |
