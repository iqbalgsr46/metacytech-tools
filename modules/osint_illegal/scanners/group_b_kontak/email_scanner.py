import asyncio
from ..base_scanner import BaseScanner
from ...config import register_scanner

@register_scanner
class EmailScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "KONTAK"
        self.fields = [
            "Email", "Provider", "Platform_Terdaftar", "Nama_Terkait",
            "Breach_History", "Password_Hash_Bocor"
        ]

    async def scan(self, email: str) -> dict:
        from ...utils.validators import validate_email
        if not validate_email(email):
            return {"error": "Email tidak valid", "status": "INVALID"}
        
        provider = email.split("@")[1] if "@" in email else ""
        
        return {
            "target": email,
            "type": "EMAIL",
            "status": "FOUND",
            "fields": {
                "Email": email,
                "Provider": provider,
            },
            "confidence": "LOW",
            "note": "Gunakan mode deep scan untuk cek breach history"
        }
