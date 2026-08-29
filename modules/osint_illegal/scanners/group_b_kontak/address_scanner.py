import asyncio
from ..base_scanner import BaseScanner
from ...config import register_scanner

@register_scanner
class AddressScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "KONTAK"
        self.fields = ["Alamat_Lengkap", "RT", "RW", "Kelurahan", "Kecamatan", "Kabupaten", "Provinsi", "Kode_Pos"]

    async def scan(self, address: str) -> dict:
        if len(address) < 10:
            return {"error": "Alamat terlalu pendek", "status": "INVALID"}
        return {
            "target": address,
            "type": "ADDRESS",
            "status": "FOUND",
            "fields": {"Alamat": address[:100]},
            "confidence": "MEDIUM"
        }
