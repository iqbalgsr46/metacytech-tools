"""
OTP Flood - Main Engine
Orchestrates the flood execution flow
"""

from datetime import datetime
import sys
import os

# Ensure modules path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from modules.otp_flood.profiles import PROFILES, get_generator
from modules.otp_flood.templates import (
    CATEGORIES,
    CATEGORY_LABELS,
    get_brands_by_category,
    format_brand_message,
)
from modules.otp_flood.sender import Sender
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
        "start_time": datetime.now().strftime("%H:%M:%S"),
        "end_time": "",
        "logs": [],
    }

    brand_idx = 0
    consecutive_blocks = 0

    for i in range(max_msgs):
        # Pick brand (rotate or use first)
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
                "message": f"Kode OTP Anda: {str(hash(str(i)))[:6]}",
                "sender": "System",
            }

        # Send
        result = sender.send(msg_data["message"], msg_data["sender"])

        timestamp = datetime.now().strftime("%H:%M:%S")
        icon = "✓" if result["sent"] else "✗ BLOCK"
        results["logs"].append(
            f"{timestamp}  {msg_data['brand']:<10} - OTP: {msg_data['otp']:<6} {icon}"
        )

        if result["sent"]:
            results["total_sent"] += 1
            consecutive_blocks = 0
        else:
            results["total_blocked"] += 1
            consecutive_blocks += 1

        # Status display
        progress = f"[{i+1}/{max_msgs}]"
        bar_len = 20
        filled = int((i + 1) / max_msgs * bar_len)
        bar = "█" * filled + "░" * (bar_len - filled)

        status_line = (
            f"  {'🟢' if result['sent'] else '🔴'} Sending... {progress} {bar}\n"
            f"  Blocked : {results['total_blocked']} | "
            f"Sent: {results['total_sent']} | "
            f"Det Rate: {results['total_blocked']/(i+1)*100:.1f}%\n"
        )
        yield status_line

        # Cooldown on consecutive blocks
        if consecutive_blocks >= 3:
            warning = f"  ⏸  Blocked {consecutive_blocks}x berturut-turut! Cooldown {block_cooldown}s...\n"
            yield warning
            import time as ttime

            for remaining in range(block_cooldown, 0, -1):
                yield f"  ⏳ Cooldown: {remaining}s  \r"
                ttime.sleep(1)
            yield f"  ✅ Resume\n"
            consecutive_blocks = 0

        # Wait for next interval
        try:
            wait = next(gen)
            if wait > 0:
                import time as ttime

                ttime.sleep(wait)
        except StopIteration:
            break

    # Final stats
    results["end_time"] = datetime.now().strftime("%H:%M:%S")
    results["total_sent"] = sender.sent_count
    results["total_blocked"] = sender.block_count

    # Generate report
    report_text, grade, det_rate = generate_report(results, config)

    yield f"\n{report_text}\n"

    # Save report
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "reports"
    )
    os.makedirs(output_dir, exist_ok=True)
    saved = save_report(report_text, output_dir)

    if saved:
        yield f"  📄 Report saved: {saved}\n"
