#coding:utf-8
import config
import arcpy
import numpy as np
import os #读写文件


# #切割影像
# originalRaster = arcpy.Raster("d:/temp/original/raster/raster12.TIF")
# originalClass  = arcpy.Raster("d:/temp/original/class/class12.TIF")

# clipRasterPath = "d:/temp/clip/raster/raster.TIF"
# clipClassPath  = "d:/temp/clip/class/class.TIF"


# originalRasterXMax = originalRaster.meanCellWidth*(originalRaster.width/256)*256 + originalRaster.extent.XMin
# originalRasterYMax = originalRaster.meanCellHeight*(originalRaster.height/256)*256 + originalRaster.extent.YMin
# rasterRectangle = ""+str(originalRaster.extent.XMin)+" "+str(originalRaster.extent.YMin)+" "+str(originalRasterXMax)+" "+str(originalRasterYMax)
# arcpy.Clip_management(originalRaster,rasterRectangle,clipRasterPath)

# originalClassXMax = originalClass.meanCellWidth*(originalClass.width/256)*256 + originalClass.extent.XMin
# originalClassYMax = originalClass.meanCellHeight*(originalClass.height/256)*256 + originalClass.extent.YMin
# classRectangle = ""+str(originalClass.extent.XMin)+" "+str(originalClass.extent.YMin)+" "+str(originalClassXMax)+" "+str(originalClassYMax)
# arcpy.Clip_management(originalClass,classRectangle,clipClassPath)

# 影像分幅
clipRaster = arcpy.Raster("d:/temp/clip/raster/raster.TIF")
clipClass = arcpy.Raster("d:/temp/clip/class/class.TIF")
splitRasterPath = "d:/temp/split/raster/"
splitClassPath = "d:/temp/split/class/"

clipRasterH = clipRaster.height/256
clipRasterW = clipRaster.width/256
clipRasterWH = ""+str(clipRaster.width/256)+" "+str(clipRaster.height/256)
arcpy.SplitRaster_management(clipRaster,splitRasterPath,"rasterSplit","NUMBER_OF_TILES","TIFF","NEAREST",clipRasterWH,"#","","PIXELS")

clipClassH = clipClass.height/256
clipClassW = clipClass.width/256
clipClassWH = ""+str(clipClass.width/256)+" "+str(clipClass.height/256)
arcpy.SplitRaster_management(clipClass,splitClassPath,"classSplit","NUMBER_OF_TILES","TIFF","NEAREST",clipClassWH,"#","","PIXELS")
