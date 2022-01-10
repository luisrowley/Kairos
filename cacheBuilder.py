import json

class CacheBuilder():
    def __init__(self, fileName="cache.json"):
        self.name = fileName
        
    def createCache(self, filename, data):
        with open(filename, "w") as jsonFile:
            json.dump(data, jsonFile)