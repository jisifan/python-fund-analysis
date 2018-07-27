# coding=utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import matplotlib
import datetime

print('Python version ' + sys.version)
print('Pandas version: ' + pd.__version__)
print('Matplotlib version ' + matplotlib.__version__)

Location = r'C:\Users\tangheng\Dropbox\summerIntern\data\fundPriceSeries.xlsx'

fileSave = r'C:\Users\tangheng\Dropbox\summerIntern\data\test.xlsx'


#计算起始时间
startTime = datetime.datetime(2014,1,3,0,0)
endTime = datetime.datetime(2016,1,3,0,0)
#计算起始时间结点
startIndex = 0
endIndex = 1

# 读取数据dataframe
data = pd.read_excel(Location)
matrix = data.iloc[2:,:]

result = pd.DataFrame()

# 时间列表
times = matrix.iloc[:,0].values

# 开始提示符
sign = 0
for i in range(0,len(times)):
    if times[i] <= endTime:
        endIndex = i
    if times[i] >= startTime and sign == 0:
        startIndex = i
        sign = 1

# 只取这一时间段的数据
matrix = matrix.iloc[startIndex:(endIndex+1),:]

# 排序
for x in matrix.keys()[1:]:
    vector = matrix[x].values
    maxshortfall = 0
    for i in range(0,len(vector)-1):
        shortfall = (vector[i]-min(vector[i:]))/vector[i]
        if shortfall > maxshortfall:
            maxshortfall = shortfall
    yieldRate = vector[len(vector)-1]/vector[0] - 1
    result[x] = [data[x].iloc[0],maxshortfall,yieldRate]

# 计算分位数
result2 = result.copy()
result2.iloc[1:3] = result2.iloc[1:3].rank(1)
result2.iloc[1] = result2.iloc[1]/len(result2.columns)
result2.iloc[2] = result2.iloc[2]/len(result2.columns)

#原值表示法
result3 = result.T.copy()
result3.columns = ["基金名称","最大回撤","收益"]

# 分位数表示法
result4 = result2.T.copy()
result4.columns = ["基金名称","最大回撤分位数","收益分位数"]

# 最小回撤前30%
shortfall = result3["最大回撤"].quantile(0.3)

# 最大收益前30%
yieldRate = result3["收益"].quantile(0.7)

# 收益排名前30%，回撤排名前30%
result5 = result3[(result3.最大回撤<=shortfall)&(result3.收益>=yieldRate)].copy()


with pd.ExcelWriter(fileSave) as writer:
    result3.to_excel(writer,sheet_name = '原值表示')
    result4.to_excel(writer,sheet_name = '分位数表示')
    result5.to_excel(writer,sheet_name = '收益回撤前30%基金原值')






