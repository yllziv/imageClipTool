#coding:utf-8
import os #读写文件
import config
#全局变量，用来创造31个文件夹
classFileName = config.classFileName
resultfilelocation=config.resultfilelocation#结果数据文件夹
N = config.N
for i in range(N):
    savestr=resultfilelocation+classFileName[i]
    if(os.path.exists(savestr)):
        continue
    else:
        os.mkdir(savestr)#创建文件夹，保存结果，







