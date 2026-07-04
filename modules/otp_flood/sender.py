"""
OTP Flood - Message Sender (Real WhatsApp)
Bridges Python to Node.js Baileys for actual message delivery
No browser needed — pure WhatsApp Web API implementation
"""

import subprocess
import os
import sys
import time


class Sender:
    """
    WhatsApp message sender using @whiskeysockets/baileys.
    First launch displays QR code — scan with WhatsApp to authenticate.
    Session saved locally in .auth_session folder.
    """

    def __init__(self, target_number):
        self.target = target_number
        self.sent_count = 0
        self.block_count = 0
        self.error_count = 0
        self._node_script = os.path.join(
            os.path.dirname(__file__), "sender_wa.js"
        )
        self._ready = False

    def send(self, message, sender_name=""):
        """Send real WhatsApp message via Node.js Baileys bridge."""
        try:
            result = self._call_node(message, sender_name)
            status = result.get("status", "error")

            if status == "sent":
                self.sent_count += 1
                if not self._ready:
                    self._ready = True
                return {
                    "status": "sent",
                    "code": 200,
                    "message": "Delivered via WhatsApp",
                    "sent": True,
                }
            elif status == "blocked":
                self.block_count += 1
                return {
                    "status": "blocked",
                    "code": 429,
                    "message": "Rate limited by WhatsApp",
                    "sent": False,
                }
            else:
                self.error_count += 1
                if status == "auth_fail":
                    self._ready = False
                return {
                    "status": "error",
                    "code": 0,
                    "message": result.get("error", "Unknown error"),
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

    def _call_node(self, message, sender_name):
        """Execute Node.js Baileys sender and parse output."""
        env = os.environ.copy()

        proc = subprocess.Popen(
            [
                "node",
                self._node_script,
                self.target,
                message,
                sender_name or "System",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
            cwd=os.path.dirname(self._node_script),
        )

        # Timeout: 120s for first run (QR), 30s for subsequent
        timeout = 120 if not self._ready else 30
        start = time.time()

        result = {"status": "error", "error": "No output"}

        for line in iter(proc.stdout.readline, ""):
            line = line.strip()
            if not line:
                continue

            # QR code detection
            if line.startswith("�") or "█" in line or "▄" in line or "▀" in line:
                print(f"  {line}")
                continue

            # QR instructions
            if "SCAN QR" in line or "QR CODE" in line:
                print(f"\n  ⚠️  {line}")
                continue

            if "Linked Devices" in line or "titik 3" in line:
                print(f"  {line}")
                continue

            # Parse status messages
            if line.startswith("SENT:"):
                result = {"status": "sent", "id": line[5:].strip()}
                self._ready = True
            elif line == "BLOCKED: Rate limited":
                result = {"status": "blocked"}
            elif line.startswith("ERR: Number not on WhatsApp"):
                result = {"status": "error", "error": "Nomor tidak terdaftar WhatsApp"}
            elif line.startswith("ERR:"):
                result = {"status": "error", "error": line[4:].strip()}
            elif line.startswith("AUTH_FAIL:"):
                result = {"status": "auth_fail", "error": line[10:].strip()}
                self._ready = False
                print(f"\n  {_color.RED}⚠️  Session expired! Scan QR lagi.{_color.RST}\n")
            elif line.startswith("DISCONNECTED:"):
                if "LOGGED_OUT" in line:
                    self._ready = False
            elif line.startswith("TIMEOUT:"):
                result = {"status": "error", "error": "Timeout"}
            elif line.startswith("INIT_ERR:"):
                result = {"status": "error", "error": line[9:].strip()}

            # Check timeout
            if time.time() - start > timeout:
                proc.kill()
                result = {"status": "error", "error": "Process timeout"}
                break

        proc.wait(timeout=5)
        return result

    def get_stats(self):
        """Return current sender statistics."""
        return {
            "target": self.target,
            "sent": self.sent_count,
            "blocked": self.block_count,
        }


class _color:
    RST = "\033[0m"
    YLW = "\033[93m"
    GRN = "\033[92m"
    RED = "\033[91m"
