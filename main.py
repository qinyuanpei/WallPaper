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
import win32gui ,win32con, win32api
from unsplashSpider import UnsplashSpider

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
        module = importlib.import_module('.',pluginFile.replace('.py',''))
        instance = getattr(module,pluginName)
        imageFile = instance().getImage(downloadFolder)
        setWallPaper(imageFile)

if(__name__ == '__main__'):
    main()
