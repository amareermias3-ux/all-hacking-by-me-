```markdown
# 🛡️ Advanced Security Audit Framework (v11)

A professional-grade, multi-functional Red-Teaming and Security Audit Framework written in Python. Designed for authorized security assessments, penetration testing, and educational research, featuring high-concurrency handling, real-time Telegram alerting, advanced device telemetry, client-side screenshot harvesting, URL cloaking, and an SSL-secured admin dashboard.

---

## 🌟 Key Features & Capabilities (v1 to v11 Milestones)

* **High-Concurrency Core:** Built on Python's `http.server` with `ThreadingMixIn` for fast multi-threaded request processing.
* **HTTPS & SSL Encryption (v11):** Automatic self-signed SSL certificate generation (`cert.pem`, `key.pem`) to ensure secure encrypted communication and bypass basic browser security warnings.
* **Secured Web Admin Dashboard (v10 & v11):** Real-time monitoring of captured credentials, system audit logs, and harvested media, protected by HTTP Basic Authentication (`admin` / `audit2026`).
* **Multi-Brand Template Engine:** Ready-to-use templates for popular platforms (Facebook, Google, Instagram, Netflix) with dynamic URL path masking/cloaking.
* **Anti-Bot & Human Verification:** Interactive mouse movement and touch tracking to block automated web crawlers and security sandboxes.
* **Real-Time Telegram Integration:** Instant alerts delivered directly to your Telegram bot for credentials, 2FA/OTP codes, and captured screenshots.
* **Client-Side Screenshot Capture:** Uses `html2canvas` to secretly capture and exfiltrate browser view images upon credential submission.
* **Device Telemetry & Geolocation:** Harvests screen resolution, platform details, hardware concurrency, device memory, battery status, and IP geolocation (`ip-api`).
* **Terminal Audio Alerts:** Instant `\a` acoustic beeps on the host terminal whenever a target visits or interacts with the portal.

---

## 🛠️ Installation, Setup & Execution Guide

### Step 1: Clone the Repository
```bash
git clone [https://github.com/amareermias3-ux/hacking-.git](https://github.com/amareermias3-ux/hacking-.git)
cd hacking-

```

### Step 2: Run the Audit Framework Server

Open your first terminal and start the Python script:

```bash
python3 advanced_security_audit_tool.py

```

*(Select your target template from the interactive menu when prompted).*

### Step 3: Expose via Public Tunneling (Choose One Method)

To make your local secure server accessible over the public internet, open a **second/new terminal** and choose either **Cloudflare** or **Ngrok**:

* **Method A: Using Cloudflare Tunnel (Recommended for HTTPS)**
```bash
cloudflared tunnel --url https://localhost:8080 --no-tls-verify

```


* **Method B: Using Ngrok Tunnel**
```bash
ngrok http 8080

```



---

## 💻 Usage & Execution Flow

1. Run **Step 2** to keep the local secure server listening on port `8080`.
2. Run **Step 3** to generate your public link (e.g., `https://random-words.trycloudflare.com`).
3. Send the generated public link to the target for authorized security auditing.

---

## 📊 Admin Dashboard & Monitoring

* **Terminal Logs:** Real-time visit telemetry, IP addresses, ISP info, and captured credentials will be printed directly on your terminal with color-coded alerts and logged to `audit_results.log`.
* **Captured Media:** All harvested target screenshots are automatically saved inside the `captured_media/` directory.
* **Web Admin Panel:** Access the secured management dashboard in your browser at:
* **URL:** `https://localhost:8080/admin-panel` (or via your public tunnel)
* **Credentials:** Username: `admin` | Password: `audit2026`



---

## 🔒 Disclaimer

*This tool is created strictly for educational purposes and authorized security auditing, vulnerability assessments, and penetration testing engagements with explicit permission. The author and contributors assume no liability for misuse or damage caused by this software.*

