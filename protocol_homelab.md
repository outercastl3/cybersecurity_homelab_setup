# Homelab Setup Protocol
works as my detailed steps description and a small instruction for future reference

## Setup description
- Windows 11 with a localuser setup
- Ubuntu Server with apache and wazuh
- OpenBSD 7.8 setup with pf files as main firewall

### OpenBSD Setup (09.03.2026) - Replaced, kept for reference
- Install OpenBSD and setup a singular root user
- Setup 2 Network Adapters one set to NAT other one set to Internal Network
![Network Adapter 1](setup_files/network_adapter1.png)
![Network Adapter 2](setup_files/network_adapter2.png)

##### Ifconfig output before the setup
![Ifconfig Output before](setup_files/ifconfig_output_before.png)

#### 1. Assign static IP to LAN interface
- echo 'inet 192.168.1.1 255.255.255.0' > /etc/hostname.em1

#### 2. Set em0/WAN interface to DHCP
- echo 'dhcp' > /etc/hostname.em0

#### 3. Enable IP forwarding
- echo 'net.inet.ip.forwarding=1' >> /etc/sysctl.conf

#### 4. Setup simple Pf rules for the beginning
- you can see my pf.conf below in the setup directory/folder

#### 5. Enable and load PF and make it start on Boot
- pfctl -e 
- pfctl -f /etc/pf.conf
- rcctl enable pf

#### 6. If config output after the setup
![Ifconfig output after](setup_files/ifconfig_output_after.png)

### Ubuntu Server Setup (10.03.2026)
- Setup ubuntu server and modify /etc/netplan/00-installer-config.yaml as follows(visible in the setup files)
- Change Network Adapter of the VM (see picture below)
![Network Adapter Ubuntu](setup_files/network_adapter_ubuntu.png)
- Ran into a problem, Ubuntu Server VM no longer boots properly
    - try to boot through recovery with GRUB
    - successful
- after a quick search i found that its VirtualBox console issue fixable by Right Ctrl + F1/F2/F3
- ip a output after the setup
![Ip A output after](setup_files/ip_a_output_after.png)
- Download wazuh with help of curl -sO https://packages.wazuh.com/4.14/wazuh-install.sh (ensure the O in curl is capital letter o and not a zero)
- install wazuh with sudo bash ./wazuh-install.sh -a
- save given credentials

### Win11 Client Setup (10.03.2026)
- Setup Windows 11 with a local user setup via Microsoft account bypass 
- Change Network Adapter of the VM
![Network Adapter Windows11](setup_files/network_adapter_win11.png)
- in Network & Internet, change Ethernet to Manual IP with
    - IP: 192.168.1.10
    - Subnet mask: 255.255.255.0
    - Gateway: 192.168.1.1
    - DNS: 8.8.8.8
![Network Settings Windows](setup_files/network_win11.png)
- test connection by pinging the gateway and Internet(8.8.8.8 in this case)
![Test connectivity gateway](setup_files/ping_gateway.png)


![Test Connectivity to Internet](setup_files/ping_8.png)
- The setup Works, now we try to Access Wazuh to check if wazuh set up correctly
![Wazuh Setup](setup_files/wazuh_setup.png)
- Try and Login to ensure that credentials are correct and Wazuh is working
![Wazuh Home Page](setup_files/wazuh_page.png)
- It works
- install sysmon and Wazuh agent on win11
- install sysmon off official Microsoft Sysinternals and setup the SwiftOnSecurity config of Github
    - Run PowerShell as administrator and run
        - .\Sysmon64.exe -accepteula -i sysmonconfig-export.xml
        - as i installed it incorrectly, i had to update with .\Sysmon64.exe -c sysmonconfig-export.xml
![Sysmon Setup](setup_files/sysmon_update.png)
- For wazuh follow instructions on the local host website
- Successful agent installation
![Wazuh Agent Setup](setup_files/wazuh_agent.png)

### New gateway setup pfSense Community edition (10.03.2026)
- I decided to replace OpenBSD with pfSense
- Decision was based upon pfSense having more similarities to Enterprise environments and an easier log forwarding
- Download pfSense Community edition off Netgate website
- Setup pfSense similarly with 2 Network Adapters
![Network Adapter1 pfSense](setup_files/network1_pfsense.png)
![Network Adapter2 pfSense](setup_files/network2_pfsense.png)
- Install the OS itself and choose WAN for interface em0 and LAN for interface em1
- Reboot the VM
![pfSense setup Screenshot](setup_files/setup_pfsense.png)
- from Win11 access pfSense local website on 192.168.1.1
- Change the default password in System -> User Manager -> Admin -> Change password
- Setup of the OS is finished

### Host change and Switch to KVM (12.03.2026)
- unfortunetly my initial Host Device is no longer functional so i had to move my Setup to my spare Machine
- Also a switch towards KVM was made, as it has better stability and performance and is widely used in production Environments
- I will be using virt-manager as my GUI for KVM, which means i had to change Create new network plan for the VMs
- i created a new Virtual network lab-lan, which is has following parameters
![lab-lan](setup_files/lab-lan.png)
- and a NAT WAN named default
![nat-wan](setup_files/lab_default.png)
- Also an additional VM was added, Kali Linux as its not longer my host
- So my machines got following network settings:
    - pfSense -> Virtual Network: default
    - Windows 11 -> Virtual Network: lab-lan
    - Ubuntu Server -> Virtual Network: lab-lan
    - Kali Linux -> Virtual Network: lab-lan
- I decided to put Kali Linux on LAN as well, so i can have multiple angles to attack not only the gateway but also client and wazuh server, to simulate not only attack from Internet but also possible internal breach in action

### Log Forwarding Setup from pfSense to Wazuh (15.03.2026)
- Logs from pfSense are not directly accepted by the Wazuh Manager as they have a different formatting, so my approach is to reformat them with help of syslog-ng sitting on the Ubuntu server
- Topology would be this way then: pfSense -> syslog on UDP 514 -> syslog-ng reciever (UbuntuS) -> formatting -> Wazuh Manager
- First we setup the pfSense forwarding of the logs
    - Open WebGUI and access Status -> System Logs -> Settings
    - at the end of the page enable log forwarding
    - Select LAN option as we send the logs localy in this Lab
    - for IP select our Ubuntu Server IP on port 5140 -> 192.168.1.20:5140 
    - i will be using port 5140, to make sure there are no conflicts with Wazuh setup on port 514
    - select to forward everything

- On Ubuntu Server
    - install syslog-ng by running sudo apt install syslog-ng
    - we edit syslog-ng config and add pfSense as source
    ![source syslog-ng](setup_files/source_pfsense_syslog_ng.png)
    ![destination syslog-ng](setup_files/destination_wazuh_syslog_ng.png)
    ![log syslog-ng](setup_files/log_syslog_ng.png)
    - then we try if its working
        - see if the daemon itself is working
        - sudo systemctl status syslog-ng
        - then if its listening on right port and protocol
        - sudo ss -ulnp | grep 5140
        - then we generate some activity on the pfSense
        - and check through sudo tail -f /var/log/pfsense.log
        ![tail output](setup_files/tail_output.png)
        - success
        - now we forward those logs to Wazuh with editing syslog-ng.conf again
        ![destination syslog-ng2](setup_files/destination_syslog.png)
        ![log syslog-ng2](setup_files/log_syslog2.png)
        - restart the syslog-ng
        - now we edit ossec.conf or Wazuh config to accept forwarded logs
        ![ossec configuration](setup_files/ossec_local.png)
        - now check through Wazuh Dashboard if the logs are showing
        - navigate to Server Management -> Logs -> filter for 192.168.1.1
        ![wazuh dashboard 192.168.1.1](setup_files/wazuh_dashboard.png)
        - success
   - Lab Setup is Finished
