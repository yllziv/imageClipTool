# -*- coding:utf-8 -*-

import os
import arcpy
from arcpy.sa import *

def createAllFile(allFilePath, classFileName, R):


    # 创建文件夹
    if not os.path.exists(allFilePath): #若不存在，则创建
        os.mkdir(allFilePath) # 创建文件夹
    outputRaster = allFilePath+"outputRaster/"
    if not os.path.exists(outputRaster): #若不存在，则创建
        os.mkdir(outputRaster) # 创建文件夹

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


def clip(raster,rasterclass,n,resultpath):
    inSQLClause="VALUE = "+str(n)
    attExtract=ExtractByAttributes(rasterclass,inSQLClause)
    outExtractByMask=ExtractByMask(raster,attExtract)
    outExtractByMask.save(resultpath)

def getLastCount(shpFile):
    lastRowCount = []
    cursor = arcpy.SearchCursor(shpFile)
    row = cursor.next()
    while row:
        lastRowCount.append(int(row.getValue("OBJECTID")))
        row = cursor.next()
    return lastRowCount