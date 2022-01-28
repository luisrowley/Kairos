# -*- coding: utf-8 -*-
import argparse
import os
import sys
import re
import validators

from shared.constants import DEFAULT_METHOD, MIN_ROUNDS

class ArgumentChecker():
    
    def __init__(self):
        # Instantiate the parser
        parser = argparse.ArgumentParser(description='Simple brute-force timing attack to get valid username based on average-time after n login requests.')

        # Required positional arguments
        parser.add_argument('-w', '--wordlist', type=str, help='Wordlist file with the list of usernames.')
        parser.add_argument('-u', '--url', type=str, help='Target URL with login form to attack.')

        # Optional positional arguments
        parser.add_argument('-n', '--rounds', type=int, default=MIN_ROUNDS, help='Number of attempts per userID to gain statistical significance (default 5).')
        parser.add_argument('-X', '--http-method', type=str, default=DEFAULT_METHOD, help='Specifies the HTTP method for the request (defaults to POST).')
        parser.add_argument('-d', '--data', type=str, default='', help='Comma-separated data containing user and password field names. Example: -d userfield,passfield')

        # Parse arguments
        self.args = parser.parse_args()

        if self.args.data:
            self.args.userfield = self.args.data.split(',')[0]
            self.args.passfield = self.args.data.split(',')[-1]
        else:
            self.args.data = ''


    """
    Simple getter function for arguments
    """
    def getArgs(self):   
        return self.args

    """
    Perform checks against valid arguments for the script to run
    """
    def parse(self):    
        # check if this script has been runned with an argument, and the argument exists and is a file
        if self.args.wordlist and (len(self.args.wordlist) > 1) and (os.path.isfile(self.args.wordlist)):
            fname = self.args.wordlist
        else:
            print("[!] Error: please provide a wordlist.")
            print("[-] Usage: python3 {} -w /path/to/wordlist".format(sys.argv[0]))
            sys.exit()

        if self.args.url and (len(self.args.url) > 1) and validators.url(self.args.url):
            url = self.args.url
        else:
            print("[!] Error: please provide a valid URL.")
            print("[-] Usage: python3 {} -u http://target.url".format(sys.argv[0]))
            sys.exit()
            
        if self.args.rounds < MIN_ROUNDS:
            print("[!] Warning: less than {} rounds can't guarantee robust results.".format(MIN_ROUNDS))
            
        return fname, url