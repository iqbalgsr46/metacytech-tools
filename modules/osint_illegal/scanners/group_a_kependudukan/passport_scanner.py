import asyncio
from ..base_scanner import BaseScanner
from ...config import register_scanner

@register_scanner
class PassportScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "DATA_KEPENDUDUKAN"
        self.fields = ["No_Paspor", "Nama", "Kewarganegaraan", "Tgl_Terbit", "Tgl_Expired"]

    async def scan(self, passport: str) -> dict:
        return {
            "target": passport, "type": "PASPOR", "status": "FOUND",
            "fields": {"No_Paspor": passport},
            "confidence": "LOW", "note": "Full data memerlukan akses imigrasi"
        }
