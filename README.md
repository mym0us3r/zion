# ZION - External Attack Surface Monitor v1.0

### ZION is a reconnaissance and monitoring tool designed for SOC Analysts and Blue Teams. It consolidates intelligence from multiple high-fidelity threat sources and delivers a unified risk verdict for digital assets, removing the need for fragmented manual analysis.

---

## Key Features

- **Recursive Triple-Check**  
  Simultaneous analysis of:
  - Apex Domain  
  - Canonical Subdomain  
  - Infrastructure IP  

- **Unified Intelligence**  
  Native integration with:
  - AbuseIPDB  
  - VirusTotal  
  - OTX AlienVault  

- **Real-Time Dashboards**  
  Interactive UI with geolocated asset visualization using Leaflet.js.

- **Security News Feed**  
  Integrated threat intelligence from:
  - The Hacker News  
  - CISO Advisor  

- **Automated Heuristics**  
  Dynamic asset classification:
  - Clean  
  - Suspicious  
  - Malicious  

---

## Technical Edge

ZION bridges the gap between Web UI limitations and raw API intelligence. It frequently detects threat indicators that manual platform searches fail to surface.

### Detection Strategies

- **TLD Inheritance**  
  Captures OTX pulses associated with root domains and related DNS or MX records.

- **ASN Correlation**  
  Identifies infrastructure hosted in ASN ranges historically linked to botnets, phishing, or abuse campaigns.

- **Low-Latency Intelligence**  
  Direct API consumption exposes threat data before it becomes indexed in graphical dashboards.

---

## Installation & Setup

### 1. Prerequisites

- **Operating System**: Ubuntu 24.04.2 LTS or compatible Linux distribution  
- **Language**: Python 3.12 or newer  
- **Installation Directory**: `/opt/ZION`

---

### 2. Environment Setup

- **Clone the repository**

`mkdir -p /opt/ZION ; cd /opt/ZION`

`git clone https://github.com/mym0us3r/zion.git`


- **Create and activate virtual environment**

`python3 -m venv venv`

`source venv/bin/activate`

- **Install dependencies**

`pip install -r requirements.txt`

---

### 3. Configuration


- **Create a .env file in the project root directory.**

``` 

touch /opt/ZION/.env

ABUSE_API=your_abuseipdb_key
VT_API=your_virustotal_key
OTX_API=your_otx_alienvault_key
IPINFO_TOKEN=your_ipinfo_token

```

---

- **Project Structure**

```
ZION
├── app
│   ├── core
│   │   ├── abuse_client.py    # AbuseIPDB integration
│   │   ├── analyzer.py        # Recursive analysis engine
│   │   ├── otx_client.py      # OTX AlienVault integration
│   │   └── vt_client.py       # VirusTotal integration
│   ├── main.py                # FastAPI entrypoint
│   ├── static                 # CSS and JavaScript assets
│   └── templates              # HTML dashboard templates
├── .env                       # API secrets
└── requirements.txt           # Python dependencies
```

---

- **Deployment (systemd)**

To run ZION as a persistent service, configure a systemd unit.

**Create the service file**

`sudo nano /etc/systemd/system/zion.service`

**Paste the service configuration.**

```

[Unit]
Description=ZION - External Attack Surface Monitor
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=/opt/ZION/app
ExecStart=/opt/ZION/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target

```

---

**Enable and start the service -Maintenance & Logs**

```

sudo systemctl daemon-reload
sudo systemctl enable zion
sudo systemctl start zion
sudo systemctl status zion

```

- **Monitor logs**

`journalctl -fu zion`

- **Flush cache and restart**

`systemctl stop zion`

`find /opt/ZION/ -name "__pycache__" -type d -exec rm -rf {} +`

`systemctl start zion`

--- 

- **Disclaimer:**
This tool is for educational and defensive security purposes only!


THERE IS NO ANONYMITY ON THE ATTACK SURFACE. ONLY DELAYS :)
