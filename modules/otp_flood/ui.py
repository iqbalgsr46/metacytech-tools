"""
OTP Flood - Terminal UI
Interactive menu for OTP flood testing
"""

import os
import sys
import time
from datetime import datetime

# Ensure modules path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from modules.otp_flood.profiles import PROFILES, describe_profile
from modules.otp_flood.templates import CATEGORIES
from modules.otp_flood.engine import run_flood


# ANSI colors (matching launcher style)
class C:
    RST = "\033[0m"
    B = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GRN = "\033[92m"
    YLW = "\033[93m"
    BLU = "\033[94m"
    CYN = "\033[96m"
    WHT = "\033[97m"
    MAG = "\033[35m"
    BG_B = "\033[44m"
    BG_R = "\033[41m"


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    """Print OTP Flood header banner."""
    cls()
    print(f"\n{C.B}{C.RED}  ╔══════════════════════════════════════════════════╗{C.RST}")
    print(f"{C.B}{C.RED}  ║         OTP FLOOD TESTING FRAMEWORK              ║{C.RST}")
    print(f"{C.B}{C.RED}  ╚══════════════════════════════════════════════════╝{C.RST}")
    print(f"{C.DIM}  Security Testing — Validasi Ketahanan Sistem Verifikasi{C.RST}")
    print(f"{C.DIM}  ==================================================={C.RST}\n")


def input_target():
    """Get and validate target WhatsApp number."""
    while True:
        print(f"  Masukkan nomor WhatsApp target:")
        print(f"  {C.DIM}  (dengan kode negara, contoh: 6281234567890){C.RST}")
        print(f"  {C.DIM}  (ketik 'q' untuk kembali){C.RST}")
        print(f"\n  {C.CYN}Nomor target: {C.RST}", end="")
        val = input().strip()

        if val.lower() == "q":
            return None
        if not val.isdigit():
            print(f"  {C.RED}Hanya angka! Coba lagi.{C.RST}\n")
            continue
        if len(val) < 10:
            print(f"  {C.RED}Nomor terlalu pendek (min 10 digit). Coba lagi.{C.RST}\n")
            continue

        print(f"  {C.GRN}✓ Nomor target: {val}{C.RST}\n")
        return val


def select_profile():
    """Show profile selection menu."""
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
    """Let user configure profile parameters."""
    profile = PROFILES[profile_key]
    params = dict(profile["default_params"])

    print(f"\n  {C.B}Konfigurasi parameter:{C.RST}\n")

    if "interval" in params:
        while True:
            val = input(f"  Interval antar pesan (detik) [default: {params['interval']}]: ").strip()
            if not val:
                break
            try:
                params["interval"] = float(val)
                break
            except ValueError:
                print(f"  {C.RED}Masukkan angka!{C.RST}")

    if "max_messages" not in params:
        while True:
            val = input(f"  Total maksimal pesan [default: 50]: ").strip()
            if not val:
                params["max_messages"] = 50
                break
            try:
                params["max_messages"] = int(val)
                break
            except ValueError:
                print(f"  {C.RED}Masukkan angka!{C.RST}")
    else:
        params["max_messages"] = 50

    val = input(f"  Cooldown jika kena block (detik) [default: 60]: ").strip()
    params["block_cooldown"] = int(val) if val else 60

    if profile_key == "exponential":
        for key in ["base", "max_rate"]:
            if key in params:
                val = input(f"  {key} [default: {params[key]}]: ").strip()
                if val:
                    try:
                        params[key] = float(val)
                    except ValueError:
                        pass

    if profile_key == "random":
        for key in ["min_interval", "max_interval"]:
            if key in params:
                val = input(f"  {key} [default: {params[key]}]: ").strip()
                if val:
                    try:
                        params[key] = float(val)
                    except ValueError:
                        pass

    return params


def select_categories():
    """Let user select brand categories."""
    print(f"\n  {C.B}Pilih kategori brand untuk OTP:{C.RST}\n")

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
        count = len(CATEGORIES[key])
        print(f"  {C.CYN}[{i}]{C.RST} {labels.get(key, key)} ({count} brand)")

    print(f"\n  {C.CYN}[A]{C.RST} ALL — semua kategori")
    print(f"  {C.CYN}[Q]{C.RST} Kembali\n")

    while True:
        print(f"  {C.CYN}Pilih (contoh: 1,2,3 atau A): {C.RST}", end="")
        ch = input().strip().upper()
        if ch == "Q":
            return None
        if ch == "A":
            return None  # None = all categories
        try:
            indices = [int(x.strip()) - 1 for x in ch.split(",")]
            selected = [keys[i] for i in indices if 0 <= i < len(keys)]
            if selected:
                brand_count = sum(len(CATEGORIES[k]) for k in selected)
                print(f"  {C.GRN}✓ {brand_count} brand dari {len(selected)} kategori{C.RST}")
                return selected
        except (ValueError, IndexError):
            pass
        print(f"  {C.RED}Pilihan tidak valid!{C.RST}")


def show_confirm(config):
    """Show configuration summary and ask for confirmation."""
    profile = PROFILES[config["profile"]]
    cats = config.get("categories")
    if cats:
        total_brands = sum(len(CATEGORIES[c]) for c in cats)
        cat_names = ", ".join(cats)
    else:
        total_brands = sum(len(v) for v in CATEGORIES.values())
        cat_names = "ALL"

    estimated = (config.get("max_messages", 50) * config.get("interval", 3)) // 60
    if estimated < 1:
        estimated = 1

    print(f"\n  {C.B}{C.CYN}  ╔═══════════════════════════════════════════╗{C.RST}")
    print(f"  {C.B}{C.CYN}  ║       KONFIRMASI PENGATURAN               ║{C.RST}")
    print(f"  {C.B}{C.CYN}  ╚═══════════════════════════════════════════╝{C.RST}\n")
    print(f"  {C.B}Target    :{C.RST} {config['target']}")
    print(f"  {C.B}Profile   :{C.RST} {profile['name']}")
    print(f"  {C.B}Interval  :{C.RST} {config.get('interval', 'N/A')} detik")
    print(f"  {C.B}Max Pesan :{C.RST} {config.get('max_messages', 50)}")
    print(f"  {C.B}Brand     :{C.RST} {total_brands} brand ({cat_names})")
    print(f"  {C.B}Estimasi  :{C.RST} ~{estimated} menit\n")

    while True:
        print(f"  {C.CYN}Mulai serangan? (Y/n): {C.RST}", end="")
        ch = input().strip().lower()
        if ch in ("y", ""):
            return True
        elif ch == "n":
            return False
        print(f"  {C.RED}Y atau n saja.{C.RST}")


def execute_flood(config):
    """Run the flood with real-time display."""
    print(f"\n  {C.B}{C.CYN}  ╔═══════════════════════════════════════════╗{C.RST}")
    print(f"  {C.B}{C.CYN}  ║       OTP FLOOD - RUNNING                  ║{C.RST}")
    print(f"  {C.B}{C.CYN}  ╚═══════════════════════════════════════════╝{C.RST}\n")

    for output in run_flood(config):
        # Clear previous lines
        sys.stdout.write("\033[2K\033[1A" * 4)
        lines = output.strip().split("\n")
        for line in lines:
            sys.stdout.write("\033[2K")
            print(line)


def otp_flood_menu():
    """Main OTP flood menu flow."""
    print_header()

    # Step 1: Input target
    target = input_target()
    if target is None:
        return

    print_header()

    # Step 2: Select profile
    profile = select_profile()
    if profile is None:
        return

    print_header()

    # Step 3: Configure parameters
    params = configure_params(profile)

    # Step 4: Select categories
    print_header()
    categories = select_categories()

    # Build config
    config = {
        "target": target,
        "profile": profile,
        **params,
        "categories": categories,
    }

    # Step 5: Confirm
    print_header()
    if not show_confirm(config):
        print(f"\n  {C.YLW}Dibatalkan.{C.RST}\n")
        return

    # Step 6: Execute
    execute_flood(config)

    # After execution
    print(f"\n  {C.CYN}[1]{C.RST} Ulangi dengan profile berbeda")
    print(f"  {C.CYN}[2]{C.RST} Kembali ke menu utama")
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
        print(f"  {C.RED}Pilihan tidak valid.{C.RST}")
