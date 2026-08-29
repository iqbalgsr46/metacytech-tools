import http.server
import socketserver
import json
import os
import sys
import webbrowser
import threading

PORT = 8080
TEMPLATE_DIR = sys.argv[1] if len(sys.argv) > 1 else ""
DATA_FILE = os.path.join(TEMPLATE_DIR, "data.json")

# Ensure file exists
if not os.path.exists(DATA_FILE):
    print(f"Error: {DATA_FILE} not found.")
    sys.exit(1)

def load_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

class DashboardHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            
            data = load_data()
            
            # Build the form HTML
            html = """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>SYSTEM_CONFIG // LOCAL_DASHBOARD</title>
                <script src="https://cdn.tailwindcss.com"></script>
                <style>
                    body { 
                        font-family: 'Courier New', Courier, monospace; 
                        background-color: #050505; 
                        color: #00ff00;
                    }
                    .crt::before {
                        content: " ";
                        display: block;
                        position: absolute;
                        top: 0;
                        left: 0;
                        bottom: 0;
                        right: 0;
                        background: rgba(0, 255, 0, 0.02);
                        z-index: 2;
                        pointer-events: none;
                    }
                    .glow-text { text-shadow: 0 0 5px #00ff00; }
                    .glow-border { box-shadow: 0 0 8px #00ff00; border: 1px solid #00ff00; }
                    input:focus { outline: none; box-shadow: 0 0 12px #00ff00; border-color: #00ff00; background-color: rgba(0, 255, 0, 0.1); }
                    ::-webkit-scrollbar { width: 8px; }
                    ::-webkit-scrollbar-track { background: #050505; }
                    ::-webkit-scrollbar-thumb { background: #00ff00; }
                </style>
            </head>
            <body class="relative min-h-screen crt">
                <div class="max-w-4xl mx-auto py-10 px-4 sm:px-6 lg:px-8 relative z-10">
                    <div class="border border-[#00ff00] bg-black/80 backdrop-blur-sm glow-border">
                        <div class="border-b border-[#00ff00] px-6 py-4 bg-[#00ff00]/10 flex justify-between items-center">
                            <div>
                                <h1 class="text-xl font-bold tracking-widest glow-text">> ROOT_DASHBOARD_EDITOR_</h1>
                                <p class="text-[#00cc00] text-xs mt-1">Configure target payload parameters before execution.</p>
                            </div>
                            <div class="text-xs animate-pulse">STATUS: ONLINE</div>
                        </div>
                        
                        <form id="editForm" class="p-6">
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            """
            
            # Generate input fields for each key in data.json
            for key, value in data.items():
                label = key.replace('receipt', 'Resi ').replace('amount', 'Nominal ').upper()
                field_html = """
                                <div class="flex flex-col">
                                    <label class="text-xs font-bold text-[#00cc00] mb-1">[__LABEL__]</label>
                                    <input type="text" name="__KEY__" value="__VALUE__" 
                                        class="w-full bg-black/50 border border-[#00ff00]/50 px-3 py-2 text-sm text-[#00ff00] transition-all">
                                </div>
                """
                field_html = field_html.replace('__LABEL__', label).replace('__KEY__', key).replace('__VALUE__', value)
                html += field_html
                
            html += """
                            </div>
                            
                            <div class="mt-8 pt-5 border-t border-[#00ff00]/30 flex items-center justify-end">
                                <button type="submit" 
                                    class="bg-[#00ff00]/20 text-[#00ff00] border border-[#00ff00] px-6 py-2 font-bold hover:bg-[#00ff00] hover:text-black transition-all flex items-center gap-2 glow-text">
                                    > EXECUTE_BUILD
                                </button>
                            </div>
                        </form>
                    </div>
                </div>

                <div id="loadingOverlay" class="fixed inset-0 bg-black/90 hidden flex items-center justify-center z-50">
                    <div class="border border-[#00ff00] bg-black p-8 flex flex-col items-center max-w-sm w-full glow-border">
                        <div class="text-[#00ff00] text-4xl mb-4 animate-spin">\\|/</div>
                        <h3 class="text-lg font-bold text-[#00ff00] mb-2 glow-text">OVERWRITING_DATA...</h3>
                        <p class="text-xs text-[#00cc00] text-center">Connection will be terminated. Return to terminal to proceed with payload injection.</p>
                        <div class="w-full h-1 bg-[#00ff00]/30 mt-4 relative overflow-hidden">
                            <div class="absolute top-0 left-0 h-full bg-[#00ff00] animate-ping"></div>
                        </div>
                    </div>
                </div>

                <script>
                    document.getElementById('editForm').addEventListener('submit', async (e) => {
                        e.preventDefault();
                        const formData = new FormData(e.target);
                        const data = Object.fromEntries(formData.entries());
                        
                        document.getElementById('loadingOverlay').classList.remove('hidden');
                        
                        try {
                            const response = await fetch('/save', {
                                method: 'POST',
                                headers: {
                                    'Content-Type': 'application/json',
                                },
                                body: JSON.stringify(data)
                            });
                            
                            if (response.ok) {
                                setTimeout(() => {
                                    window.close();
                                }, 2500);
                            } else {
                                alert("ERR: OVERWRITE_FAILED");
                                document.getElementById('loadingOverlay').classList.add('hidden');
                            }
                        } catch (error) {
                            console.error("Error:", error);
                            alert("ERR: CONNECTION_LOST");
                            document.getElementById('loadingOverlay').classList.add('hidden');
                        }
                    });
                </script>
            </body>
            </html>
            """
            
            self.wfile.write(html.encode('utf-8'))
            return
        
        # Handle other GET requests (e.g. favicon) quietly
        super().do_GET()

    def do_POST(self):
        if self.path == '/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                new_data = json.loads(post_data.decode('utf-8'))
                save_data(new_data)
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}).encode('utf-8'))
                
                # Shut down the server forcefully after saving
                def kill_server():
                    os._exit(0)
                threading.Timer(0.5, kill_server).start()
                
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "error", "message": str(e)}).encode('utf-8'))

# Mute logging to console
class QuietServer(socketserver.TCPServer):
    def handle_error(self, request, client_address):
        pass

http.server.SimpleHTTPRequestHandler.log_message = lambda *args: None

with QuietServer(("", PORT), DashboardHandler) as httpd:
    print(f"\\nDashboard lokal aktif di http://localhost:{PORT}")
    print(f"Membuka browser... Setelah menekan 'Terapkan', server ini akan otomatis mati.")
    webbrowser.open(f"http://localhost:{PORT}")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
