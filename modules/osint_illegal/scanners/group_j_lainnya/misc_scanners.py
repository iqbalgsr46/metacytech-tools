import asyncio
from ..base_scanner import BaseScanner
from ...config import register_scanner

@register_scanner
class UsernameScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "LAINNYA"
        self.fields = ["Username", "Platform_Ditemukan", "Profile_URL", "Bio"]

    async def scan(self, username: str) -> dict:
        if len(username) < 2:
            return {"error": "Username terlalu pendek", "status": "INVALID"}
        
        platforms = [
            "instagram.com", "twitter.com", "tiktok.com", "facebook.com",
            "github.com", "medium.com", "reddit.com", "telegram.org",
            "linkedin.com", "youtube.com", "twitch.tv", "discord.com",
            "pinterest.com", "tumblr.com", "snapchat.com", "flickr.com"
        ]
        
        return {
            "target": username,
            "type": "USERNAME",
            "status": "FOUND",
            "fields": {
                "username": username,
                "platforms_to_check": platforms,
                "total_platforms": len(platforms)
            },
            "confidence": "LOW",
            "note": "Gunakan tools seperti Sherlock / Maigret untuk cek otomatis"
        }

@register_scanner
class ImageScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "LAINNYA"
        self.fields = ["Image_URL", "Sumber_Ditemukan", "EXIF_Data", "Similar_Images"]

    async def scan(self, image_url: str) -> dict:
        return {
            "target": image_url, "type": "REVERSE_IMAGE", "status": "FOUND",
            "fields": {"url": image_url, "engines": ["Google Images", "Yandex", "TinEye"]},
            "confidence": "LOW"
        }

@register_scanner
class DomainScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "LAINNYA"
        self.fields = ["Domain", "Pemilik", "Registrar", "Tanggal_Daftar", "IP"]

    async def scan(self, domain: str) -> dict:
        return {
            "target": domain, "type": "DOMAIN", "status": "FOUND",
            "fields": {"domain": domain},
            "confidence": "LOW",
            "note": "Gunakan WHOIS lookup"
        }

@register_scanner
class IPScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "LAINNYA"
        self.fields = ["IP", "ISP", "Lokasi", "Hostname", "DNS"]

    async def scan(self, ip: str) -> dict:
        return {
            "target": ip, "type": "IP", "status": "FOUND",
            "fields": {"ip": ip},
            "confidence": "LOW"
        }

@register_scanner
class DeviceScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "LAINNYA"
        self.fields = ["User_Agent", "OS", "Browser", "Device"]

    async def scan(self, ua: str) -> dict:
        return {
            "target": ua[:50], "type": "DEVICE", "status": "FOUND",
            "fields": {"ua": ua[:100]},
            "confidence": "MEDIUM"
        }
