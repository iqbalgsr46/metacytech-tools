"""
OTP Flood - Attack Profiles
Defines attack timing profiles and pattern generators
"""

import random
import time
import math


def linear_generator(interval=3):
    """Yield constant wait times."""
    while True:
        yield interval


def exponential_generator(base=1, multiplier=1.5, max_rate=10):
    """Yield progressively shorter wait times (exponential ramp-up)."""
    current = base
    while True:
        yield current
        current = max(max_rate, current * multiplier)


def random_burst_generator(min_interval=1, max_interval=10):
    """Yield random wait times within range (human-like)."""
    while True:
        yield random.uniform(min_interval, max_interval)


PROFILES = {
    "linear": {
        "name": "LINEAR FLOOD",
        "description": "Konstan tiap X detik — test rate limiting dasar",
        "generator": linear_generator,
        "default_params": {"interval": 3},
    },
    "exponential": {
        "name": "EXPONENTIAL BURST",
        "description": "Makin lama makin cepat — test threshold detection",
        "generator": exponential_generator,
        "default_params": {"base": 1, "multiplier": 1.5, "max_rate": 0.5},
    },
    "random": {
        "name": "RANDOM BURST",
        "description": "Timing acak 1-10 detik — test behavioral detection",
        "generator": random_burst_generator,
        "default_params": {"min_interval": 1, "max_interval": 10},
    },
    "rotating": {
        "name": "ROTATING BRAND",
        "description": "Ganti brand tiap pesan dari 18 brand — test multi-vector",
        "generator": linear_generator,
        "default_params": {"interval": 4},
        "rotate_brand": True,
    },
}


def get_generator(profile_key, params=None):
    """Get a timing generator for the given profile."""
    profile = PROFILES.get(profile_key)
    if not profile:
        return None

    gen_params = dict(profile["default_params"])
    if params:
        gen_params.update(params)

    return profile["generator"](**gen_params)


def describe_profile(profile_key):
    """Return formatted profile description string."""
    p = PROFILES.get(profile_key)
    if not p:
        return ""
    return f"[{profile_key.upper()}] {p['name']} — {p['description']}"
