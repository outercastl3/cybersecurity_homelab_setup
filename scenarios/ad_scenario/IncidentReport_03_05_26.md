# Incident Report of Malware File Execution of 03.05.26
- Windows 11 clock experienced drift during the incident, timestamps have been normalized
## Initial Detection
At 16:06 UTC a unusual amount of alerts was detected on our windows11_client machine. With top 3 alerts mapped to MITRE ATT&CK of Lateral Tool Transfer, DLL Search Order Hijacking and DLL Side-Loading
![Wazuh Dashboard](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/1602_wazuhdashboard.png)
After investigating Lateral Tool Transfer alerts, we could witness a multiple firing of the rule 92217 with first instance being noticed at 14:11:40.480, or the "Executable dropped in Windows root folder" which could hint towards malicious executable, insufficient evidence to come to a conclusion yet. 
![lateral tool transfer](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/rule92217.png)
![file drop](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/drop.png)
With a following execution timestamp confirmed via Sysmon Event ID 1, indicating invoice.exe was spawned with LAB\user1 context.
![execution](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/execution.png)
We can see that new services are being created at 14:11:47 14:11:48 and 14:15:10, possible hint towards reverse shell, tied with the dropped executable
![hklm](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/hklm.png)
And an abnormal cmd execution at 14:20:59, confirming our theory about reverse shell
starting from 14:21:45 and up to 14:21:51 we can see multiple executables dropped in Windows folder, hinting towards possible attempt to bypass UAC
Also multiple DLL hijack attempts hint towards privilege escalation attempts
Another cmd was executed, correlating with exploit execution
![dll_hijack](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/dll_hijack.png)
this hints towards multiple privilege escalation attempts and confirms that our system was compromised via a malicious file
Up until 14:42:19 multiple attempts of privilege escalation were made, and adversary started attempting creating persistence
at 14:49:45 an attempt at creating a scheduled task was made, but it was unsuccessful
at 14:50:46 adversary attempted adding a Value to a registry key, the operation was successful, possibly creating persistence on our System
![event viewer](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/event_viever_pers.png)
As we can see reg.exe was used for creating a run key, which maps to T1547.001. It was created under user1, so no admin rights were needed for HKCU

## Author
Bogdan Ermakov
