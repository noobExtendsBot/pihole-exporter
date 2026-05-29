from typing import Dict, List, Optional

from pydantic import BaseModel, Field

# --- Auth ---


class SessionInfo(BaseModel):
    sid: str
    validity: int
    totp: bool = False


class AuthResponse(BaseModel):
    session: SessionInfo


# --- Stats: Summary ---


class QueryTypes(BaseModel):
    A: int = 0
    AAAA: int = 0
    ANY: int = 0
    SRV: int = 0
    SOA: int = 0
    PTR: int = 0
    TXT: int = 0
    NAPTR: int = 0
    MX: int = 0
    DS: int = 0
    RRSIG: int = 0
    DNSKEY: int = 0
    NS: int = 0
    SVCB: int = 0
    HTTPS: int = 0
    OTHER: int = 0


class QueryStatus(BaseModel):
    UNKNOWN: int = 0
    GRAVITY: int = 0
    FORWARDED: int = 0
    CACHE: int = 0
    REGEX: int = 0
    DENYLIST: int = 0
    EXTERNAL_BLOCKED_IP: int = 0
    EXTERNAL_BLOCKED_NULL: int = 0
    EXTERNAL_BLOCKED_NXRA: int = 0
    GRAVITY_CNAME: int = 0
    REGEX_CNAME: int = 0
    DENYLIST_CNAME: int = 0
    RETRIED: int = 0
    RETRIED_DNSSEC: int = 0
    IN_PROGRESS: int = 0
    DBBUSY: int = 0
    SPECIAL_DOMAIN: int = 0
    CACHE_STALE: int = 0
    EXTERNAL_BLOCKED_EDE15: int = 0


class QueryReplies(BaseModel):
    UNKNOWN: int = 0
    NODATA: int = 0
    NXDOMAIN: int = 0
    CNAME: int = 0
    IP: int = 0
    DOMAIN: int = 0
    RRNAME: int = 0
    SERVFAIL: int = 0
    REFUSED: int = 0
    NOTIMP: int = 0
    OTHER: int = 0
    DNSSEC: int = 0
    NONE: int = 0
    BLOB: int = 0


class QueriesSummary(BaseModel):
    total: int
    blocked: int
    percent_blocked: float
    unique_domains: int
    forwarded: int
    cached: int
    frequency: float
    types: QueryTypes
    status: QueryStatus
    replies: QueryReplies


class ActiveClients(BaseModel):
    active: int
    total: int


class GravityInfo(BaseModel):
    domains_being_blocked: int
    last_update: int


class SummaryResponse(BaseModel):
    queries: QueriesSummary
    clients: ActiveClients
    gravity: GravityInfo


# --- Stats: Upstreams ---


class UpstreamStatistics(BaseModel):
    response: float
    variance: float


class Upstream(BaseModel):
    ip: Optional[str] = None
    name: Optional[str] = None
    port: int
    count: int
    statistics: UpstreamStatistics


class UpstreamsResponse(BaseModel):
    upstreams: List[Upstream]
    forwarded_queries: int
    total_queries: int


# --- Stats: Top Domains ---


class TopDomainEntry(BaseModel):
    domain: str
    count: int


class TopDomainsResponse(BaseModel):
    domains: List[TopDomainEntry]
    total_queries: int
    blocked_queries: int


# --- Stats: Top Clients ---


class TopClientEntry(BaseModel):
    ip: str
    name: str
    count: int


class TopClientsResponse(BaseModel):
    clients: List[TopClientEntry]
    total_queries: int
    blocked_queries: int


# --- Stats: Query Types ---


class QueryTypesResponse(BaseModel):
    types: QueryTypes


# --- Stats: Recent Blocked ---


class RecentBlockedResponse(BaseModel):
    blocked: List[str]


# --- Stats: Database Summary ---


class DatabaseSummaryResponse(BaseModel):
    sum_queries: int
    sum_blocked: int
    percent_blocked: float
    total_clients: int


# --- History ---


class HistoryEntry(BaseModel):
    timestamp: float
    total: int
    cached: int
    blocked: int
    forwarded: int


class HistoryResponse(BaseModel):
    history: List[HistoryEntry]


# --- History: Clients ---


class ClientHistoryInfo(BaseModel):
    name: Optional[str] = None
    total: int


class ClientHistoryDataEntry(BaseModel):
    timestamp: float
    data: Dict[str, int]


class ClientHistoryResponse(BaseModel):
    clients: Dict[str, ClientHistoryInfo]
    history: List[ClientHistoryDataEntry]


# --- Info: System ---


class RAMInfo(BaseModel):
    model_config = {"populate_by_name": True}

    total: int
    free: int
    used: int
    available: int
    percent_used: float = Field(alias="%used")


class SwapInfo(BaseModel):
    model_config = {"populate_by_name": True}

    total: int
    used: int
    free: int
    percent_used: float = Field(alias="%used")


class MemoryInfo(BaseModel):
    ram: RAMInfo
    swap: SwapInfo


class CPULoad(BaseModel):
    raw: List[float]
    percent: List[float]


class CPUInfo(BaseModel):
    model_config = {"populate_by_name": True}

    nprocs: int
    percent_cpu: float = Field(alias="%cpu")
    load: CPULoad


class FTLProcessInfo(BaseModel):
    model_config = {"populate_by_name": True}

    percent_mem: float = Field(alias="%mem")
    percent_cpu: float = Field(alias="%cpu")


class SystemInfo(BaseModel):
    uptime: int
    memory: MemoryInfo
    procs: int
    cpu: CPUInfo
    ftl: FTLProcessInfo


class SystemResponse(BaseModel):
    system: SystemInfo


# --- Info: FTL ---


class FTLDomainCount(BaseModel):
    total: int
    enabled: int


class FTLDomainCategory(BaseModel):
    allowed: FTLDomainCount
    denied: FTLDomainCount


class FTLDatabase(BaseModel):
    gravity: int
    groups: int
    lists: int
    clients: int
    domains: FTLDomainCategory
    regex: FTLDomainCategory


class FTLClientCount(BaseModel):
    total: int
    active: int


class DnsmasqMetrics(BaseModel):
    dns_cache_inserted: int = 0
    dns_cache_live_freed: int = 0
    dns_queries_forwarded: int = 0
    dns_auth_answered: int = 0
    dns_local_answered: int = 0
    dns_stale_answered: int = 0
    dns_unanswered: int = 0
    bootp: int = 0
    pxe: int = 0
    dhcp_ack: int = 0
    dhcp_decline: int = 0
    dhcp_discover: int = 0
    dhcp_inform: int = 0
    dhcp_nak: int = 0
    dhcp_offer: int = 0
    dhcp_release: int = 0
    dhcp_request: int = 0
    noanswer: int = 0
    leases_allocated_4: int = 0
    leases_pruned_4: int = 0
    leases_allocated_6: int = 0
    leases_pruned_6: int = 0
    tcp_connections: int = 0
    dhcp_leasequery: int = 0
    dhcp_lease_unassigned: int = 0
    dhcp_lease_actve: int = 0  # typo preserved from API spec
    dhcp_lease_unknown: int = 0
    dnssec_max_crypto_use: int = 0
    dnssec_max_sig_fail: int = 0
    dnssec_max_work: int = 0


class FTLInfo(BaseModel):
    model_config = {"populate_by_name": True}

    database: FTLDatabase
    privacy_level: int
    query_frequency: float
    clients: FTLClientCount
    pid: int
    uptime: float
    percent_mem: float = Field(alias="%mem")
    percent_cpu: float = Field(alias="%cpu")
    allow_destructive: bool
    dnsmasq: DnsmasqMetrics


class FTLResponse(BaseModel):
    ftl: FTLInfo


# --- Info: Sensors ---


class TempReading(BaseModel):
    name: Optional[str] = None
    value: float
    max: Optional[float] = None
    crit: Optional[float] = None
    sensor: str


class SensorDevice(BaseModel):
    name: Optional[str] = None
    path: str
    source: str
    temps: List[TempReading]


class SensorsData(BaseModel):
    list: List[SensorDevice]
    cpu_temp: Optional[float] = None
    hot_limit: float
    unit: str


class SensorsResponse(BaseModel):
    sensors: SensorsData


# --- Info: Live Metrics (DNS/DHCP) ---


class CacheContentCount(BaseModel):
    valid: int
    stale: int


class CacheContentEntry(BaseModel):
    type: int
    name: str
    count: CacheContentCount


class DNSCache(BaseModel):
    size: int
    inserted: int
    evicted: int
    expired: int
    immortal: int
    content: List[CacheContentEntry]


class DNSReplies(BaseModel):
    forwarded: int
    unanswered: int
    local: int
    optimized: int
    auth: int
    sum: int


class DNSMetrics(BaseModel):
    cache: DNSCache
    replies: DNSReplies


class DHCPLeases(BaseModel):
    allocated_4: int
    pruned_4: int
    allocated_6: int
    pruned_6: int


class DHCPMetrics(BaseModel):
    ack: int = 0
    nak: int = 0
    decline: int = 0
    offer: int = 0
    discover: int = 0
    inform: int = 0
    request: int = 0
    release: int = 0
    noanswer: int = 0
    bootp: int = 0
    pxe: int = 0
    leases: DHCPLeases


class InfoMetricsData(BaseModel):
    dns: DNSMetrics
    dhcp: DHCPMetrics


class InfoMetricsResponse(BaseModel):
    metrics: InfoMetricsData


# --- DNS Blocking ---


class BlockingResponse(BaseModel):
    blocking: str
    timer: Optional[float] = None
