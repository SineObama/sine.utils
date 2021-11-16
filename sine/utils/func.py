# encoding: UTF-8
import os

def byte2readable(value):
    units = ["B", "KB", "MB", "GB", "TB", "PB"]
    size = 1024.0
    for i in range(len(units)):
        if (value / size) < 1:
            return "%.2f%s" % (value, units[i])
        value = value / size

def mkdir(path):
    if os.path.exists(path) is not True:
        os.makedirs(path)

#__all__ = ['']
