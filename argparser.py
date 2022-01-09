# -*- coding: utf-8 -*-
import argparse

# Instantiate the parser
parser = argparse.ArgumentParser(description='Simple brute-force timing attack to get valid username based on average-time after n login requests.')

# Required positional arguments
parser.add_argument('-w', '--wordlist', type=str, help='Wordlist file with the list of usernames.')
parser.add_argument('-u', '--url', type=str, help='Target URL with login form to attack.')

# Optional positional argument
parser.add_argument('-n', '--rounds', type=int, default=5, help='Number of attempts per userID to gain statistical significance (default 5).')
parser.add_argument('-X', '--http-method', type=str, default='POST', help='Specifies the HTTP method for the request (defaults to POST).')

# Parse arguments
args = parser.parse_args()