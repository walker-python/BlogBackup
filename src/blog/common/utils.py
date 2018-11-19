#! encoding=utf-8
__author__ = 'apple'

from urlparse import urlparse
import urllib2
import os
import time
import re
import html5lib

class Utils:

    @staticmethod
    def FilterSlash(url):
        newurl = url.replace("//","/../")
        if newurl == url:
            return newurl
        else:
            return Utils.FilterSlash(newurl)

    @staticmethod
    def GetConcatUrl(url,png):
        # one: "../images/f_icon.png" -- url http://static.csdn.net/public/common/toolbar/css/index.css
        count = 0
        png = Utils.FilterSlash(png)
        index = png.find("..")
        startindex = None
        while index != -1:
            count = count + 1;
            startindex = index + 2
            index = png.find("..",startindex)

        second = png[startindex:]
        length = len(url)
        index = url.rfind("/")
        endindex = 0
        while count >= 0 and index != -1:
            endindex = index
            index = url.rfind("/",0, endindex)
            count = count - 1
        first = url[0:endindex]
        return first+second

    @staticmethod
    def DownloadFile(url,output):
        responseText = None
        dirssPath = None
        # 有些css里的image超链接竟然带空格?csdn不检查的?
        url = url.replace(" ","")
        try:
            res = urlparse(url)
            url = res.scheme+"://"+res.netloc+res.path
            path = res.path
            index = path.rfind('/')
            dirss = "/"
            if index != -1:
                dirss =  output + "/" + res.netloc.encode("utf-8") + path[0:index].encode("utf-8")
                dirssPath = output + "/" + res.netloc.encode("utf-8") + path.encode("utf-8")
                dirss_ansi = dirss.decode('utf-8')
                if not os.path.exists(dirss_ansi):
                    os.makedirs(dirss_ansi)
            count = 1
            while True:
                if count < 0:
                    break
                count = count - 1
                header={"User-Agent": "Mozilla-Firefox5.0"}

                if (not url.startswith("http://")) and (not url.startswith("https://")):
                    break
                try:
                    # print "url: %s:%d" % (url,count)
                    # time.sleep(0.5)
                    request = urllib2.Request(url,None,header)
                    response = urllib2.urlopen(request)
                    dirssPath_ansi = dirssPath.decode("utf-8")
                    if not os.path.exists(dirssPath_ansi):
                        resourceFile = open(dirssPath_ansi,"wb")
                        responseText = response.read()
                        if url.endswith(".js"):
                            responseText = responseText.replace("http://","")
                            responseText = responseText.replace("https://","")
                        resourceFile.write(responseText)
                        resourceFile.close()
                    break
                except Exception,e:
                    # print "DownloadFile: %s:%d:%s" % (e,count,url)
                    pass
                    # exstr = traceback.format_exc()
                    # print exstr

        except Exception,e:
                pass
                # exstr = traceback.format_exc()
                # print exstr

        return (responseText,url,output)

    @staticmethod
    def ReadCss(css):
        # print "ReadCss"
        mode = 'url\([\'\"]?([^)\'\"]+)[\'\"]?\)'
        pattern = re.compile(mode)
        try:
            text = css[0]
            if css[0] == None:
                return
            strMatch = pattern.findall(text)
            size = len(strMatch)
            # print "size: ",size
            for i in range(0,size,1):
                one = strMatch[i]
                newurl = Utils.GetConcatUrl(css[1],one)
                # print "newurl %s,%s,%s" % (newurl ,css[1] , one)
                Utils.DownloadFile(newurl,css[2])
        except Exception,e:
                print e

    @staticmethod
    def GetHtmlName(url):
        htmlNameIndex = url.rfind("/");
        urlLen = len(url)
        htmlName = ""
        if htmlNameIndex+1 == urlLen:
            htmlNameIndex = url.rfind("/",0,htmlNameIndex)
            htmlName = url[htmlNameIndex+1:urlLen-1]
        else:
            htmlName = url[htmlNameIndex+1:]
        return htmlName

