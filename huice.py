# coding=utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import matplotlib
import datetime
import math as ma

print('Python version ' + sys.version)
print('Pandas version: ' + pd.__version__)
print('Matplotlib version ' + matplotlib.__version__)

inputFile = r'C:\Users\tangheng\Dropbox\summerIntern\data\fundPriceSeries.xlsx'
inputFile2 = r'C:\Users\tangheng\Dropbox\summerIntern\代码\mutual-fund-analysis\研报备份\回测数据（中证800、没换过基金经理）.xlsm'

outputFile = r'C:\Users\tangheng\Dropbox\summerIntern\data\基金平均股价.xlsx'

#计算起始时间
# startTime = datetime.datetime(2016,1,28,0,0)
# endTime = datetime.datetime(2018,7,24,0,0)
startTime = datetime.datetime(2014,1,1,0,0)
endTime = datetime.datetime(2018,7,24,0,0)


class Huice:
    def __init__(self,inputFile,startTime,endTime):
        #计算起始时间结点
        self.startIndex = 0
        self.endIndex = 1
        self.data = pd.read_excel(inputFile)
        self.data2 = pd.read_excel(inputFile)
        
        self.matrix = self.data.iloc[2:,:]
        
        # 时间列表
        self.times = self.matrix.iloc[:,0].values
        
        # 开始提示符
        sign = 0
        for i in range(0,len(self.times)):
            if self.times[i] <= endTime:
                self.endIndex = i
            if self.times[i] >= startTime and sign == 0:
                self.startIndex = i
                sign = 1
                
        # 只取这一时间段的数据
        self.times = self.matrix.iloc[self.startIndex:(self.endIndex+1),0]
        self.matrix = self.matrix.iloc[self.startIndex:(self.endIndex+1),:]
        self.N = self.endIndex - self.startIndex + 1
        
a = Huice(inputFile,startTime,endTime)

data2 = pd.read_excel(inputFile2,sheet_name="category2")

k = np.zeros((10,))
j=0
sign = 0
for i in range(data2.shape[0]):
    if data2.iloc[i,0] == "强势基金":
        k[j] = i+1
        j = j+1
        sign = 1
    if data2.iloc[i,0] == "熊强组合":
        k[j] = i+1
        j = j+1
        sign = 1
    if data2.iloc[i,0] == "震荡强组合":
        k[j] = i+1
        j = j+1
        sign = 1
    if data2.iloc[i,0] == "牛强组合":
        k[j] = i+1
        j = j+1
        sign = 1
    if pd.isna(data2.iloc[i,0]) and sign == 1:
        k[j] = i
        j = j+1
        sign = 0
k[j] = data2.shape[0]
k = np.array(k,dtype=np.int32)

result = {"强势":data2.iloc[k[0]:k[1],0],"熊市组合":data2.iloc[k[2]:k[3],0],"震荡市组合":data2.iloc[k[4]:k[5],0],"牛市组合":data2.iloc[k[6]:k[7],0]}  

result2 = pd.DataFrame({"时间" : a.times})
for x in result.keys():
    p = np.dot((a.matrix[result[x]])/(a.matrix[result[x]].iloc[0,:]),np.ones((len(result[x]),1)))/len(result[x])
    result2[x] = np.array(p,dtype=np.float64)


# # 计算所有基金的走势，寻找其最匹配的指数
# result3 = pd.DataFrame({"时间" : a.times})
# p = np.dot((a.matrix.iloc[:,1:])/(a.matrix.iloc[0,1:]),np.ones((a.matrix.iloc[:,1:].shape[1],1)))/a.matrix.iloc[:,1:].shape[1]
# result3["基金数据"] = np.array(p,dtype=np.float64)

with pd.ExcelWriter(outputFile) as writer:
    result2.to_excel(writer,sheet_name = '数据')
