# Scenarios SSH BruteForce protocol

## First Preparations and steps
- Firstly i have written a small script for a simulation
- its based on Paramiko python library
- as wordlist i would be using a shortened version of rockyou.txt ~1000 lines
- The goal is to see how bruteforce attack looks like in a real environment
- Create tools to limit influence of bruteforce attack (reduce noise, automate ip-ban)
- Such can be achieved by creating custom SIEM Rules and creating an automated ip blacklist script would SSH into pfSense via Paramiko and add the adversary's IP-Address into pfctl tables upon detection
- Such script creates a weakpoint from security perspective, it would be more beneficial to have ssh-authentification from a secure file, rather then passing Arguments, but for sake of this lab, i would ignore those concerns, so the lab itself is not overcomplicated and provides a best learning experience at my level. 
- I have my Kali/attacker machine both on LAN and NAT to have 2 angles of attack if necessary
    - NAT interface would simulate external attacks towards pfSense from the internet
    - LAN would simulate internal breach / lateral movement within the network
    for LAN to work properly modify interface on /etc/network/interfaces
        ![interface-kali](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ssh_bruteforce/screenshots/kali_network1.png)
- For first walkthrough i would go with internal breach and targeting Ubuntu Servers SSH (192.168.1.20 on port 22)

## Walkthrough
- from kali machine run nmap scan to see if ssh ports are open
- run a nmap scan which picks up service versions by running
![Nmap Scan](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ssh_bruteforce/screenshots/nmap_scan.png)
- now we check if Wazuh picked it up in Wazuh WEB UI
- navigate to Threat Hunting and in Events we can see multiple failed HTTP 400 error codes, which hints to our nmap scan
![nmap output Wazuh](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ssh_bruteforce/screenshots/wazuh_nmap.png)
- now we run our SSH script
- i let my script run for 50 different passwords
![bruteforce](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ssh_bruteforce/screenshots/bruteforce_scrit.png)
- Now is the time to check the Wazuh dashboard
- we navigate to Threat Hunting
- we immediately see 102 failed auth-attempts
![wazuh dashboard1](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ssh_bruteforce/screenshots/wazuh_dashboard1.png)
- when we navigate to Events, we can see a lot of failed logon attempts as well
![wazuh events](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ssh_bruteforce/screenshots/wazuh_dasboard2.png)
- we can see Wazuh assigned different severity levels to different alerts, most dangerous one in this case is Multiple failed logons in short time with a severity level 10
- and also different rule ids:
    - failed sshd logon attempts with 5760
    - PAM: User login failed with 5503
    - Multiple Failed logons with 5551 in this case
- wordlist did not have my real password for purpose of seeing failed ssh bruteforce attemp, as a successful bruteforce would be a future idea for a scenario
- Wazuh is able to trigger scripts on its own, which is a good practice for our  automatic-ban script that we wrote
- My idea is to trigger script as soon as level 10 alert is triggered
- for it we need to edit ossec.conf
- we add active response
![active response](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ssh_bruteforce/screenshots/active_response.png)
- and then we add a corresponding command
![command](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ssh_bruteforce/screenshots/command_ossec.png)
- also for it to work, we need to modify pfSense to have SSH running
- we do it by going to pfSense WEB UI -> System -> Advanced -> Admin Access
![ssh setup](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ssh_bruteforce/screenshots/ssh_setup.png)
- then we need implement a Block Rule
- open WEB UI -> Firewall -> Aliases and we add a bruteforce HOST
- then we navigate to Firewall -> Rules -> LAN, then we add new Action block, with host bruteforce, any destination
![pfsense ui](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ssh_bruteforce/screenshots/pfsense_ui.png)
- Sadly due to my lab limitations i couldn't fully  implement automatic ip blockage, as my network is not segmented as good as enterprise systems, but also that pfSense does not allow custom pfctl rules and prefers to use WEB UI, i have some limitation in my Lab. In a Work environment, it is possible to implement my script with help of REST-API provided by the pfSense
- Otherwise the main goal of the LAB was achieved
