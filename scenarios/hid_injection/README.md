# HID Malicious Code Injection Scenario
Scenario gives an overview of Physical Attack angles, specifically HID Attacks
executing malicious keystroke injection via a Raspberry Pi Zero WH.
Physical access to a target machine is simulated by connecting the Pi Zero WH
via USB, which registers as a trusted HID keyboard device, bypassing endpoint
security controls.

## Tech Used
- Raspberry Pi Zero WH
- P4wnP1 OS
- P4wnP1 HID JavaScript
- Windows 11 VM
- Wazuh SIEM

## Planned Scenarios
- Data exfiltration to a remote host
- Persistence creation via registry run key
- Reverse shell connection establishment
- Credential harvesting via fake login prompt

## Author
Bogdan Ermakov


