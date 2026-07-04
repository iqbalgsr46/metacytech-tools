"use client";

export default function LoadingScreen() {
  return (
    <main className="flex-grow flex flex-col items-center justify-center w-full px-5 md:px-16 animate-fade-in relative z-10 min-h-screen bg-white">
      {/* Logo Container */}
      <div className="mb-8 relative animate-pulse-slow">
        <img
          alt="BDCB Logo"
          className="w-64 h-auto md:w-80 object-contain mx-auto transition-transform duration-500 hover:scale-105"
          src="https://lh3.googleusercontent.com/aida-public/AB6AXuATBmsIEarjki0ZhY-adi499onA6rI28KBoXWTxJj02TDaNHsvs9gLexMbCpj5yGG_VZ860RM-o4JoIBryRbnnHHEcoQRP7KfdI_4DOsLzhzZL2zmON-kKtdJcdtnXx_8_wix01GScSZrg2G0fm4Da5oRZIUOVm5iqVscvrwm9lAi-GEiZR0LXXncXsaXssIKoN0xlzzrKRiQxcIb8rH6JefP3xrLysqwbpg_h82sA-Q2TLq9MTxWHqgMI6bTE_cZOxcEsGHDZ_dfE"
        />
        {/* Subtle glow effect behind logo */}
        <div className="absolute inset-0 bg-[#66004d] opacity-5 blur-3xl rounded-full -z-10"></div>
      </div>

      {/* Loading Indicator */}
      <div className="mt-8 flex flex-col items-center">
        <span className="loader shadow-sm"></span>
      </div>

      <style jsx>{`
        .loader {
          width: 48px;
          height: 48px;
          border: 3px solid rgba(102, 0, 77, 0.1);
          border-bottom-color: #66004d;
          border-radius: 50%;
          display: inline-block;
          box-sizing: border-box;
          animation: rotation 1s linear infinite;
        }

        @keyframes rotation {
          0% {
            transform: rotate(0deg);
          }
          100% {
            transform: rotate(360deg);
          }
        }

        @keyframes fadeIn {
          0% {
            opacity: 0;
            transform: translateY(10px);
          }
          100% {
            opacity: 1;
            transform: translateY(0);
          }
        }

        .animate-fade-in {
          animation: fadeIn 1s ease-out;
        }

        .animate-pulse-slow {
          animation: pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }

        @keyframes pulse {
          0%,
          100% {
            opacity: 1;
          }
          50% {
            opacity: 0.8;
          }
        }
      `}</style>
    </main>
  );
}
