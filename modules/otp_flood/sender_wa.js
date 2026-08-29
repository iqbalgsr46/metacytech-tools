/**
 * OTP Flood - Persistent WhatsApp Daemon & Direct Sender (Node.js + Baileys)
 * Supports single message or persistent streaming stdin mode.
 * 
 * Usage 1 (Single): node sender_wa.js <target_number> <message> [sender_name]
 * Usage 2 (Daemon): node sender_wa.js --daemon
 */

const { 
  default: makeWASocket, 
  useMultiFileAuthState, 
  DisconnectReason,
  fetchLatestBaileysVersion,
  makeCacheableSignalKeyStore,
} = require("@whiskeysockets/baileys");
const qrcode = require("qrcode-terminal");
const path = require("path");
const fs = require("fs");
const readline = require("readline");
const NodeCache = require("node-cache");
const pino = require("pino");

const AUTH_DIR = path.join(__dirname, ".auth_session");
const logger = pino({ level: "silent" });
const isDaemon = process.argv.includes("--daemon");

function formatTargetJid(num) {
  let clean = num.toString().trim().replace(/[^0-9]/g, "");
  if (clean.startsWith("0")) clean = "62" + clean.slice(1);
  if (!clean.includes("@s.whatsapp.net")) clean = `${clean}@s.whatsapp.net`;
  return clean;
}

async function start() {
  const { state, saveCreds } = await useMultiFileAuthState(AUTH_DIR);
  const { version } = await fetchLatestBaileysVersion().catch(() => ({ version: [2, 3000, 1015901307] }));
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
    defaultQueryTimeoutMs: 30000,
    keepAliveIntervalMs: 15000,
    printQRInTerminal: false,
    markOnlineOnConnect: true,
    connectTimeoutMs: 60000,
  });

  let qrShown = false;
  let isConnected = false;

  sock.ev.on("connection.update", async (update) => {
    const { connection, lastDisconnect, qr } = update;

    if (qr && !qrShown) {
      qrShown = true;
      console.log("\n[QR_CODE_START]");
      qrcode.generate(qr, { small: true });
      console.log("[QR_CODE_END]");
      console.log("SCAN_REQUIRED: Silakan scan QR code di atas menggunakan aplikasi WhatsApp.");
    }

    if (connection === "open") {
      isConnected = true;
      console.log("STATUS: CONNECTED");

      if (!isDaemon) {
        // Single shot mode
        const target = process.argv[2];
        const message = process.argv[3];
        const sender = process.argv[4] || "System";
        
        if (target && message) {
          try {
            const jid = formatTargetJid(target);
            const fullMsg = `[${sender}] ${message}`;
            const res = await sock.sendMessage(jid, { text: fullMsg });
            if (res && res.key) {
              console.log(`SENT: ${res.key.id}`);
            } else {
              console.log("ERR: Failed to deliver");
            }
          } catch (e) {
            console.log(`ERR: ${e.message || e}`);
          }
        }
        setTimeout(() => process.exit(0), 1000);
      }
    }

    if (connection === "close") {
      isConnected = false;
      const statusCode = lastDisconnect?.error?.output?.statusCode;
      const shouldReconnect = statusCode !== DisconnectReason.LOGGED_OUT;
      
      if (statusCode === DisconnectReason.LOGGED_OUT) {
        console.log("AUTH_FAIL: Session logged out");
        try { fs.rmSync(AUTH_DIR, { recursive: true, force: true }); } catch (e) {}
        process.exit(1);
      } else {
        console.log(`STATUS: DISCONNECTED (${statusCode || 'Unknown'})`);
        if (isDaemon && shouldReconnect) {
          setTimeout(start, 3000);
        } else if (!isDaemon) {
          process.exit(1);
        }
      }
    }
  });

  sock.ev.on("creds.update", saveCreds);

  if (isDaemon) {
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout,
      terminal: false,
    });

    rl.on("line", async (line) => {
      line = line.trim();
      if (!line) return;
      if (line === "PING") {
        console.log(isConnected ? "PONG: READY" : "PONG: CONNECTING");
        return;
      }
      if (line === "EXIT") {
        process.exit(0);
      }

      try {
        const payload = JSON.parse(line);
        if (!isConnected) {
          console.log(JSON.stringify({ id: payload.id, status: "error", error: "WhatsApp not connected yet" }));
          return;
        }

        const jid = formatTargetJid(payload.target);
        const text = payload.sender ? `[${payload.sender}] ${payload.message}` : payload.message;
        const res = await sock.sendMessage(jid, { text });

        console.log(JSON.stringify({
          id: payload.id || res?.key?.id,
          status: "sent",
          msgId: res?.key?.id,
          target: payload.target,
        }));
      } catch (err) {
        console.log(JSON.stringify({
          status: "error",
          error: err.message || String(err),
        }));
      }
    });
  }
}

start().catch((err) => {
  console.log(`INIT_ERR: ${err.message || err}`);
  process.exit(1);
});
