"""
OTP Flood - Report Generator
Produces structured reports from test execution data
"""

import os
import json
from datetime import datetime


def generate_report(results, config):
    """Generate a structured report from execution results."""
    total = results.get("total_sent", 0)
    blocked = results.get("total_blocked", 0)
    detection_rate = (blocked / total * 100) if total > 0 else 0

    if detection_rate < 5:
        severity = "CRITICAL"
        grade = "F"
        summary = "Sistem hampir tidak memiliki deteksi. Hampir semua pesan lolos."
    elif detection_rate < 20:
        severity = "HIGH"
        grade = "D"
        summary = "Deteksi sangat rendah. Mayoritas pesan lolos."
    elif detection_rate < 50:
        severity = "MEDIUM"
        grade = "C"
        summary = "Deteksi parsial. Separuh pesan terdeteksi."
    elif detection_rate < 80:
        severity = "LOW"
        grade = "B"
        summary = "Deteksi cukup baik. Sebagian besar pesan terblokir."
    else:
        severity = "INFO"
        grade = "A"
        summary = "Deteksi kuat. Hampir semua pesan terblokir."

    report = f"""
╔══════════════════════════════════════════════════╗
║         OTP FLOOD TESTING - REPORT               ║
║     {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}           ║
╠══════════════════════════════════════════════════╣
║  TARGET INFORMATION                            ║
║    Phone    : {config.get('target', 'N/A')}║
║    Profile  : {config.get('profile', 'N/A')}║
║    Interval : {config.get('interval', 'N/A')}s║
║    Brand    : {config.get('brand_count', 'N/A')} brand║
╠══════════════════════════════════════════════════╣
║  EXECUTION RESULTS                             ║
║    Total Sent    : {total}║
║    Total Blocked : {blocked}║
║    Detection Rate: {detection_rate:.1f}%║
║    Grade         : {grade} ({severity})  ║
╠══════════════════════════════════════════════════╣
║  ASSESSMENT                                    ║
║  {summary:<49}║
╠══════════════════════════════════════════════════╣
║  RECOMMENDATIONS                               ║
"""
    if detection_rate < 20:
        report += (
            "║  • Implement rate limiting segera                        ║\n"
            "║  • Tambahkan behavioral detection engine                ║\n"
            "║  • Aktifkan device fingerprinting                       ║\n"
            "║  • Integrasikan CAPTCHA challenge                       ║\n"
            "║  • Monitor via SOC dengan anomaly detection             ║\n"
        )
    elif detection_rate < 50:
        report += (
            "║  • Perkuat pattern recognition                          ║\n"
            "║  • Turunkan threshold rate limiting                      ║\n"
            "║  • Tambahkan geolocation sanity check                   ║\n"
            "║  • Review timing detection accuracy                     ║\n"
        )
    else:
        report += (
            "║  • Pertahankan konfigurasi keamanan saat ini             ║\n"
            "║  • Review anomaly detection untuk false positive         ║\n"
            "║  • Evaluasi scalability di bawah pressure tinggi        ║\n"
        )

    report += (
        "╠══════════════════════════════════════════════════╣\n"
        "║  TEST PERIOD                                   ║\n"
        f"║    Start : {results.get('start_time', 'N/A')}║\n"
        f"║    End   : {results.get('end_time', 'N/A')}║\n"
        "╚══════════════════════════════════════════════════╝\n"
    )

    return report, grade, detection_rate


def save_report(report_text, output_dir="."):
    """Save report to file and return path."""
    filename = f"otp_flood_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    path = os.path.join(output_dir, filename)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(report_text)
        return path
    except IOError:
        return None
