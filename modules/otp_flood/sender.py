"""
OTP Flood - Message Sender
Handles WhatsApp message sending interface
"""

import time
import random
import urllib.request
import urllib.parse
import json as json_lib
import os


class Sender:
    """
    WhatsApp message sender.
    Currently uses simulated responses for framework validation.
    Extend with real WhatsApp Business API / third-party integration.
    """

    def __init__(self, target_number):
        self.target = target_number
        self.sent_count = 0
        self.block_count = 0
        self.api_key = os.environ.get("WA_API_KEY", "")

    def send(self, message, sender_name=""):
        """
        Attempt to send a message.
        Returns dict with status, code, and message.
        """
        # Simulated rate limit detection
        # In production, this would call actual WhatsApp API
        time.sleep(0.1)  # simulate network latency

        self.sent_count += 1

        # Simulate occasional blocking (5% chance)
        if random.random() < 0.05:
            self.block_count += 1
            return {
                "status": "blocked",
                "code": 429,
                "message": "Rate limited by provider",
                "sent": False,
            }

        return {
            "status": "sent",
            "code": 200,
            "message": "Message sent successfully",
            "sent": True,
        }

    def send_via_api(self, message, sender_name=""):
        """
        Send via configured WhatsApp API endpoint.
        Configurable through environment variables.
        """
        api_url = os.environ.get("WA_API_URL", "")
        if not api_url:
            return self.send(message, sender_name)

        try:
            payload = json_lib.dumps(
                {
                    "phone": self.target,
                    "message": message,
                    "sender": sender_name,
                }
            ).encode("utf-8")

            req = urllib.request.Request(
                api_url,
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json_lib.loads(resp.read())
                self.sent_count += 1
                return {
                    "status": "sent",
                    "code": resp.getcode(),
                    "message": data.get("message", "Sent"),
                    "sent": True,
                }
        except Exception as e:
            return {
                "status": "error",
                "code": 0,
                "message": str(e),
                "sent": False,
            }

    def get_stats(self):
        """Return current sender statistics."""
        return {
            "target": self.target,
            "sent": self.sent_count,
            "blocked": self.block_count,
        }
