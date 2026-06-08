# Setup protocol for DMZ and Web-Applications hosting
A detailed description of my setup for this particular scenario

## Operating System Install
- Used debian 13.4 install from official website
- Allocated 2 cores and 2048 MB of RAM with 20gb of space
- No Desktop Environment, only web server and ssh server
- created a non-root user outercastle 

## DMZ Setup
First we need create DMZ interface for the OS and pfSense. We perform it through KVM/QEMU GUI
![create new DMZ interface](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/screenshots/network_interface.png)
Afterwards we add the newly created Interface into our DMZ machine as the only network interface
And into pfSense as 3rd network interface. In pfSense console, we add new interface as OPT1 and assign 192.168.20.1/24 as its static IP
![assign static IP](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/screenshots/static_ip.png)
Now we create new specific firewall rules, to accommodate for the creation of DMZ
First rule would allow us to connect a wazuh agent in the future
![wazuh rule](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/screenshots/wazuh_rule.png)
Second rule would allow us package installation (for docker etc.)
![outbound rule](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/screenshots/outbound_rule.png)
And finally a rule that specifies that DMZ will not be able to touch lab-lan
![block rule](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/screenshots/block_rule.png)
Our rules hierarchy for our OPT1/DMZ interface looks like this
![rules hierarchy](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/screenshots/rules_hier.png)
We also create a lab-lan rule which allows us to access DMZ from lab-lan machines
![lablan rule](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/screenshots/lablan_rule.png)
Due to pfSense quirks, i had to create a small script, which reloads all services, and brings the network interface up at /usr/local/etc/rc.d/dmz_up.sh
![script](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/screenshots/script.png)
rc.reload_all is used in script to force complete restart of all functions in pfSense equivalent to applying changes in the WebGUI, Delay is necessary as rc.d scripts run immediately at boot before network interfaces are fully initialized, causing the command to fail without it
For our DMZ to have internet connection, we also need to change Outbound NAT Mode from Automatic to Hybrid and add new NAT rule for WAN interface
![nat rule](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/screenshots/wan_nat_rule.png)
Now we need to point our dmz towards our pfSense gateway, i will be using systemd-networkd, by modifing the /etc/systemd/network/10-enp1s0.network
![networking dmz](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/screenshots/networkingdmz.png)
Then we apply by:
- sudo systemctl enable systemd-networkd
- sudo systemctl restart systemd-networkd
Afterwards we check if it works
![ipa dmz](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/screenshots/ipa_dmz.png)
To have domain name resolution on the Debian DMZ, we point it towards our windows server with help of resolv.conf by adding
```bash
echo "nameserver 192.168.1.40" >> /etc/resolv.conf
```
Now we can start getting necessary packages for the JuiceShop and DVWA
Through the bash script i created install.sh, should be ran as root
Now we create project directory structure and necessary configs
- We create a folder dmz-lab
```bash
mkdir -p ~/dmz-lab/nginx
cd ~/dmz-lab

usermod -aG docker outercastle # To add my user into docker group
```
We create a docker compose config (you can find it in scripts and files folder)
The DVWA also requires the underlying database which is hosted with mysql5.7
Then we create the nginx config file (can be found in scripts and files folder as well)
After writing both scripts, we start by fetching the files for both web-applications
```bash
docker compose up -d
```
Our services are up
![docker services](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/screenshots/services.png)
Now as last we add another firewall rule, to allow traffic on port 80 for 192.168.20.10, so we can simulate users accessing our web-services
![lan rule](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/screenshots/lan_rule2.png)
Our setup is finished and we can test if the web-applications are working as expected
For this scenario i will be using Windows Server as my main domain name resolver, so i have to point Kali machine towards my Windows Server as well, by running:
```bash
echo "nameserver 192.168.1.40" >> /etc/resolv.conf
```
And we add ip to domain DNS Server Resource Record on Windows Domain Controller
```powershell
Add-DnsServerResourceRecordA -ZoneName "lab.local" -Name "dvwa" -IPv4Address "192.168.20.10"
Add-DnsServerResourceRecordA -ZoneName "lab.local" -Name "juiceshop" -IPv4Address "192.168.20.10"
```
Now from Kali machine we test if the web-applications are accessible
![dvwa](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/screenshots/dvwa.png)
![juiceshop](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/screenshots/juiceshop.png)
Both web-services are accessible and ready to be used
Last preparations would be deploying a wazuh agent and forwarding logs towards our Wazuh Manager
We deploy the Agent based on the instructions from the Wazuh
```bash
wget https://packages.wazuh.com/4.x/apt/pool/main/w/wazuh-agent/wazuh-agent_4.14.3-1_amd64.deb && sudo WAZUH_MANAGER='192.168.1.20' dpkg -i
./wazuh-agent_4.14.3-1_amd64.deb
```
and we check if installation worked in Endpoints
![wazuh dmz](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/screenshots/wazuh_dmz.png)
Docker doesnt automatically forwards logs towards Wazuh Agent, so we need to manually where we injest the Docker created log into wazuh
As Docker logs are not directly analyzed by Wazuh, we gonna do a pipe, where we translate the Logs into plaintext and inject them into the Wazuh

```bash
docker logs -f nginx-proxy 2>&1 | while read line; do echo "$line" >> /var/log/dvwa_access.log; done &
```
and add the file to be monitored in ossec.conf

```xml
<localfile>
    <log_format>syslog</log_format>
    <location>/var/log/dvwa_access.log</location>
</localfile>
```

Repeat the same with juiceshop
We also add nginx logs, because those are the ones capturing all the HTTP traffic including brute force requests, which are a part of my scenario
Now we run a small test, to see if the logs are being injected, by checking raw logs created by wazuh directly 
```bash
tail -f /var/ossec/logs/ossec.log | grep dmz
```
On the dmz machine, and created fake traffic from our kali machine or in another terminal
![Log forwarding test](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/screenshots/log_forwarding_test.png)
## Temporary workarounds
- pfSense OPT1 interface not coming up on boot -> rc.d script fix
- MySQL 8 incompatibility with DVWA -> downgrade to 5.7

## Author
Bogdan Ermakov
