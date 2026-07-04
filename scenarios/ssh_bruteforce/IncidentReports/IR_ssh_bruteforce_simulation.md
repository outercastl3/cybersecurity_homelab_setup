# Incident Report of SSH Brute Force attempt on 08.04.2026

# Overview
- Detected and responded to real internal SSH brute-force attack against Ubuntu server, correlating Wazuh alerts with a custom parser
- Followed SANS IR framework explicitly: Identification -> Containment -> Eradication
- Contained via firewall block (ufw) and active session termination (loginctl), while preserving evidence
- Discovered adversary had created a new unauthorized user account during the compromise window; disabled compromised and rogue accounts
- Root-cuased a timestamp normalization issue (Ubuntu server clock offset) that had to be corrected during analysis

At 20:09:48, a network scan was detected from 192.168.1.30 targeting our internal Ubuntu Server 192.168.1.20 using Nmap.  
The Ubuntu system was configured in UTC, resulting in a two-hour offset from other systems. All timestamps in this report have been normalized to a common timeline.  

![Nmap Scan](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ssh_bruteforce/screenshots/nmap_scan_ir.png)

At 20:18:23, multiple failed login attempts to SSH on our Ubuntu Server were observed.  

![Failed Logons Wazuh](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ssh_bruteforce/screenshots/failed_wazuh.png)

This was followed by a successful login at 20:19:19.  

I decided to check logs with my parser, and at 20:21:32 found out a successful login was made from IP 192.168.1.30 at 20:19:17.  

![Parser and Log tail outputs](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ssh_bruteforce/screenshots/parser_and_log.png)

Due to processing delay, Wazuh showed the successful login later than it appeared in the raw logs, explaining the timestamp discrepancy.  

After approximately 12 minutes have passed, another successful login was made at 20:30:52.  

![Successful Logon](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ssh_bruteforce/screenshots/log_succesful.png)

This corresponds to the Identification phase of the SANS Incident Response Framework.  

The next phase is Containment.  

The attacker’s IP was blocked at the firewall level, and SSH was temporarily restricted, as the attacker was within the local network and could have already established persistence.  

    - sudo ufw deny from 192.168.1.30

Then we check for further possible damage or persistence creation by the adversary.  

We perform Preservation of Evidence:  
Logs were saved to a secure location:  

    - cp /var/log/auth.log /home/admin1

Afterwards, we check if the adversary is still logged in and if the session is still active.  

    - the `who` command was executed  

![Who output](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ssh_bruteforce/screenshots/who_output.png)

We can see there is still an admin1 session running from 192.168.1.30, the adversary IP.  

Alternatively, we use `loginctl list-sessions`:  

![loginctl](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ssh_bruteforce/screenshots/loginctl.png)

We see that session 11 is the adversary’s session, so it is terminated by running:  

![terminate](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ssh_bruteforce/screenshots/terminate.png)

At this point, the malicious session was terminated, evidence was preserved, and the incident was contained.  

The system was then checked for further persistence attempts by the adversary.  

I used grep on the auth.log and found a newly created user at 20:37:25.  

![New User created](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ssh_bruteforce/screenshots/new_user.png)

The compromised user accounts were disabled at 20:38:13:  

    - sudo usermod -L user1  
    - sudo usermod -L admin1  

## Eradication steps included:
- Removal of unauthorized user accounts  
- Verification of SSH authorized_keys  
- Review of cron jobs  
- Inspection of running processes  

## Lessons Learned:
- Disable SSH password authentication and operate primarily using SSH keys  
- The current logging setup proved effective in spotting SSH brute force attempts  
- User account monitoring should be enhanced  
- Time synchronization across systems should be standardized  

No evidence of data exfiltration or system modification was found beyond the user creation and unauthorized access.  

Continuous monitoring of logs should be maintained.  

## Incident Maps to the following MITRE ATT&CK techniques:
- T1110 - Brute Force  
- T1078 - Valid Accounts  
- T1021 - Remote Services (SSH)  
