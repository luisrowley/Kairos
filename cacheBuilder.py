import json
from shared.utils import Utils

"""
Perform checks against possible username/password field names and get valid ones
"""
class CacheBuilder():
    def __init__(self, fileName="cache.json"):
        self.name = fileName
        
    def writeCache(self, url, userfield, passfield):
        with open(self.name, "w") as jsonFile:
            domainID = Utils.generateDomainID(url)
            data = {}
            data[domainID] = []
            data[domainID].append({
                'url': url,
                'userfield': userfield,
                'passfield': passfield
            })
            json.dump(data, jsonFile)
            
    def readCache(self, domain):
        userfield = ''
        passfield = ''
        data = self.getFileData()
        for d in data[domain]:
            userfield = d['userfield']
            passfield = d['passfield']
        return userfield, passfield

    def checkEntry(self, key):
        list = self.getFileData()
        return key in list
    
    def getFileData(self):
        with open(self.name) as jsonFile:
            return json.load(jsonFile)