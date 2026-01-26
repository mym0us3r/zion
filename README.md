# ZION - External Attack Surface Monitor v1.0

### ZION is a reconnaissance and monitoring tool designed for SOC Analysts and Blue Teams. It consolidates intelligence from multiple high-fidelity threat sources and delivers a unified risk verdict for digital assets, removing the need for fragmented manual analysis.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/mym0us3r/zion/blob/main/LICENSE)
![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen.svg)
![FastAPI](https://img.shields.io/badge/framework-FastAPI-009688.svg)

> There is no anonymity on the attack surface. Only delays :)

**ZION** is a robust **External Attack Surface Management (EASM)** platform that consolidates intelligence from multiple sources to provide a real-time, panoramic view of digital assets and global threats.

## 3. Interface & Case Studies

This section demonstrates ZION's capability to map diverse digital asset profiles and infrastructure types.

### Dashboard Overview
This dashboard provides real-time visibility into the external attack surface, mapping assets globally and delivering instant insights via integrated security engines and feeds.
![Zion Interface View](https://github.com/mym0us3r/zion/raw/main/screenshots/zion.png)

---

### Asset Analysis: GitHub - Status: CLEAN
Demonstration of reconnaissance on development and code hosting infrastructure, validating edge nodes and associated IP netblocks.
![GitHub Analysis](https://github.com/mym0us3r/zion/raw/main/screenshots/zion_github.png)

---

### Asset Analysis: LinkedIn - Status: SUSPICIOUS
Demonstration of reconnaissance on corporate infrastructure. This case study shows ZION identifying a **SUSPICIOUS** verdict, illustrating the dashboard's sensitivity to reputation scores and behavioral telemetry even on high-profile corporate domains.
![LinkedIn Suspicious Analysis](https://github.com/mym0us3r/zion/raw/main/screenshots/zion_linkedin.png)

---

### Asset Analysis: conviteamexcenturionblack[.]com - Status: MALICIOUS
This case study demonstrates ZION’s efficiency in detecting active phishing campaigns. By analyzing this malicious domain, the dashboard immediately triggers a **MALICIOUS** verdict, correlating high abuse scores and negative reputation from multiple security engines.
![Malicious Phishing Analysis](https://github.com/mym0us3r/zion/raw/main/screenshots/zion_conv.png)

### Asset Analysis: Malicious Node 45[.]78[.]194[.]230
This case study showcases the dashboard's ability to identify a high-risk network node. The system correlates multiple threat indicators—including VirusTotal detections for Malware—to trigger a **MALICIOUS** status, providing the analyst with immediate visual confirmation of the threat level.
![Malicious Malware Analysis](https://github.com/mym0us3r/zion/blob/main/screenshots/zion_45_78_194_230.png) 

---

## 1. Key Features

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
  - Ransomware Live
  - PhishStats 
  - SHODAN  
  - CENSYS  

- **Real-Time Dashboards**  
  Interactive UI with geolocated asset visualization using Leaflet.js.

- **Security News Feed**  
  Real-time RSS feed consumption from:
  - The Hacker News  
  - CISO Advisor Brazil  

### Threat Telemetry Dashboard
Centralized interface displaying:
* **Identity Details**: Organization/ISP, IP, and location via IPInfo.
* **Threat Scores**: Aggregated AbuseIPDB (Score %) and VirusTotal (Hits).
* **OTX Pulses**: Triple sum of IoCs via AlienVault.
* **Final Verdict**: Intelligent decision algorithm (Clean, Suspicious, Malicious).

### Ransomware Live Monitor
Native integration with Ransomware Live tracking:
* Number of active ransomware groups.
* Victims recorded in the current year (2026).
* Total historical victims with persistent caching for high availability.

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

SHODAN_API=your_abuseipdb_key
VT_API=your_virustotal_key
ABUSE_API=your_abuseipdb_key
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

**Enable and start the service - Maintenance & Logs**

```

sudo systemctl daemon-reload
sudo systemctl enable zion
sudo systemctl start zion
sudo systemctl status zion
sudo systemctl stop zion
sudo systemctl restart zion

```

- **Monitor logs**:
`journalctl -fu zion`

- **Flush cache**: 
`systemctl stop zion ; find /opt/ZION/ -name "__pycache__" -type d -exec rm -rf {} +`

--- 

*The project is still in its early stages, but it brings a powerful concept to the table. When you search for an address, it doesn't just look up the target, it performs a triple-check, across the Domain, sub-domain (as www - the most common entry point), and IP. While a more aggressive reconnaissance feature to scan entire infrastructures is on the roadmap, the primary focus right now is to empower SOC teams. ZION provides a broader perspective that is essential for handling alerts, threat hunting, or executing incident responses.*

---

## Disclaimer & Purpose

**ZION** was developed to **streamline SOC operations**, drastically reducing manual reconnaissance time by consolidating fragmented intelligence into a single, actionable dashboard. 
The core mission is to replace repetitive, manual lookups with **instant, high-fidelity telemetry**, allowing analysts to focus on what matters: threat response.

> [!IMPORTANT]
> This tool is intended strictly for **educational and defensive security purposes**. Always ensure you have proper authorization before analyzing third-party assets.
