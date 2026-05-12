# Cybersecurity Homelab - SOC & Offensive Simulation
This environment includes both defensive monitoring (SIEM-based detection) and offensive simulations to replicate realistic attack and detection cycles found in enterprise SOC environments.

This project simulates a real-world SOC environment with integrated logging, detection, and attack scenarios. It was built to replicate Tier 1 SOC workflows including log analysis, incident detection, and response actions while also incorporating offensive security simulations.

The goal is to bridge defensive monitoring (Blue Team) with attack simulation (Red Team) to build a practical understanding of modern security operations

## Key Skills Demonstrated

- SIEM deployment and configuration (Wazuh)
- Centralized log pipeline engineering (syslog-ng)
- Network security architecture (pfSense firewalling)
- Active Directory environment setup and attack simulation
- Incident detection and response workflows
- MITRE ATT&CK framework mapping

## Technologies Used:
- pfSense, Wazuh, Ubuntu Server, Windows Server, Kali Linux

## Setup Description

- Ubuntu Server with Wazuh SIEM collecting logs from an Win11 agent
- Win11 client acting as a workstation
- pfSense(on FreeBSD basis) gateway with PF firewall rules

## Implemented Scenarios

- SSH brute-force attack detection and analysis
- Nmap reconnaissance detection via log monitoring
- Windows workstation security event monitoring
- Log correlation and alerting using Wazuh rules

## Planned Enhancements

- Malware analysis sandbox integration
- Advanced Active Directory attack scenarios
- Automated incident response playbooks

## Goals of the Homelab

- Gain familiarity with workflows revolving around SIEMs
- Develop ability to analyze raw logs and identify security-relevant events
- Optimize workflows for log investigation and SIEM usage
- Gain experience in setting up a multi-level Network and Virual Machines setups


## Network Diagram
![Network Diagram](https://outercastl3.github.io/cybersecurity_homelab_setup/Network_DiagramV3.png)

# Author 
Bogdan Ermakov
