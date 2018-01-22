#! encoding=utf-8

from Tkinter import *
from importlib import import_module
import string
from tkFileDialog import *
import tkFont
import sys
import os
import re
import webbrowser
from ctypes import *
from ctypes.wintypes import *
import subprocess
import tempfile
from PIL import ImageFile
from PIL import ImageTk
import ctypes
import locale
# from blog.plugins import *
import blog.common
import threading

class Blackhole(object):
    softspace = 0

    def write(self, text):
        pass

    def flush(self):
        pass


# sys.stderr = Blackhole()
# sys.stdout = Blackhole()

# Dll
user32 = windll.user32
kernel32 = windll.kernel32
clib = cdll.msvcrt

CF_TEXT = 1

######################## decrypt code
from ScrolledText import ScrolledText
import os
import struct
import Tkinter
import Tkconstants
import tkMessageBox
import traceback

import zlib
import zipfile
from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED
from contextlib import closing

import hashlib
from itertools import chain, islice
import xml.etree.ElementTree as etree
import Tkinter
import Tkconstants
import tkFileDialog

import subprocess


def get_dir(path):
    flag = ("\\", "/")
    for i in (0, 1):
        index = path.rfind(flag[i])
        if -1 != index:
            dir = path[0:index + 1]
            filename = path[index + 1:]
            return (dir, filename)
    return ("/", "")


#注意,py2exe打包时,module下的源文件会一起打包进去library.zip
class App:
    def __init__(self, master, width1, height1):
        self.toplevel = master
        self.appdir = get_dir(sys.argv[0])[0]
        frame = Frame(master, bd=0, width=width1, height=height1)
        #frame["bg"]="#ffffff"
        frame.grid(column=0, row=0, sticky=N + E + S + W)
        frame.rowconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.columnconfigure(0, weight=1)

        # panel1 top
        self.panel1 = Canvas(frame, bd=0, highlightthickness=0)
        self.panel1["bg"] = "#ffffff"
        self.panel1["width"] = "%d" % width1
        self.panel1["height"] = "%d" % 40
        self.panel1.grid(column=0, row=0, sticky=E + W + N + S)
        self.panel1.rowconfigure(0, weight=1)
        self.panel1.columnconfigure(0, weight=20)
        self.panel1.columnconfigure(1, weight=1)
        self.panel1.columnconfigure(2, weight=1)
        self.panel1.columnconfigure(3, weight=1)

        self.logo_link = Canvas(self.panel1, bd=0, highlightthickness=0)
        self.logo_link["bg"] = "#ffffff"
        self.logo_link["width"] = "%d" % 300
        self.logo_link["height"] = "%d" % 40

        self.font = tkFont.Font(family="Arial", size=19, weight=tkFont.BOLD)
        self.logo_link.create_text(30, 60, text=self.toplevel.title2(),
                                   anchor=SW, font=self.font)
        self.logo_link.grid(row=0, column=0, sticky=N + E + S + W)

        # panel2 top
        self.panel2 = Canvas(frame, bd=0, highlightthickness=0)
        self.panel2.toplevel = self.toplevel
        #self.panel2["bg"]="#ffffff"
        self.panel2["width"] = "%d" % width1
        self.panel2["height"] = "%d" % (height1 - 100)
        self.panel2.grid(column=0, row=1, sticky=N + E + S + W)

        self.panel2.filechoose = SimpleFileChoose(self.panel2, 20, 20, width1 - 40, 100)
        self.panel2.backuppanel = BackupPanel(self.panel2, 20, 130, width1 - 40, 100)


class Diacritical:
    """Mix-in class that adds keyboard bindings for accented characters, plus
    other common functionality.
    
    An inheriting class must define a select_all method that will respond
    to Ctrl-A."""

    accents = (('acute', "'"), ('grave', '`'), ('circumflex', '^'),
               ('tilde', '='), ('diaeresis', '"'), ('cedilla', ','),
               ('stroke', '/'), ('ring above', ';'))

    def __init__(self):
        # Fix some key bindings
        self.bind("<Control-Key-a>", self.select_all)
        # We will need Ctrl-/ for the "stroke", but it cannot be unbound, so
        # let's prevent it from being passed to the standard handler
        self.bind("<Control-Key-/>", lambda event: "break")
        # Diacritical bindings
        for a, k in self.accents:
            # Little-known feature of Tk, it allows to bind an event to
            # multiple keystrokes
            self.bind("<Control-Key-%s><Key>" % k,
                      lambda event, a=a: self.insert_accented(event.char, a))


class DiacriticalEntry(Entry, Diacritical):
    """Tkinter Entry widget with some extra key bindings for
    entering typical Unicode characters - with umlauts, accents, etc."""

    def __init__(self, master=None, **kwargs):
        Entry.__init__(self, master=None, **kwargs)
        Diacritical.__init__(self)

    def select_all(self, event=None):
        self.selection_range(0, END)
        return "break"


class DiacriticalText(ScrolledText, Diacritical):
    """Tkinter ScrolledText widget with some extra key bindings for
    entering typical Unicode characters - with umlauts, accents, etc."""

    def __init__(self, master=None, **kwargs):
        ScrolledText.__init__(self, master=None, **kwargs)
        Diacritical.__init__(self)

    def select_all(self, event=None):
        self.tag_add(SEL, "1.0", "end-1c")
        self.mark_set(INSERT, "1.0")
        self.see(INSERT)
        return "break"


################## Thread Run
def asyncRun(url,path):
        moduleName = blog.common.getDomainMainPart(url)
        pyName = "plugins."+moduleName+"."+moduleName
        try:
            p1 = import_module(pyName)
            p1.run(url,path)
        except Exception,e:
             print e

################## TextRedirector
class TextRedirector(object):
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")


################## BackupPanel
class BackupPanel:
    def __init__(self, master, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.parent = master
        self.toplevel = master.toplevel
        self.canvas = Canvas(master, bd=0, highlightthickness=0)
        self.canvas["width"] = "%d" % width
        self.canvas["height"] = "%d" % height
        self.canvas.place(x=x, y=y, width=width, height=height)
        self.create_widget()
        self.appdir = get_dir(sys.argv[0])[0]
        self.inpath = ''
        toplevel = self.toplevel


    def create_widget(self):
        self.text = DiacriticalText(self.canvas, width=50, height=5, wrap="word")
        if os.name == "nt":
            self.text.config(font="Arial 10")
        x = self.x
        y = self.y + 90
        self.text.place(x=x, y=y)

        sys.stdout = TextRedirector(self.text, "stdout")
        # sys.stderr = TextRedirector(self.text, "stderr")

        self.second_font = tkFont.Font(family="Arial", size=10, weight=tkFont.BOLD)
        self.backupbutton = Button(self.canvas, text="开始备份", height=2,
                                   font=self.second_font, command=self.download_blog)
        self.backupbutton.place(x=400, y=10, width=158, height=44)

        self.output_font = tkFont.Font(family="Arial", size=10)
        self.ckbutton = Button(self.canvas, text="打开输出目录", height=2,
                               font=self.output_font, command=self.open_output_dir)
        self.ckbutton.place(x=400, y=64, width=158, height=30)

    def open_output_dir(self):
        temp_dir = self.parent.filechoose.get_output_dir();
        try:
            temp = self.toplevel.GetNativeEncode(temp_dir.replace("/", "\\"))
            subprocess.Popen('explorer ' + '"' + temp + '"')
        except Exception, e:
            print "open_output_dir error"

    def sort_list(self, list, first):
        for i in range(len(list)):
            if list[i][1].endswith(first):
                t = list[0]
                list[0] = list[i]
                list[i] = t
                break
        return list

    def download_blog(self):
        self.inurl = self.parent.filechoose.get_input_file_name()
        if len(self.inurl) == 0:
            self.text.insert(END, "请输入个人博客首页网址" + "\n")
            return

        self.indir = self.parent.filechoose.get_output_dir()
        if len(self.indir) == 0:
            self.text.insert(END, "请选择一个输出目录" + "\n")
            return

        t1 = threading.Thread(target=asyncRun,args=(self.inurl,self.indir))
        t1.start()



#############################SimpleButton
class SimpleButton:
    def __init__(self, master, image, text):
        self.image = image
        self.text = text
        self.canvas = Canvas(master, bd=0, highlightthickness=0)
        width = ((self.image.width() >> 1) << 1) + 25
        height = ((self.image.height() >> 1) << 1) + 25

        self.canvas["width"] = "%d" % width
        self.canvas["height"] = "%d" % height
        self.width = width
        self.height = height

        self.canvas["bg"] = "#ffffff"
        self.create_button(width / 2, height / 2);
        self.canvas.bind("<Enter>", self.mouse_enter)
        self.canvas.bind("<Leave>", self.mouse_leave)
        self.canvas.bind("<Button-1>", self.left_mouse_press)
        self.canvas.bind("<ButtonRelease-1>", self.left_mouse_release)

    def grid(self, **options):
        self.canvas.grid(column=options["column"], row=options["row"],
                         sticky=options['sticky'])

    #pack(side=LEFT)

    def create_button(self, x, y):
        self.font = tkFont.Font(family="Courier New", size=10, weight=tkFont.BOLD)
        self.font_width = self.font.measure(self.text)
        self.text_x = (self.width - self.font_width) / 2

        self.canvas.image_id = self.canvas.create_image(x, y, image=self.image)
        self.canvas.text_id = self.canvas.create_text(self.text_x, self.height, text=self.text,
                                                      anchor=SW, font=self.font)

    def left_mouse_press(self, event):
        canvas = self.canvas
        x1 = 0
        y1 = string.atoi(canvas["height"])
        x2 = 0
        y2 = 0
        x3 = string.atoi(canvas["width"])
        y3 = 0

        self.canvas.line3 = self.canvas.create_line(x2, y2, x1, y1, fill="#8F8681")
        self.canvas.line4 = self.canvas.create_line(x2, y2, x3, y3, fill="#8F8681")

        x1 = 1
        y1 = string.atoi(canvas["height"]) - 1
        x2 = string.atoi(canvas["width"]) - 1
        y2 = string.atoi(canvas["height"]) - 1
        x3 = string.atoi(canvas["width"]) - 1
        y3 = 1

        self.canvas.line1 = self.canvas.create_line(x1, y1, x2, y2, fill="#ffffff")
        self.canvas.line2 = self.canvas.create_line(x2, y2, x3, y3, fill="#ffffff")

    def left_mouse_release(self, event):
        canvas = self.canvas
        x1 = 0
        y1 = string.atoi(canvas["height"])
        x2 = 0
        y2 = 0
        x3 = string.atoi(canvas["width"])
        y3 = 0

        self.canvas.line3 = self.canvas.create_line(x1, y1, x2, y2, fill="#ffffff")
        self.canvas.line4 = self.canvas.create_line(x2, y2, x3, y3, fill="#ffffff")
        if hasattr(self, "click_hanlder"):
            self.click_hanlder(event)

    def mouse_enter(self, event):
        canvas = self.canvas

        x1 = 1
        y1 = string.atoi(canvas["height"]) - 1
        x2 = string.atoi(canvas["width"]) - 1
        y2 = string.atoi(canvas["height"]) - 1
        x3 = string.atoi(canvas["width"]) - 1
        y3 = 1

        self.canvas.line1 = self.canvas.create_line(x1, y1, x2, y2, fill="#8F8681")
        self.canvas.line2 = self.canvas.create_line(x2, y2, x3, y3, fill="#8F8681")

    def mouse_leave(self, event):
        canvas = self.canvas
        x1 = 1
        y1 = string.atoi(canvas["height"]) - 1
        x2 = string.atoi(canvas["width"]) - 1
        y2 = string.atoi(canvas["height"]) - 1
        x3 = string.atoi(canvas["width"]) - 1
        y3 = 1

        self.canvas.line1 = self.canvas.create_line(x1, y1, x2, y2, fill="#ffffff")
        self.canvas.line2 = self.canvas.create_line(x2, y2, x3, y3, fill="#ffffff")

    def regist_click_hanlder(self, click_hanlder):
        self.click_hanlder = click_hanlder


############################SimpleFileChoose
class SimpleFileChoose:
    def __init__(self, master, x, y, width, height):

        self.toplevel = master.toplevel
        toplevel = self.toplevel
        self.width = width
        self.height = height
        self.parent = master
        self.canvas = Canvas(master, bd=0, highlightthickness=0)
        #self.canvas["bg"]="#000000"
        self.canvas["width"] = "%d" % width
        self.canvas["height"] = "%d" % height
        #temp_dir.encode("gbk")
        try:
            self.outputdir = toplevel.EncodeUTF8(toplevel.GetNativeDecode(toplevel.realdir))
        except Exception, e:
            self.outputdir = self.toplevel.realdir

        toplevel = self.toplevel
        self.dir = toplevel.GetPropertyValue("default_input_folder", "Setting")
        if self.dir == None:
            # self.dir = self.toplevel.GetMyDocumentPath()
            self.dir = ""
        self.toplevel.input_dir = self.dir
        self.filename = ""

        self.create_widget()
        self.canvas.place(x=x, y=y, width=width, height=height)

        # file options


    def create_widget(self):
        x = 0 + 5
        y = 0 + 5
        x1 = self.width - 5
        y1 = 0 + 5
        x2 = self.width - 5
        y2 = self.height - 5
        x3 = 0 + 5
        y3 = self.height - 5

        self.font = tkFont.Font(family="Courier New", size=8)
        self.text = "请输入个人博客首页网址"
        self.font_width = self.font.measure(self.text)
        self.text_center_x = x + self.font_width / 2 + 10
        self.canvas.create_text(self.text_center_x, y, text=self.text, font=self.font)

        self.canvas.create_line(x, y, x + 10, y, fill="#8F8681")
        self.canvas.create_line(x + 1, y + 1, x + 10, y1 + 1, fill="#ffffff")

        self.canvas.create_line(x + self.font_width + 10, y, x1, y1, fill="#8F8681")
        self.canvas.create_line(x + self.font_width + 10, y + 1, x1 - 1, y1 + 1, fill="#ffffff")

        self.canvas.create_line(x, y, x3, y3, fill="#8F8681")
        self.canvas.create_line(x + 1, y + 1, x3 + 1, y3 - 1, fill="#ffffff")

        self.canvas.create_line(x1, y1, x2, y2, fill="#8F8681")
        self.canvas.create_line(x1 + 1, y1, x2 + 1, y2, fill="#ffffff")

        # buttom line
        self.canvas.create_line(x2, y2, x3, y3, fill="#8F8681")
        self.canvas.create_line(x2, y2 + 1, x3, y3 + 1, fill="#ffffff")

        # input file
        self.second_font = tkFont.Font(family="Arial", size=8)
        self.second_text = "       博客: "
        self.second_font_width = self.second_font.measure(self.second_text)
        self.second_text_center_x = x + self.second_font_width / 2 + 10
        self.canvas.create_text(self.second_text_center_x, self.height / 4 + y, text=self.second_text,
                                font=self.second_font)

        self.entry_font = tkFont.Font(family="Arial", size=10)
        self.entry = Entry(self.canvas, font=self.entry_font)
        self.entry.insert(0,"http://blog.csdn.net/infoworld")
        self.entry.bind("<Control-KeyPress-a>", self.call_select_all)
        self.entry.place(x=x + self.second_font_width + 10, y=self.height / 4 + y - 15, width=380,
                         height=28)

        self.input_font = tkFont.Font(family="Arial", size=8, weight=tkFont.BOLD)

        # output file
        self.third_text = "输出目录: "
        self.canvas.create_text(self.second_text_center_x, self.height * 4 / 6 + y, text=self.third_text,
                                font=self.second_font)

        self.third_entry = Entry(self.canvas, font=self.entry_font)
        self.third_entry.insert(0, self.outputdir)
        #		self.third_entry.bind("<Button-1>",self.fn_igore_event);
        self.third_entry["state"] = "readonly"
        self.third_entry.bind("<Control-KeyPress-a>", self.call_select_all_third_entry)
        self.third_entry.place(x=x + self.second_font_width + 10, y=self.height * 4 / 6 + y - 15, width=380,
                               height=28)

        self.third_sfbutton = Button(self.canvas, text="选择输出目录", height=2, font=self.second_font,
                                     command=self.call_file_dialog_third_sfbutton)
        self.third_sfbutton.place(x=self.width - 100, y=self.height * 4 / 6 + y - 15, width=80, height=25)

    def call_file_dialog_third_sfbutton(self):

        if len(self.dir) != 0:
            self.file_opt["initialdir"] = self.dir

        self.outputdir = tkFileDialog.askdirectory()

        if len(self.outputdir) == 0:
            self.parent.backuppanel.text.insert(END, "请选择输出目录\n")
            self.parent.backuppanel.text.see(INSERT)
            return
        self.third_entry["state"] = "normal"
        self.third_entry.delete(0, END)
        self.third_entry.insert(0, self.outputdir)
        self.third_entry["state"] = "readonly"
        self.parent.backuppanel.text.insert(END, "选择输出目录: " + self.outputdir + "\n")
        self.parent.backuppanel.text.see(INSERT)


    def call_select_all_third_entry(self, event):
        self.third_entry.selection_range(0, END)
        self.third_entry.focus()
        return "break"

    def call_select_all(self, event):
        self.entry.selection_range(0, END)
        self.entry.focus()
        return "break"

    def get_input_file_name(self):
        return self.entry.get()

    def get_output_dir(self):
        if len(self.third_entry.get()) == 0:
            return "."
        return self.third_entry.get()


class ImageFp:
    def __init__(self, attributes, encrypt_file, header_size):
        self.attributes = attributes
        self.encrypt_file = encrypt_file
        self.header_size = header_size

    def fn_get_image_from_fp(self, fp, file_size):
        BSIZE = 1024
        left_size = file_size

        p = ImageFile.Parser()
        while 1:
            if left_size - BSIZE <= 0:
                s = fp.read(left_size)
                p.feed(s)
                break;
            left_size = left_size - BSIZE
            s = fp.read(BSIZE)
            p.feed(s)
        im = p.close()
        return im

    def fn_get_image(self, image_name):
        ia = None
        for file in self.attributes:
            if image_name == file[0]:
                ia = file
                break
        fp = open(self.encrypt_file, "rb")
        fp.seek(ia[3] + self.header_size, os.SEEK_SET)
        im = self.fn_get_image_from_fp(fp, file[2])
        fp.close()
        return im

    def fn_get_photoimage_from_image(self, image_name):
        return ImageTk.PhotoImage(self.fn_get_image(image_name))

    def fn_create_icon_on_temp(self, image_name):
        ia = None
        for file in self.attributes:
            if image_name == file[0]:
                ia = file
                break
        path = os.path.split(os.path.realpath(sys.argv[0]))[0]
        fp = open(self.encrypt_file, "rb")
        fp.seek(ia[3] + self.header_size, os.SEEK_SET)
        path = path + "/" + image_name
        fw = open(path, "wb")
        str = fp.read(ia[2])
        fw.write(str)
        fp.close()
        fw.close()
        return path


def getCompanyName():
    return "infoworld"


def getProductName():
    return "BlogBackup"


def get_title2():
    return "博客备份"


def get_title():
    return getCompanyName() + " " + get_title2()


def get_site_url():
    return "http://blog.csdn.net/infoworld"


def get_version():
    return "2.0.1"


def root_close():
    root.destroy()


def GetMyDocumentPath():
    dll = ctypes.windll.shell32
    buf = ctypes.create_unicode_buffer(300)

    dll.SHGetFolderPathW(None, 0x0005, None, 0, buf)
    return buf.value


def EncodeUTF8(str):
    print "EncodeUTF8"
    return str.encode("utf-8");


def DecodeUTF8(str):
    print "DecodeUTF8"
    return str.decode("utf-8");


def DecodeGBK(str):
    print "DecodeGBK"
    return str.decode("gbk")


def EncodeGBK(str):
    print "EncodeGBK"
    return str.encode("gbk")


def NotDecode(str):
    print "NotDecode"
    return str


def GetNativeDecode():
    nLocale = locale.getlocale()[1]
    print nLocale
    if nLocale == "936":
        return DecodeGBK
    else:
        return NotDecode


def GetNativeEncode():
    nLocale = locale.getlocale()[1]
    print nLocale
    if nLocale == "936":
        return EncodeGBK
    else:
        return NotDecode


def SetPropertyValue(key, value, file_name):
    if not os.path.exists(file_name):
        return
    #use utf-8 store value
    value = EncodeUTF8(value)
    f = open(file_name, "r")
    lines = f.readlines()
    f.close()

    f = open(file_name, "w+")
    line_length = len(lines)
    exists = False
    key_name = key + "="
    for i in range(line_length):
        if lines[i].startswith(key_name):
            exists = True
            lines[i] = key_name + value + "\r\n"
            break

    if not exists:
        lines.append(key_name + value + "\r\n")
    try:
        f.writelines(lines)
    except Exception, e:
        print "write"

    try:
        f.close()
    except Exception, e:
        print "close"


def GetPropertyValue(key, file_name):
    if not os.path.exists(file_name):
        return None

    f = open(file_name, "r")
    lines = f.readlines()

    line_length = len(lines)
    line = None
    for i in range(line_length):
        if lines[i].startswith(key):
            index = lines[i].find("=")
            line = lines[i][index + 1:].strip()
            break
    f.close()
    if not line == None:
        return DecodeUTF8(line)
    return line


def fn_onsetup():
    return True


def startGUI():
    global root
    locale.setlocale(locale.LC_ALL, '')
    root = Tk()
    root.GetNativeDecode = GetNativeDecode()
    root.GetNativeEncode = GetNativeEncode()
    root.EncodeUTF8 = EncodeUTF8
    root.DecodeUTF8 = DecodeUTF8

    fn_onsetup()

    root.title(get_title())

    #	root.overrideredirect(1)
    #root["bg"]="#ffffff"

    width = 600
    height = 330
    root.x = (root.winfo_screenwidth() - width) / 2
    root.y = (root.winfo_screenheight() - height) / 2
    geometry = "%dx%d+%d+%d" % (width, height, root.x, root.y)

    print sys.argv[0]
    root.realpath = os.path.realpath(sys.argv[0])
    root.realdir = os.path.split(root.realpath)[0]
    root.version = get_version
    root.title2 = get_title2
    root.get_site_url = get_site_url
    root.getProductName = getProductName
    root.getCompanyName = getCompanyName
    root.GetPropertyValue = GetPropertyValue
    root.SetPropertyValue = SetPropertyValue
    root.maxtime = 3
    root.copyright = "Copyright http://blog.csdn.net/infoworld."
    root.geometry(geometry)
    root.resizable(width=False, height=False)
    root.rowconfigure(0, weight=1)
    root.columnconfigure(0, weight=1)
    root.overtime = 0
    root.input_dir = "."
    root.protocol("WM_DELETE_WINDOW", root_close)
    root.withdraw()
    root.deiconify()
    root.grid()
    app = App(root, width1=width, height1=height)
    root.mainloop()

	