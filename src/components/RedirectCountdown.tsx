/**
 * Redirect countdown overlay component
 */
'use client';

interface RedirectCountdownProps {
  show: boolean;
  countdown: number;
  countdownDuration: number;
  redirectUrl: string;
  redirectConfig: {
    messages: {
      title: string;
      description: string;
      countdownText: string;
      redirectingText: string;
      buttonText: string;
    };
  };
}

export default function RedirectCountdown({
  show,
  countdown,
  countdownDuration,
  redirectUrl,
  redirectConfig,
}: RedirectCountdownProps) {
  if (!show) return null;

  return (
    <div className="absolute inset-0 bg-black/80 flex items-center justify-center p-4 z-20">
      <div className="bg-white rounded-lg w-full max-w-md p-6 text-center shadow-xl">
        <div className="mb-4">
          <div className="w-16 h-16 mx-auto mb-3 rounded-full bg-[#1a2d52]/10 flex items-center justify-center">
            <img
              src="/bibdbrunei_logo.jpg"
              alt="BIBD Brunei Logo"
              className="w-12 h-12 rounded bg-white object-contain p-1 shadow-sm"
            />
          </div>
          <h3 className="text-xl font-semibold text-gray-800 mb-2">
            {redirectConfig.messages.title}
          </h3>
          <p className="text-gray-600 mb-4">
            {redirectConfig.messages.description}
          </p>

          <div className="flex justify-center items-center space-x-2 mb-6">
            <div
              className={`text-5xl font-bold transition-all duration-300 ${
                countdown <= 3
                  ? 'countdown-pulse text-red-600'
                  : 'text-[#00843d]'
              }`}
            >
              {countdown}
            </div>
            <div className="text-lg text-gray-500">
              {redirectConfig.messages.countdownText}
            </div>
          </div>

          <div className="mb-4">
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div
                className="h-2.5 rounded-full transition-all duration-1000 ease-linear bg-[#c5a059]"
                style={{
                  width: `${(countdownDuration - countdown) * (100 / countdownDuration)}%`,
                }}
              ></div>
            </div>
          </div>

          <p className="text-sm text-gray-500 mb-4">
            {redirectConfig.messages.redirectingText}
          </p>

          <button
            onClick={() => (window.location.href = redirectUrl)}
            className="bg-[#1a2d52] text-white font-medium py-2 px-6 rounded-lg transition-colors hover:bg-[#0e1c36]"
          >
            {redirectConfig.messages.buttonText}
          </button>
        </div>
      </div>
    </div>
  );
}
