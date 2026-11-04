# ZION - External Attack Surface Monitor v1.0

### ZION is a reconnaissance and monitoring tool designed for SOC Analysts and Blue Teams. It consolidates intelligence from multiple high-fidelity threat sources and delivers a unified risk verdict for digital assets, removing the need for fragmented manual analysis.

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/mym0us3r/zion/blob/main/LICENSE)
![Python](https://img.shields.io/badge/python-3.9%2B-brightgreen.svg)
![FastAPI](https://img.shields.io/badge/framework-FastAPI-009688.svg)

> There is no anonymity on the attack surface. Only delays :)

**ZION** is a robust **External Attack Surface Management (EASM)** platform that consolidates intelligence from multiple sources to provide a real-time, panoramic view of digital assets and global threats.

## Interface & Case Studies

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

> [!WARNING]
> **Known limitations (v1.x):** an engine that is not configured, times out or returns an error contributes 0 to the verdict, so a **CLEAN** result does not confirm that every engine was queried. Confirm the result through the engine links on the dashboard. The PhishStats panel has no live data source in v1.x and is shown as OFFLINE.

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

`git clone https://github.com/mym0us3r/zion.git /opt/ZION`

`cd /opt/ZION`


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
│   ├── config.py                # Global configurations and environment variable management
│   ├── core                     # Search engines and Threat Intelligence integrations
│   │   ├── abuse_client.py      # AbuseIPDB API integration
│   │   ├── analyzer.py          # Central recursive analysis engine
│   │   ├── censys_client.py     # Censys integration (Infrastructure discovery)
│   │   ├── __init__.py          # Core package initializer
│   │   ├── otx_client.py        # AlienVault OTX integration
│   │   ├── phishstats_client.py # Real-time Phishing monitoring
│   │   ├── ransomware_client.py # Ransomware threat actors intelligence
│   │   ├── shodan_client.py     # Shodan integration (Exposed devices search)
│   │   └── vt_client.py         # VirusTotal API integration
│   ├── __init__.py
│   ├── main.py                  # FastAPI entrypoint (Backend and Routing)
│   ├── static                   # Frontend assets (CSS, JS, Images)
│   └── templates
│       └── dashboard.html       # Web-based UI Dashboard
├── requirements.txt             # Python project dependencies
└── venv                         # Local virtual environment
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
ExecStart=/opt/ZION/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8080
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

### How to Access

Once the service is running, open your browser and go to:
`http://localhost:8080` or `http://your-server-ip:8080`

--- 

### 4. Understanding IP Discrepancies: Geo-DNS, CDNs & Threat Intelligence
When investigating a domain, you might notice that a local nslookup returns a different IP address than services like AbuseIPDB. This isn't an error; it's a reflection of how the modern internet works.

- **The Role of Geo-DNS and CDNs**:
Major service providers (e.g., Google, Microsoft, Cloudflare) operate through thousands of servers worldwide known as Edge Nodes.

- **Local Resolution**: When you run nslookup on your machine, the DNS resolves to the IP of the server closest to you to ensure the lowest possible latency.
- **Threat Intel Services (e.g., AbuseIPDB)**: These platforms often perform resolutions from servers located in different regions (typically the US or Europe) or display the infrastructure's primary origin IP rather than your local edge node.

- **Practical Example (Real-World Scenario)**:
Imagine you are investigating a suspicious domain, such as cdn-malicious.com.

- **On your local terminal (e.g., Brazil)**:
`nslookup cdn-malicious.com`
`Output: 189.x.x.x (A CDN node IP located in São Paulo)`

- **On AbuseIPDB (Global Query)**:
When searching the same domain, it might list:
`IP: 104.x.x.x (A Cloudflare main network IP in the US).`

The Difference: AbuseIPDB is showing you the "owner" of the IP block or the specific IP detected by their crawlers from a different geographical location.

- **Why is this critical for Threat Hunting**?
You must be aware of two key phenomena:

- **Fast Flux DNS**:
Attackers frequently change the IP address associated with a domain (every few minutes) to evade detection. What you see in nslookup now might differ from what was indexed 10 minutes ago.

- **Domain Fronting**:
Attackers may use a legitimate CDN domain to camouflage malicious traffic. Your local nslookup will show a legitimate CDN IP, while Threat Intel might be flagging the historical malicious behavior of that specific infrastructure in another region.

---

*The project is still in its early stages, but it brings a powerful concept to the table. When you search for an address, it doesn't just look up the target, it performs a triple-check, across the Domain, sub-domain (as www - the most common entry point), and IP. While a more aggressive reconnaissance feature to scan entire infrastructures is on the roadmap, the primary focus right now is to empower SOC teams. ZION provides a broader perspective that is essential for handling alerts, threat hunting, or executing incident responses.*

---

## Disclaimer & Purpose

**ZION** was developed to **streamline SOC operations**, drastically reducing manual reconnaissance time by consolidating fragmented intelligence into a single, actionable dashboard. 
The core mission is to replace repetitive, manual lookups with **instant, high-fidelity telemetry**, allowing analysts to focus on what matters: threat response.

> [!IMPORTANT]
> This tool is intended strictly for **educational and defensive security purposes**. Always ensure you have proper authorization before analyzing third-party assets.

> [!NOTE]
> **Project status:** ZION v1 will not receive further updates or revisions. Development is focused on ZION v2. Everyone is welcome to download, modify and adapt ZION v1 to their needs under the terms of the GPLv3 license.
