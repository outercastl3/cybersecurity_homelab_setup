# Custom Wazuh Rules
Developed as part of a hands-on homelab SOC environment simulating real-world 
attack and detection scenarios. Goals: refined understanding of SIEM rule 
structure, improved detectability, noise reduction, and correlation of 
multi-stage attacks.

## Rules

| ID | Name | Goal |
|---|---|---|
| 10001 | SSH Brute Force Threshold | Trigger only after 15 failed SSH logins in 2 minutes, reducing noise from default rule 5760 |
| 10002 | Unauthorized User Creation | Detect new user accounts created outside of expected windows |
| 10003 | Cron Job Modification | Detect modifications to cron jobs as a persistence indicator |
| 10004 | Outbound Connection from Server | Flag unexpected outbound connections as potential C2 or reverse shell activity |
| 10005 | SSH Authorized Keys Modification | Detect changes to authorized_keys as a persistence indicator |
| 10006 | Incoming Scan Detection (Host) | Detect port scans observed by the Ubuntu agent |

## Grouping
Rules 10002–10005 share the group tag `attack.persistence` for dashboard correlation.

## Author
Bogdan Ermakov 
