# Scenarios SSH BruteForce protocol

## First Preparations and steps
- Firstly i have written a small script for a simulation
- its based on Paramiko python library
- as wordlist i would be using a shortened version of rockyou.txt ~1000 lines
- The goal is to see how bruteforce attack looks like in a real environment
- Create tools to limit influence of bruteforce attack (reduce noise, automate ip-ban)
- Such can be achieved by creating custom SIEM Rules and creating an automated ip blacklist script would SSH into pfSense via Paramiko and add the adversariy's IP-Address into pfctl tables upon detection
