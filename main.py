#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import re
import sys
import json
import random
import requests
import importlib
import configparser
from os import path
from PIL import Image
from bs4 import BeautifulSoup
from PIL import Image
import logging
import win32gui ,win32con, win32api
from unsplashSpider import UnsplashSpider
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler
from watchdog.events import FileSystemEventHandler

# 监听配置变化
class LoggingEventHandler(FileSystemEventHandler):

    def on_moved(self, event):
        super(LoggingEventHandler, self).on_moved(event)
        what = 'directory' if event.is_directory else 'file'
        logging.info("Moved %s: from %s to %s", what, event.src_path, event.dest_path)

    def on_created(self, event):
        super(LoggingEventHandler, self).on_created(event)
        what = 'directory' if event.is_directory else 'file'
        logging.info("Created %s: %s", what, event.src_path)

    def on_deleted(self, event):
        super(LoggingEventHandler, self).on_deleted(event)
        what = 'directory' if event.is_directory else 'file'
        logging.info("Deleted %s: %s", what, event.src_path)

    def on_modified(self, event):
        super(LoggingEventHandler, self).on_modified(event)
        what = 'directory' if event.is_directory else 'file'
        confPath = os.path.join(sys.path[0],'config.ini')
        if(what =='file' and event.src_path == confPath):
            importlib.reload(module)
        logging.info("Modified %s: %s", what, event.src_path)

# 初始化配置
def init(confPath,addonPath):
    cf = configparser.ConfigParser()
    if(not os.path.exists(confPath)):
        cf['main']={}
        cf['main']['downloadFolder']='download'
        cf['plugin']={}
        cf['plugin']['pluginName']=''
        cf['plugin']['pluginFile']=''
        with open(confPath,'w',encoding='utf-8') as f:
            cf.write(f)
    if(not os.path.exists(addonPath)):
        os.mkdir(addonPath)

# 校验插件
def check(addonName, addonPath):
    for plugin in os.listdir(addonPath):
        if(plugin == addonName):
            return True
    return False

# 设置壁纸
def setWallPaper(filePath):
    baseFolder = os.path.dirname(filePath)
    fileName = os.path.basename(filePath).split('.')[0] + '.bmp'
    bmpFile = os.path.join(baseFolder, fileName)
    if (not os.path.exists(fileName)):
        img = Image.open(filePath)
        img.save(bmpFile,'BMP')
        
    print(u'正在设置图片:%s为桌面壁纸...' % fileName)
    key = win32api.RegOpenKeyEx(win32con.HKEY_CURRENT_USER, "Control Panel\\Desktop", 0, win32con.KEY_SET_VALUE)
    win32api.RegSetValueEx(key, "WallpaperStyle", 0, win32con.REG_SZ, "2") #2拉伸适应桌面,0桌面居中
    win32api.RegSetValueEx(key, "TileWallpaper", 0, win32con.REG_SZ, "0")
    win32gui.SystemParametersInfo(win32con.SPI_SETDESKWALLPAPER, bmpFile, 1+2)
    print(u'成功应用图片:%s为桌面壁纸'  % fileName)

# 主程序入口
def main():
    addonPath = os.path.join(sys.path[0],'plugins')
    confPath = os.path.join(sys.path[0],'config.ini')
    init(confPath,addonPath)
    sys.path.append(addonPath)
    cf = configparser.ConfigParser()
    cf.read(confPath)
    downloadFolder = cf['main']['downloadFolder']
    downloadFolder = os.path.join(sys.path[0], downloadFolder)
    pluginFile = cf['plugin']['pluginFile']
    pluginName = cf['plugin']['pluginName']
    if(pluginFile == '' or pluginName == ''):
        spider = UnsplashSpider()
        imageFile = spider.getImage(downloadFolder)
        setWallPaper(imageFile)
    else:
        if(not check(pluginFile,addonPath)):
            print('插件%s不存在或配置不正确' % pluginName)
            return
        module = importlib.import_module('.', pluginFile.replace('.py',''))
        instance = getattr(module, pluginName)
        imageFile = instance().getImage(downloadFolder)
        setWallPaper(imageFile)

if(__name__ == '__main__'):
    main()
