#! encoding=utf-8


import urllib3
import certifi
import re
import os
import math
import sys
# from HTMLParser import HTMLParser
import html5lib
# from xml.etree.ElementTree import ElementTree
from urllib.parse import urlparse
import xml
import codecs
import blog.gui.utility
import traceback
import time
import threading
from blog.common.utils import Utils

gTestTime = 5

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

# 2018.8.17
# 获取页数, 通过 ceil(307.0/20)
# var pageSize = 20 ;
# var listTotal = 307 ;
# https://blog.csdn.net/infoworld/article/list
def getAllListUrl(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
    }
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    response = http.request('GET',url,None,header)
    data = response.data.decode('utf-8')
    if(Utils.is_backuping_stop()):
        return None

    m = re.search("var[ ]{1,}pageSize[ ]+=[ ]*([0-9]+)",data)
    pageSize = m.group(1)
    m = re.search("var[ ]{1,}listTotal[ ]+=[ ]*([0-9]+)",data)
    listTotal = m.group(1)
    blog.gui.utility.get_queue().put((0, pageSize))
    blog.gui.utility.get_queue().put((0, listTotal))

    lastPageNum = int(math.ceil(float(listTotal)/float(pageSize)))
    urlList = []
    for x in range(1,lastPageNum+1):
        listUrl = url+"/article/list/"+str(x)
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
    time.sleep(1) #访问太快,csdn会报503错误.
    if(urlList is None):
        return None
    blog.gui.utility.get_queue().put((0, "文章页数 %d" % len(urlList)))
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
    }
    allLists = []

    strPage = "分析 第 {0} 页 "
    pageNum = 0
    global gTestTime
    artices = []
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    for one in urlList:
        tryCount = gTestTime # try count
        while tryCount > 0:

                if(Utils.is_backuping_stop()):
                    return None


                blog.gui.utility.get_queue().put((0, "%s:tryCount %d" % (one,tryCount)))
                print ("%s:tryCount %d" % (one,tryCount))
                tryCount = tryCount - 1
                try:
                    time.sleep(1) #访问太快会不响应
                    response = http.request('GET',one,None,header)
                    data = response.data.decode("utf-8")
                except Exception as e:
                    print(e)
                    continue

                # patternText = '<p class="content">[^<]*<a href="([^"]+)"\s+target="_blank">'
                patternText = '<h4 class="">[^<]*<a href="([^"]+)"\s+target="_blank">[\s\S]+?</span>([\s\S]+?)</a>'
                pattern = re.compile(patternText)
                m = re.findall(pattern,data)
                size = len(m)

                for i in range(0,size,1):
                    urls = m[i]
                    oneUrl = urls[0]
                    if(oneUrl.startswith(url)):
                        oneTitle = urls[1]
                        oneTitle = oneTitle.strip()
                        artices.append((oneUrl,oneTitle))

                # print "size: ",size
                break

    blog.gui.utility.get_queue().put((0, "getArtistList Finish"))
    return artices


# <div style="display:none;">
# 	<img src="" onerror='setTimeout(function(){if(!/(csdn.net|iteye.com|baiducontent.com|googleusercontent.com|360webcache.com|sogoucdn.com|bingj.com|baidu.com)$/.test(window.location.hostname)){window.location.href="\x68\x74\x74\x70\x73\x3a\x2f\x2f\x77\x77\x77\x2e\x63\x73\x64\x6e\x2e\x6e\x65\x74"}},3000);'>
# </div>
def Download(url,output):
    # try:
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
    }
    namespace = "{http://www.w3.org/1999/xhtml}"
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    response = http.request('GET',url,None,header)

    data = response.data.decode("utf-8")
    document = html5lib.parse(data)
    imgElements = document.findall('.//{0}img'.format(namespace))

    # print "imgElements %d" % len(imgElements)
    for img in imgElements:
        if(Utils.is_backuping_stop()):
            return
        src = img.attrib["src"]
        # print "image %s" % src
        try:
            res = urlparse(src)
            # 非csdn的图片不下载
            if (-1 == res.netloc.find("csdn")) and (-1 == res.netloc.find("iteye")):
                # print "image not download: %s:%s" % (src,res.netloc)
                continue

            Utils.DownloadFile(src, output, http)
        except Exception as e:
            pass


    linkElements = document.findall('.//{0}link'.format(namespace))
    # print "linkElements %d" % len(linkElements)
    for link in linkElements:
        if(Utils.is_backuping_stop()):
            return

        href = link.attrib["href"]
        # print "css %s" % href
        if -1 != href.find("https://blog.csdn.net"):
            continue
        text = Utils.DownloadFile(href,output,http)
        if "rel" in link.attrib and link.attrib["rel"].lower() == "stylesheet":
            css_result = Utils.ReadCss(text)
            if css_result is not None:
                Utils.DownloadFile(css_result[0],css_result[1],http)

    scriptElements = document.findall('.//{0}script'.format(namespace))
    # print "scriptElements %d" % len(scriptElements)
    for script in scriptElements:
        if(Utils.is_backuping_stop()):
            return
        if "src" in script.attrib:
            src = script.attrib["src"]
            # print "script %s-%s" % (src,output)
            if(src.startswith("//")):
                src="https:"+src

            Utils.DownloadFile(src,output,http)

    htmlName = Utils.GetHtmlName(url)
    output = output + "/"+htmlName+".htm"
    data = data.replace("http://","")
    data = data.replace("https://","")
    data = data.replace("src=\"//","src=\"")
    data = data.replace("www.w3.org/1999/xhtml","http://www.w3.org/1999/xhtml")
    data = re.sub('<div style="display:none;">[\\s\\S]*?</div>','',data)

    resourceFile = open(output,"wb")
    data = data.encode("utf-8")
    resourceFile.write(data)
    resourceFile.close()

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

def run(url,output):
    url = queryCsdnUrl(url)
    url = "https://blog.csdn.net/"+url
    queue = blog.gui.utility.get_queue()
    queue.put((0,"备份开始"))
    lists = getArticleList(url)
    loopcount = 1
    result = (-1,"备份中止")
    while(loopcount > 0):
        loopcount-=1
        if(lists is None):
            break
        username = Utils.GetHtmlName(url)
        if not os.path.exists(output):
            os.mkdir(output)
        output_username = output+"/"+username
        output_username = output_username.replace("\\","/")
        if not os.path.exists(output_username):
            os.mkdir(output_username)

        totalNum = len(lists)
        blog.gui.utility.get_queue().put((0, "总文章数: %d" % totalNum))

        # 生成首页文件
        doctype = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n'
        charset = '<meta http-equiv="Content-Type" content="text/html;charset=utf-8" />'
        indexHtml = output_username + ".htm"
        f = open(indexHtml,"w",encoding="utf-8")
        f.write(doctype)
        f.write('<html>')
        f.write('<head>')
        f.write(charset)
        f.write('</head>')
        f.write('<frameset cols=\"20%,*\">')
        navigationHtmlName = username+'-navigation.htm'
        f.write('<frame src=\"'+navigationHtmlName+'\" />')
        firstHtmlName = ""
        if(len(lists) > 0):
            firstHtmlName = Utils.GetHtmlName(lists[0][0])
        f.write('<frame src=\"'+username+'/'+firstHtmlName+'.htm\" name=\"showframe\">')
        f.write('</frameset>')
        f.write('</html>')
        f.close()

        # 生成导航文件
        navigationHtml = output+"/"+navigationHtmlName
        # f = open(navigationHtml.decode("utf-8"),"w")
        f = open(navigationHtml, "w", encoding="utf-8")
        f.write(doctype)
        f.write('<html>')
        f.write('<head>')
        f.write(charset)
        f.write('<style> body{font: 12px Verdana, Arial, Helvetica, sans-serif;}a{color: #808080;}</style>')
        f.write('</head>')
        f.write('<body>')
        count = 0
        for x in lists:
            count = count + 1
            articleIdHtml = username+"/"+Utils.GetHtmlName(x[0])+".htm"
            f.write('<a href=\"'+articleIdHtml + '\" target=\"showframe\">'+str(count)+'.'+x[1]+'</a><br /><br />')
        f.write('</body>')
        f.write('</html>')
        f.close()

        blog.gui.utility.get_queue().put((0,  "开始下载文章"))
        currentNum = 0
        strPage = "{0}:{1}."
        global gTestTime
        for x in lists:
            try:
                if(Utils.is_backuping_stop()):
                    break
                time.sleep(1) #访问太快,csdn会报503错误.
                currentNum = currentNum+1
                strPageTemp = strPage.format(totalNum,currentNum)
                strPageTemp = strPageTemp+x[1]
                blog.gui.utility.get_queue().put((0,""+strPageTemp)) #这里有时候会不能输出,报output is not utf-8错误,单独执行时
                Download(x[0],output_username)
            except Exception as e:
                exstr = traceback.format_exc()
                blog.gui.utility.get_queue().put((0, exstr))
                print (exstr)

        if(not Utils.is_backuping_stop()):
            result = (1,"备份完成")

    blog.gui.utility.get_queue().put(result)