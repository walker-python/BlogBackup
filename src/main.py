#! encoding=utf-8

import html5lib
import urllib2
import sys
import os
import time
import re
import blog.plugins.csdn
from urlparse import *

__author__ = 'apple'

# if __name__ == "__main__":
#     namespace = "{http://www.w3.org/1999/xhtml}"
#     document  = html5lib.parse("<form action='http://www.baidu.com'></form>")
#     elements = document.findall('.//{0}form'.format(namespace))
#     for one in elements:
#         action = one.attrib["action"]
#         print action

def getDomainMainPart(url):

    http = "http://"
    https = "https://"
    if(url.startswith(http)):
        url=url[len(http):]
    elif(url.startswith(https)):
        url=url[len(https):]

    index = url.find("/")
    if(index != -1):
        url = url[0:index+1]
    else:
        url += "/"

    pattern = re.compile(r'^[^/]+\.([^.]+)\.(com\.cn|net\.cn|gov\.cn|org\.cn|com|cn|edu|gov|org|cc|net|tk|biz|info|tv|pro|co|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cf|cg|ch|ci|ck|cl|cm|cn|co|cq|cr|cu|cv|cx|cy|cz|de|dj|dk|dm|do|dz|ec|ee|eg|eh|es|et|ev|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gh|gi|gl|gm|gn|gp|gr|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|in|io|iq|ir|is|it|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|mg|mh|ml|mm|mn|mo|mp|mq|mr|ms|mt|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nt|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|pt|pw|py|qa|re|ro|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sk|sl|sm|sn|so|sr|st|su|sy|sz|tc|td|tf|tg|th|tj|tk|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|va|vc|ve|vg|vn|vu|wf|ws|ye|yu|za|zm|zr|zw|me)/$', re.I)
    strMatch = pattern.findall(url)
    if len(strMatch)>0:
        return strMatch[0][0]
    else:
        return ""

def testGetDomainMainPart():
    result= getDomainMainPart("http://blog.csdn.net/infoworld")
    print "1",result

    result= getDomainMainPart("http://12.disd.cnblogs.com/")
    print "2",result

    result= getDomainMainPart("http://12.disd.cnblogs.com")
    print "3",result

    result= getDomainMainPart("http://12.disd.cnblogs.com/zhyg/p/4315787.html")
    print "4",result

def queryBlogUser(url,pos):
    if(pos != -1):
        pos+=1
        last = url.find("/",pos)
        if(last == -1):
            return url[pos:]
        else:
            return url[pos:last]
    else:
        return ""

def queryCsdnUrl(url):
    pos = url.find("//")
    last = -1
    if(pos != -1):
        pos = url.find("/",pos+2)
    else:
        pos = url.find("/")

    return queryBlogUser(url,pos)

if __name__ == "__main__":
    url = "blog.csdn.net/infoworld/adfaadfa"
    userId = queryCsdnUrl(url)
    print userId
    # moduleName = getDomainMainPart(url)
    # if moduleName == "csdn":
    #     blog.plugins.csdn.run(url,"C:\\Users\\apple\\Desktop\\New folder")
