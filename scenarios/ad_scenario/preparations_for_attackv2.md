# Preparation steps for second attack protocol 
In this file, i would describe which and "how-to" meassures that were taken to expand the experience of the Active Directory Scenarios

## Meassures taken
- A service account with weak password was created
    - New-ADUser -Name "svc_backup" -SamAccountName "svc_backup" -AccountPassword (ConvertTo-SecureString "Password123" -AsPlainText -Force) -Enabled $true
- and we set a SPN, to enable possible Kerberoasting attacks for learning experience
    - Set-ADUser -Identity "svc_backup" -ServicePrincipalNames @{Add="backup/dc.lab.local"}

- A AS-REP roastable user was created
    - New-ADUser -Name "svc_legacy" -SamAccountName "svc_legacy" -AccountPassword (ConvertTo-SecureString "Summer2017!" -AsPlainText -Force) -Enabled $true
    - Set-ADAccountControl -Identity "svc_legacy" -DoesNotRequirePreAuth $true

- Enable unconstrained delegation on workstation
    - Set-ADComputer -Identity "TESTNAME1" -TrustedForDelegation $true

- Add svc_backup to a privileged group
    - Add-ADGroupMember -Identity "Domain Admins" -Members "svc_backup"

## Test the environment
![Domain Controller environment test](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/env.png)

## Possible new attack angles
- such misconfigurations allow us attack angles as:
    - Kerberoasting
    - AS-REP roasting
    - exploitation through delegation user misconfiguration
