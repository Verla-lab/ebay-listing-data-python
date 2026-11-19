from __future__ import annotations

from urllib.parse import urljoin

from bs4 import BeautifulSoup

from .models import AccessResult, ListingRecord

BASE_URL = "https://www.ebay.com"
VERIFICATION_MARKERS = (
    "security measure",
    "verify yourself",
    "verification challenge",
)
LOGIN_MARKERS = ("sign in to continue", "signin.ebay")


def classify_access(html: str) -> AccessResult:
    lowered = html.lower()
    if any(marker in lowered for marker in VERIFICATION_MARKERS):
        return AccessResult(
            status="verification_required",
            checkpoint="interactive_verification",
            retryable=False,
            manual_action_required=True,
        )
    if any(marker in lowered for marker in LOGIN_MARKERS):
        return AccessResult(
            status="verification_required",
            checkpoint="login_required",
            retryable=False,
            manual_action_required=True,
        )
    return AccessResult(status="ok")


def _text(element) -> str | None:
    if element is None:
        return None
    value = element.get_text(" ", strip=True)
    return value or None


def parse_listings(html: str, base_url: str = BASE_URL) -> list[ListingRecord]:
    access = classify_access(html)
    if access.status != "ok":
        return []

    soup = BeautifulSoup(html, "html.parser")
    listings: list[ListingRecord] = []

    for card in soup.select("li.s-item[data-item-id], article[data-item-id]"):
        item_id = (card.get("data-item-id") or "").strip() or None
        title = _text(card.select_one(".s-item__title, [data-field='title']"))
        if not title:
            continue

        link = card.select_one("a.s-item__link[href], a[data-field='url'][href]")
        href = link.get("href") if link else None
        url = urljoin(base_url, href) if href else None

        price = _text(card.select_one(".s-item__price, [data-field='price']"))
        condition = _text(card.select_one(".SECONDARY_INFO, [data-field='condition']"))
        shipping = _text(card.select_one(".s-item__shipping, [data-field='shipping']"))
        seller = _text(card.select_one(".s-item__seller-info-text, [data-field='seller']"))

        listings.append(
            ListingRecord(
                item_id=item_id,
                title=title,
                price=price,
                condition=condition,
                shipping=shipping,
                seller=seller,
                url=url,
            )
        )

    return listings
