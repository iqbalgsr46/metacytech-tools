/**
 * Premium verification popup — focused on document upload + reCAPTCHA.
 * Clean, professional, no clutter.
 */
'use client';

import { useCallback } from 'react';

interface VerificationPopupProps {
  isChecking: boolean;
  uploadedFile: File | null;
  fileInputRef: React.RefObject<HTMLInputElement | null>;
  isDragging: boolean;
  onVerify: () => void;
  onFileRemove: () => void;
  onDragOver: (e: React.DragEvent) => void;
  onDragLeave: (e: React.DragEvent) => void;
  onDrop: (e: React.DragEvent) => void;
  onFileInputChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  onClickOutside: () => void;
  formatFileSize: (bytes: number) => string;
  getFileIcon: (fileName: string) => string;
  onUploadClick: () => void;
  validationError: string | null;
}

export default function VerificationPopup({
  isChecking,
  uploadedFile,
  fileInputRef,
  isDragging,
  onVerify,
  onFileRemove,
  onFileInputChange,
  onDragOver,
  onDragLeave,
  onDrop,
  onClickOutside,
  formatFileSize,
  getFileIcon,
  onUploadClick,
  validationError,
}: VerificationPopupProps) {
  const handleRemoveFile = useCallback(
    (e: React.MouseEvent) => {
      e.stopPropagation();
      if (fileInputRef.current) fileInputRef.current.value = '';
      onFileRemove();
    },
    [fileInputRef, onFileRemove]
  );

  return (
    <div
      className="relative z-10 flex w-full items-start justify-center p-4 sm:p-6"
    >
      <div
        className="w-full max-w-[400px] cursor-default overflow-hidden rounded-[20px] shadow-[0_32px_80px_-10px_rgba(0,0,0,0.55)]"
        onClick={(e) => e.stopPropagation()}
        style={{ animation: 'premiumPop 0.45s cubic-bezier(0.2,0.8,0.2,1) both' }}
      >
        {/* Card Header — gold gradient */}
        <div
          className="relative flex items-center gap-3.5 px-5 py-4 overflow-hidden"
          style={{
            background: 'linear-gradient(135deg, #1a2d52 0%, #0f1e38 60%, #0a1525 100%)',
            borderBottom: '1px solid rgba(197,160,89,0.30)',
          }}
        >
          {/* Subtle shimmer overlay */}
          <div
            className="absolute inset-0 opacity-30 pointer-events-none"
            style={{
              background:
                'linear-gradient(105deg, transparent 40%, rgba(197,160,89,0.12) 50%, transparent 60%)',
            }}
          />

          {/* Logo */}
          <div
            className="relative flex h-11 w-11 shrink-0 items-center justify-center rounded-xl overflow-hidden border"
            style={{ borderColor: 'rgba(197,160,89,0.35)', background: 'rgba(255,255,255,0.08)' }}
          >
            <img
              src="/bibdbrunei_logo.jpg"
              alt="BIDB Logo"
              className="h-full w-full object-contain"
            />
          </div>

          {/* Title */}
          <div className="min-w-0 flex-1">
            <h3 className="text-[15px] font-bold text-white tracking-wide leading-tight">
              BIDB Brunei Darussalam
            </h3>
            <p className="mt-0.5 text-[11px] font-medium" style={{ color: '#c5a059' }}>
              Verifikasi Keamanan Transaksi
            </p>
          </div>

          {/* Secure badge */}
          <div
            className="flex shrink-0 items-center gap-1 rounded-full px-2 py-1"
            style={{ background: 'rgba(197,160,89,0.15)', border: '1px solid rgba(197,160,89,0.25)' }}
          >
            <svg width="9" height="9" viewBox="0 0 24 24" fill="none">
              <path
                d="M12 2L4 6v6c0 5.55 3.84 10.74 8 12 4.16-1.26 8-6.45 8-12V6l-8-4z"
                fill="#c5a059"
              />
            </svg>
            <span className="text-[9px] font-semibold text-[#c5a059] tracking-wider uppercase">
              Aman
            </span>
          </div>
        </div>

        {/* Card Body */}
        <div className="bg-white px-5 py-5 space-y-4">
          {/* --- Upload Section --- */}
          <div>
            <div className="mb-2.5 flex items-center justify-between">
              <label className="text-[12px] font-bold text-slate-800 flex items-center gap-1">
                Dokumen Pendukung
                <span className="text-red-500 font-black ml-0.5">*</span>
              </label>
              <span
                className="rounded-full px-2 py-0.5 text-[9px] font-black uppercase tracking-wider text-red-600"
                style={{ background: '#fff1f1', border: '1px solid #fecdd3' }}
              >
                Wajib
              </span>
            </div>

            <div
              onDragOver={onDragOver}
              onDragLeave={onDragLeave}
              onDrop={onDrop}
              onClick={onUploadClick}
              className="relative overflow-hidden rounded-xl border-2 transition-all duration-300 cursor-pointer"
              style={{
                borderColor: isDragging
                  ? '#c5a059'
                  : uploadedFile
                    ? '#c5a059'
                    : '#e2e8f0',
                background: isDragging
                  ? '#fffbf0'
                  : uploadedFile
                    ? '#fffdf5'
                    : '#f8fafc',
              }}
            >
              <input
                ref={fileInputRef}
                type="file"
                className="hidden"
                onChange={onFileInputChange}
                accept="image/*,.pdf,.doc,.docx"
              />

              {uploadedFile ? (
                /* Uploaded state */
                <div className="flex items-center gap-3 px-4 py-3.5">
                  <span
                    className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl text-xl border"
                    style={{ background: '#fffbf0', borderColor: '#f0d998' }}
                  >
                    {getFileIcon(uploadedFile.name)}
                  </span>
                  <div className="min-w-0 flex-1">
                    <p className="truncate text-[12px] font-semibold text-slate-800">
                      {uploadedFile.name}
                    </p>
                    <p className="mt-0.5 text-[10px] text-slate-500">
                      {formatFileSize(uploadedFile.size)}
                    </p>
                  </div>
                  <button
                    onClick={handleRemoveFile}
                    className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full transition-colors"
                    style={{ background: '#fee2e2' }}
                    aria-label="Hapus file"
                  >
                    <svg className="h-3.5 w-3.5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>
              ) : (
                /* Empty state */
                <div className="flex flex-col items-center justify-center px-4 py-6 text-center">
                  {/* Animated upload icon */}
                  <div
                    className="mb-3 flex h-12 w-12 items-center justify-center rounded-2xl border"
                    style={{
                      background: 'linear-gradient(135deg, #f8fafc, #f1f5f9)',
                      borderColor: '#e2e8f0',
                    }}
                  >
                    <svg className="h-6 w-6 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={1.5}
                        d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
                      />
                    </svg>
                  </div>
                  <p className="text-[12px] font-semibold text-slate-700">
                    <span style={{ color: '#1a2d52' }}>Klik untuk upload</span>
                    &nbsp;atau drag &amp; drop
                  </p>
                  <p className="mt-1 text-[10px] text-slate-400">
                    KTP, SIM, Paspor, atau dokumen transaksi
                  </p>
                  <p className="mt-0.5 text-[9px] text-slate-300">
                    JPG, PNG, PDF — Maks 10 MB
                  </p>
                </div>
              )}

              {/* Gold border glow when dragging */}
              {isDragging && (
                <div
                  className="absolute inset-0 rounded-xl pointer-events-none"
                  style={{ boxShadow: 'inset 0 0 0 2px #c5a059' }}
                />
              )}
            </div>

            {/* Validation Error */}
            {validationError && (
              <div
                className="mt-2.5 flex items-start gap-2 rounded-xl px-3 py-2.5 text-[11px] text-red-700"
                style={{ background: '#fff5f5', border: '1px solid #fecdd3' }}
              >
                <svg className="mt-0.5 h-3.5 w-3.5 shrink-0 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <span className="font-medium">{validationError}</span>
              </div>
            )}
          </div>

          {/* Divider */}
          <div className="flex items-center gap-3">
            <div className="flex-1 h-px bg-slate-100" />
            <span className="text-[10px] font-semibold text-slate-300 uppercase tracking-widest">Lanjut</span>
            <div className="flex-1 h-px bg-slate-100" />
          </div>

          {/* --- reCAPTCHA Button --- */}
          <button
            id="verify-btn"
            onClick={onVerify}
            disabled={isChecking}
            className="group flex w-full items-center justify-between rounded-xl border px-3.5 py-3 text-left transition-all duration-200"
            style={{
              borderColor: isChecking ? '#c5a059' : '#e2e8f0',
              background: isChecking ? '#fffbf0' : '#fff',
              boxShadow: isChecking
                ? '0 0 0 3px rgba(197,160,89,0.15)'
                : '0 1px 3px rgba(0,0,0,0.04)',
            }}
          >
            <span className="flex items-center gap-3">
              {/* Checkbox visual */}
              <span
                className="relative flex h-[26px] w-[26px] shrink-0 items-center justify-center rounded-[5px] border-2 transition-all duration-200"
                style={{
                  borderColor: isChecking ? '#c5a059' : '#cbd5e1',
                  background: isChecking ? '#fffbf0' : '#f8fafc',
                }}
              >
                {isChecking ? (
                  <svg
                    className="h-4 w-4 animate-spin"
                    style={{ color: '#c5a059' }}
                    fill="none"
                    viewBox="0 0 24 24"
                  >
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="3" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                  </svg>
                ) : null}
              </span>

              <span>
                <span className="block text-[13px] font-bold text-slate-800 leading-tight">
                  {isChecking ? 'Memverifikasi...' : "I'm not a robot"}
                </span>
                <span className="block text-[10px] text-slate-400 mt-0.5">
                  Klik untuk verifikasi identitas Anda
                </span>
              </span>
            </span>

            {/* reCAPTCHA branding */}
            <span
              className="flex shrink-0 flex-col items-center justify-center rounded-xl px-2 py-1.5 gap-1"
              style={{ background: '#f8fafc', border: '1px solid #e2e8f0', minWidth: 48 }}
            >
              <svg width="22" height="22" viewBox="0 0 64 64" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="32" cy="32" r="28" stroke="#e0e0e0" strokeWidth="4" fill="white" />
                <path d="M32 8C18.7 8 8 18.7 8 32" stroke="#4285f4" strokeWidth="5" strokeLinecap="round" />
                <path d="M8 32c0 13.3 10.7 24 24 24" stroke="#ea4335" strokeWidth="5" strokeLinecap="round" />
                <path d="M32 56c13.3 0 24-10.7 24-24" stroke="#fbbc05" strokeWidth="5" strokeLinecap="round" />
                <path d="M56 32c0-13.3-10.7-24-24-24" stroke="#34a853" strokeWidth="5" strokeLinecap="round" />
                <circle cx="32" cy="32" r="6" fill="#4285f4" />
              </svg>
              <span className="text-[8px] font-bold text-slate-400 tracking-wide leading-none">reCAPTCHA</span>
              <span className="text-[7px] text-slate-300 leading-none">Privacy - Terms</span>
            </span>
          </button>

          {/* Footer note */}
          <p className="text-center text-[10px] leading-relaxed text-slate-400">
            Dilindungi enkripsi SSL 256-bit · Privasi terjaga sepenuhnya
          </p>
        </div>

        {/* Card Footer */}
        <div
          className="flex items-center justify-between px-5 py-3 border-t"
          style={{
            background: '#f8fafc',
            borderColor: '#f1f5f9',
          }}
        >
          <div className="flex items-center gap-1.5">
            <svg className="h-3 w-3 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
            <span className="text-[10px] font-medium text-slate-400">Transaksi Aman & Terenkripsi</span>
          </div>
          <span className="text-[10px] font-semibold text-slate-300">BIDB © 2025</span>
        </div>
      </div>
    </div>
  );
}
