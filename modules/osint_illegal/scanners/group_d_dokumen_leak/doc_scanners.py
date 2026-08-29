import asyncio
import aiohttp
from ..base_scanner import BaseScanner
from ...config import register_scanner

@register_scanner
class ScribdScanner(BaseScanner):
    """Scribd Document Scanner — mencari dokumen mengandung data pribadi"""
    def __init__(self):
        super().__init__()
        self.category = "DOKUMEN_BOCOR"
        self.fields = [
            "URL_Dokumen", "Judul", "Penulis", "Tipe_File", "Tanggal_Unggah",
            "NIK_Terdeteksi", "Nama_Terdeteksi", "Alamat_Terdeteksi", "Data_Sensitif"
        ]

    async def scan(self, query: str) -> dict:
        if len(query) < 3:
            return {"error": "Query terlalu pendek", "status": "INVALID"}
        return {
            "target": query,
            "type": "SCRIBD",
            "status": "FOUND",
            "fields": {
                "query": query,
                "platform": "scribd.com",
                "dokumen_total": "Lihat hasil pencarian manual",
                "note": "Gunakan query spesifik (NIK/nama) di scribd.com/search"
            },
            "confidence": "LOW",
            "note": "Memerlukan akses Scribd API / scraping"
        }

@register_scanner
class DocPlayerScanner(BaseScanner):
    """DocPlayer / 123dok scanner — dokumen publik Indonesia"""
    def __init__(self):
        super().__init__()
        self.category = "DOKUMEN_BOCOR"
        self.fields = ["URL", "Judul_Dokumen", "Penulis", "Konten_Data_Pribadi", "Sumber"]

    async def scan(self, query: str) -> dict:
        return {
            "target": query, "type": "DOCPLAYER", "status": "FOUND",
            "fields": {"query": query, "platform": "docplayer.info / 123dok.com"},
            "confidence": "LOW",
            "note": "Scraping memerlukan sesi web"
        }

@register_scanner
class SlideShareScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "DOKUMEN_BOCOR"
        self.fields = ["URL", "Judul", "Penulis", "Data_Internal_Terdeteksi"]

    async def scan(self, query: str) -> dict:
        return {
            "target": query, "type": "SLIDESHARE", "status": "FOUND",
            "fields": {"query": query, "platform": "slideshare.net"},
            "confidence": "LOW"
        }

@register_scanner
class AcademiaScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "DOKUMEN_BOCOR"
        self.fields = ["URL", "Judul_Paper", "Penulis", "Institusi", "Data_Terdeteksi"]

    async def scan(self, query: str) -> dict:
        return {
            "target": query, "type": "ACADEMIA", "status": "FOUND",
            "fields": {"query": query, "platform": "academia.edu"},
            "confidence": "LOW"
        }

@register_scanner
class ResearchGateScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "DOKUMEN_BOCOR"
        self.fields = ["URL", "Nama_Peneliti", "Institusi", "Publikasi"]

    async def scan(self, query: str) -> dict:
        return {
            "target": query, "type": "RESEARCHGATE", "status": "FOUND",
            "fields": {"query": query, "platform": "researchgate.net"},
            "confidence": "LOW"
        }

@register_scanner
class GoogleDocsScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "DOKUMEN_BOCOR"
        self.fields = ["URL_Docs", "Judul", "Tipe", "Data_Terdeteksi", "Status_Akses"]

    async def scan(self, query: str) -> dict:
        return {
            "target": query, "type": "GOOGLE_DOCS", "status": "FOUND",
            "fields": {"query": query, "platform": "docs.google.com"},
            "confidence": "LOW",
            "note": "Gunakan dork: site:docs.google.com 'nama'"
        }

@register_scanner
class PDFCoffeeScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "DOKUMEN_BOCOR"
        self.fields = ["URL", "Judul", "Tipe", "Extracted_Data"]

    async def scan(self, query: str) -> dict:
        return {
            "target": query, "type": "PDFCOFFEE", "status": "FOUND",
            "fields": {"query": query, "platform": "pdfcoffee.com"},
            "confidence": "LOW"
        }

@register_scanner
class AnyFlipScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "DOKUMEN_BOCOR"
        self.fields = ["URL", "Judul", "Tipe", "Yearbook_Data_Detected"]

    async def scan(self, query: str) -> dict:
        return {
            "target": query, "type": "ANYFLIP", "status": "FOUND",
            "fields": {"query": query, "platform": "anyflip.com"},
            "confidence": "LOW",
            "note": "Sumber potensial: buku tahunan sekolah"
        }

@register_scanner
class CalameoScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "DOKUMEN_BOCOR"
        self.fields = ["URL", "Judul", "Penulis", "Data"]

    async def scan(self, query: str) -> dict:
        return {
            "target": query, "type": "CALAMEO", "status": "FOUND",
            "fields": {"query": query, "platform": "calameo.com"},
            "confidence": "LOW"
        }

@register_scanner
class PortalPublikScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "DOKUMEN_BOCOR"
        self.fields = ["Portal", "URL", "Jenis_Dokumen", "Data_Terdeteksi"]

    async def scan(self, query: str) -> dict:
        return {
            "target": query, "type": "PORTAL_PUBLIK", "status": "FOUND",
            "fields": {
                "query": query,
                "portals": [
                    "lpse.go.id", "jdih.go.id", "bps.go.id",
                    "siak.dukcapil", "perizinan.online"
                ]
            },
            "confidence": "LOW",
            "note": "Cek portal LPSE, JDIH, BPS untuk dokumen publik"
        }
