#! encoding=utf-8

import html5lib
import urllib2
import sys
import os
import time
import re
# import blog.plugins.csdn
from urlparse import *
import Tkinter
from Tkinter import *
from blog.gui import gui

__author__ = 'apple'

# if __name__ == "__main__":
#     namespace = "{http://www.w3.org/1999/xhtml}"
#     document  = html5lib.parse("<form action='http://www.baidu.com'></form>")
#     elements = document.findall('.//{0}form'.format(namespace))
#     for one in elements:
#         action = one.attrib["action"]
#         print action

gui.startGUI()