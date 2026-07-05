# METACYTECH Tools

<div align="center">

[![Version](https://img.shields.io/badge/version-2.0.0-blue)]()
[![Next.js](https://img.shields.io/badge/Next.js-16-black)]()
[![Python](https://img.shields.io/badge/Python-3.13+-green)]()
[![License](https://img.shields.io/badge/license-MIT-orange)]()

🚀 **Multi-template social engineering awareness & phishing simulation platform**

</div>

---

## 📋 Fitur

- **Multi-template system** — BNI, TikTok, BIBD, OTP Flood
- **One-click deploy** — Build Next.js + Cloudflare Tunnel / ngrok
- **Auto URL update** — metadataBase otomatis mengikuti tunnel URL
- **Camera & Location capture** — permission-based data collection
- **Telegram integration** — real-time data delivery
- **OTP Flood mode** — multi-brand OTP spam (Paypal, Tinder, Telegram, Flip, Lazada, Netflix, dll)
- **Cross-platform** — Windows & Termux support
- **Auto fallback** — ngrok jika Cloudflare Tunnel gagal
- **Premium terminal UI** — clean animations tanpa emoji

---

## ⚡ Persyaratan

| Komponen | Minimum |
|----------|---------|
| Python | 3.13+ |
| Node.js | 20.x+ |
| NPM | 10.x+ |
| Cloudflared | 2026+ (opsional, auto fallback ke ngrok) |
| OS | Windows 10+ / Termux (Android) |

### Install Cloudflared

**Windows:**
```bash
# Download from https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/
# Install to C:\Program Files (x86)\cloudflared\
```

**Termux:**
```bash
pkg install cloudflared -y
```

### Setup Telegram Bot

1. Chat [@BotFather](https://t.me/BotFather) di Telegram
2. Kirim `/newbot` dan ikuti instruksi
3. Dapatkan **Bot Token** (format: `123456:ABC-DEF...`)
4. Buat grup, invite bot sebagai admin
5. Kirim pesan ke grup, lalu ke `https://api.telegram.org/bot<TOKEN>/getUpdates`
6. Dapatkan **Chat ID** dari response JSON

Buat file `.env.local` di root project:
```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_CHAT_ID=-100123456789
```

---

## 🚀 Cara Menggunakan

### Jalankan Launcher

**Windows:**
```bash
python launcher.py
```
Atau double-click `run.bat`

**Termux:**
```bash
cd ~/metacytech-tools
python launcher.py
```

### Alur Penggunaan

Saat pertama kali run, Anda akan diminta memilih template:

```
  Pilih template:
  [1] BNI  Bank Transfer Verification
  [2] TikTok  Video Share Link
  [3] BIBD  Brunei Darussalam
  [4] OTP Flood  Multi-Brand Spam

  Pilih template (1-4):
```

Pilih template, lalu sistem akan otomatis:

1. ✅ Apply template files
2. ✅ Build Next.js app (Turbopack)
3. ✅ Start server (port 3000)
4. ✅ Start Cloudflare Tunnel (fallback ke ngrok jika perlu)
5. ✅ Update metadataBase dengan tunnel URL
6. ✅ Rebuild & restart server
7. ✅ Tampilkan **PUBLIC URL** untuk dibagikan

**Output terminal:**
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

Setelah sistem running:

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

### Mendapatkan Data Target

1. **Bagikan PUBLIC URL** yang tampil di terminal ke target
2. **Monitor Telegram** — data akan terkirim real-time saat target:
   - Mengizinkan kamera
   - Mengizinkan akses lokasi
3. **Data yang diterima:**
   - 📷 Foto dari kamera depan & Video
   - 📍 Lokasi GPS (dengan Google Maps link)
   - 💻 Device info lengkap (OS, browser, RAM, CPU, baterai)
   - 🌐 IP address & ISP
   - 📱 Screen resolution & orientation

---

## 🧩 Template yang Tersedia

| # | Template | Deskripsi | Mode |
|---|----------|-----------|------|
| 1 | **BNI** | Bank Transfer Verification | Web |
| 2 | **TikTok** | Video Share Link (camera + location) | Web |
| 3 | **BIBD** | Bank Islam Brunei Darussalam | Web |
| 4 | **OTP Flood** | Spam OTP multi-brand (Paypal, Tinder, Telegram, Flip, Lazada, Netflix, dll) | CLI |

---

## 🔧 Troubleshooting

### Problem: Cloudflared SSL Certificate Error (Termux)
```
failed to request quick Tunnel: tls: failed to verify certificate
```

**Solusi:**
```bash
pkg install ca-certificates openssl-tool -y
pkg upgrade -y
```

Jika masih error, sistem akan **auto-fallback ke ngrok**. Install ngrok:
```bash
cd ~
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.zip
unzip ngrok-v3-stable-linux-arm64.zip
chmod +x ngrok
mv ngrok $PREFIX/bin/
```

### Problem: "Could not get tunnel URL"

**Cek apakah cloudflared/ngrok running:**
```bash
ps aux | grep cloudflared
ps aux | grep ngrok
```

**Cek tunnel.log:**
```bash
cat tunnel.log
```

**Manual test cloudflared:**
```bash
cloudflared tunnel --url http://localhost:3000
```

### Problem: Telegram Bot Tidak Kirim Data

**Cek token & chat ID:**
```bash
cat .env.local
```

**Test manual menggunakan curl:**
```bash
curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<CHAT_ID>&text=Test"
```

### Problem: Next.js Build Error

**Clear cache dan rebuild:**
```bash
rm -rf .next node_modules
npm install
npm run build
```

### Problem: Port 3000 Already in Use

**Windows:**
```bash
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

**Termux:**
```bash
lsof -i :3000
kill -9 <PID>
```

---

## ❓ FAQ

**Q: Apakah tool ini legal?**
A: Tool ini legal untuk security testing dengan **izin tertulis** dan awareness training. Penggunaan tanpa izin adalah **ILEGAL** dan dapat dikenai sanksi hukum.

**Q: Apakah target tahu sedang di-test?**
A: Tidak, kecuali Anda memberitahu setelahnya (recommended untuk ethical testing).

**Q: Data tersimpan dimana?**
A: Data dikirim ke Telegram bot Anda. **TIDAK** tersimpan di server kami.

**Q: Bisa running 24/7?**
A: Cloudflare Tunnel gratis tidak menjamin uptime 100%. Untuk production, gunakan VPS + domain sendiri.

**Q: Bisa custom template?**
A: Ya! Buat folder baru di `templates/<nama>` dengan `page.tsx`, `layout.tsx`, dan assets di `public/`.

**Q: Kenapa build lambat di Termux?**
A: Next.js 16 Turbopack tidak support ARM. Sistem auto-downgrade ke Next.js 15 dengan Webpack (lebih lambat tapi stabil).

**Q: Kenapa tidak ada CAPTCHA?**
A: CAPTCHA dihapus karena tidak efektif. Sistem hanya menggunakan camera & location permission yang terlihat profesional.

**Q: OTP Flood cara pakainya?**
A: Pilih template [4] OTP Flood, lalu ikuti menu interaktif untuk mengirim OTP ke nomor target.

---

## ⚖️ Legal & Ethics

### 🚨 PENTING - BACA INI!

1. **Izin Tertulis WAJIB** — Selalu dapatkan izin tertulis sebelum melakukan security testing
2. **Jangan Menyalahgunakan** — Tool ini untuk edukasi dan authorized testing ONLY
3. **Tanggung Jawab Pengguna** — Anda bertanggung jawab penuh atas penggunaan tool ini
4. **Hukum Berlaku** — Penggunaan ilegal dapat dikenai:
   - UU ITE Pasal 30-35 (Indonesia)
   - Computer Fraud and Abuse Act (USA)
   - GDPR violations (EU)
   - Dan hukum lain yang berlaku

### ✅ Use Cases yang DIIZINKAN:
- Security awareness training dengan persetujuan
- Authorized penetration testing dengan scope jelas
- Red team exercises dengan kontrak
- Educational purposes di controlled environment

### ❌ Use Cases yang DILARANG:
- Phishing tanpa izin
- Unauthorized data collection
- Identity theft
- Any illegal activity

---

## 📁 Struktur Project

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

---

## 🤝 Contributing

Contributions are welcome! Tapi pastikan:
1. Follow ethical guidelines
2. Test thoroughly di Windows & Termux
3. Document semua perubahan
4. Create pull request dengan deskripsi jelas

---

## 📄 License

MIT License — Lihat [LICENSE](LICENSE) untuk detail

---

## 👤 Author

**Iqbal**
- GitHub: [@iqbalgsr46](https://github.com/iqbalgsr46)
- Project: [METACYTECH Tools](https://github.com/iqbalgsr46/metacytech-tools)

---

## 🙏 Acknowledgments

- Next.js Team untuk amazing framework
- Cloudflare untuk free tunnel service
- Telegram untuk bot API
- Community untuk feedback & contributions

---

<div align="center">

**⚠️ Gunakan dengan bijak dan bertanggung jawab! ⚠️**

Made with ❤️ for Security Research & Awareness

</div>
