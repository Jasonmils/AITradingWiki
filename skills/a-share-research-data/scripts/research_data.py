#!/usr/bin/env python3
"""Read-only A-share research-data adapters with injectable HTTP transport."""

from __future__ import annotations

import base64
import hashlib
import html
import json
import math
import os
import re
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Mapping, Protocol, Sequence
from zoneinfo import ZoneInfo


UTC = timezone.utc
SHANGHAI = ZoneInfo("Asia/Shanghai")
TIMEZONE_NAME = "Asia/Shanghai"
USER_AGENT = "Mozilla/5.0 (compatible; AITradingWiki/1.0; read-only research)"
SCHEMA_VERSION = "a-share-research-data-v1"

TENCENT_QUOTE_URL = "https://qt.gtimg.cn/q="
EASTMONEY_DATACENTER_URL = "https://datacenter-web.eastmoney.com/api/data/v1/get"
CNINFO_ORG_MAP_URL = "https://www.cninfo.com.cn/new/data/szse_stock.json"
CNINFO_ANNOUNCEMENT_URL = "https://www.cninfo.com.cn/new/hisAnnouncement/query"
CNINFO_STATIC_BASE = "https://static.cninfo.com.cn/"
SINA_FINANCE_URL = (
    "https://quotes.sina.cn/cn/api/openapi.php/"
    "CompanyFinanceService.getFinanceReport2022"
)
THS_CONSENSUS_URL = "https://basic.10jqka.com.cn/new/{code}/worth.html"
CNINFO_IR_SEARCH_URL = "https://irm.cninfo.com.cn/newircs/index/queryKeyboardInfo"
CNINFO_IR_QUESTION_URL = "https://irm.cninfo.com.cn/newircs/company/question"
EASTMONEY_NEWS_URL = "https://search-api-web.eastmoney.com/search/jsonp"
MAX_QUOTE_FUTURE_SKEW_SECONDS = 300
FINANCIAL_REPORT_CATEGORIES = ";".join(
    (
        "category_ndbg_szsh",
        "category_bndbg_szsh",
        "category_yjdbg_szsh",
        "category_sjdbg_szsh",
    )
)


def utc_now() -> datetime:
    return datetime.now(UTC)


def iso_utc(value: datetime | None = None) -> str:
    return (value or utc_now()).astimezone(UTC).isoformat().replace("+00:00", "Z")


def _hash_bodies(bodies: Sequence[bytes]) -> str | None:
    if not bodies:
        return None
    digest = hashlib.sha256()
    for body in bodies:
        digest.update(body)
    return digest.hexdigest()


def _safe_float(value: Any) -> float | None:
    if value in (None, "", "-"):
        return None
    try:
        return float(str(value).replace(",", ""))
    except (TypeError, ValueError):
        return None


def _required_positive_float(value: Any, field: str) -> float:
    number = _safe_float(value)
    if number is None or not math.isfinite(number) or number <= 0:
        raise ValueError(f"{field} must be a finite positive number")
    return number


def _safe_int(value: Any) -> int | None:
    number = _safe_float(value)
    return int(number) if number is not None else None


def _date_text(value: Any) -> str | None:
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        try:
            return datetime.fromtimestamp(value / 1000, UTC).astimezone(SHANGHAI).date().isoformat()
        except (OverflowError, OSError, ValueError):
            return None
    text = str(value).strip()
    match = re.search(r"(20\d{2})[-/]?(\d{2})[-/]?(\d{2})", text)
    return "-".join(match.groups()) if match else text[:10] or None


def _max_date(records: Sequence[Mapping[str, Any]], *keys: str) -> str | None:
    dates = []
    for record in records:
        for key in keys:
            value = _date_text(record.get(key))
            if value and re.fullmatch(r"20\d{2}-\d{2}-\d{2}", value):
                dates.append(value)
                break
    return max(dates) if dates else None


def _record_dates_as_of(records: Sequence[Mapping[str, Any]]) -> str | None:
    dates: list[str] = []
    for record in records:
        for key, raw_value in record.items():
            normalized_key = str(key).lower()
            if not (
                "date" in normalized_key
                or normalized_key.endswith("_at")
                or "period" in normalized_key
                or normalized_key in {"free_date", "end_date"}
            ):
                continue
            value = _date_text(raw_value)
            if value and re.fullmatch(r"20\d{2}-\d{2}-\d{2}", value):
                dates.append(value)
    return max(dates) if dates else None


def _require_iso_date(value: Any, field: str) -> str:
    normalized = _date_text(value)
    if normalized is None or not re.fullmatch(r"20\d{2}-\d{2}-\d{2}", normalized):
        raise ValueError(f"{field} is missing or not a supported date")
    try:
        datetime.strptime(normalized, "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(f"{field} is not a valid calendar date") from exc
    return normalized


def _pagination_error(page_size: Any, max_pages: Any) -> str | None:
    for name, value in (("page_size", page_size), ("max_pages", max_pages)):
        if isinstance(value, bool) or not isinstance(value, int) or value < 1:
            return f"{name} must be a positive integer"
    return None


@dataclass(frozen=True)
class SecurityId:
    exchange: str
    code: str

    @classmethod
    def parse(cls, value: str) -> "SecurityId":
        match = re.fullmatch(r"(SSE|SZSE|BJSE):(\d{6})", str(value).strip().upper())
        if not match:
            raise ValueError(
                "ticker must be exchange-prefixed, for example SSE:600519, "
                "SZSE:000001, or BJSE:920982"
            )
        exchange, code = match.groups()
        if exchange == "BJSE" and not code.startswith(("92", "43", "83", "87")):
            raise ValueError(f"{value!r} conflicts with known BJSE code ranges")
        if exchange == "SSE" and code.startswith(("30", "00", "92", "43", "83", "87")):
            raise ValueError(f"{value!r} conflicts with known SSE equity code ranges")
        if exchange == "SZSE" and code.startswith(("5", "6", "9", "43", "83", "87")):
            raise ValueError(f"{value!r} conflicts with known SZSE code ranges")
        return cls(exchange=exchange, code=code)

    @property
    def canonical(self) -> str:
        return f"{self.exchange}:{self.code}"

    @property
    def tencent(self) -> str:
        return {"SSE": "sh", "SZSE": "sz", "BJSE": "bj"}[self.exchange] + self.code

    @property
    def eastmoney_secid(self) -> str:
        market = "1" if self.exchange == "SSE" else "0"
        return f"{market}.{self.code}"

    @property
    def sina(self) -> str:
        return {"SSE": "sh", "SZSE": "sz", "BJSE": "bj"}[self.exchange] + self.code

    @property
    def legacy_bjse(self) -> bool:
        return self.exchange == "BJSE" and self.code.startswith(("43", "83", "87"))


@dataclass
class HttpResponse:
    status: int
    headers: dict[str, str]
    body: bytes
    url: str
    fetched_at: str
    from_cache: bool = False


class TransportError(RuntimeError):
    def __init__(self, error_type: str, message: str):
        super().__init__(message)
        self.error_type = error_type


class HttpTransport(Protocol):
    def request(
        self,
        method: str,
        url: str,
        *,
        params: Mapping[str, Any] | None = None,
        form: Mapping[str, Any] | None = None,
        json_body: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        timeout: float = 20,
        fixture_key: str | None = None,
    ) -> HttpResponse: ...


def _encode_request(
    url: str,
    params: Mapping[str, Any] | None,
    form: Mapping[str, Any] | None,
    json_body: Mapping[str, Any] | None,
) -> tuple[str, bytes | None, str | None]:
    resolved = url
    if params:
        query = urllib.parse.urlencode(params, doseq=True)
        resolved += ("&" if "?" in resolved else "?") + query
    if form is not None and json_body is not None:
        raise ValueError("form and json_body are mutually exclusive")
    if form is not None:
        return resolved, urllib.parse.urlencode(form, doseq=True).encode(), "application/x-www-form-urlencoded"
    if json_body is not None:
        return resolved, json.dumps(json_body, ensure_ascii=False, separators=(",", ":")).encode(), "application/json"
    return resolved, None, None


class UrllibTransport:
    def request(
        self,
        method: str,
        url: str,
        *,
        params: Mapping[str, Any] | None = None,
        form: Mapping[str, Any] | None = None,
        json_body: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        timeout: float = 20,
        fixture_key: str | None = None,
    ) -> HttpResponse:
        del fixture_key
        resolved, body, content_type = _encode_request(url, params, form, json_body)
        request_headers = {"User-Agent": USER_AGENT, **dict(headers or {})}
        if content_type and "Content-Type" not in request_headers:
            request_headers["Content-Type"] = content_type
        request = urllib.request.Request(
            resolved,
            data=body,
            headers=request_headers,
            method=method.upper(),
        )
        fetched_at = iso_utc()
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return HttpResponse(
                    status=int(response.status),
                    headers={str(k).lower(): str(v) for k, v in response.headers.items()},
                    body=response.read(),
                    url=response.geturl(),
                    fetched_at=fetched_at,
                )
        except urllib.error.HTTPError as exc:
            return HttpResponse(
                status=int(exc.code),
                headers={str(k).lower(): str(v) for k, v in exc.headers.items()},
                body=exc.read(),
                url=resolved,
                fetched_at=fetched_at,
            )
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise TransportError("transport_error", str(exc)) from exc


class FixtureTransport:
    """Network-free transport keyed by adapters' stable ``fixture_key`` values."""

    def __init__(self, fixtures: Mapping[str, Any]):
        raw = fixtures.get("responses", fixtures)
        if not isinstance(raw, Mapping):
            raise ValueError("fixture must be a mapping or contain a responses mapping")
        self._fixtures = dict(raw)
        self.calls: list[str] = []

    @classmethod
    def from_file(cls, path: str | Path) -> "FixtureTransport":
        return cls(json.loads(Path(path).read_text(encoding="utf-8")))

    def request(
        self,
        method: str,
        url: str,
        *,
        params: Mapping[str, Any] | None = None,
        form: Mapping[str, Any] | None = None,
        json_body: Mapping[str, Any] | None = None,
        headers: Mapping[str, str] | None = None,
        timeout: float = 20,
        fixture_key: str | None = None,
    ) -> HttpResponse:
        del method, params, form, json_body, headers, timeout
        if not fixture_key:
            raise TransportError("fixture_error", f"request for {url} has no fixture key")
        self.calls.append(fixture_key)
        if fixture_key not in self._fixtures:
            raise TransportError("fixture_missing", f"missing fixture response: {fixture_key}")
        item = self._fixtures[fixture_key]
        if isinstance(item, list):
            if not item:
                raise TransportError("fixture_exhausted", fixture_key)
            item = item.pop(0)
        if not isinstance(item, Mapping):
            item = {"status": 200, "body": item}
        body_value = item.get("body", b"")
        if isinstance(body_value, (dict, list)):
            body = json.dumps(body_value, ensure_ascii=False).encode()
        elif isinstance(body_value, str):
            encoding = str(item.get("encoding", "utf-8"))
            body = body_value.encode(encoding)
        else:
            body = bytes(body_value)
        return HttpResponse(
            status=int(item.get("status", 200)),
            headers={str(k).lower(): str(v) for k, v in dict(item.get("headers", {})).items()},
            body=body,
            url=str(item.get("url", url)),
            fetched_at=str(item.get("fetched_at", iso_utc())),
        )


class CachingTransport:
    def __init__(self, inner: HttpTransport, cache_dir: str | Path, ttl_seconds: int = 900):
        self.inner = inner
        self.cache_dir = Path(cache_dir)
        self.ttl_seconds = max(0, int(ttl_seconds))

    def request(self, method: str, url: str, **kwargs: Any) -> HttpResponse:
        identity = json.dumps(
            {
                "method": method.upper(),
                "url": url,
                "params": kwargs.get("params"),
                "form": kwargs.get("form"),
                "json_body": kwargs.get("json_body"),
            },
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        key = hashlib.sha256(identity.encode()).hexdigest()
        path = self.cache_dir / f"{key}.json"
        if path.is_file() and self.ttl_seconds:
            try:
                cached = json.loads(path.read_text(encoding="utf-8"))
                age = time.time() - float(cached["cached_epoch"])
                if 0 <= age <= self.ttl_seconds:
                    return HttpResponse(
                        status=int(cached["status"]),
                        headers=dict(cached["headers"]),
                        body=base64.b64decode(cached["body_b64"]),
                        url=str(cached["url"]),
                        fetched_at=str(cached["fetched_at"]),
                        from_cache=True,
                    )
            except (KeyError, ValueError, OSError, json.JSONDecodeError):
                pass
        response = self.inner.request(method, url, **kwargs)
        if 200 <= response.status < 300:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            payload = {
                "cached_epoch": time.time(),
                "status": response.status,
                "headers": response.headers,
                "body_b64": base64.b64encode(response.body).decode(),
                "url": response.url,
                "fetched_at": response.fetched_at,
            }
            temporary_path: Path | None = None
            try:
                with tempfile.NamedTemporaryFile(
                    mode="w",
                    encoding="utf-8",
                    dir=self.cache_dir,
                    prefix=f".{path.name}.",
                    suffix=".tmp",
                    delete=False,
                ) as stream:
                    stream.write(json.dumps(payload, ensure_ascii=False))
                    stream.flush()
                    os.fsync(stream.fileno())
                    temporary_path = Path(stream.name)
                temporary_path.replace(path)
            finally:
                if temporary_path is not None and temporary_path.exists():
                    temporary_path.unlink()
        return response


class _TableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.tables: list[list[list[str]]] = []
        self._table: list[list[str]] | None = None
        self._row: list[str] | None = None
        self._cell: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del attrs
        if tag == "table" and self._table is None:
            self._table = []
        elif tag == "tr" and self._table is not None:
            self._row = []
        elif tag in {"td", "th"} and self._row is not None:
            self._cell = []

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag in {"td", "th"} and self._cell is not None and self._row is not None:
            value = html.unescape(" ".join(self._cell))
            self._row.append(re.sub(r"\s+", " ", value).strip())
            self._cell = None
        elif tag == "tr" and self._row is not None and self._table is not None:
            if any(self._row):
                self._table.append(self._row)
            self._row = None
        elif tag == "table" and self._table is not None:
            self.tables.append(self._table)
            self._table = None


def _decode_body(response: HttpResponse) -> str:
    content_type = response.headers.get("content-type", "")
    match = re.search(r"charset=([\w-]+)", content_type, re.I)
    candidates = [match.group(1)] if match else []
    candidates.extend(["utf-8", "gb18030"])
    for encoding in candidates:
        try:
            return response.body.decode(encoding)
        except (LookupError, UnicodeDecodeError):
            continue
    return response.body.decode("utf-8", errors="replace")


def _json_body(response: HttpResponse) -> Any:
    return json.loads(_decode_body(response))


def _jsonp_body(response: HttpResponse) -> Any:
    text = _decode_body(response).strip()
    start, end = text.find("("), text.rfind(")")
    if start < 0 or end <= start:
        raise ValueError("response is not JSONP")
    return json.loads(text[start + 1 : end])


def _error_envelope(
    security: SecurityId,
    provider: str,
    endpoint: str,
    source_url: str,
    error_type: str,
    message: str,
    *,
    responses: Sequence[HttpResponse] = (),
    records: Sequence[Mapping[str, Any]] = (),
    field_units: Mapping[str, str] | None = None,
    evidence_class_hint: str = "unverified",
    as_of: str | None = None,
) -> dict[str, Any]:
    response_fetched_at = max((r.fetched_at for r in responses), default=None)
    return {
        "canonical_ticker": security.canonical,
        "provider": provider,
        "endpoint": endpoint,
        "source_url": source_url,
        "queried_at": iso_utc(),
        "response_fetched_at": response_fetched_at,
        "as_of": as_of or _record_dates_as_of(records),
        "timezone": TIMEZONE_NAME,
        "raw_response_sha256": _hash_bodies([r.body for r in responses]),
        "field_units": dict(field_units or {}),
        "evidence_class_hint": evidence_class_hint,
        "data_quality_status": "degraded" if records else "unavailable",
        "error_type": error_type,
        "error_message": message,
        "result_status": "error",
        "record_count": len(records),
        "records": list(records),
        "from_cache": bool(responses) and all(r.from_cache for r in responses),
    }


def _success_envelope(
    security: SecurityId,
    provider: str,
    endpoint: str,
    source_url: str,
    records: Sequence[Mapping[str, Any]],
    responses: Sequence[HttpResponse],
    *,
    as_of: str | None,
    field_units: Mapping[str, str],
    evidence_class_hint: str,
    quality: str,
    notes: Sequence[str] = (),
) -> dict[str, Any]:
    response_fetched_at = max((r.fetched_at for r in responses), default=None)
    return {
        "canonical_ticker": security.canonical,
        "provider": provider,
        "endpoint": endpoint,
        "source_url": source_url,
        "queried_at": iso_utc(),
        "response_fetched_at": response_fetched_at,
        "as_of": as_of,
        "timezone": TIMEZONE_NAME,
        "raw_response_sha256": _hash_bodies([r.body for r in responses]),
        "field_units": dict(field_units),
        "evidence_class_hint": evidence_class_hint,
        "data_quality_status": quality,
        "error_type": None,
        "error_message": None,
        "result_status": "ok" if records else "empty",
        "record_count": len(records),
        "records": list(records),
        "notes": list(notes),
        "from_cache": bool(responses) and all(r.from_cache for r in responses),
    }


@dataclass(frozen=True)
class DiscoverySpec:
    endpoint: str
    report_name: str
    code_field: str
    date_field: str
    sort_column: str
    columns: tuple[str, ...]
    units: Mapping[str, str]


DISCOVERY_SPECS: dict[str, DiscoverySpec] = {
    "lockups": DiscoverySpec(
        "lockups", "RPT_LIFT_STAGE", "SECURITY_CODE", "FREE_DATE", "FREE_DATE",
        ("FREE_DATE", "FREE_SHARES_TYPE", "FREE_SHARES", "ABLE_FREE_SHARES", "FREE_RATIO"),
        {"FREE_SHARES": "provider_native; verify with official filing", "ABLE_FREE_SHARES": "provider_native; verify with official filing", "FREE_RATIO": "ratio"},
    ),
    "dividends": DiscoverySpec(
        "dividends", "RPT_SHAREBONUS_DET", "SECURITY_CODE", "EX_DIVIDEND_DATE", "EX_DIVIDEND_DATE",
        ("EX_DIVIDEND_DATE", "PRETAX_BONUS_RMB", "TRANSFER_RATIO", "BONUS_RATIO", "ASSIGN_PROGRESS"),
        {"PRETAX_BONUS_RMB": "provider_native; reconcile per-share/per-10-share basis", "TRANSFER_RATIO": "provider_native per 10 shares", "BONUS_RATIO": "provider_native per 10 shares"},
    ),
    "holder_counts": DiscoverySpec(
        "holder_counts", "RPT_HOLDERNUMLATEST", "SECURITY_CODE", "END_DATE", "END_DATE",
        ("END_DATE", "HOLDER_NUM", "HOLDER_NUM_CHANGE", "HOLDER_NUM_RATIO", "AVG_FREE_SHARES"),
        {"HOLDER_NUM": "accounts", "HOLDER_NUM_CHANGE": "accounts", "HOLDER_NUM_RATIO": "percent", "AVG_FREE_SHARES": "shares/account"},
    ),
    "block_trades": DiscoverySpec(
        "block_trades", "RPT_DATA_BLOCKTRADE", "SECURITY_CODE", "TRADE_DATE", "TRADE_DATE",
        ("TRADE_DATE", "DEAL_PRICE", "CLOSE_PRICE", "DEAL_VOLUME", "DEAL_AMT", "PREMIUM_RATIO", "BUYER_NAME", "SELLER_NAME"),
        {"DEAL_PRICE": "CNY/share", "CLOSE_PRICE": "CNY/share", "DEAL_VOLUME": "provider_native; verify with exchange", "DEAL_AMT": "provider_native; verify with exchange", "PREMIUM_RATIO": "percent"},
    ),
    "margin": DiscoverySpec(
        "margin", "RPTA_WEB_RZRQ_GGMX", "SCODE", "DATE", "DATE",
        ("DATE", "RZYE", "RZMRE", "RZCHE", "RQYE", "RQMCL", "RQCHL", "RZRQYE"),
        {"RZYE": "CNY", "RZMRE": "CNY", "RZCHE": "CNY", "RQYE": "CNY", "RQMCL": "shares", "RQCHL": "shares", "RZRQYE": "CNY"},
    ),
}


class ResearchDataClient:
    def __init__(self, transport: HttpTransport | None = None):
        self.transport = transport or UrllibTransport()
        self._cninfo_org_cache: dict[str, str] | None = None

    def _request(self, security: SecurityId, provider: str, endpoint: str, url: str, **kwargs: Any) -> tuple[HttpResponse | None, dict[str, Any] | None]:
        try:
            response = self.transport.request(**{"method": kwargs.pop("method", "GET"), "url": url, **kwargs})
        except TransportError as exc:
            return None, _error_envelope(security, provider, endpoint, url, exc.error_type, str(exc))
        if response.status < 200 or response.status >= 300:
            return response, _error_envelope(
                security, provider, endpoint, url, "http_error", f"HTTP {response.status}", responses=[response]
            )
        return response, None

    def quote(self, ticker: str, *, max_age_hours: float = 96.0) -> dict[str, Any]:
        security = SecurityId.parse(ticker)
        url = TENCENT_QUOTE_URL + security.tencent
        response, error = self._request(
            security, "Tencent Finance", "quote", url,
            headers={"Referer": "https://gu.qq.com/"}, fixture_key="quote",
        )
        if error:
            return error
        assert response is not None
        try:
            text = _decode_body(response)
            match = re.search(r'="([^"]*)"', text)
            if not match:
                raise ValueError("missing quote payload")
            values = match.group(1).split("~")
            if len(values) < 53 or values[2] != security.code:
                raise ValueError("quote schema or ticker mismatch")
            timestamp_text = values[30]
            quote_time = datetime.strptime(timestamp_text, "%Y%m%d%H%M%S").replace(tzinfo=SHANGHAI)
            signed_age_seconds = (
                utc_now() - quote_time.astimezone(UTC)
            ).total_seconds()
            age_seconds = max(0.0, signed_age_seconds)
            future_skew_seconds = max(0.0, -signed_age_seconds)
            future_clock_skew = future_skew_seconds > MAX_QUOTE_FUTURE_SKEW_SECONDS
            price = _required_positive_float(values[3], "price")
            previous_close = _required_positive_float(
                values[4], "previous_close"
            )
            high = _required_positive_float(values[33], "high")
            low = _required_positive_float(values[34], "low")
            if high < low:
                raise ValueError("high must be greater than or equal to low")
            amount_ten_thousand = _safe_float(values[37])
            frozen = price == previous_close and (amount_ten_thousand or 0) == 0
            stale = (
                security.legacy_bjse
                or frozen
                or future_clock_skew
                or age_seconds > max_age_hours * 3600
            )
            if security.legacy_bjse:
                stale_reason = "legacy BJSE 43/83/87 code; resolve the current 920xxx code by issuer identity"
            elif frozen:
                stale_reason = "zero turnover with unchanged price; possible suspension, no active session, or frozen quote"
            elif future_clock_skew:
                stale_reason = (
                    "provider timestamp is more than "
                    f"{MAX_QUOTE_FUTURE_SKEW_SECONDS} seconds in the future"
                )
            elif age_seconds > max_age_hours * 3600:
                stale_reason = f"provider timestamp is older than {max_age_hours:g} hours"
            else:
                stale_reason = None
            record = {
                "name": values[1],
                "provider_ticker": security.tencent,
                "quote_time": quote_time.isoformat(),
                "price": price,
                "previous_close": previous_close,
                "open": _safe_float(values[5]),
                "change": _safe_float(values[31]),
                "change_pct": _safe_float(values[32]),
                "high": high,
                "low": low,
                "amount_ten_thousand_cny": amount_ten_thousand,
                "turnover_pct": _safe_float(values[38]),
                "pe_ttm": _safe_float(values[39]),
                "float_market_cap_100m_cny": _safe_float(values[44]),
                "total_market_cap_100m_cny": _safe_float(values[45]),
                "pb": _safe_float(values[46]),
                "limit_up": _safe_float(values[47]),
                "limit_down": _safe_float(values[48]),
                "pe_static": _safe_float(values[52]),
                "age_seconds": round(age_seconds),
                "future_clock_skew_seconds": round(future_skew_seconds),
                "is_stale": stale,
                "stale_reason": stale_reason,
                "suspension_status": "possible_suspension_or_no_active_session" if frozen else "not_indicated_by_quote",
                "suspension_check_is_definitive": False,
                "official_recheck_required": stale,
            }
        except (ValueError, IndexError) as exc:
            return _error_envelope(
                security, "Tencent Finance", "quote", url, "schema_error", str(exc), responses=[response]
            )
        return _success_envelope(
            security, "Tencent Finance", "quote", url, [record], [response],
            as_of=quote_time.date().isoformat(),
            field_units={
                "price": "CNY/share", "amount_ten_thousand_cny": "10,000 CNY",
                "turnover_pct": "percent", "pe_ttm": "ratio", "pe_static": "ratio",
                "pb": "ratio", "float_market_cap_100m_cny": "100m CNY",
                "total_market_cap_100m_cny": "100m CNY", "age_seconds": "seconds",
                "future_clock_skew_seconds": "seconds",
            },
            evidence_class_hint="third_party_market_observation",
            quality="degraded",
            notes=[
                "Quality remains degraded because this is a single third-party quote source.",
                "No valuation threshold or directional signal is applied.",
                "Suspension status requires an official check.",
            ],
        )

    def _cninfo_org_map(self, security: SecurityId) -> tuple[dict[str, str] | None, HttpResponse | None, dict[str, Any] | None]:
        if self._cninfo_org_cache is not None:
            return self._cninfo_org_cache, None, None
        response, error = self._request(
            security, "CNINFO", "cninfo_org_map", CNINFO_ORG_MAP_URL,
            fixture_key="cninfo_org_map",
        )
        if error:
            return None, response, error
        assert response is not None
        try:
            payload = _json_body(response)
            stocks = payload.get("stockList") if isinstance(payload, Mapping) else None
            if not isinstance(stocks, list):
                raise ValueError("stockList is missing")
            mapping: dict[str, str] = {}
            for item in stocks:
                if (
                    not isinstance(item, Mapping)
                    or not item.get("code")
                    or not item.get("orgId")
                ):
                    raise ValueError(
                        "stockList row is not an object with code and orgId"
                    )
                code = str(item["code"])
                org_id = str(item["orgId"])
                if code in mapping and mapping[code] != org_id:
                    raise ValueError(f"stockList contains conflicting orgId for {code}")
                mapping[code] = org_id
            if not mapping:
                raise ValueError("stockList contains no usable identifiers")
            self._cninfo_org_cache = mapping
            return mapping, response, None
        except (ValueError, KeyError, json.JSONDecodeError) as exc:
            error = _error_envelope(
                security, "CNINFO", "cninfo_org_map", CNINFO_ORG_MAP_URL,
                "schema_error", str(exc), responses=[response],
            )
            return None, response, error

    def announcements(
        self,
        ticker: str,
        *,
        page_size: int = 30,
        max_pages: int = 10,
        start_date: str = "",
        end_date: str = "",
        category: str = "",
        search_key: str = "",
    ) -> dict[str, Any]:
        security = SecurityId.parse(ticker)
        invalid_pagination = _pagination_error(page_size, max_pages)
        if invalid_pagination:
            return _error_envelope(
                security,
                "CNINFO",
                "announcements",
                CNINFO_ANNOUNCEMENT_URL,
                "invalid_request",
                invalid_pagination,
                evidence_class_hint="verified_fact_candidate",
            )
        org_map, map_response, map_error = self._cninfo_org_map(security)
        if map_error:
            map_error["endpoint"] = "announcements"
            map_error["source_url"] = CNINFO_ANNOUNCEMENT_URL
            return map_error
        assert org_map is not None
        org_id = org_map.get(security.code)
        if not org_id:
            return _error_envelope(
                security, "CNINFO", "announcements", CNINFO_ANNOUNCEMENT_URL,
                "identifier_not_found", "exact CNINFO orgId not found; no hard-coded fallback was used",
                responses=[map_response] if map_response else [], evidence_class_hint="verified_fact_candidate",
            )
        responses = [map_response] if map_response else []
        records: list[dict[str, Any]] = []
        expected_total: int | None = None
        final_page_full = False
        for page in range(1, max_pages + 1):
            payload = {
                "stock": f"{security.code},{org_id}", "tabName": "fulltext",
                "pageSize": str(page_size), "pageNum": str(page), "column": "",
                "category": category, "plate": "", "seDate": f"{start_date}~{end_date}" if start_date or end_date else "",
                "searchkey": search_key, "secid": "", "sortName": "", "sortType": "", "isHLtitle": "true",
            }
            response, error = self._request(
                security, "CNINFO", "announcements", CNINFO_ANNOUNCEMENT_URL,
                method="POST", form=payload,
                headers={"Referer": "https://www.cninfo.com.cn/new/disclosure", "Origin": "https://www.cninfo.com.cn"},
                fixture_key=f"announcements:{page}",
            )
            if error:
                error["records"] = records
                error["record_count"] = len(records)
                error["data_quality_status"] = "degraded" if records else "unavailable"
                error["raw_response_sha256"] = _hash_bodies([r.body for r in responses] + ([response.body] if response else []))
                return error
            assert response is not None
            responses.append(response)
            try:
                body = _json_body(response)
                if not isinstance(body, Mapping) or "announcements" not in body or not isinstance(body.get("announcements"), list):
                    raise ValueError("announcements list is missing")
                page_rows = body.get("announcements") or []
                total_value = body.get("totalAnnouncement")
                if total_value is not None:
                    expected_total = int(total_value)
            except (ValueError, TypeError, json.JSONDecodeError) as exc:
                return _error_envelope(
                    security, "CNINFO", "announcements", CNINFO_ANNOUNCEMENT_URL,
                    "schema_error", str(exc), responses=responses, records=records,
                    evidence_class_hint="verified_fact_candidate",
                )
            for item in page_rows:
                if not isinstance(item, Mapping):
                    return _error_envelope(
                        security,
                        "CNINFO",
                        "announcements",
                        CNINFO_ANNOUNCEMENT_URL,
                        "schema_error",
                        "announcement row is not an object",
                        responses=responses,
                        records=records,
                        evidence_class_hint="verified_fact_candidate",
                    )
                announcement_id = item.get("announcementId")
                title = re.sub(
                    r"<[^>]+>", "", str(item.get("announcementTitle") or "")
                ).strip()
                try:
                    if announcement_id in (None, ""):
                        raise ValueError("announcementId is missing")
                    if not title:
                        raise ValueError("announcementTitle is missing")
                    announcement_date = _require_iso_date(
                        item.get("announcementTime"), "announcementTime"
                    )
                except ValueError as exc:
                    return _error_envelope(
                        security,
                        "CNINFO",
                        "announcements",
                        CNINFO_ANNOUNCEMENT_URL,
                        "schema_error",
                        str(exc),
                        responses=responses,
                        records=records,
                        evidence_class_hint="verified_fact_candidate",
                    )
                attachment = str(item.get("adjunctUrl") or "").lstrip("/")
                records.append({
                    "announcement_id": announcement_id,
                    "title": title,
                    "announcement_type": item.get("announcementTypeName"),
                    "announcement_date": announcement_date,
                    "detail_url": f"https://www.cninfo.com.cn/new/disclosure/detail?annoId={announcement_id}",
                    "attachment_url": urllib.parse.urljoin(CNINFO_STATIC_BASE, attachment) if attachment else None,
                    "primary_source": True,
                    "official_document_must_be_read": True,
                })
            final_page_full = len(page_rows) >= page_size
            if not page_rows or (expected_total is not None and len(records) >= expected_total) or len(page_rows) < page_size:
                break
        if expected_total is not None and len(records) < expected_total:
            return _error_envelope(
                security, "CNINFO", "announcements", CNINFO_ANNOUNCEMENT_URL,
                "pagination_limit", f"retrieved {len(records)} of {expected_total} records",
                responses=responses, records=records, evidence_class_hint="verified_fact_candidate",
            )
        if expected_total is None and final_page_full:
            return _error_envelope(
                security, "CNINFO", "announcements", CNINFO_ANNOUNCEMENT_URL,
                "pagination_limit", f"last retrieved page was full; max_pages={max_pages}",
                responses=responses, records=records, evidence_class_hint="verified_fact_candidate",
            )
        return _success_envelope(
            security, "CNINFO", "announcements", CNINFO_ANNOUNCEMENT_URL,
            records, responses, as_of=_max_date(records, "announcement_date"), field_units={},
            evidence_class_hint="verified_fact_candidate_from_official_filing", quality="complete",
            notes=["Read the original attachment before promoting a material assertion."],
        )

    def discovery(self, ticker: str, kind: str, *, page_size: int = 50, max_pages: int = 5) -> dict[str, Any]:
        security = SecurityId.parse(ticker)
        if kind not in DISCOVERY_SPECS:
            raise ValueError(f"unsupported discovery kind: {kind}")
        spec = DISCOVERY_SPECS[kind]
        invalid_pagination = _pagination_error(page_size, max_pages)
        if invalid_pagination:
            return _error_envelope(
                security,
                "Eastmoney Datacenter",
                spec.endpoint,
                EASTMONEY_DATACENTER_URL,
                "invalid_request",
                invalid_pagination,
                field_units=spec.units,
                evidence_class_hint="third_party_discovery_requires_official_recheck",
            )
        responses: list[HttpResponse] = []
        records: list[dict[str, Any]] = []
        expected_pages: int | None = None
        final_page_full = False
        for page in range(1, max_pages + 1):
            params = {
                "reportName": spec.report_name, "columns": "ALL",
                "filter": f'({spec.code_field}="{security.code}")',
                "pageNumber": str(page), "pageSize": str(page_size),
                "sortColumns": spec.sort_column, "sortTypes": "-1",
                "source": "WEB", "client": "WEB",
            }
            response, error = self._request(
                security, "Eastmoney Datacenter", spec.endpoint, EASTMONEY_DATACENTER_URL,
                params=params, headers={"Referer": "https://data.eastmoney.com/"},
                fixture_key=f"{kind}:{page}",
            )
            if error:
                return _error_envelope(
                    security, "Eastmoney Datacenter", spec.endpoint, EASTMONEY_DATACENTER_URL,
                    error["error_type"], error["error_message"], responses=responses + ([response] if response else []),
                    records=records, field_units=spec.units, evidence_class_hint="third_party_discovery_requires_official_recheck",
                )
            assert response is not None
            responses.append(response)
            try:
                body = _json_body(response)
                if not isinstance(body, Mapping):
                    raise ValueError("top-level JSON object is missing")
                if body.get("success") is False:
                    raise RuntimeError(str(body.get("message") or "provider reported failure"))
                result = body.get("result")
                if result is None and body.get("success") is True:
                    page_rows = []
                elif (
                    isinstance(result, Mapping)
                    and "data" in result
                    and isinstance(result.get("data"), list)
                ):
                    page_rows = result.get("data") or []
                    page_value = result.get("pages") or result.get("totalPage")
                    expected_pages = int(page_value) if page_value not in (None, "") else expected_pages
                else:
                    raise ValueError("result.data list is missing")
            except RuntimeError as exc:
                return _error_envelope(
                    security, "Eastmoney Datacenter", spec.endpoint, EASTMONEY_DATACENTER_URL,
                    "provider_error", str(exc), responses=responses, records=records,
                    field_units=spec.units, evidence_class_hint="third_party_discovery_requires_official_recheck",
                )
            except (ValueError, TypeError, json.JSONDecodeError) as exc:
                return _error_envelope(
                    security, "Eastmoney Datacenter", spec.endpoint, EASTMONEY_DATACENTER_URL,
                    "schema_error", str(exc), responses=responses, records=records,
                    field_units=spec.units, evidence_class_hint="third_party_discovery_requires_official_recheck",
                )
            for item in page_rows:
                if not isinstance(item, Mapping):
                    return _error_envelope(
                        security,
                        "Eastmoney Datacenter",
                        spec.endpoint,
                        EASTMONEY_DATACENTER_URL,
                        "schema_error",
                        "discovery row is not an object",
                        responses=responses,
                        records=records,
                        field_units=spec.units,
                        evidence_class_hint="third_party_discovery_requires_official_recheck",
                    )
                provider_code = str(item.get(spec.code_field) or "")
                try:
                    if provider_code != security.code:
                        raise ValueError(
                            f"{spec.code_field} is missing or does not match ticker"
                        )
                    _require_iso_date(item.get(spec.date_field), spec.date_field)
                except ValueError as exc:
                    return _error_envelope(
                        security,
                        "Eastmoney Datacenter",
                        spec.endpoint,
                        EASTMONEY_DATACENTER_URL,
                        "schema_error",
                        str(exc),
                        responses=responses,
                        records=records,
                        field_units=spec.units,
                        evidence_class_hint="third_party_discovery_requires_official_recheck",
                    )
                record = {column: item.get(column) for column in spec.columns}
                record["official_recheck_required"] = True
                record["verification_note"] = "Reconcile material details with the exchange or issuer filing."
                records.append(record)
            final_page_full = len(page_rows) >= page_size
            if not page_rows or len(page_rows) < page_size or (expected_pages is not None and page >= expected_pages):
                break
        if expected_pages is not None and expected_pages > max_pages:
            return _error_envelope(
                security, "Eastmoney Datacenter", spec.endpoint, EASTMONEY_DATACENTER_URL,
                "pagination_limit", f"provider reports {expected_pages} pages; max_pages={max_pages}",
                responses=responses, records=records, field_units=spec.units,
                evidence_class_hint="third_party_discovery_requires_official_recheck",
            )
        if expected_pages is None and final_page_full:
            return _error_envelope(
                security, "Eastmoney Datacenter", spec.endpoint, EASTMONEY_DATACENTER_URL,
                "pagination_limit", f"last retrieved page was full; max_pages={max_pages}",
                responses=responses, records=records, field_units=spec.units,
                evidence_class_hint="third_party_discovery_requires_official_recheck",
            )
        return _success_envelope(
            security, "Eastmoney Datacenter", spec.endpoint, EASTMONEY_DATACENTER_URL,
            records, responses, as_of=_max_date(records, spec.date_field), field_units=spec.units,
            evidence_class_hint="third_party_discovery_requires_official_recheck", quality="degraded",
            notes=["Provider observations are discovery only; important matters require an official recheck."],
        )

    def lockups(self, ticker: str, **kwargs: Any) -> dict[str, Any]:
        return self.discovery(ticker, "lockups", **kwargs)

    def dividends(self, ticker: str, **kwargs: Any) -> dict[str, Any]:
        return self.discovery(ticker, "dividends", **kwargs)

    def holder_counts(self, ticker: str, **kwargs: Any) -> dict[str, Any]:
        return self.discovery(ticker, "holder_counts", **kwargs)

    def block_trades(self, ticker: str, **kwargs: Any) -> dict[str, Any]:
        return self.discovery(ticker, "block_trades", **kwargs)

    def margin(self, ticker: str, **kwargs: Any) -> dict[str, Any]:
        return self.discovery(ticker, "margin", **kwargs)

    def financial_filings(
        self,
        ticker: str,
        *,
        max_pages: int = 10,
        lookback_years: int = 6,
    ) -> dict[str, Any]:
        security = SecurityId.parse(ticker)
        if (
            isinstance(lookback_years, bool)
            or not isinstance(lookback_years, int)
            or lookback_years < 1
        ):
            return _error_envelope(
                security,
                "CNINFO",
                "financial_filings",
                CNINFO_ANNOUNCEMENT_URL,
                "invalid_request",
                "lookback_years must be a positive integer",
                evidence_class_hint="verified_fact_candidate",
            )
        end_date = utc_now().astimezone(SHANGHAI).date()
        start_date = end_date - timedelta(days=366 * lookback_years)
        source = self.announcements(
            security.canonical,
            max_pages=max_pages,
            start_date=start_date.isoformat(),
            end_date=end_date.isoformat(),
            category=FINANCIAL_REPORT_CATEGORIES,
        )
        source["endpoint"] = "financial_filings"
        if source["result_status"] == "error":
            return source
        patterns = ("年度报告", "半年度报告", "季度报告", "审计报告")
        records = [record for record in source["records"] if any(term in str(record.get("title", "")) for term in patterns)]
        source["records"] = records
        source["record_count"] = len(records)
        source["result_status"] = "ok" if records else "empty"
        source["as_of"] = _max_date(records, "announcement_date")
        source["notes"] = [
            "Official filings are primary. Parse and reconcile the attachment before using statement values.",
            (
                "CNINFO query was narrowed to periodic-report categories for "
                f"{start_date.isoformat()} through {end_date.isoformat()}."
            ),
        ]
        return source

    def financial_crosscheck(self, ticker: str, *, periods: int = 8) -> dict[str, Any]:
        security = SecurityId.parse(ticker)
        if isinstance(periods, bool) or not isinstance(periods, int) or periods < 1:
            return _error_envelope(
                security,
                "Sina Finance",
                "financial_crosscheck",
                SINA_FINANCE_URL,
                "invalid_request",
                "periods must be a positive integer",
                field_units={
                    "statement_values": "provider_native; reconcile with official filing"
                },
                evidence_class_hint="third_party_financial_cross_check_only",
            )
        responses: list[HttpResponse] = []
        records: list[dict[str, Any]] = []
        for statement, source in (("balance_sheet", "fzb"), ("income_statement", "lrb"), ("cash_flow_statement", "llb")):
            response, error = self._request(
                security, "Sina Finance", "financial_crosscheck", SINA_FINANCE_URL,
                params={"paperCode": security.sina, "source": source, "type": "0", "page": "1", "num": str(periods)},
                fixture_key=f"financial_crosscheck:{source}",
            )
            if error:
                return _error_envelope(
                    security, "Sina Finance", "financial_crosscheck", SINA_FINANCE_URL,
                    error["error_type"], error["error_message"], responses=responses + ([response] if response else []),
                    records=records, field_units={"statement_values": "provider_native; reconcile with official filing"},
                    evidence_class_hint="third_party_financial_cross_check_only",
                )
            assert response is not None
            responses.append(response)
            try:
                body = _json_body(response)
                report_list = body.get("result", {}).get("data", {}).get("report_list") if isinstance(body, Mapping) else None
                if report_list is None:
                    raise ValueError("result.data.report_list is missing")
                if not isinstance(report_list, Mapping):
                    raise ValueError("report_list is not an object")
            except (ValueError, AttributeError, json.JSONDecodeError) as exc:
                return _error_envelope(
                    security, "Sina Finance", "financial_crosscheck", SINA_FINANCE_URL,
                    "schema_error", str(exc), responses=responses, records=records,
                    field_units={"statement_values": "provider_native; reconcile with official filing"},
                    evidence_class_hint="third_party_financial_cross_check_only",
                )
            for period in sorted(report_list, reverse=True)[:periods]:
                obj = report_list[period]
                if (
                    not isinstance(obj, Mapping)
                    or "data" not in obj
                    or not isinstance(obj.get("data"), list)
                ):
                    return _error_envelope(
                        security,
                        "Sina Finance",
                        "financial_crosscheck",
                        SINA_FINANCE_URL,
                        "schema_error",
                        f"report_list[{period!r}].data is not a list",
                        responses=responses,
                        records=records,
                        field_units={
                            "statement_values": "provider_native; reconcile with official filing"
                        },
                        evidence_class_hint="third_party_financial_cross_check_only",
                    )
                try:
                    reporting_period = _require_iso_date(period, "reporting_period")
                except ValueError as exc:
                    return _error_envelope(
                        security,
                        "Sina Finance",
                        "financial_crosscheck",
                        SINA_FINANCE_URL,
                        "schema_error",
                        str(exc),
                        responses=responses,
                        records=records,
                        field_units={
                            "statement_values": "provider_native; reconcile with official filing"
                        },
                        evidence_class_hint="third_party_financial_cross_check_only",
                    )
                items = {}
                for item in obj.get("data") or []:
                    if not isinstance(item, Mapping) or not item.get("item_title"):
                        return _error_envelope(
                            security,
                            "Sina Finance",
                            "financial_crosscheck",
                            SINA_FINANCE_URL,
                            "schema_error",
                            "financial statement row is not an object with item_title",
                            responses=responses,
                            records=records,
                            field_units={
                                "statement_values": "provider_native; reconcile with official filing"
                            },
                            evidence_class_hint="third_party_financial_cross_check_only",
                        )
                    items[str(item["item_title"])] = {
                        "value": item.get("item_value"),
                        "yoy": item.get("item_tongbi"),
                    }
                records.append({
                    "statement": statement,
                    "reporting_period": reporting_period,
                    "items": items,
                    "official_recheck_required": True,
                })
        return _success_envelope(
            security, "Sina Finance", "financial_crosscheck", SINA_FINANCE_URL,
            records, responses, as_of=_max_date(records, "reporting_period"),
            field_units={"statement_values": "provider_native; currency/unit/basis must be reconciled with official filing"},
            evidence_class_hint="third_party_financial_cross_check_only", quality="degraded",
            notes=["Do not use as a primary statement source.", "Consolidated/parent, cumulative/single-quarter, audit, restatement, currency and units require official reconciliation."],
        )

    def consensus(self, ticker: str) -> dict[str, Any]:
        security = SecurityId.parse(ticker)
        url = THS_CONSENSUS_URL.format(code=security.code)
        response, error = self._request(
            security, "THS", "consensus", url,
            headers={"Referer": "https://basic.10jqka.com.cn/"}, fixture_key="consensus",
        )
        if error:
            return error
        assert response is not None
        parser = _TableParser()
        try:
            parser.feed(_decode_body(response))
            candidates = [table for table in parser.tables if "预测机构数" in " ".join(cell for row in table for cell in row) and "均值" in " ".join(cell for row in table for cell in row)]
            if len(candidates) != 1:
                raise ValueError(f"expected one consensus table, found {len(candidates)}")
            table = candidates[0]
            header_index = next(i for i, row in enumerate(table) if any("年度" in cell for cell in row) and any("均值" in cell for cell in row))
            headers = table[header_index]
            year_key = next((key for key in headers if "年度" in key), None)
            mean_key = next((key for key in headers if "均值" in key), None)
            institution_key = next(
                (key for key in headers if "预测机构数" in key), None
            )
            update_key = next(
                (
                    key
                    for key in headers
                    if "更新" in key and ("时间" in key or "日期" in key)
                ),
                None,
            )
            if not all((year_key, mean_key, institution_key, update_key)):
                raise ValueError(
                    "consensus headers must include forecast year, mean, "
                    "institution count, and update time"
                )
            records = []
            update_dates: list[str] = []
            for row in table[header_index + 1 :]:
                if len(row) < len(headers):
                    raise ValueError("consensus row has fewer cells than headers")
                item = {headers[i] or f"column_{i}": row[i] for i in range(len(headers))}
                forecast_text = str(item.get(year_key) or "").strip()
                forecast_match = re.search(r"20\d{2}", forecast_text)
                if forecast_match is None:
                    raise ValueError("consensus forecast year is missing or invalid")
                if item.get(mean_key) in (None, ""):
                    raise ValueError("consensus mean value is missing")
                update_time = _require_iso_date(
                    item.get(update_key), "consensus update time"
                )
                count = _safe_int(item.get(institution_key))
                item["forecast_year"] = forecast_match.group(0)
                item["update_time"] = update_time
                item["institution_count"] = count
                item["coverage_warning"] = count is None or count < 3
                item["official_recheck_required"] = False
                records.append(item)
                update_dates.append(update_time)
        except (ValueError, StopIteration) as exc:
            return _error_envelope(
                security, "THS", "consensus", url, "schema_error", str(exc), responses=[response],
                field_units={"EPS mean/min/max": "CNY/share unless provider table states otherwise"},
                evidence_class_hint="market_consensus_with_coverage_caveat",
            )
        return _success_envelope(
            security, "THS", "consensus", url, records, [response],
            as_of=max(update_dates) if update_dates else response.fetched_at[:10],
            field_units={"EPS mean/min/max": "CNY/share unless provider table states otherwise", "institution_count": "institutions"},
            evidence_class_hint="market_consensus_with_coverage_caveat", quality="degraded",
            notes=["Retain forecast year and institution coverage.", "Low coverage is not robust consensus; this source is not an official filing."],
        )

    def ir(self, ticker: str, *, page_size: int = 30, max_pages: int = 5) -> dict[str, Any]:
        security = SecurityId.parse(ticker)
        invalid_pagination = _pagination_error(page_size, max_pages)
        if invalid_pagination:
            return _error_envelope(
                security,
                "CNINFO IR",
                "ir",
                CNINFO_IR_QUESTION_URL,
                "invalid_request",
                invalid_pagination,
                evidence_class_hint="company_statement_for_answers_only",
            )
        search_response, error = self._request(
            security, "CNINFO IR", "ir", CNINFO_IR_SEARCH_URL,
            method="POST", form={"keyWord": security.code}, fixture_key="ir:lookup",
        )
        if error:
            return error
        assert search_response is not None
        try:
            body = _json_body(search_response)
            candidates = body.get("data") if isinstance(body, Mapping) else None
            if not isinstance(candidates, list):
                raise ValueError("IR lookup data list is missing")
            exact = [item for item in candidates if isinstance(item, Mapping) and str(item.get("stockCode") or item.get("code") or item.get("secCode") or "") == security.code]
            if len(exact) != 1 or not exact[0].get("secid"):
                raise LookupError("exact IR issuer identifier was not resolved")
            org_id = str(exact[0]["secid"])
        except LookupError as exc:
            return _error_envelope(
                security, "CNINFO IR", "ir", CNINFO_IR_SEARCH_URL,
                "identifier_not_found", str(exc), responses=[search_response], evidence_class_hint="company_statement",
            )
        except (ValueError, json.JSONDecodeError) as exc:
            return _error_envelope(
                security, "CNINFO IR", "ir", CNINFO_IR_SEARCH_URL,
                "schema_error", str(exc), responses=[search_response], evidence_class_hint="company_statement",
            )
        responses = [search_response]
        records: list[dict[str, Any]] = []
        final_page_full = False
        for page in range(1, max_pages + 1):
            params = {
                "_t": "1", "stockcode": security.code, "orgId": org_id,
                "pageSize": str(page_size), "pageNum": str(page), "keyWord": "", "startDay": "", "endDay": "",
            }
            response, request_error = self._request(
                security, "CNINFO IR", "ir", CNINFO_IR_QUESTION_URL,
                method="POST", params=params, fixture_key=f"ir:{page}",
            )
            if request_error:
                return _error_envelope(
                    security, "CNINFO IR", "ir", CNINFO_IR_QUESTION_URL,
                    request_error["error_type"], request_error["error_message"], responses=responses + ([response] if response else []),
                    records=records, evidence_class_hint="company_statement",
                )
            assert response is not None
            responses.append(response)
            try:
                body = _json_body(response)
                rows = body.get("rows") if isinstance(body, Mapping) else None
                if not isinstance(rows, list):
                    raise ValueError("IR rows list is missing")
            except (ValueError, json.JSONDecodeError) as exc:
                return _error_envelope(
                    security, "CNINFO IR", "ir", CNINFO_IR_QUESTION_URL,
                    "schema_error", str(exc), responses=responses, records=records, evidence_class_hint="company_statement",
                )
            for item in rows:
                if not isinstance(item, Mapping):
                    return _error_envelope(
                        security,
                        "CNINFO IR",
                        "ir",
                        CNINFO_IR_QUESTION_URL,
                        "schema_error",
                        "IR row is not an object",
                        responses=responses,
                        records=records,
                        evidence_class_hint="company_statement_for_answers_only",
                    )
                question_id = item.get("questionId") or item.get("id")
                question = str(item.get("mainContent") or "").strip()
                answer = item.get("attachedContent")
                try:
                    if str(item.get("stockCode") or "") != security.code:
                        raise ValueError("IR row ticker is missing or does not match")
                    if question_id in (None, ""):
                        raise ValueError("IR question identifier is missing")
                    if not question:
                        raise ValueError("IR question content is missing")
                    asked_at = _require_iso_date(item.get("pubDate"), "IR pubDate")
                    answered_at = (
                        _require_iso_date(
                            item.get("attachedPubDate"), "IR attachedPubDate"
                        )
                        if answer not in (None, "")
                        else None
                    )
                except ValueError as exc:
                    return _error_envelope(
                        security,
                        "CNINFO IR",
                        "ir",
                        CNINFO_IR_QUESTION_URL,
                        "schema_error",
                        str(exc),
                        responses=responses,
                        records=records,
                        evidence_class_hint="company_statement_for_answers_only",
                    )
                records.append({
                    "question_id": question_id,
                    "company": item.get("companyShortName"),
                    "question": question,
                    "question_evidence": "unverified_investor_question",
                    "answer": answer,
                    "answerer": item.get("attachedAuthor"),
                    "answer_evidence": "company_statement" if answer not in (None, "") else None,
                    "asked_at": asked_at,
                    "answered_at": answered_at,
                })
            final_page_full = len(rows) >= page_size
            if len(rows) < page_size:
                break
        if final_page_full:
            return _error_envelope(
                security, "CNINFO IR", "ir", CNINFO_IR_QUESTION_URL,
                "pagination_limit", f"last retrieved page was full; max_pages={max_pages}",
                responses=responses, records=records, evidence_class_hint="company_statement_for_answers_only",
            )
        return _success_envelope(
            security, "CNINFO IR", "ir", CNINFO_IR_QUESTION_URL,
            records, responses, as_of=_max_date(records, "answered_at", "asked_at"), field_units={},
            evidence_class_hint="company_statement_for_answers_only", quality="complete",
            notes=["Investor questions are not facts. Company answers are company_statement, not verified outcomes."],
        )

    def news(self, ticker: str, *, page_size: int = 20, max_pages: int = 3) -> dict[str, Any]:
        security = SecurityId.parse(ticker)
        invalid_pagination = _pagination_error(page_size, max_pages)
        if invalid_pagination:
            return _error_envelope(
                security,
                "Eastmoney News",
                "news",
                EASTMONEY_NEWS_URL,
                "invalid_request",
                invalid_pagination,
                evidence_class_hint="news_lead_only",
            )
        responses: list[HttpResponse] = []
        records: list[dict[str, Any]] = []
        final_page_full = False
        for page in range(1, max_pages + 1):
            callback = "researchDataCallback"
            inner = {
                "uid": "", "keyword": security.code, "type": ["cmsArticleWebOld"],
                "client": "web", "clientType": "web", "clientVersion": "curr",
                "param": {"cmsArticleWebOld": {"searchScope": "default", "sort": "default", "pageIndex": page, "pageSize": page_size, "preTag": "", "postTag": ""}},
            }
            response, error = self._request(
                security, "Eastmoney News", "news", EASTMONEY_NEWS_URL,
                params={"cb": callback, "param": json.dumps(inner, ensure_ascii=False, separators=(",", ":"))},
                headers={"Referer": "https://so.eastmoney.com/"}, fixture_key=f"news:{page}",
            )
            if error:
                return _error_envelope(
                    security, "Eastmoney News", "news", EASTMONEY_NEWS_URL,
                    error["error_type"], error["error_message"], responses=responses + ([response] if response else []),
                    records=records, evidence_class_hint="news_lead_only",
                )
            assert response is not None
            responses.append(response)
            try:
                body = _jsonp_body(response)
                result = body.get("result") if isinstance(body, Mapping) else None
                if not isinstance(result, Mapping) or "cmsArticleWebOld" not in result:
                    raise ValueError("cmsArticleWebOld is missing; possible provider control response")
                rows = result.get("cmsArticleWebOld")
                if not isinstance(rows, list):
                    raise ValueError("cmsArticleWebOld is not a list")
            except (ValueError, json.JSONDecodeError) as exc:
                return _error_envelope(
                    security, "Eastmoney News", "news", EASTMONEY_NEWS_URL,
                    "schema_error", str(exc), responses=responses, records=records, evidence_class_hint="news_lead_only",
                )
            for item in rows:
                if not isinstance(item, Mapping):
                    return _error_envelope(
                        security,
                        "Eastmoney News",
                        "news",
                        EASTMONEY_NEWS_URL,
                        "schema_error",
                        "news row is not an object",
                        responses=responses,
                        records=records,
                        evidence_class_hint="news_lead_only",
                    )
                title = re.sub(
                    r"<[^>]+>", "", str(item.get("title") or "")
                ).strip()
                url = str(item.get("url") or "").strip()
                try:
                    if not title:
                        raise ValueError("news title is missing")
                    if not url:
                        raise ValueError("news URL is missing")
                    published_date = _require_iso_date(
                        item.get("date"), "news published date"
                    )
                except ValueError as exc:
                    return _error_envelope(
                        security,
                        "Eastmoney News",
                        "news",
                        EASTMONEY_NEWS_URL,
                        "schema_error",
                        str(exc),
                        responses=responses,
                        records=records,
                        evidence_class_hint="news_lead_only",
                    )
                records.append({
                    "title": title,
                    "snippet": re.sub(r"<[^>]+>", "", str(item.get("content") or ""))[:500],
                    "published_at": item.get("date"),
                    "published_date": published_date,
                    "media": item.get("mediaName"),
                    "url": url,
                    "official_recheck_required": True,
                    "evidence_note": "Lead only; classify by the original publisher and verify material claims.",
                })
            final_page_full = len(rows) >= page_size
            if len(rows) < page_size:
                break
        if final_page_full:
            return _error_envelope(
                security, "Eastmoney News", "news", EASTMONEY_NEWS_URL,
                "pagination_limit", f"last retrieved page was full; max_pages={max_pages}",
                responses=responses, records=records, evidence_class_hint="news_lead_only",
            )
        return _success_envelope(
            security, "Eastmoney News", "news", EASTMONEY_NEWS_URL,
            records, responses, as_of=_max_date(records, "published_at"), field_units={},
            evidence_class_hint="news_lead_only", quality="degraded",
            notes=["News search is discovery only and may contain opinions, rumors, duplicates, or irrelevant matches."],
        )


MODULE_ALIASES: dict[str, tuple[str, ...]] = {
    "d1": ("quote",),
    "d2": ("announcements", "lockups", "dividends", "holder_counts", "block_trades", "margin"),
    "d3": ("financial_filings", "financial_crosscheck", "consensus"),
    "d4": ("ir", "news"),
}
ALL_MODULES = tuple(dict.fromkeys(item for values in MODULE_ALIASES.values() for item in values))


def resolve_modules(values: str | Sequence[str]) -> list[str]:
    requested = [item.strip().lower() for item in (values.split(",") if isinstance(values, str) else values) if item.strip()]
    if not requested or "all" in requested:
        return list(ALL_MODULES)
    resolved: list[str] = []
    for item in requested:
        candidates = MODULE_ALIASES.get(item, (item,))
        for candidate in candidates:
            if candidate not in ALL_MODULES:
                raise ValueError(f"unknown module: {candidate}")
            if candidate not in resolved:
                resolved.append(candidate)
    return resolved


def build_snapshot(client: ResearchDataClient, ticker: str, modules: str | Sequence[str]) -> dict[str, Any]:
    security = SecurityId.parse(ticker)
    resolved = resolve_modules(modules)
    results = {name: getattr(client, name)(security.canonical) for name in resolved}
    return {
        "schema_version": SCHEMA_VERSION,
        "canonical_ticker": security.canonical,
        "generated_at": iso_utc(),
        "timezone": TIMEZONE_NAME,
        "modules": resolved,
        "results": results,
        "canonical_wiki_written": False,
    }


__all__ = [
    "ALL_MODULES", "CachingTransport", "FixtureTransport", "HttpResponse",
    "HttpTransport", "ResearchDataClient", "SecurityId", "TransportError",
    "UrllibTransport", "build_snapshot", "resolve_modules",
]
