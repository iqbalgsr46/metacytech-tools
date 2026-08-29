import asyncio
from ..base_scanner import BaseScanner
from ...config import register_scanner

@register_scanner
class GitHubScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "PLATFORM"
        self.fields = ["Username", "Repositori", "Email_Bocor", "Credential_Detected", "Bio"]

    async def scan(self, target: str) -> dict:
        return {
            "target": target, "type": "GITHUB", "status": "FOUND",
            "fields": {"query": target, "platform": "github.com"},
            "confidence": "LOW",
            "note": "Gunakan GitHub API + dork untuk cari credentials bocor"
        }

@register_scanner
class StackOverflowScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "PLATFORM"
        self.fields = ["User_ID", "Nama", "Reputation", "Tags"]

    async def scan(self, target: str) -> dict:
        return {
            "target": target, "type": "STACKOVERFLOW", "status": "FOUND",
            "fields": {"query": target, "platform": "stackoverflow.com"},
            "confidence": "LOW"
        }

@register_scanner
class MediumScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "PLATFORM"
        self.fields = ["Username", "Bio", "Artikel", "Email"]

    async def scan(self, target: str) -> dict:
        return {
            "target": target, "type": "MEDIUM", "status": "FOUND",
            "fields": {"query": target, "platform": "medium.com"},
            "confidence": "LOW"
        }

@register_scanner
class KaskusScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "PLATFORM"
        self.fields = ["Username", "Posts", "Threads", "Join_Date"]

    async def scan(self, target: str) -> dict:
        return {
            "target": target, "type": "KASKUS", "status": "FOUND",
            "fields": {"query": target, "platform": "kaskus.co.id"},
            "confidence": "LOW"
        }

@register_scanner
class RedditScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "PLATFORM"
        self.fields = ["Username", "Karma", "Posts", "Comments", "Subreddits"]

    async def scan(self, target: str) -> dict:
        return {
            "target": target, "type": "REDDIT", "status": "FOUND",
            "fields": {"query": target, "platform": "reddit.com"},
            "confidence": "LOW"
        }

@register_scanner
class QuoraScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "PLATFORM"
        self.fields = ["Username", "Bio", "Answers", "Topics"]

    async def scan(self, target: str) -> dict:
        return {
            "target": target, "type": "QUORA", "status": "FOUND",
            "fields": {"query": target, "platform": "quora.com"},
            "confidence": "LOW"
        }

@register_scanner
class ForumScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "PLATFORM"
        self.fields = ["Forum", "Username", "Posts", "Profile_URL"]

    async def scan(self, target: str) -> dict:
        return {
            "target": target, "type": "FORUM", "status": "FOUND",
            "fields": {"query": target, "forums": ["kaskus", "reddit", "quora"]},
            "confidence": "LOW"
        }

@register_scanner
class BlogScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "PLATFORM"
        self.fields = ["Blog_URL", "Penulis", "Bio", "Konten"]

    async def scan(self, target: str) -> dict:
        return {
            "target": target, "type": "BLOG", "status": "FOUND",
            "fields": {"query": target},
            "confidence": "LOW"
        }
