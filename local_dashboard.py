#!/usr/bin/env python3
"""
METACYTECH - Interactive Local Dashboard v4.0
Editor visual terupdate untuk template transfer perbankan BIBD Brunei Darussalam.
Dilengkapi Live Smartphone Preview real-time, grouping terstruktur, dan preset instan.
"""

import http.server
import socketserver
import json
import os
import sys
import webbrowser
import threading
import time

PORT = 8080
APP_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(APP_DIR, "templates", "bibd")
DATA_FILE = os.path.join(TEMPLATE_DIR, "data.json")

# Pastikan file data.json ada
if not os.path.exists(DATA_FILE):
    # Coba fallback ke src/app/data.json
    fallback = os.path.join(APP_DIR, "src", "app", "data.json")
    if os.path.exists(fallback):
        DATA_FILE = fallback
    else:
        print(f"Error: {DATA_FILE} tidak ditemukan.")
        sys.exit(1)


def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {}


def save_data(data):
    # Simpan ke templates/bibd/data.json
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    # Sinkronkan juga ke src/app/data.json
    src_data = os.path.abspath(os.path.join(APP_DIR, "src", "app", "data.json"))
    if os.path.abspath(DATA_FILE) != src_data:
        try:
            with open(src_data, 'w', encoding='utf-8') as sf:
                json.dump(data, sf, indent=2)
        except Exception:
            pass


class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        clean_path = self.path.split('?')[0].lstrip('/')
        
        # Sajikan file statis (gambar, icon, logo) jika diminta
        if clean_path:
            for base_dir in [
                os.path.join(APP_DIR, "public"),
                os.path.join(TEMPLATE_DIR, "public"),
                APP_DIR
            ]:
                target = os.path.join(base_dir, clean_path)
                if os.path.isfile(target):
                    self.send_response(200)
                    if target.endswith('.png'):
                        self.send_header("Content-type", "image/png")
                    elif target.endswith('.jpg') or target.endswith('.jpeg'):
                        self.send_header("Content-type", "image/jpeg")
                    elif target.endswith('.svg'):
                        self.send_header("Content-type", "image/svg+xml")
                    elif target.endswith('.ico'):
                        self.send_header("Content-type", "image/x-icon")
                    self.end_headers()
                    with open(target, 'rb') as f:
                        self.wfile.write(f.read())
                    return

        # Halaman Utama Dashboard
        if self.path == '/' or self.path.startswith('/?'):
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()

            data = load_data()
            logo_val = data.get("transactionLogo", "dana").lower()
            if data.get("receiverBank", "").upper() == "QRIS":
                logo_val = "qris"
            elif data.get("receiverBank", "").upper() == "GOPAY":
                logo_val = "gopay"

            html = f"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BIBD EDITOR // METACYTECH DASHBOARD</title>
    <link rel="icon" type="image/png" href="/metacytech-logo.png">
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body {{
            font-family: 'Plus Jakarta Sans', sans-serif;
            background-color: #090d12;
            color: #e2e8f0;
        }}
        .font-mono {{
            font-family: 'JetBrains Mono', monospace;
        }}
        /* Custom scrollbar */
        ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
        ::-webkit-scrollbar-track {{ background: #0b1118; }}
        ::-webkit-scrollbar-thumb {{ background: #1e293b; border-radius: 9999px; }}
        ::-webkit-scrollbar-thumb:hover {{ background: #334155; }}

        .glow-teal {{
            box-shadow: 0 0 25px rgba(20, 184, 166, 0.15);
        }}
        .phone-shadow {{
            box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7), 0 0 0 1px rgba(255, 255, 255, 0.1);
        }}
    </style>
</head>
<body class="min-h-screen antialiased selection:bg-teal-500 selection:text-black">

    <!-- Top Navigation Bar -->
    <header class="sticky top-0 z-30 bg-[#090d12]/90 backdrop-blur-md border-b border-slate-800/80 px-6 py-3.5">
        <div class="max-w-7xl mx-auto flex flex-wrap items-center justify-between gap-4">
            <div class="flex items-center gap-3">
                <div class="w-10 h-10 rounded-xl bg-white p-0.5 shadow-lg shadow-teal-500/20 border border-teal-500/40 flex items-center justify-center shrink-0 overflow-hidden">
                    <img src="/metacytech-logo.png" alt="METACYTECH" class="w-full h-full object-contain rounded-lg">
                </div>
                <div>
                    <div class="flex items-center gap-2">
                        <h1 class="text-sm font-bold tracking-wide text-white uppercase font-mono">BIBD Transfer Editor</h1>
                        <span class="text-[10px] font-semibold bg-teal-500/10 text-teal-400 px-2 py-0.5 rounded-full border border-teal-500/20 font-mono">v4.0 ACTIVE</span>
                    </div>
                    <p class="text-xs text-slate-400">Atur teks tampilan "Review payment" terbaru dengan simulasi live</p>
                </div>
            </div>

            <!-- Quick Presets -->
            <div class="flex items-center gap-2 flex-wrap">
                <span class="text-xs text-slate-400 font-medium mr-1 hidden sm:inline">Isi Cepat:</span>
                <button type="button" onclick="applyPreset('dana')" class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-blue-500/10 hover:bg-blue-500/20 text-blue-400 border border-blue-500/30 transition-all flex items-center gap-1.5 active:scale-95">
                    <span class="w-2 h-2 rounded-full bg-blue-500"></span> Preset DANA
                </button>
                <button type="button" onclick="applyPreset('qris')" class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 transition-all flex items-center gap-1.5 active:scale-95">
                    <span class="w-2 h-2 rounded-full bg-emerald-500"></span> Preset QRIS
                </button>
                <button type="button" onclick="applyPreset('gopay')" class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 transition-all flex items-center gap-1.5 active:scale-95">
                    <span class="w-2 h-2 rounded-full bg-cyan-400"></span> Preset GOPAY
                </button>
                <button type="button" onclick="randomizeRef()" class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 transition-all flex items-center gap-1.5 active:scale-95 font-mono">
                    🎲 Acak No. Ref
                </button>
            </div>
        </div>
    </header>

    <main class="max-w-7xl mx-auto p-4 sm:p-6 lg:p-8">
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">

            <!-- LEFT COLUMN: Input Form Sections (7 cols) -->
            <div class="lg:col-span-7 space-y-6">

                <form id="editForm" class="space-y-6">

                    <!-- SECTION 1: PILIHAN LOGO TRANSAKSI -->
                    <div class="bg-[#0f172a]/90 rounded-2xl p-5 border border-slate-800 shadow-sm glow-teal">
                        <div class="flex items-center justify-between mb-4">
                            <div class="flex items-center gap-2">
                                <span class="text-lg">💳</span>
                                <div>
                                    <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono">1. Logo Transaksi Penerima</h2>
                                    <p class="text-xs text-slate-400">Pilih logo yang muncul di kartu kanan dan baris penerima</p>
                                </div>
                            </div>
                            <span id="activeLogoBadge" class="text-xs font-bold font-mono px-2.5 py-1 rounded-full uppercase bg-teal-500/10 text-teal-400 border border-teal-500/30">
                                {logo_val.upper()} AKTIF
                            </span>
                        </div>

                        <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                            <!-- Card DANA -->
                            <label class="cursor-pointer">
                                <input type="radio" name="transactionLogo" value="dana" class="sr-only peer" {"checked" if logo_val == "dana" else ""}>
                                <div class="p-3.5 rounded-xl border border-slate-700 bg-slate-900/60 peer-checked:border-blue-500 peer-checked:bg-blue-500/10 peer-checked:shadow-sm transition-all flex items-center gap-3">
                                    <img src="/dana-icon.png" alt="DANA" class="w-10 h-10 rounded-full object-cover shadow-sm bg-white p-0.5 flex-shrink-0">
                                    <div class="flex-1 min-w-0">
                                        <div class="flex items-center justify-between">
                                            <span class="text-sm font-bold text-white">DANA</span>
                                            <span class="text-[10px] font-mono text-blue-400 font-semibold">E-Wallet</span>
                                        </div>
                                        <p class="text-xs text-slate-400 truncate">DANA ID</p>
                                    </div>
                                </div>
                            </label>

                            <!-- Card QRIS -->
                            <label class="cursor-pointer">
                                <input type="radio" name="transactionLogo" value="qris" class="sr-only peer" {"checked" if logo_val == "qris" else ""}>
                                <div class="p-3.5 rounded-xl border border-slate-700 bg-slate-900/60 peer-checked:border-emerald-500 peer-checked:bg-emerald-500/10 peer-checked:shadow-sm transition-all flex items-center gap-3">
                                    <img src="/qris-icon.png" alt="QRIS" class="w-10 h-10 rounded-full object-cover shadow-sm bg-white p-0.5 flex-shrink-0">
                                    <div class="flex-1 min-w-0">
                                        <div class="flex items-center justify-between">
                                            <span class="text-sm font-bold text-white">QRIS</span>
                                            <span class="text-[10px] font-mono text-emerald-400 font-semibold">Standar</span>
                                        </div>
                                        <p class="text-xs text-slate-400 truncate">QRIS ID</p>
                                    </div>
                                </div>
                            </label>

                            <!-- Card GOPAY -->
                            <label class="cursor-pointer">
                                <input type="radio" name="transactionLogo" value="gopay" class="sr-only peer" {"checked" if logo_val == "gopay" else ""}>
                                <div class="p-3.5 rounded-xl border border-slate-700 bg-slate-900/60 peer-checked:border-cyan-400 peer-checked:bg-cyan-500/10 peer-checked:shadow-sm transition-all flex items-center gap-3">
                                    <img src="/gopay-icon.png" alt="GOPAY" class="w-10 h-10 rounded-full object-cover shadow-sm bg-white p-0.5 flex-shrink-0">
                                    <div class="flex-1 min-w-0">
                                        <div class="flex items-center justify-between">
                                            <span class="text-sm font-bold text-white">GOPAY</span>
                                            <span class="text-[10px] font-mono text-cyan-400 font-semibold">E-Wallet</span>
                                        </div>
                                        <p class="text-xs text-slate-400 truncate">GoPay ID</p>
                                    </div>
                                </div>
                            </label>
                        </div>
                    </div>

                    <!-- SECTION 2: IDENTITAS PENGIRIM (BIBD BRUNEI) -->
                    <div class="bg-[#0f172a]/90 rounded-2xl p-5 border border-slate-800 shadow-sm">
                        <div class="flex items-center gap-2 mb-4">
                            <span class="text-lg">🏛️</span>
                            <div>
                                <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono">2. Akun Pengirim (BIBD Brunei)</h2>
                                <p class="text-xs text-slate-400">Tampil pada kartu kiri dan baris 'Sender'</p>
                            </div>
                        </div>

                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div class="sm:col-span-2">
                                <label class="block text-xs font-bold text-slate-300 mb-1.5">NAMA LENGKAP PENGIRIM</label>
                                <input type="text" id="senderName" name="senderName" value="{data.get('senderName', 'TUBAGUS IQBAL HUSAENI')}" 
                                    placeholder="Contoh: TUBAGUS IQBAL HUSAENI"
                                    class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500 transition-all">
                                <p class="text-[11px] text-slate-500 mt-1">Nama nasabah bank pengirim yang akan dilihat korban</p>
                            </div>

                            <div>
                                <label class="block text-xs font-bold text-slate-300 mb-1.5">BANK PENGIRIM</label>
                                <input type="text" id="senderBank" name="senderBank" value="{data.get('senderBank', 'BIBD')}" 
                                    class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500 transition-all font-mono">
                                <p class="text-[11px] text-slate-500 mt-1">Default: BIBD</p>
                            </div>

                            <div>
                                <label class="block text-xs font-bold text-slate-300 mb-1.5">NOMOR REKENING PENGIRIM</label>
                                <input type="text" id="senderAccount" name="senderAccount" value="{data.get('senderAccount', 'BND33 0006 1005 1978 6457')}" 
                                    placeholder="Contoh: BND33 0006 1005 1978 6457"
                                    class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500 transition-all font-mono">
                                <p class="text-[11px] text-slate-500 mt-1">4 digit terakhir otomatis dipasang di kartu atas</p>
                            </div>
                        </div>
                    </div>

                    <!-- SECTION 3: IDENTITAS PENERIMA (TARGET / KORBAN) -->
                    <div class="bg-[#0f172a]/90 rounded-2xl p-5 border border-slate-800 shadow-sm">
                        <div class="flex items-center gap-2 mb-4">
                            <span class="text-lg">👤</span>
                            <div>
                                <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono">3. Akun Penerima Dana</h2>
                                <p class="text-xs text-slate-400">Tampil pada kartu kanan dan baris 'Recipient'</p>
                            </div>
                        </div>

                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div class="sm:col-span-2">
                                <label class="block text-xs font-bold text-slate-300 mb-1.5">NAMA LENGKAP PENERIMA</label>
                                <input type="text" id="receiverName" name="receiverName" value="{data.get('receiverName', 'ABDUL AZIS')}" 
                                    placeholder="Contoh: ABDUL AZIS"
                                    class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500 transition-all">
                                <p class="text-[11px] text-slate-500 mt-1">Nama penerima / pemilik dompet DANA atau merchant QRIS</p>
                            </div>

                            <div>
                                <label class="block text-xs font-bold text-slate-300 mb-1.5">PROVIDER / BANK PENERIMA</label>
                                <input type="text" id="receiverBank" name="receiverBank" value="{data.get('receiverBank', 'DANA')}" 
                                    class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500 transition-all font-mono">
                                <p class="text-[11px] text-slate-500 mt-1">Otomatis sinkron dengan pilihan logo (DANA / QRIS)</p>
                            </div>

                            <div>
                                <label class="block text-xs font-bold text-slate-300 mb-1.5">NOMOR AKUN / HP PENERIMA</label>
                                <input type="text" id="receiverAccount" name="receiverAccount" value="{data.get('receiverAccount', '0821-2469-2642')}" 
                                    placeholder="Contoh: 0821-2469-2642"
                                    class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500 transition-all font-mono">
                                <p class="text-[11px] text-slate-500 mt-1">Nomor HP DANA atau ID transaksi</p>
                            </div>
                        </div>
                    </div>

                    <!-- SECTION 4: NOMINAL & KURS KONVERSI OTOMATIS -->
                    <div class="bg-[#0f172a]/90 rounded-2xl p-5 border border-slate-800 shadow-sm">
                        <div class="flex items-center justify-between mb-4 flex-wrap gap-2">
                            <div class="flex items-center gap-2">
                                <span class="text-lg">💰</span>
                                <div>
                                    <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono">4. Nominal Transaksi & Konversi Otomatis</h2>
                                    <p class="text-xs text-slate-400">Ketik nominal IDR, BND Brunei akan terhitung otomatis</p>
                                </div>
                            </div>
                            <span class="text-[10.5px] font-mono px-2.5 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center gap-1.5">
                                <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
                                1 BND ≈ Rp 13.889
                            </span>
                        </div>

                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div>
                                <label class="block text-xs font-bold text-slate-300 mb-1.5 flex items-center justify-between">
                                    <span>NOMINAL DITERIMA (IDR)</span>
                                    <span class="text-[10px] text-teal-400 font-mono font-normal">Ketik angka langsung</span>
                                </label>
                                <input type="text" id="amountPrimary" name="amountPrimary" value="{data.get('amountPrimary', 'IDR 10.000')}" 
                                    placeholder="Contoh: 50.000 atau IDR 50.000"
                                    class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500 transition-all font-bold">
                                <p class="text-[11px] text-slate-500 mt-1">Tampil tebal di atas tombol aksi</p>

                                <!-- Quick Nominal Chips -->
                                <div class="flex flex-wrap gap-1.5 mt-2.5">
                                    <button type="button" onclick="setQuickNominal(10000)" class="text-[10.5px] font-mono font-semibold px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700/80 transition-all active:scale-95">10rb</button>
                                    <button type="button" onclick="setQuickNominal(20000)" class="text-[10.5px] font-mono font-semibold px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700/80 transition-all active:scale-95">20rb</button>
                                    <button type="button" onclick="setQuickNominal(50000)" class="text-[10.5px] font-mono font-semibold px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700/80 transition-all active:scale-95">50rb</button>
                                    <button type="button" onclick="setQuickNominal(100000)" class="text-[10.5px] font-mono font-semibold px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700/80 transition-all active:scale-95">100rb</button>
                                    <button type="button" onclick="setQuickNominal(250000)" class="text-[10.5px] font-mono font-semibold px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700/80 transition-all active:scale-95">250rb</button>
                                    <button type="button" onclick="setQuickNominal(500000)" class="text-[10.5px] font-mono font-semibold px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700/80 transition-all active:scale-95">500rb</button>
                                    <button type="button" onclick="setQuickNominal(1000000)" class="text-[10.5px] font-mono font-semibold px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700/80 transition-all active:scale-95">1 Jt</button>
                                </div>
                            </div>

                            <div>
                                <label class="block text-xs font-bold text-slate-300 mb-1.5 flex items-center justify-between">
                                    <span>NOMINAL ASAL BRUNEI (BND)</span>
                                    <span class="text-[10.5px] text-emerald-400 font-mono font-medium flex items-center gap-1">
                                        ⚡ Otomatis
                                    </span>
                                </label>
                                <input type="text" id="amountSecondary" name="amountSecondary" value="{data.get('amountSecondary', 'BND 0,72')}" 
                                    placeholder="Contoh: BND 3,60"
                                    class="w-full bg-slate-900 border border-emerald-500/40 rounded-xl px-3.5 py-2.5 text-sm text-emerald-300 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500 transition-all font-mono font-bold">
                                <p class="text-[11px] text-slate-500 mt-1">Konversi mata uang asal dari BIBD Brunei Darussalam</p>

                                <div class="flex items-center gap-2 mt-2.5 p-2 bg-slate-900/80 border border-slate-800 rounded-lg text-[11px] text-slate-400">
                                    <span>💡</span>
                                    <span>Nominal BND otomatis dikalkulasikan seketika saat Anda mengetik Rupiah.</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- SECTION 5: RINCIAN VALIDASI RESI -->
                    <div class="bg-[#0f172a]/90 rounded-2xl p-5 border border-slate-800 shadow-sm">
                        <div class="flex items-center gap-2 mb-4">
                            <span class="text-lg">📋</span>
                            <div>
                                <h2 class="text-sm font-bold text-white uppercase tracking-wider font-mono">5. Rincian & Nomor Referensi</h2>
                                <p class="text-xs text-slate-400">Data pelengkap pada Card Rincian Pemindahan Dana</p>
                            </div>
                        </div>

                        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                            <div class="sm:col-span-2">
                                <label class="block text-xs font-bold text-slate-300 mb-1.5">NO. RUJUKAN TRANSAKSI</label>
                                <div class="flex gap-2">
                                    <input type="text" id="receiptReference" name="receiptReference" value="{data.get('receiptReference', '056868540003')}" 
                                        class="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500 transition-all font-mono">
                                    <button type="button" onclick="randomizeRef()" class="px-3.5 py-2.5 bg-slate-800 hover:bg-slate-700 text-teal-400 text-xs font-bold rounded-xl border border-slate-700 transition-all font-mono flex-shrink-0">
                                        Acak
                                    </button>
                                </div>
                            </div>

                            <div>
                                <label class="block text-xs font-bold text-slate-300 mb-1.5">WAKTU TRANSAKSI</label>
                                <div class="flex gap-2">
                                    <input type="text" id="receiptDate" name="receiptDate" value="{data.get('receiptDate', 'AUTO')}" 
                                        placeholder="AUTO"
                                        class="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500 transition-all font-mono">
                                    <button type="button" onclick="document.getElementById('receiptDate').value='AUTO'; updatePreview();" class="px-3 py-2.5 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold rounded-xl border border-slate-700 transition-all flex-shrink-0 font-mono">
                                        AUTO
                                    </button>
                                </div>
                                <p class="text-[11px] text-slate-500 mt-1">Gunakan 'AUTO' agar waktu menyesuaikan jam korban</p>
                            </div>

                            <div>
                                <label class="block text-xs font-bold text-slate-300 mb-1.5">JENIS TRANSAKSI</label>
                                <input type="text" id="receiptTransactionType" name="receiptTransactionType" value="{data.get('receiptTransactionType', 'Transfer Internasional')}" 
                                    class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500 transition-all">
                                <p class="text-[11px] text-slate-500 mt-1">Contoh: Transfer Internasional</p>
                            </div>
                        </div>
                    </div>

                    <!-- ADVANCED ACCORDION: SINKRONISASI BUKTI RESI POPUP -->
                    <div class="bg-[#0f172a]/70 rounded-2xl border border-slate-800/80 overflow-hidden">
                        <button type="button" onclick="toggleReceiptSection()" class="w-full px-5 py-4 flex items-center justify-between text-left hover:bg-slate-800/40 transition-colors">
                            <div class="flex items-center gap-2">
                                <span class="text-base">🧾</span>
                                <div>
                                    <span class="text-xs font-bold text-slate-300 font-mono uppercase tracking-wider">Detail Struk / Resi Selesai (Popup)</span>
                                    <p class="text-[11px] text-slate-500">Secara otomatis disamakan dengan form di atas</p>
                                </div>
                            </div>
                            <span id="receiptChevron" class="text-slate-500 text-sm font-mono transition-transform">▼</span>
                        </button>

                        <div id="receiptFields" class="hidden p-5 border-t border-slate-800/80 bg-slate-950/40 space-y-4">
                            <div class="flex items-center gap-2 p-3 bg-teal-500/10 border border-teal-500/20 rounded-xl text-xs text-teal-300">
                                <input type="checkbox" id="autoSyncReceipt" checked class="w-4 h-4 text-teal-500 rounded bg-slate-900 border-slate-700 focus:ring-teal-500">
                                <label for="autoSyncReceipt" class="cursor-pointer font-medium">Otomatis sinkronkan nama & nominal resi dengan form utama (Direkomendasikan)</label>
                            </div>

                            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
                                <div>
                                    <label class="block text-xs font-bold text-slate-400 mb-1">JUMLAH DI RESI</label>
                                    <input type="text" id="receiptAmount" name="receiptAmount" value="{data.get('receiptAmount', data.get('amountPrimary', 'IDR 10.000'))}" 
                                        class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white">
                                </div>
                                <div>
                                    <label class="block text-xs font-bold text-slate-400 mb-1">NAMA PENGIRIM RESI</label>
                                    <input type="text" id="receiptSenderName" name="receiptSenderName" value="{data.get('receiptSenderName', data.get('senderName', 'TUBAGUS IQBAL HUSAENI'))}" 
                                        class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white">
                                </div>
                                <div>
                                    <label class="block text-xs font-bold text-slate-400 mb-1">REKENING PENGIRIM RESI</label>
                                    <input type="text" id="receiptSenderAccount" name="receiptSenderAccount" value="{data.get('receiptSenderAccount', '(****2642)')}" 
                                        class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white font-mono">
                                </div>
                                <div>
                                    <label class="block text-xs font-bold text-slate-400 mb-1">NAMA PENERIMA RESI</label>
                                    <input type="text" id="receiptReceiverName" name="receiptReceiverName" value="{data.get('receiptReceiverName', data.get('receiverName', 'ABDUL AZIS'))}" 
                                        class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white">
                                </div>
                                <div class="sm:col-span-2">
                                    <label class="block text-xs font-bold text-slate-400 mb-1">REKENING PENERIMA RESI</label>
                                    <input type="text" id="receiptReceiverAccount" name="receiptReceiverAccount" value="{data.get('receiptReceiverAccount', '(****3113)')}" 
                                        class="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-white font-mono">
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Hidden legacy keys so nothing breaks -->
                    <input type="hidden" name="title" value="{data.get('title', 'Brunei Darussalam INTERNATIONAL')}">
                    <input type="hidden" name="subtitle" value="{data.get('subtitle', 'Office Purchasing')}">

                    <!-- SAVE & EXECUTE BUTTONS -->
                    <div class="pt-2 flex flex-col sm:flex-row items-center gap-3">
                        <button type="submit" id="saveBtn"
                            class="w-full sm:flex-1 py-3.5 px-6 rounded-xl bg-gradient-to-r from-teal-400 via-emerald-500 to-teal-500 hover:opacity-95 text-black font-extrabold text-sm tracking-wide uppercase transition-all shadow-lg shadow-teal-500/20 active:scale-[0.98] flex items-center justify-center gap-2">
                            <span>💾</span> SIMPAN & TERAPKAN KE APLIKASI
                        </button>
                        <button type="button" onclick="cancelDashboard()" 
                            class="w-full sm:w-auto py-3.5 px-5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 font-bold text-xs uppercase tracking-wider transition-all border border-slate-700">
                            Batal
                        </button>
                    </div>

                </form>

            </div>

            <!-- RIGHT COLUMN: Interactive Smartphone Live Preview (5 cols) -->
            <div class="lg:col-span-5 sticky top-20">
                <div class="flex items-center justify-between mb-3 px-1">
                    <div class="flex items-center gap-2">
                        <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
                        <span class="text-xs font-bold tracking-wider uppercase font-mono text-slate-300">Live Preview Smartphone</span>
                    </div>
                    <span class="text-[11px] text-slate-500 font-mono">390 x 844 viewport</span>
                </div>

                <!-- Phone Mockup Container -->
                <div class="phone-shadow rounded-[36px] bg-[#0c1219] p-3 border-2 border-slate-700/70 max-w-[360px] mx-auto overflow-hidden">
                    
                    <!-- Screen Surface -->
                    <div class="rounded-[28px] overflow-hidden bg-[#eff4f2] text-slate-800 flex flex-col justify-between select-none relative h-[670px] border border-slate-300/40 text-[12px]">
                        
                        <!-- Top Header Area (Review payment + BIBD logo) -->
                        <div class="pt-3.5 px-4 pb-2 flex flex-col items-center flex-shrink-0">
                            <!-- Header Title Line -->
                            <div class="w-full flex items-center justify-center relative mb-1.5">
                                <span class="text-xs font-bold text-gray-900 tracking-tight">Review payment</span>
                            </div>

                            <!-- BIBD Big Logo -->
                            <div class="flex flex-col items-center justify-center my-0.5">
                                <img src="/logo-terbaru-bibd-copy.png" alt="BIBD" class="h-10 object-contain drop-shadow-xs" onerror="this.src='/bibdbrunei_logo.jpg'">
                            </div>

                            <!-- Dual Cards Visualizer -->
                            <div class="w-full mt-2 flex items-center justify-between gap-2 relative">
                                <!-- Sender Card -->
                                <div class="flex-1 h-[105px] bg-[#e1edea] rounded-[18px] p-2 flex flex-col items-center justify-center text-center border border-[#d2deda] shadow-xs">
                                    <div class="w-8 h-8 rounded-full mb-1 overflow-hidden shadow-xs">
                                        <img src="/bibd-icon.png" alt="BIBD" class="w-full h-full object-cover">
                                    </div>
                                    <p id="prevSenderName1" class="font-bold text-[11px] text-[#1a1c1e] tracking-tight truncate w-full max-w-[105px]">
                                        {data.get('senderName', 'TUBAGUS IQBAL HUSAENI')}
                                    </p>
                                    <p id="prevSenderAcc1" class="text-[9.5px] text-[#78828a] mt-0.5 truncate w-full max-w-[105px]">
                                        {data.get('senderBank', 'BIBD')} · {str(data.get('senderAccount', '6457'))[-4:]}
                                    </p>
                                </div>

                                <!-- Arrow Divider Badge -->
                                <div class="w-5 h-5 rounded-full bg-[#dbe7e4] border border-[#cedbd7] flex items-center justify-center flex-shrink-0 text-[#536066] -mx-1 z-10 text-[10px]">
                                    →
                                </div>

                                <!-- Receiver Card -->
                                <div class="flex-1 h-[105px] bg-[#e1edea] rounded-[18px] p-2 flex flex-col items-center justify-center text-center border border-[#d2deda] shadow-xs">
                                    <div class="w-8 h-8 rounded-full mb-1 overflow-hidden shadow-xs bg-white flex items-center justify-center">
                                        <img id="prevReceiverLogo1" src="/{'qris-icon.png' if logo_val == 'qris' else ('gopay-icon.png' if logo_val == 'gopay' else 'dana-icon.png')}" alt="Provider" class="w-full h-full object-cover">
                                    </div>
                                    <p id="prevReceiverName1" class="font-bold text-[11px] text-[#1a1c1e] tracking-tight truncate w-full max-w-[105px]">
                                        {data.get('receiverName', 'ABDUL AZIS')}
                                    </p>
                                    <p id="prevReceiverAcc1" class="text-[9.5px] text-[#78828a] mt-0.5 truncate w-full max-w-[105px]">
                                        {data.get('receiverBank', 'DANA')} · {str(data.get('receiverAccount', '2642'))[-4:]}
                                    </p>
                                </div>
                            </div>
                        </div>

                        <!-- White Bottom Sheet -->
                        <div class="flex-1 bg-white rounded-t-[26px] px-4 pt-2.5 pb-3 shadow-md flex flex-col justify-between border-t border-[#d8e2e0] overflow-hidden">
                            <div class="space-y-1.5 my-auto">
                                <!-- Sender Row -->
                                <div class="flex items-center justify-between text-[11px]">
                                    <div class="flex items-center gap-1.5 text-gray-500 font-medium">
                                        <span class="w-4 h-4 rounded-full bg-[#84919a] text-white flex items-center justify-center text-[9px]">↑</span>
                                        <span>Sender</span>
                                    </div>
                                    <div class="flex items-center gap-1 font-bold text-gray-900 text-[11px]">
                                        <img src="/bibd-icon.png" alt="BIBD" class="w-4 h-4 rounded-full object-cover shadow-2xs">
                                        <span id="prevSenderName2" class="truncate max-w-[120px]">{data.get('senderName', 'TUBAGUS IQBAL HUSAENI')}</span>
                                    </div>
                                </div>

                                <!-- Recipient Row -->
                                <div class="flex items-center justify-between text-[11px]">
                                    <div class="flex items-center gap-1.5 text-gray-500 font-medium">
                                        <span class="w-4 h-4 rounded-full bg-[#84919a] text-white flex items-center justify-center text-[9px]">↓</span>
                                        <span>Recipient</span>
                                    </div>
                                    <div class="flex items-center gap-1 font-bold text-gray-900 text-[11px]">
                                        <img id="prevReceiverLogo2" src="/{'qris-icon.png' if logo_val == 'qris' else ('gopay-icon.png' if logo_val == 'gopay' else 'dana-icon.png')}" alt="Provider" class="w-4 h-4 rounded-full object-cover shadow-2xs">
                                        <span id="prevReceiverName2" class="truncate max-w-[120px]">{data.get('receiverName', 'ABDUL AZIS')}</span>
                                    </div>
                                </div>

                                <!-- Total Pay Amount Row -->
                                <div class="flex items-center justify-between text-[11px] pb-1 border-b border-gray-100">
                                    <div class="flex items-center gap-1.5 text-gray-500 font-medium">
                                        <span class="w-4 h-4 rounded-full bg-[#84919a] text-white flex items-center justify-center text-[9px]">$</span>
                                        <span>Total pay amount</span>
                                    </div>
                                    <span id="prevAmount1" class="font-bold text-gray-900 text-[12px]">{data.get('amountPrimary', 'IDR 10.000')}</span>
                                </div>

                                <!-- Breakdown Card -->
                                <div class="bg-[#f8faf9] rounded-xl p-2 border border-[#d2d9df] text-[10px] space-y-1 my-1 shadow-2xs">
                                    <div class="flex items-center justify-between pb-1 border-b border-gray-200">
                                        <span class="text-[9px] font-bold text-gray-500 uppercase tracking-wider">Rincian Pemindahan Dana</span>
                                        <span class="text-[8.5px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded-full border border-emerald-200">
                                            Terverifikasi
                                        </span>
                                    </div>
                                    <div class="flex justify-between items-center text-gray-600">
                                        <span>Akun Pengirim</span>
                                        <span id="prevSenderAccFull" class="font-semibold text-gray-900 truncate max-w-[130px]">{data.get('senderBank', 'BIBD')} · {data.get('senderAccount', 'BND33...')}</span>
                                    </div>
                                    <div class="flex justify-between items-center text-gray-600">
                                        <span>Akun Penerima</span>
                                        <span id="prevReceiverAccFull" class="font-semibold text-gray-900 truncate max-w-[130px]">{data.get('receiverBank', 'DANA')} · {data.get('receiverAccount', '0821...')}</span>
                                    </div>
                                    <div class="flex justify-between items-center text-gray-600 pt-0.5 border-t border-gray-100">
                                        <span>Nominal Asal (BND)</span>
                                        <span id="prevAmountSec1" class="font-semibold text-gray-900">{data.get('amountSecondary', 'BND 0,72')}</span>
                                    </div>
                                    <div class="flex justify-between items-center text-gray-600">
                                        <span>Biaya Layanan</span>
                                        <span class="font-bold text-emerald-600">GRATIS (BND 0,00)</span>
                                    </div>
                                    <div class="flex justify-between items-center text-gray-600">
                                        <span>No. Rujukan</span>
                                        <span id="prevRef" class="font-mono text-gray-800">{data.get('receiptReference', '056868540003')}</span>
                                    </div>
                                </div>
                            </div>

                            <!-- Bottom Bar & Black Button -->
                            <div class="pt-1.5 flex flex-col gap-1.5">
                                <div class="flex justify-between items-baseline px-0.5">
                                    <span class="text-[11px] font-medium text-gray-500">Total diterima</span>
                                    <div class="text-right">
                                        <div id="prevAmount2" class="font-extrabold text-[13px] text-gray-900 leading-none">{data.get('amountPrimary', 'IDR 10.000')}</div>
                                        <div id="prevAmountSec2" class="text-[9.5px] text-gray-400 mt-0.5">({data.get('amountSecondary', 'BND 0,72')})</div>
                                    </div>
                                </div>
                                <button type="button" class="w-full bg-black text-white font-bold text-[10.5px] py-2 rounded-xl text-center shadow-xs">
                                    AMBIL FOTO RESIT / BUKTI
                                </button>
                            </div>
                        </div>

                    </div>
                </div>
            </div>

        </div>
    </main>

    <!-- Save Overlay Feedback -->
    <div id="saveOverlay" class="fixed inset-0 bg-black/90 backdrop-blur-sm hidden flex items-center justify-center z-50 p-4">
        <div class="bg-slate-900 border border-teal-500/40 p-6 rounded-2xl max-w-sm w-full text-center space-y-3 shadow-2xl">
            <div class="w-12 h-12 rounded-full bg-teal-500/20 text-teal-400 flex items-center justify-center mx-auto text-2xl animate-bounce">
                ✓
            </div>
            <h3 class="text-base font-bold text-white">DATA BERHASIL DISIMPAN!</h3>
            <p class="text-xs text-slate-400 leading-relaxed">Parameter tampilan telah diperbarui. Jendela browser dapat ditutup, proses build akan otomatis dilanjutkan di terminal.</p>
            <div class="pt-2">
                <span class="text-[11px] font-mono text-teal-400 animate-pulse">Menutup browser dalam 2 detik...</span>
            </div>
        </div>
    </div>

    <script>
        function getSelectedLogo() {{
            const rad = document.querySelector('input[name="transactionLogo"]:checked');
            return rad ? rad.value.toLowerCase() : 'dana';
        }}

        function updatePreview() {{
            const logo = getSelectedLogo();
            const senderName = document.getElementById('senderName').value.trim() || 'PENGIRIM';
            const senderBank = document.getElementById('senderBank').value.trim() || 'BIBD';
            const senderAcc = document.getElementById('senderAccount').value.trim() || '0000';
            const receiverName = document.getElementById('receiverName').value.trim() || 'PENERIMA';
            const receiverBank = document.getElementById('receiverBank').value.trim() || (logo === 'qris' ? 'QRIS' : (logo === 'gopay' ? 'GOPAY' : 'DANA'));
            const receiverAcc = document.getElementById('receiverAccount').value.trim() || '0000';
            const amountPrimary = document.getElementById('amountPrimary').value.trim() || 'IDR 0';
            const amountSec = document.getElementById('amountSecondary').value.trim() || 'BND 0,00';
            const ref = document.getElementById('receiptReference').value.trim() || '000000000000';

            // Update badge logo
            const activeBadge = document.getElementById('activeLogoBadge');
            if (activeBadge) {{
                activeBadge.textContent = logo.toUpperCase() + ' AKTIF';
                if (logo === 'qris') {{
                    activeBadge.className = 'text-xs font-bold font-mono px-2.5 py-1 rounded-full uppercase bg-emerald-500/10 text-emerald-400 border border-emerald-500/30';
                }} else if (logo === 'gopay') {{
                    activeBadge.className = 'text-xs font-bold font-mono px-2.5 py-1 rounded-full uppercase bg-cyan-500/10 text-cyan-400 border border-cyan-500/30';
                }} else {{
                    activeBadge.className = 'text-xs font-bold font-mono px-2.5 py-1 rounded-full uppercase bg-blue-500/10 text-blue-400 border border-blue-500/30';
                }}
            }}

            // Logos in preview
            let logoSrc = '/dana-icon.png';
            if (logo === 'qris') logoSrc = '/qris-icon.png';
            else if (logo === 'gopay') logoSrc = '/gopay-icon.png';
            document.getElementById('prevReceiverLogo1').src = logoSrc;
            document.getElementById('prevReceiverLogo2').src = logoSrc;

            // Sender updates
            document.getElementById('prevSenderName1').textContent = senderName;
            document.getElementById('prevSenderName2').textContent = senderName;
            const sender4 = senderAcc.slice(-4) || '6457';
            document.getElementById('prevSenderAcc1').textContent = senderBank + ' · ' + sender4;
            document.getElementById('prevSenderAccFull').textContent = senderBank + ' · ' + senderAcc;

            // Receiver updates
            document.getElementById('prevReceiverName1').textContent = receiverName;
            document.getElementById('prevReceiverName2').textContent = receiverName;
            const receiver4 = receiverAcc.slice(-4) || '2642';
            document.getElementById('prevReceiverAcc1').textContent = receiverBank + ' · ' + receiver4;
            document.getElementById('prevReceiverAccFull').textContent = receiverBank + ' · ' + receiverAcc;

            // Amounts
            document.getElementById('prevAmount1').textContent = amountPrimary;
            document.getElementById('prevAmount2').textContent = amountPrimary;
            document.getElementById('prevAmountSec1').textContent = amountSec;
            document.getElementById('prevAmountSec2').textContent = '(' + amountSec + ')';

            // Reference
            document.getElementById('prevRef').textContent = ref;

            // Auto sync receipt modal inputs if enabled
            const autoSync = document.getElementById('autoSyncReceipt');
            if (autoSync && autoSync.checked) {{
                document.getElementById('receiptAmount').value = amountPrimary;
                document.getElementById('receiptSenderName').value = senderName;
                document.getElementById('receiptSenderAccount').value = '(****' + sender4 + ')';
                document.getElementById('receiptReceiverName').value = receiverName;
                document.getElementById('receiptReceiverAccount').value = '(****' + receiver4 + ')';
            }}
        }}

        const IDR_TO_BND_RATE = 0.000072; // 10.000 IDR = 0,72 BND (1 BND ≈ 13.888,89 IDR)
        let isConverting = false;

        function parseIdrNum(val) {{
            if (!val) return 0;
            const digits = val.toString().replace(/[^0-9]/g, '');
            return digits ? parseInt(digits, 10) : 0;
        }}

        function formatIdr(num) {{
            return 'IDR ' + num.toLocaleString('id-ID');
        }}

        function formatBnd(num) {{
            return 'BND ' + num.toFixed(2).replace('.', ',');
        }}

        function convertIdrToBnd(autoFormat = false) {{
            if (isConverting) return;
            isConverting = true;
            try {{
                const idrInput = document.getElementById('amountPrimary');
                const bndInput = document.getElementById('amountSecondary');
                const num = parseIdrNum(idrInput.value);

                if (num > 0) {{
                    const bnd = num * IDR_TO_BND_RATE;
                    bndInput.value = formatBnd(bnd);
                    if (autoFormat) {{
                        idrInput.value = formatIdr(num);
                    }}
                }} else if (idrInput.value.trim() === '') {{
                    bndInput.value = 'BND 0,00';
                }}
            }} finally {{
                isConverting = false;
            }}
            updatePreview();
        }}

        function convertBndToIdr() {{
            if (isConverting) return;
            isConverting = true;
            try {{
                const bndInput = document.getElementById('amountSecondary');
                const idrInput = document.getElementById('amountPrimary');
                const cleaned = bndInput.value.replace(/[^0-9.,]/g, '').replace(',', '.');
                const bndNum = parseFloat(cleaned);

                if (!isNaN(bndNum) && bndNum > 0) {{
                    const idrNum = Math.round(bndNum / IDR_TO_BND_RATE);
                    idrInput.value = formatIdr(idrNum);
                }}
            }} finally {{
                isConverting = false;
            }}
            updatePreview();
        }}

        function setQuickNominal(num) {{
            const idrInput = document.getElementById('amountPrimary');
            idrInput.value = formatIdr(num);
            convertIdrToBnd(false);
        }}

        // Listen for live input changes
        document.querySelectorAll('#editForm input').forEach(el => {{
            if (el.id !== 'amountPrimary' && el.id !== 'amountSecondary') {{
                el.addEventListener('input', updatePreview);
                el.addEventListener('change', updatePreview);
            }}
        }});

        // Dedicated listeners for currency conversion
        const idrEl = document.getElementById('amountPrimary');
        idrEl.addEventListener('input', () => convertIdrToBnd(false));
        idrEl.addEventListener('blur', () => convertIdrToBnd(true));

        const bndEl = document.getElementById('amountSecondary');
        bndEl.addEventListener('input', convertBndToIdr);

        // Change receiverBank automatically when logo radio is clicked
        document.querySelectorAll('input[name="transactionLogo"]').forEach(radio => {{
            radio.addEventListener('change', (e) => {{
                const val = e.target.value;
                const bankInput = document.getElementById('receiverBank');
                if (val === 'qris' && (bankInput.value === 'DANA' || bankInput.value === 'GOPAY' || bankInput.value === '')) {{
                    bankInput.value = 'QRIS';
                }} else if (val === 'dana' && (bankInput.value === 'QRIS' || bankInput.value === 'GOPAY' || bankInput.value === '')) {{
                    bankInput.value = 'DANA';
                }} else if (val === 'gopay' && (bankInput.value === 'QRIS' || bankInput.value === 'DANA' || bankInput.value === '')) {{
                    bankInput.value = 'GOPAY';
                }}
                updatePreview();
            }});
        }});

        function applyPreset(type) {{
            if (type === 'dana') {{
                document.querySelector('input[name="transactionLogo"][value="dana"]').checked = true;
                document.getElementById('receiverBank').value = 'DANA';
                document.getElementById('receiverAccount').value = '0821-2469-2642';
                setQuickNominal(10000);
            }} else if (type === 'qris') {{
                document.querySelector('input[name="transactionLogo"][value="qris"]').checked = true;
                document.getElementById('receiverBank').value = 'QRIS';
                document.getElementById('receiverAccount').value = '0821-2469-2642';
                setQuickNominal(50000);
            }} else if (type === 'gopay') {{
                document.querySelector('input[name="transactionLogo"][value="gopay"]').checked = true;
                document.getElementById('receiverBank').value = 'GOPAY';
                document.getElementById('receiverAccount').value = '0821-2469-2642';
                setQuickNominal(20000);
            }}
            updatePreview();
        }}

        function randomizeRef() {{
            const rand = Math.floor(10000000 + Math.random() * 90000000);
            document.getElementById('receiptReference').value = '0568' + rand;
            updatePreview();
        }}

        function toggleReceiptSection() {{
            const fields = document.getElementById('receiptFields');
            const chev = document.getElementById('receiptChevron');
            if (fields.classList.contains('hidden')) {{
                fields.classList.remove('hidden');
                chev.style.transform = 'rotate(180deg)';
            }} else {{
                fields.classList.add('hidden');
                chev.style.transform = 'rotate(0deg)';
            }}
        }}

        async function cancelDashboard() {{
            if (confirm('Batal edit dan langsung lanjutkan proses ke terminal?')) {{
                try {{
                    await fetch('/cancel', {{ method: 'POST' }});
                }} catch (e) {{}}
                window.close();
            }}
        }}

        // Handle Save
        document.getElementById('editForm').addEventListener('submit', async (e) => {{
            e.preventDefault();
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData.entries());

            // Pastikan transactionLogo ada
            data.transactionLogo = getSelectedLogo();

            document.getElementById('saveOverlay').classList.remove('hidden');

            try {{
                const res = await fetch('/save', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(data)
                }});

                if (res.ok) {{
                    setTimeout(() => {{
                        window.close();
                    }}, 1200);
                }} else {{
                    const err = await res.json().catch(() => ({{}}));
                    alert('Gagal menyimpan perubahan: ' + (err.message || 'Terjadi kesalahan'));
                    document.getElementById('saveOverlay').classList.add('hidden');
                }}
            }} catch (err) {{
                // Server exiting quickly after saving can cause fetch disconnect; treated as success
                setTimeout(() => {{
                    window.close();
                }}, 1000);
            }}
        }});

        // Initial preview render
        updatePreview();
    </script>
</body>
</html>
"""
            self.wfile.write(html.encode('utf-8'))
            return

        super().do_GET()

    def do_POST(self):
        if self.path == '/save':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)

            try:
                new_data = json.loads(post_data.decode('utf-8'))
                save_data(new_data)

                resp = json.dumps({"status": "success"}).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(resp)))
                self.send_header('Connection', 'close')
                self.end_headers()
                self.wfile.write(resp)
                self.wfile.flush()

                print("\n  [+] Perubahan data berhasil disimpan dari dashboard!")
                print("  [+] Menutup dashboard editor dan melanjutkan proses...")
                trigger_shutdown(0.4)

            except Exception as e:
                err_body = json.dumps({"status": "error", "message": str(e)}).encode('utf-8')
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(err_body)))
                self.send_header('Connection', 'close')
                self.end_headers()
                self.wfile.write(err_body)
                self.wfile.flush()

        elif self.path == '/cancel':
            resp = json.dumps({"status": "cancelled"}).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(resp)))
            self.send_header('Connection', 'close')
            self.end_headers()
            self.wfile.write(resp)
            self.wfile.flush()

            print("\n  [*] Edit dibatalkan dari dashboard.")
            print("  [*] Melanjutkan proses di terminal...")
            trigger_shutdown(0.3)


def trigger_shutdown(delay=0.5):
    """Force exit setelah delay agar HTTP response sempat terkirim ke browser."""
    def _force_exit():
        time.sleep(delay)
        os._exit(0)

    t = threading.Thread(target=_force_exit)
    t.daemon = False  # non-daemon agar tidak dimatikan sebelum sempat jalan
    t.start()


class QuietServer(socketserver.TCPServer):
    allow_reuse_address = True
    def handle_error(self, request, client_address):
        pass

http.server.SimpleHTTPRequestHandler.log_message = lambda *args: None

if __name__ == '__main__':
    print(f"\n========================================================")
    print(f"  METACYTECH // LOCAL DASHBOARD EDITOR")
    print(f"========================================================")
    print(f"  Membuka browser di http://localhost:{PORT}")
    print(f"  Live smartphone preview aktif.")
    print(f"  Setelah klik 'SIMPAN & TERAPKAN', server ini akan otomatis selesai.")
    print(f"========================================================\n")

    webbrowser.open(f"http://localhost:{PORT}")

    with QuietServer(("", PORT), DashboardHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nDashboard ditutup.")
            sys.exit(0)
