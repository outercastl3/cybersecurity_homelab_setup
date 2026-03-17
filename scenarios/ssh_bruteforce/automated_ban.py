import paramiko
import argparse

def argument_parse():
    parser = argparse.ArgumentParser(
        prog='Automatic script to add IP-Address into pfctl ban tables',
        description='Script which SSHs into pfSense client and executes command of adding an IP-Address into firewall tables',
        usage='automated_ban.py -l [PFSENSE_LOGIN] -p [PASSWORD] -ip [IP_ADDRESS]',
        epilog='Example: automated_ban.py -l root -p 12345 -ip 192.1.1.1'
        )

    parser.add_argument(
        "-l", "--login",
        required=True,
        help="Login of the required pfSense/gateway"
        )

    parser.add_argument(
        "-gt_ip", "--gateway_ip",
        required=True,
        help="IP of the gateway"
        )

    parser.add_argument(
        "-p", "--password",
        required=True,
        help="Password for Login",
        )

    parser.add_argument(
        "-ip", "--ip_address",
        required=True,
        help="IP-Address to ban"
        )
    
    return parser.parse_args()

def connection(gateway_ip,login,password,ipaddr):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=f"{gateway_ip}", username=f"{login}", password=f"{password}")
        stdin, stdout, stderr = client.exec_command(f"pfctl -t bruteforce -T add {ipaddr}")

        output = stdout.read().decode("utf-8")
        errors = stderr.read().decode("utf-8")

        print("Output:", output)
        print("Errors:", errors)
        
        if not errors:
            print(f"Successfully banned {ipaddr} on pfSense")

    except Exception as e:
        print(f"Connection failed: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    args = argument_parse()
    connection(args.gateway_ip,args.login,args.password,args.ip_address)

