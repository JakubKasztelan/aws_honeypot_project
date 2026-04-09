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
