# Incident Report — Second Incident 10.05.26

Windows 11 clock experienced drift during the incident, 
timestamps have been normalized to Wazuh as the authoritative source.

## Initial Detection
At 19:19 we have noticed an unusual amount of several levels of triggered 
alerts, and decided to investigate further.
![dashboard](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/dashboard1.png)

## Investigation
After filtering, we notice that we yet again have an executable file 
dropped in folder commonly used by malware (92213) starting from 16:47:56, 
but also that an Application Compatibility Database launched (92058) 
at 17:46:50 and 18:46:51, hinting towards possible UAC bypass attempts.
![events](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/wazuh_filter1.png)
![events](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/wazuh_filter2.png)

After checking the exact JSON output of the alert, we determine that 
the executable is located at 
`C:\Program File (x86)\Common Files\System\UpdateChecker\UpdateChecker.exe`, 
which is not a default system folder, and should've been created by the 
adversary from the Incident on 03.05.26, surviving IR.v1 remediation.

We also find a possible Pass-The-Hash attack at 17:12:42, hinting towards 
credential access attempts and possible AS-REP roasting activity.
![passthehash](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/remotelogon.png)
For further investigation we access Windows Event Viewer and filter for relevant Event IDs 4768, 4769, 4771
![event manager](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/event_viewer.png)
During investigation, Windows Security logs on the Domain Controller showed no Kerberos related events, which indicates that Kerberos auditing was not enabled 

## Containment
Upon identifying the malicious executable, following containment 
steps were taken:

- Process UpdateChecker.exe was identified as running at this moment
![process](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/update_getprocess.png)
- Process was terminated along with any active connections
![terminate process](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/terminate_process.png)
- Malicious file was removed from the filesystem
- Attacker IP was blocked at the firewall level

## Eradication
Following containment, we again check the registry keys, this time 
conducting a more thorough sweep than in IR.v1, checking across all hives.
Malicious entry was identified and removed.
![deletion](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/deletion2.png)

- Scheduled tasks reviewed — no malicious entries found
- Startup items reviewed — no additional malicious entries found
- Running services reviewed — no malicious services identified
- User accounts reviewed — no unauthorized accounts found
- UpdateChecker directory removed entirely

## Lessons Learned
- IR.v1 failed to identify the persistence mechanism that survived 
  remediation — registry run keys must be checked across all hives
- Alert fatigue in IR.v1 contributed to missing folder creation and 
  file copy events present in Wazuh logs
- Pre-authentication should be enforced on all domain accounts 
  to prevent AS-REP roasting
- All domain service account passwords should be rotated following 
  credential access attempts
- Enable Kerberos auditing on Domain Controller level

## MITRE ATT&CK Mapping
- T1547.001 - Registry Run Keys / Startup Folder
- T1550.002 - Pass the Hash
- T1558.004 - AS-REP Roasting
- T1036.005 - Masquerading: Match Legitimate Name or Location
- T1548.002 - Bypass UAC

## Author
Bogdan Ermakov
