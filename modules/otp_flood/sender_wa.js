/**
 * OTP Flood - WhatsApp Sender (Node.js)
 * Uses @whiskeysockets/baileys - pure JS WhatsApp implementation
 * 
 * Usage: node sender_wa.js <target_number> <message> [sender_name]
 */

const { 
  makeWASocket, 
  useMultiFileAuthState, 
  DisconnectReason,
  fetchLatestBaileysVersion,
  makeCacheableSignalKeyStore,
} = require("@whiskeysockets/baileys");
const qrcode = require("qrcode-terminal");
const path = require("path");
const fs = require("fs");
const NodeCache = require("node-cache");

const TARGET = process.argv[2];
const MESSAGE = process.argv[3];
const SENDER = process.argv[4] || "System";

if (!TARGET || !MESSAGE) {
  console.error("Usage: node sender_wa.js <number> <message> [sender]");
  process.exit(1);
}

const FULL_MESSAGE = `[${SENDER}] ${MESSAGE}`;
const AUTH_DIR = path.join(__dirname, ".auth_session");

// Suppress pino debug logs
const pino = require("pino");
const logger = pino({ level: "silent" });

async function start() {
  const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);
  const { version, isLatest } = await fetchLatestBaileysVersion();

  const msgRetryCounterCache = new NodeCache({ stdTTL: 60 });

  const sock = makeWASocket({
    version,
    logger,
    auth: {
      creds: state.creds,
      keys: makeCacheableSignalKeyStore(state.keys, logger),
    },
    msgRetryCounterCache,
    generateHighQualityLinkPreview: false,
    defaultQueryTimeoutMs: 20000,
    keepAliveIntervalMs: 10000,
    printQRInTerminal: false,
    markOnlineOnConnect: false,
    connectTimeoutMs: 60000,
    shouldIgnoreJid: () => true,
    patchMessageBeforeSending: (msg) => msg,
  });

  let qrShown = false;

  sock.ev.on("connection.update", async (update) => {
    const { connection, lastDisconnect, qr } = update;

    if (qr && !qrShown) {
      qrShown = true;
      qrcode.generate(qr, { small: true });
      console.log("\nSCAN QR CODE DI ATAS dengan WhatsApp Anda");
      console.log("Buka WhatsApp → titik 3 pojok kanan → Linked Devices → Link Device\n");
    }

    if (connection === "open") {
      console.log("WA Connected");
      try {
        const jid = TARGET.includes("@s.whatsapp.net")
          ? TARGET
          : `${TARGET}@s.whatsapp.net`;

        const result = await sock.sendMessage(jid, {
          text: FULL_MESSAGE,
        });

        if (result && result.key) {
          console.log(`SENT: ${result.key.id}`);
        } else {
          console.log("ERR: Failed to send");
        }
      } catch (err) {
        const msg = err.message || String(err);
        if (msg.includes("rate") || msg.includes("429") || msg.includes("block") || msg.includes("slow")) {
          console.log("BLOCKED: Rate limited");
        } else if (msg.includes("not exists") || msg.includes("not found") || msg.includes("unavailable")) {
          console.log("ERR: Number not on WhatsApp");
        } else {
          console.log(`ERR: ${msg}`);
        }
      }

      sock.end(undefined);
      setTimeout(() => process.exit(0), 500);
    }

    if (connection === "close") {
      if (lastDisconnect) {
        const statusCode = lastDisconnect.error?.output?.statusCode;
        const reason = DisconnectReason[statusCode] || "Unknown";

        if (statusCode === DisconnectReason.LOGGED_OUT) {
          console.log("AUTH_FAIL: Session expired");
          try { fs.rmSync(AUTH_DIR, { recursive: true, force: true }); } catch(e) {}
          process.exit(1);
        } else if (statusCode === DisconnectReason.TIMEOUT) {
          // Retry silently
          return;
        } else {
          // Check if already sent
          if (!qrShown) {
            // Fresh connection failure - try again
            return;
          }
        }
      } else if (!qrShown) {
        // No QR and disconnected - retry
        return;
      }
    }
  });

  sock.ev.on("creds.update", saveCreds);

  // Cleanup timeout
  setTimeout(() => {
    process.exit(1);
  }, 90000);
}

start().catch((err) => {
  console.log(`INIT_ERR: ${err.message || err}`);
  process.exit(1);
});
