import  requests
import re
from urllib.parse import urlparse, urljoin

def links(url):
    response = requests.get(url)
    return re.findall('(?:href=")(.*?)"', response.content)

def progress(url):
    hrefLink = links(url)
    for i in hrefLink:
        parseLink = urlparse.urljoin(url, i)

        if "#" in parseLink:
            parseLink = parseLink.split('#')[0]
        else:
            pass

        if url in parseLink and parseLink not in targetLink:
            targetLink.append(parseLink)
            print(parseLink)
            progress(parseLink)
        else:
            pass

url = input("Enter target URL: ")
protocol = input("Does the target use https protocol?  (y/n)")

if protocol is 'y' or protocol is 'Y' : protocol = "https://"
if protocol is 'n' or protocol is 'N' : protocol = "http://"

targetUrl = "{}{}".format(protocol,url)
targetLink = []

links(targetUrl)

