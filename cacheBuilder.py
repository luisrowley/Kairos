import json
from utils import generateDomainID

"""
Perform checks against possible username/password field names and get valid ones
"""
class CacheBuilder():
    def __init__(self, fileName="cache.json"):
        self.name = fileName
        
    def writeCache(self, url, userfield, passfield):
        with open(self.name, "w") as jsonFile:
            domainID = generateDomainID(url)
            data = {}
            data[domainID] = []
            data[domainID].append({
                'url': url,
                'userfield': userfield,
                'passfield': passfield
            })
            json.dump(data, jsonFile)
            
    def readCache(self, domain):
        with open(self.name) as jsonFile:
            data = json.load(jsonFile)
            userfield = ''
            passfield = ''
            for d in data[domain]:
                userfield = d['userfield']
                passfield = d['passfield']
            return userfield, passfield
