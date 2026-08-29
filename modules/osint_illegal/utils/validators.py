import re

def validate_nik(nik: str) -> tuple:
    if not nik or not re.match(r"^\d{16}$", nik):
        return False, {}
    info = {
        "prov_kode": nik[0:2],
        "kab_kode": nik[2:4],
        "kec_kode": nik[4:6],
        "tgl_lahir_raw": f"{nik[6:8]}-{nik[8:10]}-{nik[10:12]}",
    }
    return True, info

def validate_kk(kk: str) -> bool:
    return bool(kk and re.match(r"^\d{16}$", kk))

def validate_npwp(npwp: str) -> bool:
    clean = re.sub(r"\D", "", npwp)
    return bool(clean and len(clean) in [15, 16])

def validate_phone(phone: str) -> tuple:
    clean = re.sub(r"\D", "", phone)
    if clean.startswith("62"):
        clean = "0" + clean[2:]
    if not clean.startswith("0"):
        clean = "0" + clean
    valid = bool(re.match(r"^08\d{8,11}$", clean))
    return valid, clean

def validate_email(email: str) -> bool:
    return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))
