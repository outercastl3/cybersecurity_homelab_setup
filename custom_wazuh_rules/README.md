# Custom Wazuh Rules
Developed as part of a hands-on homelab SOC environment simulating real-world 
attack and detection scenarios. Goals: refined understanding of SIEM rule 
structure, improved detectability, noise reduction, and correlation of 
multi-stage attacks.

## Rules

## Rules
| ID | Name | Group | MITRE | Goal |
|---|---|---|---|---|
| 10001 | SSH Brute Force Threshold | attack.network | T1110 | Trigger only after 15 failed SSH logins in 2 minutes, reducing noise from default rule 5760 |
| 10002 | Unauthorized User Creation | attack.persistence | T1136 | Detect new user accounts created outside of expected working hours |
| 10003 | Cron Job Modification | attack.persistence | T1053.003 | Detect modifications to cron jobs as a persistence indicator |
| 10004 | Scheduled Task Creation (Windows) | attack.persistence | T1053.005 | Detect creation of scheduled tasks via schtasks.exe |
| 10005 | SSH Authorized Keys Modification | attack.persistence | T1098.004 | Detect changes to authorized_keys following a successful SSH login |
| 10006 | Incoming Scan Detection (Host) | attack.network | T1046 | Detect port scans observed by the Ubuntu agent |
| 10007 | Login Page Brute Force | attack.web | T1110 | Detect 10 or more POST requests to login.php within 60 seconds |
| 10008 | SQL Injection Attempt | attack.web | T1190 | Detect SQL keywords in HTTP requests indicating injection attempts |
| 10009 | Command Injection Attempt | attack.web | T1059 | Detect shell metacharacters in HTTP requests indicating command injection |
| 10010 | Directory Enumeration | attack.web | T1083 | Detect requests to sensitive paths indicating directory bruteforcing |

## Grouping
Rules 10002–10005 share the group tag `attack.persistence` for dashboard correlation.
Rules 10007-10010 share the group tag `attack.web` for dashboard correlation.

## Author
Bogdan Ermakov 
