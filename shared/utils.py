from urllib.parse import urlparse

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
def maxDelta(list):
    tempMin = list[0]
    maxDiff = 0
    for i in range(len(list)):
        if (list[i] < tempMin):
            tempMin = list[i]
        elif (list[i] - tempMin > maxDiff):
            maxDiff = list[i] - tempMin
    return maxDiff
