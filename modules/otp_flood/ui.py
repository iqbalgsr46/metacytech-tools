"""
OTP Flood - Terminal UI
3 Mode: WA (QR) | SMS (Alpha Sender) | TRIGGER (GRATIS - trigger brand beneran)
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from modules.otp_flood.profiles import PROFILES
from modules.otp_flood.templates import CATEGORIES
from modules.otp_flood.engine import run_flood


class C:
    RST = "\033[0m"
    B = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GRN = "\033[92m"
    YLW = "\033[93m"
    CYN = "\033[96m"
    MAG = "\033[35m"


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    cls()
    print(f"\n{C.B}{C.RED}  ╔══════════════════════════════════════════════════╗{C.RST}")
    print(f"{C.B}{C.RED}  ║         OTP FLOOD TESTING FRAMEWORK              ║{C.RST}")
    print(f"{C.B}{C.RED}  ╚══════════════════════════════════════════════════╝{C.RST}")
    print(f"{C.DIM}  Mode: Trigger ▸ SMS ▸ WhatsApp — Pilih sesuai kebutuhan{C.RST}\n")


def select_mode():
    print(f"  {C.B}Pilih mode pengiriman:{C.RST}\n")

    print(f"  {C.CYN}[1]{C.RST} {C.B}🔥 TRIGGER — GRATIS TOTAL (REKOMENDASI){C.RST}")
    print(f"  {C.DIM}     ✅ Target liat OTP dari brand ASLI (Tokopedia, Gojek, dll){C.RST}")
    print(f"  {C.DIM}     ✅ Nomor lo AMAN — gak kelihatan{C.RST}")
    print(f"  {C.DIM}     ✅ GRATIS — gak perlu API key / QR scan{C.RST}")
    print(f"  {C.DIM}     ✅ Tinggal masukin nomor → gas{C.RST}\n")

    print(f"  {C.CYN}[2]{C.RST} {C.B}📡 SMS — Alpha Sender ID{C.RST}")
    print(f"  {C.DIM}     Muncul sebagai nama brand, tapi perlu API key SMS{C.RST}\n")

    print(f"  {C.CYN}[3]{C.RST} {C.B}💬 WhatsApp — Baileys (QR Scan){C.RST}")
    print(f"  {C.DIM}     Nomor lo kelihatan, perlu QR scan.{C.RST}\n")

    while True:
        print(f"  {C.CYN}Pilih (1/2/3): {C.RST}", end="")
        ch = input().strip()
        if ch == "1":
            return "trigger"
        elif ch == "2":
            from modules.otp_flood.sender_sms import SMSSender
            test = SMSSender("0")
            if not test.api_url:
                print(f"\n  {C.YLW}Konfigurasi SMS dulu.{C.RST}\n")
                configure_sms_api()
            return "sms"
        elif ch == "3":
            return "wa"
        print(f"  {C.RED}1, 2, atau 3.{C.RST}")


def configure_sms_api():
    print(f"  {C.DIM}Provider: MedanPedia, Vonage, Twilio, atau kustom{C.RST}\n")
    val = input(f"  SMS API URL [default: https://mdpedia.com/api/sms.php]: ").strip()
    os.environ["SMS_API_URL"] = val or "https://mdpedia.com/api/sms.php"
    val = input(f"  API Key / Token: ").strip()
    if val: os.environ["SMS_API_KEY"] = val
    val = input(f"  Username (jika perlu): ").strip()
    if val: os.environ["SMS_USERNAME"] = val
    print(f"\n  {C.GRN}✅ OK{C.RST}\n")


def input_target():
    while True:
        print(f"  Masukkan nomor HP target:")
        print(f"  {C.DIM}  (dengan kode negara, contoh: 6281234567890){C.RST}\n")
        print(f"  {C.CYN}Nomor target: {C.RST}", end="")
        val = input().strip()
        if val.lower() == "q":
            return None
        if not val.isdigit():
            print(f"  {C.RED}Hanya angka!{C.RST}\n")
            continue
        if len(val) < 10:
            print(f"  {C.RED}Min 10 digit.{C.RST}\n")
            continue
        print(f"  {C.GRN}✓ Target: {val}{C.RST}\n")
        return val


def select_profile():
    print(f"  {C.B}Pilih profile serangan:{C.RST}\n")
    keys = list(PROFILES.keys())
    for i, key in enumerate(keys, 1):
        p = PROFILES[key]
        print(f"  {C.CYN}[{i}]{C.RST} {C.B}{p['name']}{C.RST}")
        print(f"  {C.DIM}     {p['description']}{C.RST}\n")

    while True:
        print(f"  {C.CYN}Pilih (1-{len(keys)}): {C.RST}", end="")
        try:
            ch = input().strip()
            if ch.lower() == "q":
                return None
            idx = int(ch) - 1
            if 0 <= idx < len(keys):
                return keys[idx]
        except ValueError:
            pass
        print(f"  {C.RED}Tidak valid.{C.RST}")


def configure_params(profile_key):
    params = dict(PROFILES[profile_key]["default_params"])
    print(f"\n  {C.B}Konfigurasi:{C.RST}\n")
    print(f"  {C.DIM}1-2dtk = kenceng | 3-5 = medium | 6-10 = slow{C.RST}\n")

    while True:
        val = input(f"  Interval antar trigger (dtk) [default: 3]: ").strip()
        params["interval"] = float(val) if val else 3
        break

    while True:
        val = input(f"  Total maksimal trigger [default: 50]: ").strip()
        params["max_messages"] = int(val) if val else 50
        break

    while True:
        val = input(f"  Cooldown kalo kena block (dtk) [default: 30]: ").strip()
        params["block_cooldown"] = int(val) if val else 30
        break

    return params


def select_categories():
    """Untuk trigger mode: pilih brand"""
    # For simplicity, just return all
    return None


def show_confirm(config):
    profile = PROFILES[config["profile"]]
    interval = config.get("interval", 3)
    max_msgs = config.get("max_messages", 50)
    estimated = max(1, int((max_msgs * interval) / 60))

    if config["mode"] == "trigger":
        from modules.otp_flood.sender_trigger import OTPTrigger
        s = OTPTrigger("0")
        total_brands = len(s.BRANDS)
        mode_label = f"{C.GRN}🔥 TRIGGER (GRATIS){C.RST}"
    elif config["mode"] == "sms":
        total_brands = "SMS Gateway"
        mode_label = f"{C.MAG}📡 SMS Alpha Sender{C.RST}"
    else:
        total_brands = "WhatsApp"
        mode_label = f"{C.CYN}💬 WhatsApp QR{C.RST}"

    print(f"\n  {C.B}{C.CYN}  ╔═══════════════════════════════════════════╗{C.RST}")
    print(f"  {C.B}{C.CYN}  ║       KONFIRMASI                          ║{C.RST}")
    print(f"  {C.B}{C.CYN}  ╚═══════════════════════════════════════════╝{C.RST}\n")
    print(f"  {C.B}Mode   :{C.RST} {mode_label}")
    print(f"  {C.B}Target :{C.RST} {config['target']}")
    print(f"  {C.B}Profile:{C.RST} {profile['name']}")
    print(f"  {C.B}Rate   :{C.RST} 1 trigger/{interval}s")
    print(f"  {C.B}Total  :{C.RST} {max_msgs}x trigger")
    print(f"  {C.B}Brand  :{C.RST} {total_brands} endpoint publik")
    print(f"  {C.B}Estimasi:{C.RST} ~{estimated} menit\n")

    if config["mode"] == "trigger":
        print(f"  {C.GRN}🎯 TARGET akan nerima OTP dari brand ASLI.{C.RST}")
        print(f"  {C.GRN}🔒 Nomor lo TIDAK kelihatan.{C.RST}")
        print(f"  {C.GRN}💰 GRATIS TOTAL.{C.RST}\n")

    while True:
        print(f"  {C.CYN}Gas? (Y/n): {C.RST}", end="")
        ch = input().strip().lower()
        if ch in ("y", ""):
            return True
        elif ch == "n":
            return False
        print(f"  {C.RED}Y/n aja.{C.RST}")


def execute_flood(config):
    print(f"\n  {C.B}{C.CYN}  ╔═══════════════════════════════════════════╗{C.RST}")
    print(f"  {C.B}{C.CYN}  ║       OTP FLOOD - RUNNING                  ║{C.RST}")
    print(f"  {C.B}{C.CYN}  ╚═══════════════════════════════════════════╝{C.RST}\n")

    for output in run_flood(config):
        sys.stdout.write(output)
        sys.stdout.flush()


def otp_flood_menu():
    print_header()
    mode = select_mode()

    print_header()
    target = input_target()
    if target is None:
        return

    print_header()
    profile = select_profile()
    if profile is None:
        return

    print_header()
    params = configure_params(profile)

    print_header()
    categories = select_categories()

    config = {
        "mode": mode,
        "target": target,
        "profile": profile,
        **params,
        "categories": categories,
    }

    print_header()
    if not show_confirm(config):
        print(f"\n  {C.YLW}Batal.{C.RST}\n")
        return

    execute_flood(config)

    print(f"\n  {C.CYN}[1]{C.RST} Ulangi")
    print(f"  {C.CYN}[2]{C.RST} Menu utama")
    print(f"  {C.CYN}[3]{C.RST} Keluar\n")

    while True:
        print(f"  {C.CYN}Pilih: {C.RST}", end="")
        ch = input().strip()
        if ch == "1":
            return otp_flood_menu()
        elif ch == "2":
            return
        elif ch == "3":
            sys.exit(0)
        print(f"  {C.RED}Tidak valid.{C.RST}")
