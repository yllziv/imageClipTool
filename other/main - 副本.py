# -*- coding:utf-8 -*-
import arcpy
import os
import numpy as np
import sys
import over
import config
from arcpy.sa import *
reload(sys)
sys.setdefaultencoding( "utf-8" ) #解决编码问题

classFileName = config.classFileName #类别文件名
className = config.className #类别
shpFile = config.shpFile #矢量文件
rasterFile = config.rasterFile # 影像图
classFile = config.classFile #分类图
R = config.R # 类别长度

allFilePath = config.allFilePath

classType = [0] * R
extentArray = []

# 创建文件夹
resultfilelocation = allFilePath+"split/" #按图斑划分后保存的文件夹
os.mkdir(resultfilelocation)
rasterResultPath = resultfilelocation+"raster/"  #保存按图斑划分后的影像
classResultPath = resultfilelocation+"class/" #保存按图斑划分后的分类图
rasterOneResultPath = resultfilelocation+"rasterOne/" #保存按图斑划分后的只有一种类型的影像
# 创建文件夹
resultClipfilelocation = allFilePath+"clip/" # 按图斑划分后进行剪裁成256×256的整数倍
os.mkdir(resultClipfilelocation)
rasterClipResultPath = resultClipfilelocation+"raster/"  #保存按图斑划分后的影像
classClipResultPath = resultClipfilelocation+"class/" #保存按图斑划分后的分类图
rasterOneClipResultPath = resultClipfilelocation+"rasterOne/" #保存按图斑划分后的只有一种类型的影像
# 创建文件夹
resultCliplocation = allFilePath+"result/" # 按图斑划分后进行剪裁成256×256的整数倍,最后划分最大为256的图幅
os.mkdir(resultCliplocation)
rasterClipPath = resultCliplocation+"raster/"  #保存按图斑划分后的影像
classClipPath = resultCliplocation+"class/" #保存按图斑划分后的分类图
rasterOneClipPath = resultCliplocation+"rasterOne/" #保存按图斑划分后的只有一种类型的影像

os.mkdir(rasterClipResultPath)
os.mkdir(classClipResultPath)
os.mkdir(rasterOneClipResultPath)
os.mkdir(rasterResultPath)
os.mkdir(classResultPath)
os.mkdir(rasterOneResultPath)
os.mkdir(rasterClipPath)
os.mkdir(classClipPath)
os.mkdir(rasterOneClipPath)
for i in range(R):
    savestr=rasterClipResultPath+classFileName[i]
    os.mkdir(savestr)#创建文件夹，保存结果，
for i in range(R):
    savestr=classClipResultPath+classFileName[i]
    os.mkdir(savestr)#创建文件夹，保存结果，
for i in range(R):
    savestr=rasterOneClipResultPath+classFileName[i]
    os.mkdir(savestr)#创建文件夹，保存结果，

for i in range(R):
    savestr=rasterResultPath+classFileName[i]
    os.mkdir(savestr)#创建文件夹，保存结果，
for i in range(R):
    savestr=classResultPath+classFileName[i]
    os.mkdir(savestr)#创建文件夹，保存结果，
for i in range(R):
    savestr=rasterOneResultPath+classFileName[i]
    os.mkdir(savestr)#创建文件夹，保存结果，

for i in range(R):
    savestr=rasterClipPath+classFileName[i]
    os.mkdir(savestr)#创建文件夹，保存结果，
for i in range(R):
    savestr=classClipPath+classFileName[i]
    os.mkdir(savestr)#创建文件夹，保存结果，
for i in range(R):
    savestr=rasterOneClipPath+classFileName[i]
    os.mkdir(savestr)#创建文件夹，保存结果，

#遍历所有矢量对象
field = "DLMC" # 字段名——地类名称
cursor = arcpy.SearchCursor(shpFile)
row = cursor.next()
mycount = 1 #让下次执行的时候多next一下row
while row:
    print str(row.getValue("OBJECTID"))
    indexOfClass = className.index(str(row.getValue(field))) # 外接矩形类别索引
    classType[indexOfClass] = classType[indexOfClass] + 1
    if not int(row.getValue("OBJECTID")) in over.overArray: #若元素不在数组中
        if(mycount == 1):
            mycount = mycount+1
            row = cursor.next()
            continue
        # print "当前切割的影像类别为: " + str(row.getValue(field))
        # print "Start Clip classFile"
        arcpy.Clip_management( classFile,str(row.shape.extent.XMin)+" "+str(row.shape.extent.YMin)+" "+str(row.shape.extent.XMax)+" "+str(row.shape.extent.YMax),
            str(classResultPath)+str(row.getValue(field))+"/"+str(classType[indexOfClass])+".tif", "#", "#", "NONE")# 根据外接矩形分割分类图
        # print "Start Clip rasterFile"
        arcpy.Clip_management( rasterFile,str(row.shape.extent.XMin)+" "+str(row.shape.extent.YMin)+" "+str(row.shape.extent.XMax)+" "+str(row.shape.extent.YMax),
            str(rasterResultPath)+str(row.getValue(field))+"/"+str(classType[indexOfClass])+".tif", "#", "#", "NONE")# 根据外接矩形分割影像

        # 提取中影像中的单独一类
        #print "提取中影像中的单独一类"
        raster=arcpy.Raster(str(rasterResultPath)+str(row.getValue(field))+"/"+str(classType[indexOfClass])+".tif")
        rasterclass=arcpy.Raster(str(classResultPath)+str(row.getValue(field))+"/"+str(classType[indexOfClass])+".tif")
        # print str(rasterResultPath)+str(row.getValue(field))+"/"+str(classType[indexOfClass])+".tif"
        arrclass=arcpy.RasterToNumPyArray(rasterclass,nodata_to_value=0)#raster转数组
        npercent=np.zeros((R))
        for i in range(R):#计算不同类别所占的百分比
            indices=np.where(arrclass==i+1)
            npercent[i]=(np.take(arrclass,indices)[0].size)/float(arrclass.size)
        arrclass[np.where(arrclass!=int(indexOfClass+1))]=0
        arrclass[np.where(arrclass==int(indexOfClass+1))]=1

        #计算影像
        rasterArray = arcpy.RasterToNumPyArray(raster)
        rasterArray = rasterArray*arrclass
        # rasterArray[0] = rasterArray[0]*arrclass
        # rasterArray[1] = rasterArray[1]*arrclass
        # rasterArray[2] = rasterArray[2]*arrclass

        point = arcpy.Point(raster.extent.XMin,raster.extent.YMin)
        #下面会出现内存溢出
        result = arcpy.NumPyArrayToRaster(rasterArray,point,raster.meanCellHeight)
        #内存溢出发生在上面
        result.save(rasterOneResultPath+str(row.getValue(field))+"/"+str(classType[indexOfClass])+"_"+str(int(npercent[int(indexOfClass)]*100))+".tif") #单独一类的结果
        # print "开始切割影像"
        # originalRaster = arcpy.Raster(str(rasterResultPath)+str(row.getValue(field))+"/"+str(classType[indexOfClass])+".tif")
        # originalRasterOne = arcpy.Raster(rasterOneResultPath+str(row.getValue(field))+"/"+str(classType[indexOfClass])+"_"+str(int(npercent[int(indexOfClass)]*100))+".tif")
        # originalClass  = arcpy.Raster(str(classResultPath)+str(row.getValue(field))+"/"+str(classType[indexOfClass])+".tif")
        #
        # clipRasterPath = str(rasterClipResultPath)+str(row.getValue(field))+"/"+str(classType[indexOfClass])+".tif"
        # clipRasterOnePath = str(rasterOneClipResultPath)+str(row.getValue(field))+"/"+str(classType[indexOfClass])+"_"+str(int(npercent[int(indexOfClass)]*100))+".tif"
        # clipClassPath  = str(classClipResultPath)+str(row.getValue(field))+"/"+str(classType[indexOfClass])+".tif"
        # print "切割影像为256的整数倍，小于256不变"
        # if (originalRaster.width/256) > 0:
        #     originalRasterXMax = originalRaster.meanCellWidth*(originalRaster.width/256)*256 + originalRaster.extent.XMin
        # else:
        #     originalRasterXMax = originalRaster.extent.XMax
        # if (originalRaster.height/256) > 0:
        #     originalRasterYMax = originalRaster.meanCellHeight*(originalRaster.height/256)*256 + originalRaster.extent.YMin
        # else:
        #     originalRasterYMax = originalRaster.extent.YMax
        # rasterRectangle = str(originalRaster.extent.XMin)+" "+str(originalRaster.extent.YMin)+" "+str(originalRasterXMax)+" "+str(originalRasterYMax)
        # arcpy.Clip_management(originalRaster,rasterRectangle,clipRasterPath)
        # print "切割影像单类图"
        # if originalRasterOne.width/256 > 0:
        #     originalRasterOneXMax = originalRasterOne.meanCellWidth*(originalRasterOne.width/256)*256 + originalRasterOne.extent.XMin
        # else:
        #     originalRasterOneXMax = originalRasterOne.extent.XMax
        # if originalRaster.height/256 >0:
        #     originalRasterOneYMax = originalRasterOne.meanCellHeight*(originalRasterOne.height/256)*256 + originalRasterOne.extent.YMin
        # else:
        #     originalRasterOneYMax = originalRasterOne.extent.YMax
        # rasterOneRectangle = ""+str(originalRasterOne.extent.XMin)+" "+str(originalRasterOne.extent.YMin)+" "+str(originalRasterOneXMax)+" "+str(originalRasterOneYMax)
        # arcpy.Clip_management(originalRasterOne,rasterOneRectangle,clipRasterOnePath)
        # print "切割分类图"
        # if originalClass.width/256 > 0:
        #     originalClassXMax = originalClass.meanCellWidth*(originalClass.width/256)*256 + originalClass.extent.XMin
        # else:
        #     originalClassXMax = originalClass.extent.XMax
        # if originalRaster.height/256 >0:
        #     originalClassYMax = originalClass.meanCellHeight*(originalClass.height/256)*256 + originalClass.extent.YMin
        # else:
        #     originalClassYMax = originalClass.extent.YMax
        # classRectangle = ""+str(originalClass.extent.XMin)+" "+str(originalClass.extent.YMin)+" "+str(originalClassXMax)+" "+str(originalClassYMax)
        # arcpy.Clip_management(originalClass,classRectangle,clipClassPath)
        # print "切割完成"   #内存溢出发生在上面
        #
        # print "开始按照256保存最终结果"
        # # 命名规则：村庄_年份_矢量ID_覆盖率_编号
        # # clipRasterPath  clipRasterOnePath   clipClassPath  上一步切割的结果
        # # rasterClipPath  classClipPath  rasterOneClipPath   最终保存的结果
        # clipRasterPath = arcpy.Raster(clipRasterPath)
        # clipRasterOnePath = arcpy.Raster(clipRasterOnePath)
        # clipClassPath = arcpy.Raster(clipClassPath)
        # clipRasterH = clipRasterPath.height/256
        # clipRasterW = clipRasterPath.width/256
        # clipRasterWH = ""+str(clipRasterPath.width/256)+" "+str(clipRasterPath.height/256)
        # rasterFileName = str(row.getValue(field))\
        #                  +"_"+"2013"\
        #                  +"_"+str(row.getValue("OBJECTID"))\
        #                  +"_"+str(int(npercent[int(indexOfClass)]*100))\
        #                  +"_"+str(classType[indexOfClass])+"_"
        # rasterResult = str(rasterClipPath)+str(row.getValue(field))+"/"
        # arcpy.SplitRaster_management(clipRasterPath,rasterResult,rasterFileName,"NUMBER_OF_TILES","TIFF","NEAREST",clipRasterWH,"#","","PIXELS")
        #
        # clipRasterH = clipRasterOnePath.height/256
        # clipRasterW = clipRasterOnePath.width/256
        # clipRasterWH = ""+str(clipRasterOnePath.width/256)+" "+str(clipRasterOnePath.height/256)
        # rasterOneFileName = rasterFileName
        # rasterOneResult = str(rasterOneClipPath)+str(row.getValue(field))+"/"
        # arcpy.SplitRaster_management(clipRasterOnePath,rasterOneResult,rasterOneFileName,"NUMBER_OF_TILES","TIFF","NEAREST",clipRasterWH,"#","","PIXELS")
        #
        # clipRasterH = clipClassPath.height/256
        # clipRasterW = clipClassPath.width/256
        # clipRasterWH = ""+str(clipClassPath.width/256)+" "+str(clipClassPath.height/256)
        # classFileName = rasterFileName
        # classResult = str(classClipPath)+str(row.getValue(field))+"/"
        # arcpy.SplitRaster_management(clipClassPath,classResult,classFileName,"NUMBER_OF_TILES","TIFF","NEAREST",clipRasterWH,"#","","PIXELS")
        # print "完成一个图斑"
        row = cursor.next()
        del arrclass
        del rasterclass
        del npercent
    else:
        row = cursor.next()
