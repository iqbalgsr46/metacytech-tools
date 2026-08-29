"use client";

import React from 'react';

export default function DataBjorkaPage() {
  return (
    <main className="min-h-screen bg-[#0a0a0a] flex flex-col items-center justify-center p-4 sm:p-8 font-mono relative overflow-hidden">
      {/* Background Matrix/Hacker Effect */}
      <div className="absolute inset-0 opacity-10 pointer-events-none" style={{
        backgroundImage: 'linear-gradient(rgba(0, 255, 0, 0.2) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 255, 0, 0.2) 1px, transparent 1px)',
        backgroundSize: '20px 20px'
      }}></div>
      
      <div className="z-10 w-full max-w-4xl flex flex-col items-center animate-fade-slide">
        
        {/* Header */}
        <div className="w-full flex items-center justify-center mb-6">
          <h1 className="text-red-500 text-2xl sm:text-4xl font-bold tracking-widest text-center" style={{ textShadow: '0 0 10px rgba(239, 68, 68, 0.8)' }}>
            PERINGATAN: PERANGKAT ANDA TELAH KAMI RETAS!
          </h1>
        </div>
        
        {/* Image Container */}
        <div className="w-full relative bg-black border border-red-500/50 rounded-lg p-2 shadow-[0_0_30px_rgba(239,68,68,0.2)]">
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-red-500 to-transparent opacity-50"></div>
          <img 
            src="/bjorka.webp" 
            alt="Bjorka Data BPJS" 
            className="w-full h-auto object-contain rounded filter contrast-125"
          />
          <div className="absolute bottom-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-red-500 to-transparent opacity-50"></div>
        </div>
        
        {/* Footer info */}
        <div className="mt-8 flex flex-col items-center text-green-500 text-center gap-4">
          <p className="text-lg sm:text-xl font-bold animate-pulse text-red-500">MENGUNDUH SELURUH KONTAK, FOTO, DAN DATA REKENING...</p>
          <div className="font-mono text-sm opacity-90 mt-2 max-w-lg space-y-2">
            <p>JANGAN MENCOBA KABUR ATAU MEMATIKAN PERANGKAT INI!</p>
            <p>Kemanapun Anda pergi, lokasi GPS Anda akan tetap terpantau secara real-time. Data kependudukan berdasarkan Kartu Keluarga (KK) Anda telah diretas. Kami mengetahui secara pasti identitas, alamat, dan data pribadi seluruh anggota keluarga Anda.</p>
            <p className="text-red-400 font-bold">Seluruh aktivitas ilegal Anda telah kami rekam dan akan diteruskan ke Kepolisian. Anda akan segera dijemput paksa dan diproses hukum dalam waktu 1x24 jam.</p>
          </div>
        </div>

      </div>
    </main>
  );
}
