import asyncio
from ..base_scanner import BaseScanner
from ...config import register_scanner

@register_scanner
class PhoneScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "KONTAK"
        self.fields = [
            "Nomor_HP", "Operator", "Provider", "Jenis", "WhatsApp_Registered",
            "Telegram_Registered", "Ecommerce_Accounts", "Breach_History"
        ]

    async def scan(self, phone: str) -> dict:
        from ...utils.validators import validate_phone
        valid, clean = validate_phone(phone)
        if not valid:
            return {"error": "Nomor HP tidak valid", "status": "INVALID"}
            
        results = {"target": clean, "type": "PHONE", "status": "FOUND", "fields": {}}
        
        # Operator detection via prefix
        prefix = clean[:5]
        if prefix[:4] in ["0811", "0812", "0813", "0821", "0822", "0823", "0851", "0852", "0853", "0881", "0882", "0883", "0884", "0885", "0886", "0887", "0888", "0889"]:
            results["fields"]["Operator"] = "Telkomsel"
            results["fields"]["Provider"] = "Telkomsel (Halo/SimPATI/KartuHalo)"
        elif prefix[:4] in ["0814", "0815", "0816", "0855", "0856", "0857", "0858"]:
            results["fields"]["Operator"] = "Indosat Ooredoo Hutchison"
            results["fields"]["Provider"] = "IM3/3 (Tri)"
        elif prefix[:4] in ["0817", "0818", "0819", "0859", "0877", "0878", "0879"]:
            results["fields"]["Operator"] = "XL Axiata"
            results["fields"]["Provider"] = "XL Prabayar/Pascabayar"
        elif prefix[:4] in ["0895", "0896", "0897", "0898", "0899"]:
            results["fields"]["Operator"] = "Smartfren"
        else:
            results["fields"]["Operator"] = "Unknown/Lainnya"
        
        return results
