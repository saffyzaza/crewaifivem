"""Simple HTTP server for viewing generated FiveM scripts."""

import json
import os
import subprocess
import sys
import threading
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import unquote

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.config.settings import (
    get_effective_settings,
    load_runtime_settings,
    save_runtime_settings,
)

OUTPUT_DIR = Path("output")
LOGS_FILE = Path("generation.log")

is_generating = False


class ViewerHandler(SimpleHTTPRequestHandler):
    """Custom handler for the viewer API."""

    def do_POST(self):
        """Handle POST requests."""
        path = unquote(self.path)
        
        if path == "/api/generate":
            self.handle_generate()
        elif path == "/api/settings":
            self.handle_save_settings()
        else:
            self.send_error(404, "Not found")
    
    def handle_save_settings(self):
        """Save LLM settings."""
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body)
            current = load_runtime_settings()
            
            # Update only provided fields
            if "llm_provider" in data:
                current["llm_provider"] = data["llm_provider"]
            if "google_api_key" in data:
                current["google_api_key"] = data["google_api_key"]
            if "gemini_model_name" in data:
                current["gemini_model_name"] = data["gemini_model_name"]
            if "ollama_base_url" in data:
                current["ollama_base_url"] = data["ollama_base_url"]
            if "ollama_model_name" in data:
                current["ollama_model_name"] = data["ollama_model_name"]
            
            save_runtime_settings(current)
            self.send_json({"success": True, "settings": get_effective_settings()})
        except Exception as e:
            self.send_json({"error": str(e)}, 400)

    def handle_generate(self):
        """Handle script generation request."""
        global is_generating
        
        if is_generating:
            self.send_json({"error": "Generation already in progress"}, 400)
            return
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        
        try:
            data = json.loads(body)
            requirement = data.get('requirement', '')
            
            if not requirement:
                self.send_json({"error": "Requirement is required"}, 400)
                return
            
            is_generating = True
            
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Transfer-Encoding", "chunked")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            
            try:
                process = subprocess.Popen(
                    [sys.executable, "main.py", requirement],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    cwd=str(Path(__file__).parent),
                )
                
                for line in iter(process.stdout.readline, ''):
                    if line:
                        chunk = f"{len(line.encode('utf-8')):X}\r\n{line}\r\n"
                        self.wfile.write(chunk.encode('utf-8'))
                        self.wfile.flush()
                
                process.wait()
                self.wfile.write(b"0\r\n\r\n")
                
            except Exception as e:
                error_msg = f"Error: {str(e)}\n"
                chunk = f"{len(error_msg.encode('utf-8')):X}\r\n{error_msg}\r\n"
                self.wfile.write(chunk.encode('utf-8'))
                self.wfile.write(b"0\r\n\r\n")
            finally:
                is_generating = False
                
        except json.JSONDecodeError:
            self.send_json({"error": "Invalid JSON"}, 400)
            is_generating = False

    def do_GET(self):
        """Handle GET requests."""
        path = unquote(self.path)

        if path == "/":
            self.serve_file("viewer.html", "text/html")
        elif path == "/api/output":
            self.serve_output_list()
        elif path.startswith("/api/file/"):
            self.serve_file_content(path)
        elif path == "/api/logs":
            self.serve_logs()
        elif path == "/api/settings":
            self.serve_settings()
        else:
            super().do_GET()
    
    def serve_settings(self):
        """Serve current LLM settings."""
        settings = get_effective_settings()
        # Mask API key for security
        if settings.get("google_api_key"):
            key = settings["google_api_key"]
            settings["google_api_key_masked"] = key[:10] + "..." + key[-4:] if len(key) > 14 else "***"
        self.send_json(settings)

    def serve_file(self, filename: str, content_type: str):
        """Serve a static file."""
        try:
            with open(filename, "r", encoding="utf-8") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", f"{content_type}; charset=utf-8")
            self.end_headers()
            self.wfile.write(content.encode("utf-8"))
        except FileNotFoundError:
            self.send_error(404, "File not found")

    def serve_output_list(self):
        """Serve list of output resources and files."""
        resources = {}

        if OUTPUT_DIR.exists():
            for resource_dir in OUTPUT_DIR.iterdir():
                if resource_dir.is_dir():
                    files = []
                    for file in resource_dir.iterdir():
                        if file.is_file():
                            files.append(file.name)
                    if files:
                        resources[resource_dir.name] = sorted(files)

        self.send_json({"resources": resources})

    def serve_file_content(self, path: str):
        """Serve content of a specific file."""
        parts = path.replace("/api/file/", "").split("/")
        if len(parts) >= 2:
            resource_name = parts[0]
            file_name = "/".join(parts[1:])
            file_path = OUTPUT_DIR / resource_name / file_name

            if file_path.exists() and file_path.is_file():
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    self.send_json({"content": content, "filename": file_name})
                except Exception as e:
                    self.send_json({"error": str(e)}, 500)
            else:
                self.send_json({"error": "File not found"}, 404)
        else:
            self.send_json({"error": "Invalid path"}, 400)

    def serve_logs(self):
        """Serve generation logs."""
        logs = ""
        if LOGS_FILE.exists():
            try:
                with open(LOGS_FILE, "r", encoding="utf-8") as f:
                    logs = f.read()
            except Exception:
                logs = "Could not read logs"
        else:
            logs = "No logs file found. Logs will appear after running the generator."

        self.send_json({"logs": logs})

    def send_json(self, data: dict, status: int = 200):
        """Send JSON response."""
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def log_message(self, format, *args):
        """Override to show cleaner logs."""
        print(f"[Viewer] {args[0]}")


def main():
    """Start the viewer server."""
    port = 8080
    server = HTTPServer(("0.0.0.0", port), ViewerHandler)

    print("=" * 50)
    print("🎮 FiveM Script Generator - Output Viewer")
    print("=" * 50)
    print(f"\n🌐 Open in browser: http://localhost:{port}")
    print("\n📁 Serving files from: ./output/")
    print("\nPress Ctrl+C to stop\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped")
        server.shutdown()


if __name__ == "__main__":
    main()
