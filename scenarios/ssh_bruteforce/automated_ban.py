import paramiko
import argparse

def argument_parse():
    parser = argparse.ArgumentParser(
        prog='Automatic script to add IP-Address into pfctl ban tables',
        description='Script which SSHs into pfSense client and executes command of adding an IP-Address into firewall tables',
        usage='automated_ban.py -l [PFSENSE_LOGIN] -p [PASSWORD] -ip [IP_ADDRESS]'
        epiloge='Example: automated_ban.py -l root -p 12345 -ip 192.1.1.1'
        )

    parser.add_argument(
        "-l", "--login",
        required=True,
        help="Login of the required pfSense/gateway"
        )

    parser.add_argument(
        "-p", "--password",
        required=True,
        help="Password for Login",
        )

    parser.add_argument(
        "-ip", "--ip_address"
        required=True,
        help="IP-Address to ban"
        )
    
    return parser.parse_args()

 def connection():
    pass

 if __name__ == "__main__":
     args = argument_parse()
     connection(args.login,args.password,args.ip_address)

