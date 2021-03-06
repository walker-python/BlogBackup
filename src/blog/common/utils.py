#! encoding=utf-8
import traceback

__author__ = 'apple'

from urllib.parse import urlparse
import urllib3
import certifi
import os
import re
import blog.gui.utility
import threading
import time

class Utils:

    @staticmethod
    def is_backuping_stop():
        currentThread = threading.currentThread()
        return (not currentThread.status[0])

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
    def DownloadFile(url,output,http):
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
                dirss =  output + "/" + res.netloc+ path[0:index]
                dirssPath = output + "/" + res.netloc + path
                dirss_ansi = dirss
                if not os.path.exists(dirss_ansi):
                    os.makedirs(dirss_ansi)
            count = 1
            while True:
                if(Utils.is_backuping_stop()):
                    return None

                if count < 0:
                    break
                count = count - 1
                header = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
                }

                if (not url.startswith("http://")) and (not url.startswith("https://")):
                    break
                try:
                    # print "url: %s:%d" % (url,count)
                    dirssPath_ansi = dirssPath
                    if not os.path.exists(dirssPath_ansi):
                        print (url)
                        if (-1 != url.find("https://blog.csdn.net")):
                            return None

                        time.sleep(0.5)
                        blog.gui.utility.get_queue().put((0, url))
                        response = http.request('GET', url, None, header)
                        resourceFile = open(dirssPath_ansi,"wb")
                        responseText = response.data
                        if url.endswith(".js"):
                            responseText = responseText.decode('utf-8')
                            responseText = responseText.replace("http://","")
                            responseText = responseText.replace("https://","")
                            responseText = responseText.encode("utf-8")
                        resourceFile.write(responseText)
                        resourceFile.close()
                    break
                except Exception as e:
                    if(Utils.is_backuping_stop()):
                        return None

                    exstr = traceback.format_exc()
                    blog.gui.utility.get_queue().put((0,"DownloadFile1: %s" % exstr))
                    print (exstr)

        except Exception as e:
                exstr = traceback.format_exc()
                blog.gui.utility.get_queue().put((0, "DownloadFile1: %s" % exstr))
                print (exstr)

        return ("",url,output)

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
                if(Utils.is_backuping_stop()):
                    return None

                one = strMatch[i]
                newurl = Utils.GetConcatUrl(css[1],one)
                # print "newurl %s,%s,%s" % (newurl ,css[1] , one)
                # Utils.DownloadFile(newurl,css[2])
                return (newurl,css[2])
        except Exception as e:
                blog.gui.utility.get_queue().put((0,e))
        return None

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

