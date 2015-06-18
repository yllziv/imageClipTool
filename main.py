# -*- coding:utf-8 -*-
import os
import sys
import shutil

from arcpy import env

import config as config
import myLib.over as over
import myLib.myFunction as myFunction

print " **************************** "
print "       ClipTool V0.1"
print ""
print "        DEAMONDS"
print "   ARCGIS VERSION >= 10.0"
print "  PYTHON VERSION 2.6 OR 2.7"
print "  COMPUTER MEMORY >= 4G"
print "  PATH CANNOT INCLUDE CHINESE"
print ""
print "     yll.ziv@gmail.com"
print ""
print "                  2015/05/30"
print ""
print " ****************************"

reload(sys)
sys.setdefaultencoding( "utf-8" ) #解决编码问题

classFileName = config.classFileName #类别文件名
className = config.className #类别
shpFile = config.shpFile #矢量文件
rasterFile = config.rasterFile # 影像图
R = config.R # 类别长度
allFilePath = config.allFilePath
field = config.field # 字段名——地类名称
env.workspace= allFilePath
overArray = over.myArray[0]

classType = [0] * R
extentArray = []


# 保存id数据文件over.py
allShpIdArray = myFunction.getLastCount(shpFile) # shp图的id数组
interCount = len(allShpIdArray)/1000 #数据的长度

overArrayList = [[]]*interCount #保存所有图斑id，分成interCount份
for i in range(interCount):
    start = (i)*len(allShpIdArray)/interCount
    end = (i+1)*len(allShpIdArray)/interCount
    overArrayList[i] = (allShpIdArray[start:end])

file_object = open("myLib/over.py","w")
file_object.write("myArray=")
file_object.close()
file_object = open("myLib/over.py","a")
file_object.write(str(overArrayList))
file_object.close()

selfPath = str(sys.argv[0][sys.argv[0].rfind(os.sep)+1:])
selfFileName = selfPath.split("/")
selfUpFilePath = ""
for i in range(len(selfFileName)-1):
    selfUpFilePath = selfUpFilePath + (selfFileName[i] + "/")

# 新建临时文件并复制配置文件
if os.path.exists(selfUpFilePath+"temp"):
    shutil.rmtree(selfUpFilePath+"temp")

os.mkdir(selfUpFilePath+"temp")
os.mkdir(selfUpFilePath+"temp/myLib")
shutil.copyfile(selfUpFilePath+"config.py",selfUpFilePath+"temp/config.py")
shutil.copyfile(selfUpFilePath+"myLib/__init__.py",selfUpFilePath+"temp/myLib/__init__.py")
shutil.copyfile(selfUpFilePath+"myLib/myFunction.py",selfUpFilePath+"temp/myLib/myFunction.py")
shutil.copyfile(selfUpFilePath+"myLib/over.py",selfUpFilePath+"temp/myLib/over.py")


for index in range(interCount):
    shutil.copyfile("myLib/entrance.py","temp/"+str(index)+".py")

for systemIndex in range(interCount):
    os.system("python temp/" + str(systemIndex) + ".py")

shutil.rmtree(selfUpFilePath+"temp")
