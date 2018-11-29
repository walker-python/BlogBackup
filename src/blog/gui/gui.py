#! encoding=utf-8

import tkinter
import tkinter.font
import urllib3.contrib.pyopenssl
from tkinter.font import Font
import tkinter.commondialog
import tkinter.filedialog
from tkinter.scrolledtext import ScrolledText
import tkinter.constants
import string
import sys
import queue
import threading
import blog.gui.utility
import os
import re
import webbrowser
from ctypes import *
from ctypes.wintypes import *
import subprocess
import tempfile
import importlib
import time
import ctypes
import locale
import threading
import _thread
import blog.plugins.csdn


class Blackhole(object):
    softspace = 0

    def write(self, text):
        pass

    def flush(self):
        pass


sys.stderr = Blackhole()
sys.stdout = Blackhole()

# Dll
user32 = windll.user32
kernel32 = windll.kernel32
clib = cdll.msvcrt

CF_TEXT = 1

######################## decrypt code
import os
import struct
import traceback

import zlib
import zipfile
from zipfile import ZipFile, ZIP_STORED, ZIP_DEFLATED
from contextlib import closing

import hashlib
from itertools import chain, islice
import xml.etree.ElementTree as etree

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
        self.frame = tkinter.Frame(master, bd=0, width=width1, height=height1)
        #frame["bg"]="#ffffff"
        self.frame.grid(column=0, row=0, sticky=tkinter.N + tkinter.E + tkinter.S + tkinter.W)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)

        # panel1 top
        self.panel1 = tkinter.Canvas(self.frame, bd=0, highlightthickness=0)
        self.panel1["bg"] = "#ffffff"
        self.panel1["width"] = "%d" % width1
        self.panel1["height"] = "%d" % 40
        self.panel1.grid(column=0, row=0, sticky=tkinter.E + tkinter.W + tkinter.N + tkinter.S)
        self.panel1.rowconfigure(0, weight=1)
        self.panel1.columnconfigure(0, weight=20)
        self.panel1.columnconfigure(1, weight=1)
        self.panel1.columnconfigure(2, weight=1)
        self.panel1.columnconfigure(3, weight=1)

        self.logo_link = tkinter.Canvas(self.panel1, bd=0, highlightthickness=0)
        self.logo_link["bg"] = "#ffffff"
        self.logo_link["width"] = "%d" % 300
        self.logo_link["height"] = "%d" % 40

        self.font = Font(family="Arial", size=19, weight=tkinter.font.BOLD)
        self.logo_link.create_text(30, 60, text=self.toplevel.title2(),
                                   anchor=tkinter.SW, font=self.font)
        self.logo_link.grid(row=0, column=0, sticky=tkinter.N + tkinter.E + tkinter.S + tkinter.W)

        # panel2 top
        self.panel2 = tkinter.Canvas(self.frame, bd=0, highlightthickness=0)
        self.panel2.toplevel = self.toplevel
        #self.panel2["bg"]="#ffffff"
        self.panel2["width"] = "%d" % width1
        self.panel2["height"] = "%d" % (height1 - 100)
        self.panel2.grid(column=0, row=1, sticky=tkinter.N + tkinter.E + tkinter.S + tkinter.W)

        self.panel2.filechoose = SimpleFileChoose(self.panel2, 20, 20, width1 - 40, 100)
        self.panel2.removepanel = RemovePanel(self.panel2, 20, 130, width1 - 40, 100)


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
        self.bind("<Button-3><ButtonRelease-3>", self.show_menu)
        # Diacritical bindings
        for a, k in self.accents:
            # Little-known feature of Tk, it allows to bind an event to
            # multiple keystrokes
            self.bind("<Control-Key-%s><Key>" % k,
                      lambda event, a=a: self.insert_accented(event.char, a))

def _rc_menu_install(w):
    w.menu = tkinter.Menu(w, tearoff=0)
    w.menu.add_command(label="Cut")
    w.menu.add_command(label="Copy")
    w.menu.add_command(label="Paste")

    w.menu.entryconfigure("Cut", command=lambda: w.focus_force() or w.event_generate("<<Cut>>"))
    w.menu.entryconfigure("Copy", command=lambda: w.focus_force() or w.event_generate("<<Copy>>"))
    w.menu.entryconfigure("Paste", command=lambda: w.focus_force() or w.event_generate("<<Paste>>"))

class DiacriticalEntry(tkinter.Entry, Diacritical):
    """Tkinter Entry widget with some extra key bindings for
    entering typical Unicode characters - with umlauts, accents, etc."""

    def show_menu(self, e):
        self.tk.call("tk_popup", self.menu, e.x_root, e.y_root)

    def __init__(self, master=None, **kwargs):
        tkinter.Entry.__init__(self, master=None, **kwargs)
        Diacritical.__init__(self)
        _rc_menu_install(self)

    def select_all(self, event=None):
        self.selection_range(0, tkinter.END)
        return "break"


class DiacriticalText(ScrolledText, Diacritical):
    """Tkinter ScrolledText widget with some extra key bindings for
    entering typical Unicode characters - with umlauts, accents, etc."""

    def __init__(self, master=None, **kwargs):
        ScrolledText.__init__(self, master=None, **kwargs)
        Diacritical.__init__(self)
        _rc_menu_install(self)

    def select_all(self, event=None):
        self.tag_add(tkinter.SEL, "1.0", "end-1c")
        self.mark_set(tkinter.INSERT, "1.0")
        self.see(tkinter.INSERT)
        return "break"

    def show_menu(self, e):
        self.tk.call("tk_popup", self.menu, e.x_root, e.y_root)


################## RemovePanel
class RemovePanel:
    def __init__(self, master, x, y, width, height):
        self.x = x
        self.y = y
        self.status = [False]
        self.width = width
        self.height = height
        self.parent = master
        self.toplevel = master.toplevel
        self.canvas = tkinter.Canvas(master, bd=0, highlightthickness=0)
        self.canvas["width"] = "%d" % width
        self.canvas["height"] = "%d" % height
        self.canvas.place(x=x, y=y, width=width, height=height)
        self.create_widget()
        self.appdir = get_dir(sys.argv[0])[0]
        self.keypath = "./key/adeptkey.der"
        self.inpath = ''
        toplevel = self.toplevel


    def create_widget(self):
        self.text = DiacriticalText(self.canvas, width=50, height=5, wrap="word")
        if os.name == "nt":
            self.text.config(font="Arial 10")
        x = self.x
        y = self.y + 90
        self.text.place(x=x, y=y)

        self.button1_text = "开始备份"
        self.second_font = Font(family="Arial", size=10, weight=tkinter.font.BOLD)
        self.removebutton = tkinter.Button(self.canvas, text=self.button1_text, height=2,
                                   font=self.second_font, command=self.start_backup_blog)
        self.removebutton.place(x=400, y=10, width=158, height=44)

        self.output_font = Font(family="Arial", size=10)
        self.ckbutton = tkinter.Button(self.canvas, text="打开输出目录", height=2,
                               font=self.output_font, command=self.open_output_dir)
        self.ckbutton.place(x=400, y=64, width=158, height=30)

    def open_output_dir(self):
        temp_dir = self.parent.filechoose.get_output_dir();
        try:
            temp = self.toplevel.GetNativeEncode(temp_dir.replace("/", "\\"))
            subprocess.Popen('explorer ' + '"' + temp + '"')
        except Exception as e:
            print("open_output_dir error")

    def sort_list(self, list, first):
        for i in range(len(list)):
            if list[i][1].endswith(first):
                t = list[0]
                list[0] = list[i]
                list[i] = t
                break
        return list

    def worker(self):
        currentThread = threading.currentThread()
        currentThread.status = self.status
        # https://stackoverflow.com/questions/15959534/visibility-of-global-variables-in-imported-modules
        # module = importlib.import_module('blog.plugins.csdn')
        blog.plugins.csdn.run(self.inpath,self.output)

    def onUpdate(self):
        try:
            valueTuple = blog.gui.utility.get_queue().get(False)
            if(valueTuple == None):
                return

            if(valueTuple[0] == 0):
                self.text.insert(tkinter.END, valueTuple[1] + "\n")
                self.text.see(tkinter.END)
            elif(valueTuple[0] == -1):
                self.text.insert(tkinter.END, "备份失败" + "\n")
                self.removebutton["text"] = self.button1_text
                self.removebutton["state"]=tkinter.NORMAL
                return
            else:
                self.text.insert(tkinter.END, "备份完成" + "\n")
                self.removebutton["text"] = self.button1_text
                self.removebutton["state"]=tkinter.NORMAL
                return
        except Exception as e:
            pass
        app.frame.after(500, self.onUpdate)

    def start_backup_blog(self):
        self.inpath = self.parent.filechoose.get_input_file_name()
        if len(self.inpath) == 0:
            self.text.insert(tkinter.END, "请输入个人博客首页网址" + "\n")
            return

        self.output = self.parent.filechoose.get_output_dir()
        if len(self.output) == 0:
            self.text.insert(tkinter.END, "请选择有效的输出目录" + "\n")
            return

        if(self.status[0]):
            self.status[0] = False
            self.removebutton["text"] = self.button1_text
            self.removebutton["state"]=tkinter.DISABLED
        else:
            self.status[0] = True
            self.removebutton["text"] = "停止"
            _thread.start_new_thread(self.worker, ())
            app.frame.after(500, self.onUpdate)











#############################SimpleButton
class SimpleButton:
    def __init__(self, master, image, text):
        self.image = image
        self.text = text
        self.canvas = tkinter.Canvas(master, bd=0, highlightthickness=0)
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
        self.font = Font(family="Courier New", size=10, weight=tkinter.font.BOLD)
        self.font_width = self.font.measure(self.text)
        self.text_x = (self.width - self.font_width) / 2

        self.canvas.image_id = self.canvas.create_image(x, y, image=self.image)
        self.canvas.text_id = self.canvas.create_text(self.text_x, self.height, text=self.text,
                                                      anchor=tkinter.SW, font=self.font)

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
        self.canvas = tkinter.Canvas(master, bd=0, highlightthickness=0)
        #self.canvas["bg"]="#000000"
        self.canvas["width"] = "%d" % width
        self.canvas["height"] = "%d" % height
        #temp_dir.encode("gbk")
        try:
            self.outputdir = os.path.join(os.path.expanduser('~'), 'Desktop')
        except Exception as e:
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


    def create_widget(self):
        x = 0 + 5
        y = 0 + 5
        x1 = self.width - 5
        y1 = 0 + 5
        x2 = self.width - 5
        y2 = self.height - 5
        x3 = 0 + 5
        y3 = self.height - 5

        self.font = Font(family="Courier New", size=8)
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
        self.second_font = Font(family="Arial", size=8)
        self.second_text = "       博客: "
        self.second_font_width = self.second_font.measure(self.second_text)
        self.second_text_center_x = x + self.second_font_width / 2 + 10
        self.canvas.create_text(self.second_text_center_x, self.height / 4 + y, text=self.second_text,
                                font=self.second_font)

        self.entry_font = Font(family="Arial", size=10)
        self.entry = tkinter.Entry(self.canvas, font=self.entry_font)
        self.entry.bind("<Control-KeyPress-a>", self.call_select_all)
        self.entry.bind("<Button-3><ButtonRelease-3>", self.call_show_menu)
        _rc_menu_install(self.entry)

        self.entry.place(x=x + self.second_font_width + 10, y=self.height / 4 + y - 15, width=380,
                         height=28)

        self.input_font = Font(family="Arial", size=8, weight=tkinter.font.BOLD)

        # output file
        self.third_text = "输出目录: "
        self.canvas.create_text(self.second_text_center_x, self.height * 4 / 6 + y, text=self.third_text,
                                font=self.second_font)

        self.third_entry = tkinter.Entry(self.canvas, font=self.entry_font)
        self.third_entry.insert(0, self.outputdir)
        #		self.third_entry.bind("<Button-1>",self.fn_igore_event);
        self.third_entry["state"] = "readonly"
        self.third_entry.bind("<Control-KeyPress-a>", self.call_select_all_third_entry)
        self.third_entry.place(x=x + self.second_font_width + 10, y=self.height * 4 / 6 + y - 15, width=380,
                               height=28)

        self.third_sfbutton = tkinter.Button(self.canvas, text="选择输出目录", height=2, font=self.second_font,
                                     command=self.call_file_dialog_third_sfbutton)
        self.third_sfbutton.place(x=self.width - 100, y=self.height * 4 / 6 + y - 15, width=80, height=25)

    def call_file_dialog_third_sfbutton(self):

        options = {}
        options['initialdir'] = self.outputdir
        tempDir = tkinter.filedialog.askdirectory(**options)

        if len(tempDir) == 0:
            self.parent.removepanel.text.insert(tkinter.END, "请选择输出目录\n")
            self.parent.removepanel.text.see(tkinter.INSERT)
            return
        else:
            self.outputdir = tempDir

        self.third_entry["state"] = "normal"
        self.third_entry.delete(0, tkinter.END)
        self.third_entry.insert(0, self.outputdir)
        self.third_entry["state"] = "readonly"
        self.parent.removepanel.text.insert(tkinter.END, "选择输出目录: " + self.outputdir + "\n")
        self.parent.removepanel.text.see(tkinter.INSERT)

    def call_show_menu(self, e):
        self.entry.tk.call("tk_popup", self.entry.menu, e.x_root, e.y_root)
        return "break"

    def call_select_all_third_entry(self, event):
        self.third_entry.selection_range(0, tkinter.END)
        self.third_entry.focus()
        return "break"

    def call_select_all(self, event):
        self.entry.selection_range(0, tkinter.END)
        self.entry.focus()
        return "break"

    def get_input_file_name(self):
        return self.entry.get()

    def get_output_dir(self):
        if len(self.third_entry.get()) == 0:
            return "./output"
        return self.third_entry.get()


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
    root.SetPropertyValue("default_input_folder", root.input_dir, "Setting")
    root.destroy()


def GetMyDocumentPath():
    dll = ctypes.windll.shell32
    buf = ctypes.create_unicode_buffer(300)

    dll.SHGetFolderPathW(None, 0x0005, None, 0, buf)
    return buf.value


def EncodeUTF8(str):
    print("EncodeUTF8")
    return str.encode("utf-8");


def DecodeUTF8(str):
    print("DecodeUTF8")
    return str.decode("utf-8");


def DecodeGBK(str):
    print("DecodeGBK")
    return str.decode("gbk")


def EncodeGBK(str):
    print("EncodeGBK")
    return str.encode("gbk")


def NotDecode(str):
    print("NotDecode")
    return str


def GetNativeDecode():
    nLocale = locale.getlocale()[1]
    print(nLocale)
    if nLocale == "936":
        return DecodeGBK
    else:
        return NotDecode


def GetNativeEncode():
    nLocale = locale.getlocale()[1]
    print(nLocale)
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
    except Exception as e:
        print("write")

    try:
        f.close()
    except Exception as  e:
        print("close")


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


if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, '')
    root = tkinter.Tk()
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

    print(sys.argv[0])
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
    blog.gui.utility.init_queue()
    ct = threading.current_thread()
    global app
    urllib3.contrib.pyopenssl.inject_into_urllib3()
    app = App(root, width1=width, height1=height)
    root.mainloop()

	