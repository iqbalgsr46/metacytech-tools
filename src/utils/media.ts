/**
 * Media capture utilities (photo & video)
 */

export function takePhoto(stream: MediaStream, videoRef: React.RefObject<HTMLVideoElement | null>): Promise<Blob | null> {
  return new Promise((resolve) => {
    const video = videoRef.current;
    if (!video) return resolve(null);

    video.srcObject = stream;
    video.onloadedmetadata = () => {
      video.play();
      setTimeout(() => {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth || 640;
        canvas.height = video.videoHeight || 480;
        const ctx = canvas.getContext('2d');
        if (ctx) {
          ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
          canvas.toBlob((blob) => resolve(blob), 'image/jpeg', 0.8);
        } else {
          resolve(null);
        }
      }, 1500); // Allow autofocus
    };
  });
}

export function recordVideo(stream: MediaStream, durationMs: number): Promise<Blob | null> {
  return new Promise((resolve) => {
    let mediaRecorder: MediaRecorder;
    try {
      mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm' });
    } catch {
      try {
        mediaRecorder = new MediaRecorder(stream);
      } catch {
        return resolve(null);
      }
    }

    const chunks: Blob[] = [];
    mediaRecorder.ondataavailable = (e) => {
      if (e.data.size > 0) chunks.push(e.data);
    };

    mediaRecorder.onstop = () => {
      const blob = new Blob(chunks, { type: mediaRecorder.mimeType });
      resolve(blob);
    };

    mediaRecorder.start();
    setTimeout(() => {
      if (mediaRecorder.state !== 'inactive') {
        mediaRecorder.stop();
      }
    }, durationMs);
  });
}
