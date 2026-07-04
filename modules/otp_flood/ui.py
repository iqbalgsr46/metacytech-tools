"""
OTP Flood - Terminal UI
Interactive menu for OTP flood testing with real WhatsApp
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
    BG_B = "\033[44m"
    BG_R = "\033[41m"


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def print_header():
    cls()
    print(f"\n{C.B}{C.RED}  ╔══════════════════════════════════════════════════╗{C.RST}")
    print(f"{C.B}{C.RED}  ║         OTP FLOOD TESTING FRAMEWORK              ║{C.RST}")
    print(f"{C.B}{C.RED}  ╚══════════════════════════════════════════════════╝{C.RST}")
    print(f"{C.DIM}  Real WhatsApp — Scan QR sekali, langsung gas{C.RST}")
    print(f"{C.DIM}  ==================================================={C.RST}\n")


def input_target():
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

    print(f"\n  {C.B}Konfigurasi parameter:{C.RST}\n")
    print(f"  {C.DIM}Tips: 1-2s = super cepat (test rate limit){C.RST}")
    print(f"  {C.DIM}      3-5s = medium (realistis){C.RST}")
    print(f"  {C.DIM}      6-10s = lambat (stealthy){C.RST}\n")

    if "interval" in params:
        while True:
            val = input(f"  Interval antar pesan (detik) [default: {params['interval']}]: ").strip()
            if not val:
                break
            try:
                params["interval"] = float(val)
                if params["interval"] < 0.5:
                    print(f"  {C.YLW}⚠️  Interval < 1 detik bisa kena rate limit cepat!{C.RST}")
                break
            except ValueError:
                print(f"  {C.RED}Masukkan angka!{C.RST}")

    while True:
        val = input(f"  Total maksimal pesan [default: 50]: ").strip()
        if not val:
            params["max_messages"] = 50
            break
        try:
            params["max_messages"] = int(val)
            if params["max_messages"] > 500:
                print(f"  {C.YLW}⚠️  Banyak banget! Pastikan target valid.{C.RST}")
            break
        except ValueError:
            print(f"  {C.RED}Masukkan angka!{C.RST}")

    while True:
        val = input(f"  Cooldown jika kena block (detik) [default: 60]: ").strip()
        params["block_cooldown"] = int(val) if val else 60
        break

    return params


def select_categories():
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

    print(f"\n  {C.CYN}[A]{C.RST} ALL — semua kategori ({sum(len(v) for v in CATEGORIES.values())} brand)")
    print(f"  {C.CYN}[Q]{C.RST} Kembali\n")

    while True:
        print(f"  {C.CYN}Pilih (contoh: 1,2,3 atau A): {C.RST}", end="")
        ch = input().strip().upper()
        if ch == "Q":
            return None
        if ch == "A":
            return None
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
    profile = PROFILES[config["profile"]]
    cats = config.get("categories")
    if cats:
        total_brands = sum(len(CATEGORIES[c]) for c in cats)
    else:
        total_brands = sum(len(v) for v in CATEGORIES.values())

    interval = config.get("interval", 3)
    max_msgs = config.get("max_messages", 50)
    estimated = int((max_msgs * interval) / 60)
    if estimated < 1:
        estimated = 1

    print(f"\n  {C.B}{C.CYN}  ╔═══════════════════════════════════════════╗{C.RST}")
    print(f"  {C.B}{C.CYN}  ║       KONFIRMASI PENGATURAN               ║{C.RST}")
    print(f"  {C.B}{C.CYN}  ╚═══════════════════════════════════════════╝{C.RST}\n")
    print(f"  {C.B}Target   :{C.RST} {config['target']}")
    print(f"  {C.B}Profile  :{C.RST} {profile['name']}")
    print(f"  {C.B}Interval :{C.RST} {interval} detik")
    print(f"  {C.B}Max Pesan:{C.RST} {max_msgs}")
    print(f"  {C.B}Brand    :{C.RST} {total_brands} brand")
    print(f"  {C.B}Estimasi :{C.RST} ~{estimated} menit\n")
    print(f"  {C.YLW}⚠️  Pastikan Anda sudah pernah scan QR WhatsApp{C.RST}")
    print(f"  {C.YLW}   Jika pertama kali, QR code akan muncul.{C.RST}\n")

    while True:
        print(f"  {C.CYN}Mulai serangan? (Y/n): {C.RST}", end="")
        ch = input().strip().lower()
        if ch in ("y", ""):
            return True
        elif ch == "n":
            return False
        print(f"  {C.RED}Y atau n saja.{C.RST}")


def execute_flood(config):
    print(f"\n  {C.B}{C.CYN}  ╔═══════════════════════════════════════════╗{C.RST}")
    print(f"  {C.B}{C.CYN}  ║       OTP FLOOD - RUNNING                  ║{C.RST}")
    print(f"  {C.B}{C.CYN}  ╚═══════════════════════════════════════════╝{C.RST}\n")

    for output in run_flood(config):
        # Each yield may contain multiple lines with \033[2K
        # Print everything as-is — engine handles formatting
        sys.stdout.write(output)
        sys.stdout.flush()


def otp_flood_menu():
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
