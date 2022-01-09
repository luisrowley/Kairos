"""
Wordlist is expected as simple list only containing userid,
password is mocked as we are not interested in its value at this point
"""
def unpack(fline):
    userid = fline
    passwd = 'foobar'
    return userid, passwd