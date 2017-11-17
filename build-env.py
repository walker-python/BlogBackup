#! encoding=utf-8
import sys
import os
import subprocess

if __name__ == '__main__':
    path = sys.executable
    installer_dir = os.path.dirname(path)+os.path.sep
    scripts_dir = installer_dir+"Scripts"+os.path.sep
    pip_exe = scripts_dir+"pip"
    print pip_exe
