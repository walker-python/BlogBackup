#! encoding=utf-8

import urllib2
import urllib
import re
import os
import math
import sys
# from HTMLParser import HTMLParser
import html5lib
# from xml.etree.ElementTree import ElementTree
from urlparse import urlparse
import xml
import codecs
import traceback
import time

# class MyHTMLParser(HTMLParser):

#     def handle_starttag(self, tag, attrs):
#         # if tag.lower() == "img":
#             print "Encountered the beginning of a %s tag,attrs size %d" % (tag ,len(attrs))
#             for x in attrs:
#                 print "name %s,value %s" % (x[0],x[1])
#     def handle_endtag(self, tag):
#         print "Encountered the end of a %s tag" % tag

#     def handle_startendtag(self, tag, attrs):
#         print "Encountered the beginning of a %s tag,attrs size %d" % (tag ,len(attrs))
#         for x in attrs:
#             print "name %s,value %s" % (x[0],x[1])

# 资源尝试次数
gTestTime = 5

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
        global gTestTime
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
                time.sleep(0.5)
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
                print "DownloadFile: %s:%d:%s" % (e,count,url)
                # pass
                # exstr = traceback.format_exc()
                # print exstr

    except Exception,e:
            pass
            # exstr = traceback.format_exc()
            # print exstr
    
    return (responseText,url,output)

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
            newurl = GetConcatUrl(css[1],one)
            print "newurl %s,%s,%s" % (newurl ,css[1] , one)
            DownloadFile(newurl,css[2])
    except Exception,e:
            pass
            # exstr = traceback.format_exc()
            # print exstr 

def Download(url,output):
    # try:
    header={"User-Agent": "Mozilla-Firefox5.0"}
    namespace = "{http://www.w3.org/1999/xhtml}"
    request = urllib2.Request(url,None,header)
    response = urllib2.urlopen(request)

    data = response.read()
    document = html5lib.parse(data)
    imgElements = document.findall('.//{0}img'.format(namespace))

    # print "imgElements %d" % len(imgElements)
    for img in imgElements:
        src = img.attrib["src"]
        print "image %s" % src
        try:
            res = urlparse(src)
            # 非csdn的图片不下载
            if (-1 == res.netloc.find("csdn")) and (-1 == res.netloc.find("iteye")):
                print "image not download: %s:%s" % (src,res.netloc)
                continue
        except Exception,e:
            pass
        DownloadFile(src,output)

    linkElements = document.findall('.//{0}link'.format(namespace))
    # print "linkElements %d" % len(linkElements)
    for link in linkElements:
        href = link.attrib["href"]
        print "css %s" % href
        text = DownloadFile(href,output)
        if link.attrib.has_key("rel") and link.attrib["rel"].lower() == "stylesheet":
            ReadCss(text)

    scriptElements = document.findall('.//{0}script'.format(namespace))
    # print "scriptElements %d" % len(scriptElements)
    for script in scriptElements:
        if script.attrib.has_key("src"):
            src = script.attrib["src"]
            print "script %s-%s" % (src,output)
            if(src.startswith("//")):
                src="https:"+src
            DownloadFile(src,output)
        
    htmlNameIndex = url.rfind("/");
    urlLen = len(url)
    htmlName = GetHtmlName(url)
    output = output.decode("utf-8") + "/"+htmlName+".htm"
    data = data.replace("http://","")
    data = data.replace("https://","")
    data = data.replace("src=\"//","src=\"")
    data = data.replace("www.w3.org/1999/xhtml","http://www.w3.org/1999/xhtml")

    resourceFile = open(output,"wb")
    resourceFile.write(data)
    resourceFile.close()

def FilterSlash(url):
    newurl = url.replace("//","/../")
    if newurl == url:
        return newurl
    else:
        return FilterSlash(newurl)

def GetConcatUrl(url,png):
    # one: "../images/f_icon.png" -- url http://static.csdn.net/public/common/toolbar/css/index.css
    count = 0
    png = FilterSlash(png)
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

# 2018.8.17
# 获取页数, 通过 ceil(307.0/20)
# var pageSize = 20 ;
# var listTotal = 307 ;
# https://blog.csdn.net/infoworld/article/list
def getAllListUrl(url):
    header={"User-Agent": "Mozilla-Firefox5.0"}
    request = urllib2.Request(url,None,header)
    response = urllib2.urlopen(request)
    data = response.read()
    m = re.search("var[ ]{1,}pageSize[ ]+=[ ]*([0-9]+)",data)
    pageSize = m.group(1)
    m = re.search("var[ ]{1,}listTotal[ ]+=[ ]*([0-9]+)",data)
    listTotal = m.group(1)
    print pageSize
    print listTotal

    lastPageNum = int(math.ceil(float(listTotal)/float(pageSize)))
    urlList = []
    for x in xrange(1,lastPageNum+1):
        listUrl = "https://blog.csdn.net/infoworld/article/list/"+str(x)
        urlList.append(listUrl)

    return urlList


def getArticleList(url):
    # 获取所有的文章url
    # <div id="article_toplist" class="list"></div>
    # <div id="article_list" class="list"  
    
    # <div class="list_item article_item"
    
    # <div class="article_title">
    # <span class="ico ico_type_Original"></span>
    # <h1>
    #     <span class="link_title">
    #         <a href="/infoworld/article/details/18984183">

    # <div class="article_manage">
    # <span class="link_postdate"></span>

    urlList = getAllListUrl(url)
    print "文章页数 ",len(urlList)
    header={"User-Agent": "Mozilla-Firefox5.0"}

    allLists = []

    strPage = "分析 第 {0} 页 ".decode("utf-8").encode("utf-8")
    pageNum = 0
    global gTestTime
    artices = []
    for one in urlList:
        tryCount = gTestTime # try count
        while tryCount > 0:
            try:
                tryCount = tryCount - 1
                time.sleep(0.5) #访问太快会不响应
                request = urllib2.Request(one,None,header)
                response = urllib2.urlopen(request)
                data = response.read()
                pattern = re.compile('<p class="content">[^<]*<a href="([^"]+)" target="_blank">')
                m = re.findall(pattern,data)
                size = len(m)
                # print "size: ",size
                for i in range(0,size,1):
                    oneUrl = m[i]
                    artices.append(oneUrl)
                break
            except Exception, e:
                print "getArticleList %s:%s:%d" % (e,one,tryCount)

    return artices

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

def run(url,output):

    print "备份开始"
    lists = getArticleList(url)
    username = GetHtmlName(url)
    if not os.path.exists(output.decode("utf-8")):
        os.mkdir(output.decode("utf-8"))
    output_username = output+"/"+username
    output_username = output_username.replace("\\","/")
    if not os.path.exists(output_username.decode("utf-8")):
        os.mkdir(output_username.decode("utf-8"))

    totalNum = len(lists)
    print "总文章数: %d" % totalNum

    # 生成首页文件
    doctype = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n'
    charset = '<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />'
    indexHtml = output_username + ".htm"
    f = open(indexHtml.decode("utf-8"),"w")
    print >> f,doctype
    print >> f,'<html>'
    print >> f,'<head>'
    print >> f,charset
    print >> f,'</head>'
    print >> f,'<frameset cols=\"20%,*\">'
    navigationHtmlName = username+'-navigation.htm'
    print >> f,'<frame src=\"'+navigationHtmlName+'\" />'
    firstHtmlName = GetHtmlName(lists[0])
    print >> f,'<frame src=\"'+username+'/'+firstHtmlName+'.htm\" name=\"showframe\">'
    print >> f,'</frameset>'
    print >> f,'</html>'
    f.close()

    # 生成导航文件
    navigationHtml = output+"/"+navigationHtmlName
    # f = open(navigationHtml.decode("utf-8"),"w")
    f = codecs.open(navigationHtml.decode("utf-8"),"w","utf-8-sig")
    print >> f,doctype
    print >> f,'<html>'
    print >> f,'<head>'
    print >> f,charset
    print >> f,'<style> body{font: 12px Verdana, Arial, Helvetica, sans-serif;}a{color: #808080;}</style>'
    print >> f,'</head>'
    print >> f,'<body>'
    count = 0
    for x in lists:
        count = count + 1
        articleIdHtml = username+"/"+GetHtmlName(x)+".htm"
        print >> f,'<a href=\"'+articleIdHtml + '\" target=\"showframe\">'+str(count)+'.'+x[1].decode("utf-8")+'</a><br /><br />'
    print >> f,'</body>'
    print >> f,'</html>'
    f.close()

    print "开始下载文章"
    currentNum = 0
    strPage = "{0}:{1}.".decode("utf-8").encode("utf-8")
    global gTestTime
    for x in lists:
        count = gTestTime
        currentNum = currentNum+1
        while True:
            if count < 0:
                break
            count = count - 1
            try:
                time.sleep(1) #访问太快,csdn会报503错误.
                strPageTemp = strPage.format(totalNum,currentNum)
                strPageTemp = strPageTemp+x[1]
                print strPageTemp #这里有时候会不能输出,报output is not utf-8错误,单独执行时

                print x
                print "\n"
                Download(x,output_username)
                break
            except Exception, e:
                # exstr = traceback.format_exc()
                # print exstr
                pass
        break