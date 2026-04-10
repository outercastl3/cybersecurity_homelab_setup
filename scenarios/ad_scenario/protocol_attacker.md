# Protocol For Domain Takeover (adversary perspective)

## Target Environment Assumptions
- Windows 11 workstation misconfigured at the install by a junior administrator with:
    - disabled real-time antivirus monitoring
    - ICMP allowed through a custom firewall policy
- Domain joined workstation with standard usr privileges

## Lab Configuration Notes
Following commands were used to simulate the configuration of the environment:
- `Set-MpPreference -DisableRealtimeMonitoring $true`
- `netsh advfirewall firewall add rule name="Allow ICMPv4" protocol=icmpv4:8,any dir=in action=allow`
