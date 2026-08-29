import asyncio
from ..base_scanner import BaseScanner
from ...config import register_scanner

@register_scanner
class NIKScanner(BaseScanner):
    def __init__(self):
        super().__init__()
        self.category = "DATA_KEPENDUDUKAN"
        self.fields = [
            "NIK", "Nama_Lengkap", "Tempat_Lahir", "Tanggal_Lahir", "Jenis_Kelamin",
            "Alamat", "RT", "RW", "Kelurahan", "Kecamatan", "Kabupaten", "Provinsi",
            "Agama", "Status_Perkawinan", "Pekerjaan", "Kewarganegaraan",
            "Golongan_Darah", "Berlaku_Hingga", "Nama_Ibu", "Nama_Ayah"
        ]

    async def scan(self, nik: str) -> dict:
        from ...utils.validators import validate_nik
        valid, info = validate_nik(nik)
        if not valid:
            return {"error": "NIK tidak valid", "status": "INVALID"}
        return {
            "target": nik,
            "type": "NIK",
            "status": "FOUND",
            "fields": {
                "NIK": nik,
                "Prov_Kode": info.get("prov_kode", ""),
                "Kab_Kode": info.get("kab_kode", ""),
                "Kec_Kode": info.get("kec_kode", ""),
                "Tgl_Lahir_Extracted": info.get("tgl_lahir_raw", ""),
            },
            "confidence": "LOW",
            "note": "Data terbatas - ekstraksi dari format NIK"
        }
