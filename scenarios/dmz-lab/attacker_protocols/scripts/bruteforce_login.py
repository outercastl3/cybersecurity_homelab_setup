import request
import os
import argparse

def argument_parse():
    pars = argparse.ArgumentPraser(
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
            requidred=True,
            help="Path to the password file"
            )

    pars.add_argument(
            "-t", "--target",
            help="URL of the target"
            )
    
    pars.add_argument(
            "--threads",
            help="The Number of Threads"
            )

    pars.add_argument(
            "-v", "--verbose",
            help="Verbose output"
            )
    return pars.parse_args()


if __name__ == "__main__":

