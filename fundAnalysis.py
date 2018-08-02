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

inputFile = r'C:\Users\tangheng\Dropbox\summerIntern\data\fundPriceSeries.xlsx'

fileSave = r'C:\Users\tangheng\Dropbox\summerIntern\data\test.xlsx'

#计算起始时间
startTime = datetime.datetime(2014,1,3,0,0)
endTime = datetime.datetime(2016,1,3,0,0)


class fundAnalyse:
    def __init__(self,inputFile,startTime,endTime):
        #计算起始时间结点
        self.startIndex = 0
        self.endIndex = 1
        self.data = pd.read_excel(inputFile)
        
        matrix = data.iloc[2:,:]
        
        # 时间列表
        times = matrix.iloc[:,0].values
        
        # 开始提示符
        sign = 0
        for i in range(0,len(times)):
            if times[i] <= endTime:
                self.endIndex = i
            if times[i] >= startTime and sign == 0:
                startIndex = i
                sign = 1
                
        # 只取这一时间段的数据
        self.matrix = matrix.iloc[startIndex:(endIndex+1),:]
        self.N = endIndex - startIndex + 1

    #计算基金最大回撤-收益
    def maxshortfall_return(self,outputFile):
        result = pd.DataFrame()
        # 排序
        for x in self.matrix.keys()[1:]:
            vector = self.matrix[x].values
            maxshortfall = 0
            for i in range(0,len(vector)-1):
                shortfall = (vector[i]-min(vector[i:]))/vector[i]
                if shortfall > maxshortfall:
                    maxshortfall = shortfall
            yieldRate = vector[len(vector)-1]/vector[0] - 1
            result[x] = [data[x].iloc[0],yieldRate,maxshortfall]
        
        # 计算分位数
        result2 = result.copy()
        result2.iloc[1:3] = result2.iloc[1:3].rank(1)
        result2.iloc[1] = result2.iloc[1]/len(result2.columns)
        result2.iloc[2] = result2.iloc[2]/len(result2.columns)
        
        #原值表示法
        result3 = result.T.copy()
        result3.columns = ["基金名称","收益","最大回撤"]
        
        # 分位数表示法
        result4 = result2.T.copy()
        result4.columns = ["基金名称","收益分位数","最大回撤分位数"]
        
        # 最小回撤前30%
        shortfall = result3["最大回撤"].quantile(0.3)
        
        # 最大收益前30%
        yieldRate = result3["收益"].quantile(0.7)
        
        # 收益排名前30%，回撤排名前30%
        result5 = result3[(result3.最大回撤<=shortfall)&(result3.收益>=yieldRate)].copy()
        
        # 写入文件
        with pd.ExcelWriter(outputFile) as writer:
            result3.to_excel(writer,sheet_name = '原值表示')
            result4.to_excel(writer,sheet_name = '分位数表示')
            result5.to_excel(writer,sheet_name = '收益回撤前30%基金原值')
        
        return [result3,result4,result5]
        
        #计算基金路径分析-收益
    def path_return(self,outputFile):
        """
        根据基金净值的面板数据计算各基金的收益率、离差均值、离差的方差、
        离差的偏度、离差的峰值
        输入：输出文件存储地址
        返回：一个list，第一个元素是原值的dataframe，第二个元素是分位数的dataframe
        """
        result = pd.DataFrame()
        # 计算一共经历了多少天
        timeLength = (times[endIndex] - times[startIndex]).days
        
        # 只取这一时间段的数据
        matrix = matrix.iloc[startIndex:(endIndex+1),:]
        
        # 计算每一天距开始日期有多少天
        timeVector =  times[startIndex:(endIndex+1)] - times[startIndex]
        dayCount = np.zeros((endIndex-startIndex+1,1))
        for i in range(0,endIndex-startIndex+1):
            dayCount[i] = int(timeVector[i].days)
        
        # 排序
        for x in matrix.keys()[1]:
            vector = matrix[x].values
            yieldRate = vector[len(vector)-1]/vector[0]
            ln_yieldRate_slope = ma.log(yieldRate)/timeLength
            ln_yieldRate_vector = ln_yieldRate_slope * dayCount
            perfectNetValue = vector[0] * np.apply_along_axis(ma.exp,1,ln_yieldRate_vector)
            # 离差epsilon = (真实的净值序列 - 如果每天收益率保持不变的净值序列)/期初基金净值
            epsilon = (vector - perfectNetValue)/vector[0]
            
            # 离差一阶矩（均值）
            re_moment1 = (np.dot(np.ones((1,N)),epsilon)/N)[0]
            # 每一个离差对于期望的偏离(计算N阶矩的中间变量)
            delta = epsilon - re_moment1
            # 离差的二阶中心矩（方差）
            re_moment2 = (np.dot(np.ones((1,N)),delta*delta)/N)[0]
            # 离差的三阶中心矩
            re_moment3 = (np.dot(np.ones((1,N)),delta*delta*delta)/N)[0]
            # 离差的三阶中心矩
            re_moment4 = (np.dot(np.ones((1,N)),delta*delta*delta*delta)/N)[0]
            result[x] = [data[x].iloc[0],yieldRate,re_moment1,re_moment2,re_moment3,re_moment4]
        
        # 计算分位数
        result2 = result.copy()
        result2.iloc[1:5] = result2.iloc[1:5].rank(1)
        for i in range(1,5):
        result2.iloc[i] = result2.iloc[i]/len(result2.columns)
        
        #原值表示法
        result3 = result.T.copy()
        result3.columns = ["基金名称","收益率","离差均值","离差方差","离差偏度","离差峰值"]
        
        # 分位数表示法
        result4 = result2.T.copy()
        result4.columns = ["基金名称","收益率分位数","离差均值分位数","离差方差分位数","离差偏度分位数","离差峰值分位数"]
        
        # 收益排名前30%，回撤排名前30%
        # result5 = result3[(result3.最大回撤<=shortfall)&(result3.收益>=yieldRate)].copy()
                # 写入文件
        with pd.ExcelWriter(outputFile) as writer:
            result3.to_excel(writer,sheet_name = '原值表示')
            result4.to_excel(writer,sheet_name = '分位数表示')
            # result5.to_excel(writer,sheet_name = '收益回撤前30%基金原值')
            
        return [result3,result4]

        
a = fundAnalyse(inputFile,startTime,endTime)
a.maxshortfall_return(fileSave)
a.path_return(fileSave)







