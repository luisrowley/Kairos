from urllib.parse import urlparse

class Utils():
    """
    Wordlist is expected as simple list only containing userid,
    password is mocked as we are not interested in its value at this point
    """
    def unpack(fline):
        userid = fline
        passwd = 'foobar'
        return userid, passwd

    """
    Converts input URL to domain identifier
    """
    def generateDomainID(url):
        return urlparse(url).netloc

    """
    Provides the maximum difference between elements of an unordered list
    """
    def maxDelta(vList):
        if not isinstance(vList, list):
            vList = list(vList) 
        tempMin = vList[0]
        maxDiff = 0
        for i in range(len(vList)):
            if (vList[i] < tempMin):
                tempMin = vList[i]
            elif (vList[i] - tempMin > maxDiff):
                maxDiff = vList[i] - tempMin
        return maxDiff
