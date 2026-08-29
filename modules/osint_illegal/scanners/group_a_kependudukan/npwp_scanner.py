import asyncio
from ..base_scanner import BaseScanner
from ...config import register_scanner

@register_scanner
class NPWPScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "DATA_KEPENDUDUKAN"
        self.fields = [
            "NPWP", "Nama_Wajib_Pajak", "Alamat", "Status_PKP",
            "KPP_Terdaftar", "Tanggal_Terdaftar", "Bidang_Usaha"
        ]

    async def scan(self, npwp: str) -> dict:
        from ...utils.validators import validate_npwp
        if not validate_npwp(npwp):
            return {"error": "NPWP tidak valid", "status": "INVALID"}
        return {
            "target": npwp,
            "type": "NPWP",
            "status": "FOUND",
            "fields": {"NPWP": npwp, "format": "valid"},
            "confidence": "LOW",
            "note": "Data wajib pajak memerlukan akses DJP online"
        }
