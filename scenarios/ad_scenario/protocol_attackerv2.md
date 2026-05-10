# Second Attacker Protocol
In this protocol, i will simulate a repeated hit on the compromised machine, and try again work up until total Domain Ownage

## Renewed access
Due to created persistence and a successful survivability of wipe, i could access the Machine again, to try to attack it again.
To confirm, i got access to the right environment or to check which of compromised machines i am accessing, i check uid of user i am currently logged in as and privileges of this user
![checks](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/checks.png)
as we can, we are still running as LAB\user1 and privileges havent changed from last time.

## Domain Enumeration
Before attempting credential access, i enumerate domain users and services account to identify potential targets
![enum domain users](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/enumeration2.png)

## Credential Access
I would try and see if there any change in Kerberos tickets, by loading kiwi and checking kerberos ticket list
![Loading kerberos ticket list](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/load_list.png)
We can see there are 3 tickets that were found in current session, we can proceed further with Kerberoasting
We also can see that this machine has unconstrained delegation, we can tell that via a closer look onto 01 ticket, which has ok_as_delegate flag, which means any privileged user authenticating to TESTNAME1 would have their TGT cached on the machine.
This could be exploited if a Domain Admin  authenticated to TESTNAME1 machine, allowing ticket extraction via mimikatz for priv. escalation
As we know the password of the user, via previous credential access attempts, we can use them to get user SPNs via impacket
After several attempts, i came to conclusion, that Kerberoasting unlikely to work, because of troubles with encryption types
![encryption Kerb](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/kerb_encr.png)
We try to AS-REP roasting with a users file, which contains different possible account names, in this case i targeted svc_legacy as i knew it had pre-auth disabled, which allows AS-REP roasting at the first place
We successfully captured the AS-REP hash, which we could attempt to crack
![as-rep](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/as_rep.png)
I will be attempting to crack the hash with hashcat and with help of my previously used short version of rockyou.txt
We successfully cracked the hash and obtained the plain text password for svc_legacy user
![hashcat](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/hash_tgt.png)
As we have another user, we could be able to do further enumeration and have attempts at lateral movement.
We check if credentials we obtained are correct with help of netexec
![netexec output](https://outercastl3.github.io/cybersecurity_homelab_setup/scenarios/ad_scenario/screenshots/netexec.png)
Also svc_legacy can help us run BloodHound to map attack paths and possibility to access resources svc_legacy is privileged to.
Biggest impact wouldve been successful Kerberoasting and hold of svc_backup credentials, as it holds Domain Administrator rights

## Outcome
Possible further attacks vectors:
- DCSync attack as Domain Admin
- Golden ticket creation
- Complete domain takeover

## Mitre ATT&CK Mapping
- T1558.003 - Steal or Forge Kerberos Tickets: Kerberoasting
- T1558.004 - Steal or Forge Kerberos Tickets: AS-REP Roasting
- T1110.002 - Brute Force: Password Cracking
- T1574 - Hijacking Execution Flow (unconstrained delegation observation)
- T1087.002 - Account Discovery: Domain Account (enumerating SPNs and accounts)
- T1078.002 - Valid Accounts: Domain Accounts
- T1550.003 - Use Alternate Authentication Material: Pass the Ticket
## Author
Bogdan Ermakov
