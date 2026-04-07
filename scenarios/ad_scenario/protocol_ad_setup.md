# Active Directory Setup
a detailed how to Active Directory setup from my perspective with all necessary screenshots and configf

## First Steps
- download the windows server iso off Microsoft official website
- i chose the 2025 version, as its the newest one and endorsed to use by Microsoft
- after iso is downloaded onto our machine, we can create the machine in virt-manager
- we assign 4 CPU cores and at least 6gb memory to the machine, as windows manager is heavy reliant on resources
![Virtual Machine Setup](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/virtualmachine_setup.png)
- also we assign size for the disk image, minimum is at 32gb i will be assigning 40gb
![Virtual Machine Disk Space allocation](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/vm_diskspace.png)
- also we change Cache mode in out disk to none for security and performance reasons
![Disk Setup](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/storage_setup.png)
- we start installation, set language we would like to install
    - english in my case
![Language](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/language.png)
- at the image type, i select a headless standard evaluation
![Image Type](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/image_type.png)
- and lastly we choose our 40gb partition for installation location
![Install Location](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/install_location.png)
- then we proceed with installation
- we setup password and proceed into Command Line of the server by typing 15
![Password Setup](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/password.png)
![Command Line](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/command_line.png)
- first we lookup Interface indexes with 
    - Get-NetAdapter to set a static ip afterwards
![NetAdapter output](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/netadapter.png)
- We have a singular ethernet or our lan-lab network on index 5
- we set static ip to this index
    - with New-NetIPAddress -InterfaceIndex 5 -IPAddress 192.168.1.40 -PrefixLength 24 -DefaultGateway 192.168.1.1
![Setting Static Ip](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/staticip_setup.png)
- and we also set the DNS to loop into itself
    - with Set-DnsClientServerAddress -InterfaceIndex 5 -ServerAddress 127.0.0.1
    - but for installation we will be looping to our own ip, for installation only (192.168.1.40)
- we install Active Directory Domain Services
    - with Install-WindowsFeature -Name AD-Domain-Services -IncludeManagementTools
![ADDS Installation](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/ad_install.png)
- we setup the installtion of Domain Controller in such manner
![Domain Controller Promotion](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/domain_promotion.png)
- i chose the name lab.local for the lab, but in enterprise env, something more like corp.name.com would be more professional
- LAB would be the shortname for the domain
- also we will setup a recovery mode password
- after we start install, the VM would reboot itself, and we will be greated with a login screen
    - we should see that Administrator was addded to the LAB group (which we can observe on the screenshot)
![Login Screen](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/login.png)
- We also can check with Get-ADDomain
![Get-ADDomain  Output](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/get_addomain_output.png)
- we successfully promotaed our Domain Controller
- now we change the default DNS address of all of the other machines to point towards the Active Directory one (192.168.1.40) and we set DNS to loop into itself
- first we start with the Domain Controller
    - with Set-DnsClientServerAddress -InterfaceIndex 5 -ServerAddress 127.0.0.1
- afterwards we change the DNS for our Windows 11 client
![Windows DNS](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/windows_dns.png)
- then we change Ubuntu's netplan config, to resolve DNS through AD
![Ubuntu DNS](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/windows_dns.png)
- apply the changes 
- Similarly we change the Kali Machine
    - edit the resolv config and add 192.168.1.40 as the default DNS resolver
- Now we join Domain from our Windows 11 machine
    - we open Powershell as administrator
![Domain Join](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/domain_join.png)
- We are greeted with a context window
![Context Window](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/context_window.png)
- after we input the password, our machine would restart itself
- We are greeted with logon screen, but first we create a user on our Domain Controller by running 
    - New-ADUser -Name "user1" -SamAccountName "user1" -AccountPassword (Read-Host -AsSecureString "Password") -Enabled $true
![New User](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/newuser.png)
- now we get on Windows 11 machine
- and login to our user1 account
![Windows Logon](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/logon_windows.png)
- we successfuly created a joined domain account
