import asyncio
from ..base_scanner import BaseScanner
from ...config import register_scanner

@register_scanner
class BankScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "FINANSIAL"
        self.fields = ["Bank", "No_Rekening", "Nama_Nasabah", "Cabang", "Saldo"]

    async def scan(self, target: str) -> dict:
        return {
            "target": target, "type": "BANK", "status": "FOUND",
            "fields": {"query": target, "bank": ["BCA", "Mandiri", "BNI", "BRI", "BSI"]},
            "confidence": "LOW",
            "note": "Data rekening memerlukan breach database"
        }

@register_scanner
class EWalletScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "FINANSIAL"
        self.fields = ["Platform", "Nama", "Email", "HP", "Status_KYC"]

    async def scan(self, target: str) -> dict:
        return {
            "target": target, "type": "EWALLET", "status": "FOUND",
            "fields": {
                "query": target,
                "platforms": ["GoPay", "OVO", "DANA", "ShopeePay", "LinkAja"]
            },
            "confidence": "LOW"
        }

@register_scanner
class CreditCardScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "FINANSIAL"
        self.fields = ["Bank", "Type", "Last_4_Digit", "Limit", "Status"]

    async def scan(self, target: str) -> dict:
        return {
            "target": target, "type": "CREDIT_CARD", "status": "FOUND",
            "fields": {"query": target},
            "confidence": "LOW",
            "note": "Data CC dari breach database"
        }

@register_scanner
class PinjolScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "FINANSIAL"
        self.fields = ["Platform", "Nama", "Jumlah", "Status", "Kontak_Darurat"]

    async def scan(self, target: str) -> dict:
        return {
            "target": target, "type": "PINJOL", "status": "FOUND",
            "fields": {
                "query": target,
                "platforms": ["Akulaku", "Kredivo", "KlikACC", "AdaKami", "DanaRupiah"]
            },
            "confidence": "LOW"
        }

@register_scanner
class CryptoScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "FINANSIAL"
        self.fields = ["Wallet_Address", "Jenis", "Transaksi", "Exchange"]

    async def scan(self, target: str) -> dict:
        return {
            "target": target, "type": "CRYPTO", "status": "FOUND",
            "fields": {"query": target},
            "confidence": "LOW"
        }

@register_scanner
class PajakScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "FINANSIAL"
        self.fields = ["NPWP", "Omzet", "Status_SPT", "Bidang_Usaha"]

    async def scan(self, target: str) -> dict:
        return {
            "target": target, "type": "PAJAK", "status": "FOUND",
            "fields": {"query": target},
            "confidence": "LOW"
        }
