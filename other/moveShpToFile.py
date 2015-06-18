#coding:utf-8
import shutil
import os
import config
N = config.N#类别数
className = config.classFileName#类别名
orginalShpFile = config.orginalShpFile
toShpFile = config.toShpFile
# N = 4
# className = ["三角形","四边形","五边形","六边形"]
# orginalShpFile = "C:/Users/ziv/Desktop/shptest/rusult/"
# toShpFile = "C:/Users/ziv/Desktop/shptest/"
for i in range(N):
    if(os.path.exists(orginalShpFile+className[i]+".dbf")&&os.path.exists(orginalShpFile+className[i]+".pri")&&os.path.exists(orginalShpFile+className[i]+".shx")&&os.path.exists(orginalShpFile+className[i]+".shp")):
        src1 = orginalShpFile+className[i]+".dbf"
        src4 = orginalShpFile+className[i]+".shp"
        src5 = orginalShpFile+className[i]+".shp.xml"
        src6 = orginalShpFile+className[i]+".shx"
        src7 = orginalShpFile+className[i]+".pri"
        des = toShpFile+className[i]
        shutil.move(src1,des)
        shutil.move(src4,des)
        shutil.move(src5,des)
        shutil.move(src6,des)
        shutil.move(src7,des)
