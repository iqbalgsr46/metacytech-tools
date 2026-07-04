/**
 * Premium background with large Arabic branding hero section.
 */
'use client';

export default function Background() {
  return (
    <div className="fixed inset-0 w-full h-full z-0 overflow-hidden">
      {/* Deep dark navy base */}
      <div className="absolute inset-0 bg-[#07152B]" />

      {/* Large Arabic brand image at the very top — full width */}
      <div
        className="absolute top-0 left-0 right-0 h-[320px] sm:h-[380px] md:h-[420px] overflow-hidden"
        style={{ zIndex: 1 }}
      >
        <img
          src="/bidbimgarb.png"
          alt="BIDB Brunei Darussalam"
          className="w-full h-full object-cover object-center"
          style={{ objectPosition: 'center top' }}
        />
        {/* Gradient overlay: top part stays clear, fades to dark navy */}
        <div
          className="absolute inset-0"
          style={{
            background:
              'linear-gradient(to bottom, rgba(7,21,43,0.10) 0%, rgba(7,21,43,0.30) 40%, rgba(7,21,43,0.85) 75%, #07152B 100%)',
          }}
        />
      </div>

      {/* Bottom gradient rest of page */}
      <div
        className="absolute left-0 right-0 bottom-0"
        style={{
          top: '320px',
          background: '#07152B',
          zIndex: 1,
        }}
      />

      {/* Subtle gold shimmer decorative line below hero */}
      <div
        className="absolute left-0 right-0 h-[2px]"
        style={{
          top: '316px',
          background: 'linear-gradient(90deg, transparent, #c5a059 30%, #e8c97b 50%, #c5a059 70%, transparent)',
          opacity: 0.6,
          zIndex: 2,
        }}
      />

      {/* Large soft glow orb — bottom center for depth */}
      <div
        className="absolute rounded-full"
        style={{
          width: 600,
          height: 600,
          bottom: -200,
          left: '50%',
          transform: 'translateX(-50%)',
          background: 'radial-gradient(circle, rgba(197,160,89,0.10) 0%, transparent 70%)',
          zIndex: 1,
        }}
      />
    </div>
  );
}
