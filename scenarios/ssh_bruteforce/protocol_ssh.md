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
- For first walkthrough i would go with internal breach and targeting Ubuntu Servers SSH (192.168.1.20 on port 22)
