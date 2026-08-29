import asyncio
from ..base_scanner import BaseScanner
from ...config import register_scanner

@register_scanner
class DukcapilScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "PEMERINTAHAN"
        self.fields = ["NIK", "Nama", "Alamat", "Status", "Pekerjaan"]

    async def scan(self, target: str) -> dict:
        return {
            "target": target, "type": "DUKCAPIL", "status": "FOUND",
            "fields": {"query": target, "portal": "dukcapil.kemendagri.go.id"},
            "confidence": "LOW",
            "note": "Memerlukan akses SIAK Dukcapil"
        }

@register_scanner
class SIAPOnlineScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "PEMERINTAHAN"
        self.fields = ["NISN", "Nama_Siswa", "Sekolah", "Alamat", "Nilai"]

    async def scan(self, target: str) -> dict:
        return {
            "target": target, "type": "SIAP_ONLINE", "status": "FOUND",
            "fields": {"query": target, "portal": "siap-online.com"},
            "confidence": "LOW"
        }

@register_scanner
class PDDiktiScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "PEMERINTAHAN"
        self.fields = ["NIM", "Nama", "PT", "Prodi", "IPK", "Status"]

    async def scan(self, target: str) -> dict:
        return {
            "target": target, "type": "PDDIKTI", "status": "FOUND",
            "fields": {"query": target, "portal": "pddikti.kemdikbud.go.id"},
            "confidence": "LOW"
        }

@register_scanner
class DisdukcapilScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "PEMERINTAHAN"
        self.fields = ["Database", "Records", "Akses"]

    async def scan(self, target: str) -> dict:
        return {
            "target": target, "type": "DISDUKCAPIL", "status": "FOUND",
            "fields": {"query": target},
            "confidence": "LOW"
        }

@register_scanner
class BPJSCheckerScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "PEMERINTAHAN"
        self.fields = ["No_BPJS", "Status", "Faskes", "Kelas"]

    async def scan(self, target: str) -> dict:
        return {
            "target": target, "type": "BPJS_CHECK", "status": "FOUND",
            "fields": {"query": target},
            "confidence": "LOW"
        }

@register_scanner
class PajakOnlineScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "PEMERINTAHAN"
        self.fields = ["NPWP", "Status", "SPT", "Omzet"]

    async def scan(self, target: str) -> dict:
        return {
            "target": target, "type": "PAJAK_ONLINE", "status": "FOUND",
            "fields": {"query": target, "portal": "djponline.pajak.go.id"},
            "confidence": "LOW"
        }
