from __future__ import annotations

from dataclasses import dataclass
from statistics import mean
from urllib.parse import urlparse


@dataclass(frozen=True)
class IterationLike:
    iteration_number: int
    gpt_output: str | None
    gem_output: str | None
    gpt_domain_mention: bool
    gem_domain_mention: bool
    gpt_brand_mention: bool
    gem_brand_mention: bool
    response_count: float | None
    brand_list: str | None
    citation_format: str | None


@dataclass(frozen=True)
class SentimentInput:
    provider: str
    iteration_number: int
    text: str
    mentioned: bool


def split_brand_variations(raw_brand: str | None) -> list[str]:
    seen: set[str] = set()
    variations: list[str] = []
    for chunk in (raw_brand or "").split(","):
        cleaned = chunk.strip()
        if not cleaned:
            continue
        lowered = cleaned.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        variations.append(cleaned)
    return variations


def normalize_domain_variations(raw_domain: str | None) -> list[str]:
    domain = (raw_domain or "").strip().lower()
    if not domain:
        return []

    prefixed = domain if "://" in domain else f"https://{domain}"
    parsed = urlparse(prefixed)
    host = (parsed.netloc or parsed.path).split("/")[0].strip().lower().rstrip("/")

    without_protocol = domain.split("://", 1)[-1].rstrip("/")
    without_www = without_protocol[4:] if without_protocol.startswith("www.") else without_protocol
    host_without_www = host[4:] if host.startswith("www.") else host

    candidates = [domain.rstrip("/"), without_protocol, without_www, host, host_without_www]

    result: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        cleaned = candidate.strip().lower().rstrip("/")
        if not cleaned or cleaned in seen:
            continue
        seen.add(cleaned)
        result.append(cleaned)
    return result


def _contains_any(text: str | None, variants: list[str]) -> bool:
    haystack = (text or "").lower()
    return any(variant in haystack for variant in variants if variant)


def detect_mentions(output_text: str | None, raw_domain: str | None, raw_brand: str | None) -> tuple[bool, bool]:
    domain_match = _contains_any(output_text, normalize_domain_variations(raw_domain))
    brand_match = _contains_any(output_text, [item.lower() for item in split_brand_variations(raw_brand)])
    return domain_match, brand_match


def merge_brand_lists(values: list[str | None]) -> str | None:
    seen: set[str] = set()
    merged: list[str] = []
    for value in values:
        for item in (value or "").split(","):
            cleaned = item.strip()
            if not cleaned:
                continue
            lowered = cleaned.lower()
            if lowered in seen:
                continue
            seen.add(lowered)
            merged.append(cleaned)
    return ", ".join(merged) if merged else None


def normalize_citation_format(value: str | None) -> str | None:
    categories: set[str] = set()
    saw_na = False

    for item in (value or "").split(","):
        cleaned = item.strip()
        if not cleaned:
            continue
        lowered = cleaned.lower()
        if lowered in {"n/a", "na", "none", "null"} or "n/a" in lowered:
            saw_na = True
            continue
        if any(token in lowered for token in ("url", "link", "http://", "https://", "www.")):
            categories.add("url")
            continue
        categories.add("text")

    ordered = [label for label in ("text", "url") if label in categories]
    if ordered:
        return ", ".join(ordered)
    if saw_na:
        return "N/A"
    return None


def merge_citation_formats(values: list[str | None]) -> str | None:
    categories: set[str] = set()
    saw_na = False

    for value in values:
        normalized = normalize_citation_format(value)
        if normalized == "N/A":
            saw_na = True
            continue
        for item in (normalized or "").split(","):
            cleaned = item.strip()
            if cleaned in {"text", "url"}:
                categories.add(cleaned)

    ordered = [label for label in ("text", "url") if label in categories]
    if ordered:
        return ", ".join(ordered)
    if saw_na:
        return "N/A"
    return None


def average_response_count(values: list[float | None]) -> float | None:
    actual = [value for value in values if value is not None]
    if not actual:
        return None
    return float(mean(actual))


def aggregate_outputs(outputs: list[IterationLike]) -> dict[str, object]:
    ordered = sorted(outputs, key=lambda item: item.iteration_number)
    return {
        "gpt_domain_mention": any(item.gpt_domain_mention for item in ordered),
        "gem_domain_mention": any(item.gem_domain_mention for item in ordered),
        "gpt_brand_mention": any(item.gpt_brand_mention for item in ordered),
        "gem_brand_mention": any(item.gem_brand_mention for item in ordered),
        "response_count_avg": average_response_count([item.response_count for item in ordered]),
        "brand_list": merge_brand_lists([item.brand_list for item in ordered]),
        "citation_format": merge_citation_formats([item.citation_format for item in ordered]),
    }


def select_sentiment_inputs(outputs: list[IterationLike], limit: int = 4) -> list[SentimentInput]:
    candidates: list[SentimentInput] = []
    for item in sorted(outputs, key=lambda row: row.iteration_number):
        if item.gpt_output:
            candidates.append(
                SentimentInput(
                    provider="gpt",
                    iteration_number=item.iteration_number,
                    text=item.gpt_output,
                    mentioned=bool(item.gpt_domain_mention or item.gpt_brand_mention),
                )
            )
        if item.gem_output:
            candidates.append(
                SentimentInput(
                    provider="gemini",
                    iteration_number=item.iteration_number,
                    text=item.gem_output,
                    mentioned=bool(item.gem_domain_mention or item.gem_brand_mention),
                )
            )

    mentioned = [candidate for candidate in candidates if candidate.mentioned]
    others = [candidate for candidate in candidates if not candidate.mentioned]
    return (mentioned + others)[:limit]


def drop_one_gpt_for_sentiment_retry(inputs: list[SentimentInput]) -> list[SentimentInput]:
    if len(inputs) <= 3:
        return list(inputs)

    reduced = list(inputs)
    for index, item in enumerate(reduced):
        if item.provider == "gpt":
            del reduced[index]
            return reduced[:3]
    return reduced[:3]
