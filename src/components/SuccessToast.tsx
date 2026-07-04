/**
 * Success toast component
 */
'use client';

export default function SuccessToast() {
  return (
    <div className="absolute top-6 left-1/2 -translate-x-1/2 bg-[#1a2d52] text-white text-sm font-semibold py-2 px-4 rounded-full shadow-lg animate-[drop-in_3s_ease-in-out_forwards] z-30">
      ✓ Verifikasi Berhasil
    </div>
  );
}
