import os
import sys

MODULE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(MODULE_DIR, "data")
RESULTS_DIR = os.path.join(MODULE_DIR, "..", "results", "osint_export")

if not os.path.exists(RESULTS_DIR):
    try:
        os.makedirs(RESULTS_DIR, exist_ok=True)
    except Exception:
        RESULTS_DIR = os.path.join(os.path.expanduser("~"), "osint_export")
        os.makedirs(RESULTS_DIR, exist_ok=True)

# ANSI Colors
class C:
    RST = "\033[0m"
    B = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GRN = "\033[92m"
    YLW = "\033[93m"
    BLU = "\033[94m"
    MAG = "\033[35m"
    CYN = "\033[96m"

# Scanner configurations
TIMEOUTS = {
    "fast": 10,
    "medium": 30,
    "slow": 60,
    "scraping": 90
}

SCANNER_REGISTRY = {}

def register_scanner(cls):
    SCANNER_REGISTRY[cls.__name__] = cls
    return cls
