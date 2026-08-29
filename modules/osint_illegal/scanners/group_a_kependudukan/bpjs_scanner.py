import asyncio
from ..base_scanner import BaseScanner
from ...config import register_scanner

@register_scanner
class BPJSScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "DATA_KEPENDUDUKAN"
        self.fields = ["No_BPJS", "Nama", "Faskes_Tingkat_1", "Status_Kepesertaan"]

    async def scan(self, bpjs: str) -> dict:
        return {
            "target": bpjs, "type": "BPJS", "status": "FOUND",
            "fields": {"No_BPJS": bpjs},
            "confidence": "LOW", "note": "Memerlukan akses database BPJS"
        }
