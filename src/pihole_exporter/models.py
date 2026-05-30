from typing import List, Optional

from pydantic import BaseModel

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


# --- DNS Blocking ---


class BlockingResponse(BaseModel):
    blocking: str
    timer: Optional[float] = None
