# 🚀 Installation Guide - FiveM Script Generator on Ubuntu VPS

## Prerequisites

- Ubuntu 20.04 / 22.04 LTS
- Minimum 2GB RAM (4GB+ recommended for Ollama)
- Python 3.10+
- Git

---

## 1. System Update

```bash
sudo apt update && sudo apt upgrade -y
```

## 2. Install Python 3.10+

```bash
# Check Python version
python3 --version

# If Python < 3.10, install newer version
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-dev python3-pip -y

# Set as default (optional)
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
```

## 3. Install Git

```bash
sudo apt install git -y
```

## 4. Clone Project

```bash
cd /opt
sudo git clone https://github.com/YOUR_USERNAME/fivem-crewai-generator.git
cd fivem-crewai-generator

# Set ownership
sudo chown -R $USER:$USER /opt/fivem-crewai-generator
```

## 5. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

## 6. Install Dependencies

```bash
pip install --upgrade pip
pip install -e .

# Or install from requirements
pip install crewai crewai[google-genai] langchain-google-genai pydantic pydantic-settings python-dotenv
```

## 7. Configure Environment

```bash
cp .env.example .env
nano .env
```

Edit `.env` file:
```env
# LLM Provider: gemini or ollama
LLM_PROVIDER=gemini

# Google Gemini API Configuration
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL_NAME=gemini-1.5-pro

# Ollama Configuration (if using local LLM)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL_NAME=llama3

# Output Configuration
OUTPUT_DIR=output
```

---

## 8. Install Ollama (Optional - for Local LLM)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
sudo systemctl enable ollama
sudo systemctl start ollama

# Check status
sudo systemctl status ollama

# Pull a model
ollama pull llama3
ollama pull codellama
```

### Configure Ollama for Remote Access

Edit Ollama service:
```bash
sudo nano /etc/systemd/system/ollama.service
```

Add/modify `Environment`:
```ini
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
```

Restart:
```bash
sudo systemctl daemon-reload
sudo systemctl restart ollama
```

---

## 9. Run the Application

### Development Mode

```bash
cd /opt/fivem-crewai-generator
source venv/bin/activate

# Start web server
python server.py
```

Access: `http://YOUR_VPS_IP:8080`

### Production Mode with Systemd

Create service file:
```bash
sudo nano /etc/systemd/system/fivem-generator.service
```

Content:
```ini
[Unit]
Description=FiveM Script Generator
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/opt/fivem-crewai-generator
Environment="PATH=/opt/fivem-crewai-generator/venv/bin"
ExecStart=/opt/fivem-crewai-generator/venv/bin/python server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable fivem-generator
sudo systemctl start fivem-generator

# Check status
sudo systemctl status fivem-generator

# View logs
sudo journalctl -u fivem-generator -f
```

---

## 10. Configure Firewall

```bash
# Allow port 8080
sudo ufw allow 8080/tcp

# If using Ollama remotely
sudo ufw allow 11434/tcp

# Enable firewall
sudo ufw enable
sudo ufw status
```

---

## 11. Setup Nginx Reverse Proxy (Optional)

Install Nginx:
```bash
sudo apt install nginx -y
```

Create config:
```bash
sudo nano /etc/nginx/sites-available/fivem-generator
```

Content:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # or VPS IP

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_cache_bypass $http_upgrade;
        proxy_read_timeout 300s;
        proxy_connect_timeout 75s;
    }
}
```

Enable:
```bash
sudo ln -s /etc/nginx/sites-available/fivem-generator /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## 12. SSL with Let's Encrypt (Optional)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

---

## Quick Commands Reference

```bash
# Start service
sudo systemctl start fivem-generator

# Stop service
sudo systemctl stop fivem-generator

# Restart service
sudo systemctl restart fivem-generator

# View logs
sudo journalctl -u fivem-generator -f

# Activate venv
source /opt/fivem-crewai-generator/venv/bin/activate

# Generate script manually
python main.py "สร้างระบบ teleport marker"

# Update project
cd /opt/fivem-crewai-generator
git pull
pip install -e .
sudo systemctl restart fivem-generator
```

---

## Troubleshooting

### Port already in use
```bash
sudo lsof -i :8080
sudo kill -9 PID
```

### Permission denied
```bash
sudo chown -R $USER:$USER /opt/fivem-crewai-generator
```

### Ollama not responding
```bash
sudo systemctl restart ollama
curl http://localhost:11434/api/tags
```

### Python module not found
```bash
source venv/bin/activate
pip install -e .
```

---

## Architecture

```
┌─────────────────┐     ┌─────────────────┐
│   Web Browser   │────▶│  Nginx (80/443) │
└─────────────────┘     └────────┬────────┘
                                 │
                        ┌────────▼────────┐
                        │  server.py:8080 │
                        └────────┬────────┘
                                 │
              ┌──────────────────┼──────────────────┐
              │                  │                  │
     ┌────────▼────────┐ ┌──────▼──────┐ ┌────────▼────────┐
     │  Gemini API     │ │   Ollama    │ │  Output Files   │
     │  (Cloud LLM)    │ │ (Local LLM) │ │   ./output/     │
     └─────────────────┘ └─────────────┘ └─────────────────┘
```

---

## Support

- GitHub Issues: [Create Issue](https://github.com/YOUR_USERNAME/fivem-crewai-generator/issues)
- Documentation: See `README.md`
