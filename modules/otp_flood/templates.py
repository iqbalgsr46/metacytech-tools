"""
OTP Flood - Template Engine
Loads brand templates and generates OTP messages
"""

import json
import os
import random
import string

BRANDS_DIR = os.path.join(os.path.dirname(__file__), "brands")
CATEGORIES = {
    "bank": ["bca", "bni", "mandiri", "bri", "bsi"],
    "e-commerce": ["tokopedia", "shopee", "lazada", "bukalapak"],
    "social-media": ["facebook", "instagram", "twitter"],
    "streaming": ["netflix", "youtube"],
    "telecom": ["telkomsel"],
    "finance": ["gojek", "grab", "dana", "ovo", "linkaja"],
}
CATEGORY_LABELS = {
    "bank": "🏦 BANK",
    "e-commerce": "🛒 E-COMMERCE",
    "social-media": "📱 SOCIAL MEDIA",
    "streaming": "🎬 STREAMING",
    "telecom": "📡 TELECOM",
    "finance": "💰 FINANCE",
}


def _load_brand(brand_key):
    """Load a single brand JSON template."""
    path = os.path.join(BRANDS_DIR, f"{brand_key}.json")
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return None


def get_all_brands():
    """Return list of all available brand dicts."""
    brands = []
    for cat, keys in CATEGORIES.items():
        for key in keys:
            brand = _load_brand(key)
            if brand:
                brand["_key"] = key
                brands.append(brand)
    return brands


def get_brands_by_category(categories=None):
    """
    Return brands filtered by category list.
    If categories is None, return all brands.
    """
    all_brands = get_all_brands()
    if categories is None:
        return all_brands
    return [b for b in all_brands if b.get("category") in categories]


def generate_otp(format_str):
    """
    Generate OTP code based on format string.
    X = random digit, other chars preserved.
    """
    result = []
    for ch in format_str:
        if ch == "X":
            result.append(str(random.randint(0, 9)))
        else:
            result.append(ch)
    return "".join(result)


def compose_message(brand, otp_code, **kwargs):
    """Compose OTP message using brand template and variables."""
    template = brand.get("message_template", "")
    variables = {"OTP": otp_code}
    variables.update(kwargs)
    try:
        return string.Template(template).safe_substitute(variables)
    except Exception:
        return template.replace("${OTP}", otp_code)


def format_brand_message(brand, **kwargs):
    """Generate OTP and compose message in one call."""
    otp = generate_otp(brand.get("otp_format", "XXXXXX"))
    msg = compose_message(brand, otp, **kwargs)
    return {
        "brand": brand["brand_name"],
        "category": brand.get("category", "unknown"),
        "otp": otp,
        "message": msg,
        "sender": brand.get("sender_name", brand["brand_name"]),
    }
