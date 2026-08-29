"""Source registry for OSINT scanning"""
import json
import os

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

def load_platforms():
    path = os.path.join(DATA_DIR, "platform_list.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return ["github", "gitlab", "stackoverflow", "medium", "reddit"]

def load_wilayah():
    path = os.path.join(DATA_DIR, "kode_wilayah.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def load_breaches():
    path = os.path.join(DATA_DIR, "breach_signatures.json")
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {"breaches": [], "sources": []}

# Known document leak platforms
DOC_LEAK_PLATFORMS = [
    {"name": "Scribd", "url": "scribd.com", "type": "documents"},
    {"name": "DocPlayer", "url": "docplayer.info", "type": "documents"},
    {"name": "123dok", "url": "123dok.com", "type": "documents"},
    {"name": "SlideShare", "url": "slideshare.net", "type": "presentations"},
    {"name": "Academia", "url": "academia.edu", "type": "academic"},
    {"name": "ResearchGate", "url": "researchgate.net", "type": "academic"},
    {"name": "Google Docs", "url": "docs.google.com", "type": "spreadsheets"},
    {"name": "PDFCoffee", "url": "pdfcoffee.com", "type": "pdf"},
    {"name": "AnyFlip", "url": "anyflip.com", "type": "flipbook"},
    {"name": "Calaméo", "url": "calameo.com", "type": "publishing"},
]

# Known breach databases
BREACH_DATABASES = [
    "HaveIBeenPwned", "DeHashed", "IntelX", "LeakCheck",
    "SnusBase", "BreachDirectory", "LeakPeek", "ScatteredSecrets",
    "Firefox Monitor", "Google Dark Web Report"
]
