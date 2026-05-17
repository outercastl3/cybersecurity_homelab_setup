import requests
import os
import argparse

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
            default=4
            help="The Number of Threads"
            )

    pars.add_argument(
            "-v", "--verbose",
            action"store_true",
            help="Verbose output"
            )
    return pars.parse_args()


def brute_force(username_file, password_file, url):
    try:
        with open(password_file, "r") as password:
            pass



if __name__ == "__main__":
    args = argument_parse()

