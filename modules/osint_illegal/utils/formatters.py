import sys
from ..config import C

def progress_bar(current: int, total: int, width: int = 40, prefix: str = ""):
    if total == 0:
        return
    percent = min(current / total, 1.0)
    filled = int(width * percent)
    bar = f"{C.GRN}{'█' * filled}{C.RST}{C.DIM}{'░' * (width - filled)}{C.RST}"
    sys.stdout.write(f"\r  {prefix} {bar} {int(percent*100)}% ({current}/{total})  ")
    sys.stdout.flush()
    if current >= total:
        sys.stdout.write(f"\n")
        sys.stdout.flush()

def format_section(title: str, data: dict, indent: int = 2):
    pad = " " * indent
    lines = [f"\n{pad}{C.B}{C.CYN}{'═══ ' + title + ' ' + '═' * (50 - len(title))}{C.RST}"]
    for k, v in data.items():
        if v and str(v).strip():
            lines.append(f"{pad}{C.BLU}{k.replace('_', ' ').title().ljust(22)}{C.RST}: {C.DIM if 'Tidak' in str(v) else ''}{v}{C.RST}")
    return "\n".join(lines)

def fmt_table(headers: list, rows: list) -> str:
    if not rows:
        return "  (no data)"
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))
    sep = "  " + "─" * (sum(col_widths) + len(col_widths) * 3 - 1)
    lines = [sep]
    hdr = "  │ " + " │ ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers)) + " │"
    lines.append(f"{C.B}{hdr}{C.RST}")
    lines.append(sep.replace("─", "═"))
    for row in rows:
        line = "  │ " + " │ ".join(str(c).ljust(col_widths[i]) if i < len(col_widths) else str(c) for i, c in enumerate(row)) + " │"
        lines.append(line)
    lines.append(sep)
    return "\n".join(lines)
