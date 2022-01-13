# -*- coding: utf-8 -*-
import os
import sys
import requests
from argchecker import ArgumentChecker
from cacheBuilder import CacheBuilder
from shared.utils import Utils
from samplelists.formfields import userfields, passfields

class Requester():
    def __init__(self):
        # get parsed arguments
        argchecker = ArgumentChecker()
        self.args = argchecker.getArgs()
        self.validFileName, self.validUrl = argchecker.parse()
        
        # cache builder instance
        self.cache = CacheBuilder()        

        # define a fake headers to present ourself as Chromium browser, change if needed
        self.headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36"}
        
        # get valid input fields
        self.userfield, self.passfield = self.preflight_request(self.args.url)

        # save average time for each user/pass combo
        self.averageTimes = []

     
    """
    Perform checks against possible username/password field names and get valid ones
    """
    def preflight_request(self, url):
        # perform target URL request one time
        data={'username': 'foo', 'password': 'foobar', "submit": "submit"}
        res = requests.post(url, headers=self.headers, data=data)
        domain = Utils.generateDomainID(url)

        print("[-] Finding valid user/pass field names...")

        # check if entry exists in the cache
        if os.path.isfile("cache.json") and self.cache.checkEntry(domain):
            validfields = self.cache.readCache(domain)
            print('[-] Fields from cache:', validfields[0], validfields[1])
            return validfields
        # look for matching fieldnames from page source
        for x in range(len(userfields)):
            for y in range(len(passfields)):
                userfield='name="{}"'.format(userfields[x])
                passfield='name="{}"'.format(passfields[y])
                if userfield in res.text and passfield in res.text:
                    print("[+] Correct combination found!", userfields[x], passfields[y])
                    print("[-] Creating cache entry for {}".format(url))
                    self.cache.writeCache(url, userfields[x], passfields[y])
                    return userfields[x], passfields[y]
        # no matching form fields then exit
        print("[!] Error: could not find valid form field names to send request.")
        sys.exit()


    """
    Send POST request to endpoint based on known user/pass field name params
    """
    def do_average_post_request(self, url, userid, passwd, headers, rounds):       
        if not self.userfield and not self.passfield:
            return False
        else:
            data = {self.userfield: userid, self.passfield: passwd, "submit": "submit"}
            total_time = 0

            for x in range(rounds):
                res = requests.post(url, headers=headers, data=data)
                total_time += res.elapsed.total_seconds()

            average_time = Utils.simpleAverage(total_time, rounds)
            # save average time for this rounds
            self.averageTimes.append(average_time)
            print("[+] user {:15}; rounds {}; average time {}".format(userid, rounds, average_time))
            # TODO: calculate max percentual change between requests and suggest greater n factor
        return True


    """
    Send POST request to endpoint based on known user/pass field name params
    """
    def send(self):
        with open(self.validFileName) as fh:
            # read file line by line
            for fline in fh:
                # skip line if it starts with a comment
                if fline.startswith("#"):
                    continue
                # extract userid and password from wordlist, removing trailing newline
                userid, passwd = Utils.unpack(fline.rstrip())

                # perform a number of rounds and get average time
                # TODO: implement multi-threading
                self.do_average_post_request(self.validUrl, userid, passwd, self.headers, self.args.rounds)

        print(Utils.listAverage(self.averageTimes), Utils.maxDelta(self.averageTimes))