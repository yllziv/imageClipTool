#coding:utf-8
import arcpy
import numpy as np
import os #读写文件
#全局变量
global R#临时文件
R=0
N=31#类别数0~(N-1)
global classCount
classCount=np.zeros((N))#给不同的类别级数



classFileName = [u"坑塘水面",u"有林地",u"其他林地",u"旱地",u"水浇地",u"其他草地",u"盐碱地",u"村庄",u"天然牧草地",u"水田",u"沼泽地",u"河流水面",u"裸地",u"设施农用地",u"果园",u"风景名胜及特殊用地",u"沟渠",u"人工牧草地",u"采矿用地",u"农村道路",u"内陆滩涂",u"灌木林地",u"铁路用地",u"水工建筑用地",u"建制镇",u"公路用地",u"湖泊水面",u"管道运输用地",u"水库水面",u"其他园地",u"沙地"]#类别
className = ["坑塘水面","有林地","其他林地","旱地","水浇地","其他草地","盐碱地","村庄","天然牧草地","水田","沼泽地","河流水面","裸地","设施农用地","果园","风景名胜及特殊用地","沟渠","人工牧草地","采矿用地","农村道路","内陆滩涂","灌木林地","铁路用地","水工建筑用地","建制镇","公路用地","湖泊水面","管道运输用地","水库水面","其他园地","沙地"]#类别
#print classCount,classCount[1]
locationraster="D:/temp/split/raster/"#原始数据位置文件夹raster
locationclass="D:/temp/split/class/"#原始数据位置文件夹class
resultfilelocation="D:/temp/test/result/"#结果数据文件夹


for i in range(N):
    savestr=resultfilelocation+classFileName[i]+str(i+1)
    os.mkdir(savestr)#创建文件夹，保存结果，
    #os.mkdir(savestr+"_clip")

def recursion(raster,rasterclass):
    arrclass=arcpy.RasterToNumPyArray(rasterclass,nodata_to_value=0)#raster转数组
    l=0
    flag=0
    npercent=np.zeros((N))
    for i in range(N):#计算不同类别所占的百分比
        indices=np.where(arrclass==i+1)
        npercent[i]=(np.take(arrclass,indices)[0].size)/float(arrclass.size)
    if (np.min(arrclass.shape)<25):
        flag=1
    if (np.max(npercent)>0.7):#判断栅格大小#判断所占比例
        l=np.argmax(npercent)
        global classCount
        classCount[l]=classCount[l]+1
        #raster.save(resultfilelocation+className[l]+str(l+1)+"/"+className[l]+"_"+str(int(classCount[l]))+"_"+str(int(np.max(npercent)*100))+".TIF")
        flag=1
        classArray=arrclass
        classArray[np.where(arrclass!=int(l+1))]=0
        classArray[np.where(arrclass==int(l+1))]=1
        rasterArray = arcpy.RasterToNumPyArray(raster)
        rasterArray[0] = rasterArray[0]*classArray
        rasterArray[1] = rasterArray[1]*classArray
        rasterArray[2] = rasterArray[2]*classArray
        point = arcpy.Point(raster.extent.XMin,raster.extent.YMin)
        result = arcpy.NumPyArrayToRaster(rasterArray,point,raster.meanCellHeight)
        result.save(resultfilelocation+className[l]+str(l+1)+"/"+className[l]+"_"+str(int(classCount[l]))+"_"+str(int(np.max(npercent)*100))+".TIF")
        #result.save(resultfilelocation+className[l]+str(l+1)+"_clip"+"/"+className[l]+"_"+str(int(classCount[l]))+"_"+str(int(np.max(npercent)*100))+".TIF")
    #elif np.max(npercent)<0.008:
    #        flag=1

    #print npercent,np.max(npercent),np.argmax(npercent),flag,np.min(arrclass.shape)
    #既不满足栅格大小，又不满足所占比例时，进行切割
    if flag==0:
        #切分成4个
        global R
        R=R+1
        dirname="D:/temp/test/temp/temp"+str(R)
        os.mkdir("D:/temp/test/temp/temp"+str(R))#创建文件夹，保存结果，
        arcpy.SplitRaster_management(raster,dirname,"number","NUMBER_OF_TILES","TIFF","BILINEAR","2 2","#","4","PIXELS")
        arcpy.SplitRaster_management(rasterclass,dirname,"catagory","NUMBER_OF_TILES","TIFF","BILINEAR","2 2","#","4","PIXELS")
        #print "split"
        rst1=arcpy.Raster(dirname+"/number"+str(0)+".TIF")
        rst2=arcpy.Raster(dirname+"/number"+str(1)+".TIF")
        rst3=arcpy.Raster(dirname+"/number"+str(2)+".TIF")
        rst4=arcpy.Raster(dirname+"/number"+str(3)+".TIF")
        rstc1=arcpy.Raster(dirname+"/catagory"+str(0)+".TIF")
        rstc2=arcpy.Raster(dirname+"/catagory"+str(1)+".TIF")
        rstc3=arcpy.Raster(dirname+"/catagory"+str(2)+".TIF")
        rstc4=arcpy.Raster(dirname+"/catagory"+str(3)+".TIF")
        recursion(rst1,rstc1)#i+1
        #print 1
        recursion(rst2,rstc2)#i+1
        #print 2
        recursion(rst3,rstc3)#i+1
        #print 3
        recursion(rst4,rstc4)#i+1
        #print "split again"

    return ()


for k in range(1056):
    print "开始下一个文件"+str(k)
    inputRaster=arcpy.Raster(locationraster+"rasterSplit"+str(k)+".TIF")
    inputclass=arcpy.Raster(locationclass+"classSplit"+str(k)+".TIF")
    recursion(inputRaster,inputclass)

