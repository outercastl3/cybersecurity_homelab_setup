# Protocol For Domain Takeover (adversary perspective)

## Target Environment Assumptions
- Windows 11 workstation misconfigured at the install by a junior administrator with:
    - disabled real-time antivirus monitoring
    - ICMP allowed through a custom firewall policy
- Domain joined workstation with standard user privileges
- Running RDP on port 3389
- Running SMB on port 445

## Lab Configuration Notes
Following commands were used to simulate the configuration of the environment:
- `Set-MpPreference -DisableRealtimeMonitoring $true`
- `netsh advfirewall firewall add rule name="Allow ICMPv4" protocol=icmpv4:8,any dir=in action=allow`
- `Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name "fDenyTSConnections" -Value 0`
- `netsh advfirewall firewall add rule name="Allow SMB" protocol=TCP dir=in localport=445 action=allow`

## Scenario Context
- Attacker gained previous access onto our local network
- through a prior compromise like
    - phishing
    - credential theft of the Company VPN

## Reconnaissance
- We start by gathering information about our Target, in this case it would be a machine corresponding to the ip:192.168.1.10
- i will run an nmap scan to gather services that are up and their version, along with OS its running etc.
    - nmap -sV -sS -A -p- 192.168.1.10
![Nmap Result](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/nmap_scan.png)
- Information we gathered:
    - we have a hardened SMB2 with signing enabled and required running on port 445
        - SMB relay attacks are not viable due to signing requierements
    - couple of internal Windows services
    - Port 135 open running MSRPC, confirming its a Windows target
    - OS fingerprinted target as Windows 11 with 96% confidence
    - Single hop confirms direct LAN access

## Intitial Access (TA0001)

## Persistance (TA0003)

## Privilege Escalation (TA0004)

## Credential Access (TA0006)

## Lateral Movement (TA0008)

## Domain Dominance

## Outcome
