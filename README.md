# AWS Security Research Lab: Automated Python Honeypot

This project focuses on deploying and managing a custom-built honeypot on AWS infrastructure. Its goal is to monitor automated botnet activity. The primary goal is to bridge the gap between **Cybersecurity** (threat detection) and **DevOps** (automation and cloud managment).

I developed a lightweight Python listener and integrated a **CI/CD Pipeline** to automate the deployment process.

## Architecture
The system follows a professional deployment workflow:
1. Local Development: Python script modifications.
2. Version Control: Changes pushed to GitHub.
3. CI/CD Pipeline: GitHub Actions triggers SSH deployment to AWS.
4. Cloud Infrastructure: AWS EC2 instance (Ubuntu) hosts the honeypot.
5. Persistence: Systemd manages the honeypot as a background service.

## Key Features
- Automated Deployment: Integrated GitHub Actions workflow for zero-downtime updates.
- Service Management: Configured as a systemd service to ensure automatic recovery after reboots.
- Realistic Decoy: Mimics a standard Apache/2.4.41 (Ubuntu) server to increase interaction rates with automated scanners.
- IP Logging: Persistent logging of connection attempts.

## Tech Stack
- Cloud: AWS EC2
- Language: Python 3
- Automation: GitHub Actions (YAML)

## Implementation Details
The deployment is handled via a custom .github/workflows/deploy.yml.

### Systemd Configuration
```
[Unit]
Description=Python Honeypot Project
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/ubuntu/aws_honeypot_project
ExecStart=/usr/bin/python3 /home/ubuntu/aws_honeypot_project/honeypot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

## Monitoring & Analysis
Logs are stored in honeypot.log.

**To view live logs:**
``` Bash
tail -f ~/aws_honeypot_project/honeypot.log
```

**To analyze unique intrusion attempts:**
``` Bash
grep "INTRUSION ATTEMPT" honeypot.log | awk '{print $6}' | sort | uniq -c
```
## Known Limitations and Security Considerations
At this initial level, several architectural have been identified for future mitigation:

1. **Privilege Level**
- **Description:** The script currently requires root privileges to bind to port 80.
- **Potential Risk:** Any vulnerability in Python interpreter or honeypot script itself could lead to a full server compromise.
- **Mitigation Strategy:** Allow non-privileged users to bind to low ports (using authbind)

2. **Synchronous Connection Handling**
- **Description:** Connections are handled synchronously in a single-thread loop.
- **Potential Risk:** The system is vulnerable to Denial of Service (DoS) attacks.
- **Mitigation Strategy:** Transition to a multi-thread architecture.

3. **Static Fingerprinting and Detection**
- **Description:** The script provides a static HTTP banner.
- **Potential Limitation:** Advanced scanner (e.g. Shodan) can easily identify the service as fake.
- **Mitigation Strategy:** Implement dynamic header generation and support for basic HTTP methods.

4. **Log Persistence**
- **Description:** Logs are stored within a project directory.
- **Potential Limitation:** Risk of data loss during updates. The logs also reset with every service restart.
- **Mitigation Strategy:** Move logging to a centralized system directory.

## Future Roadmap
I plan on expanding this project and implementing:
- **Multi-port monitoring**
- **Deep Packet Inspection (DPI)**
- **Containerization**

## Disclaimer & Legal Notice
This project is created for educational and research purposes only.
- **Not for Production Use:** The scripts and configurations provided in this repository are designed for a controlled laboratory environment and do not meet the security standards required for production systems.
- **No Liability:** The author is not responsible for any misuse, damage, or legal issues caused by the application of this project. Use it at your own risk.
- **Ethical Conduct:** Always ensure you have explicit permission before monitoring or interacting with any network traffic that is not your own.