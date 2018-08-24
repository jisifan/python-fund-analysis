import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import matplotlib
import datetime
import math as ma
from sklearn import linear_model
import statsmodels.api as sm
from PortfolioAnalyse import reportPeriod

# 回测
from Huice import Huice
inputFile = r'C:\Users\tangheng\Dropbox\summerIntern\data\fundPriceSeries.xlsx'
inputFile2 = r'C:\Users\tangheng\Dropbox\summerIntern\代码\mutual-fund-analysis\研报备份\2014年以来没换过基金经理的基金指标计算.xlsx'
startTime = datetime.datetime(2014,1,1,0,0)
endTime = datetime.datetime(2018,7,24,0,0)
a = Huice(inputFile,startTime,endTime)
data = pd.read_excel(inputFile2,sheet_name='指标')
tempDic = {}
start = 0
end = 0
key_str = ""
sign = 1
for i in range(data.shape[0]):
    if sign == 1:
        key_str = data.iloc[i,0]
        start = i+1
        sign = 0
    elif pd.isna(data.iloc[i,0]) and sign == 0:
        end = i
        tempDic[key_str] = data.iloc[start:end,:]
        sign = 1

# ####################################################################
# #前一时间段收益和回测收益的截面数据分析
# ####################################################################
# # 5个半年指标打分加两个半年数据回测
# N = 5
# for x in tempDic.keys():
#     pass

# startT = tempDic[x].iloc[7-N,0].split('-')[1]
# startT = datetime.datetime.strptime(startT, "%Y%m%d")
# panel = a.matrix
# #回测时间段
# panel = panel[panel.iloc[:,0]>=startT]

# #实际经历时间段
# startT = tempDic[x].iloc[N+1,0].split('-')[0]
# startT = datetime.datetime.strptime(startT, "%Y%m%d")
# endT = tempDic[x].iloc[7-N,0].split('-')[1]
# endT = datetime.datetime.strptime(endT, "%Y%m%d")
# panel2 = a.matrix
# panel2 = panel2[panel2.iloc[:,0]>=startT]
# panel2 = panel2[panel2.iloc[:,0]<=endT]

# shenglvDic = pd.DataFrame()
# for x in tempDic.keys():
#     jiaoyinengli = np.array(tempDic[x].iloc[(7-N):7,1],dtype = np.int32)
#     # 交易胜率
#     jyshenglv = len(jiaoyinengli[jiaoyinengli>=0])/len(jiaoyinengli)
#     # 交易获得额外收益胜率
#     jyyouxiu = len(jiaoyinengli[jiaoyinengli>0])/len(jiaoyinengli)
    
#     # 投研胜率
#     tynengli = np.array(tempDic[x].iloc[(7-N):7,3],dtype = np.int32)
#     # 投研获得额外收益胜率
#     tyshenglv = len(tynengli[tynengli>=0])/len(tynengli)
#     tyyouxiu = len(tynengli[tynengli>0])/len(tynengli)
#     # 期初收益计算
#     qichushouyi = panel[x].iloc[0]/panel2[x].iloc[0]
#     # 期末收益计算
#     qineishouyi = panel[x].iloc[-1]/panel[x].iloc[0]
    
#     shenglvDic[x] = [jyshenglv,jyyouxiu,tyshenglv,tyyouxiu,qichushouyi,qineishouyi]

# shenglvDic.index = ["交易胜率","交易额外胜率", "投研胜率", "投研额外胜率","回测期前实际收益","回测期收益"]

# trainData = shenglvDic.T
# X = trainData.iloc[:,0:4]
# Y1 = trainData["回测期前实际收益"]
# Y2 = trainData["回测期收益"]

# # 带p值的回归
# X1 = sm.add_constant(X)
# results = sm.OLS(Y1, X1).fit()
# print(results.summary())

# # OLS
# lr = linear_model.LinearRegression()
# lr.fit(X, Y1)
# lr.coef_
# lr.intercept_

# # Robust Regression
# ransac = linear_model.RANSACRegressor()
# ransac.fit(X, Y2)
# ransac.get_params()
# # 样本内数据
# inlier_mask = ransac.inlier_mask_
# # 样本外数据
# outlier_mask = np.logical_not(inlier_mask)
# # 样本纳入率
# include_rate = len(inlier_mask[inlier_mask])/len(inlier_mask)
# reg = ransac.estimator_
# reg.coef_


# X = sm.add_constant(X)
# results = sm.OLS(y,X).fit()

# #################################################################
# # #采用前一期的指标去预测下一期的收益率
# #################################################################
# # 6,5,4,3,2,1,0
# result = {}
# result2 = {}
# for i in range(6,-1,-1):
#     #各组合包含基金
#     huice_dic = {}
#     # #强势组合:交易能力和价值投资能力至少一个优秀，一个中等
#     # huice_dic["强势组合"] = list()
#     # #双强组合：交易能力为强，价值能力为弱
#     # # huice_dic["双强组合"] = list()
#     # # #交易强价值中组合：交易能力为强，价值能力为弱
#     # # huice_dic["交易强价值中组合"] = list()
#     # # #交易中价值强组合：交易能力为强，价值能力为弱
#     # # huice_dic["交易中价值强组合"] = list()
#     # #交易强组合：交易能力为强，价值能力为弱
#     # huice_dic["交易强组合"] = list()
#     # #价值强组合:价值能力为强，交易能力为弱
#     # huice_dic["价值强组合"] = list()
#     # #中间组合:交易能力和价值能力都为中等
#     # huice_dic["中等组合"] = list()
#     # #交易中势组合：交易能力为中，价值能力为弱
#     # huice_dic["交易中组合"] = list()
#     # #价值中势组合：交易能力为弱，价值能力为中
#     # huice_dic["价值中组合"] = list()
#     # #弱势组合：两者都为弱
#     # huice_dic["弱势组合"] = list()
    
#     # huice_dic["交易强组合"] = list()
#     # huice_dic["交易中组合"] = list()
#     # huice_dic["交易弱组合"] = list()
    
#     huice_dic["价值强组合"] = list()
#     huice_dic["价值中组合"] = list()
#     huice_dic["价值弱组合"] = list()
    
#     for x in tempDic.keys():
#         zhibiao = tempDic[x]
#         # 交易能力记为A,价值投资能力记为B
#         if zhibiao.shape[0] < 7:
#             continue
#         A = zhibiao.iloc[i,1]
#         B = zhibiao.iloc[i,3]
        
#         # if A+B>=1:
#         #     huice_dic["强势组合"].append(x)
#         # # if A > 0 and B > 0:
#         # #     huice_dic["双强组合"].append(x)
#         # # elif A > 0 and B == 0 :
#         # #     huice_dic["交易强价值中组合"].append(x)
#         # # elif A == 0 and B > 0 :
#         # #     huice_dic["交易中价值强组合"].append(x)
#         # elif A>0 and B<0:
#         #     huice_dic["交易强组合"].append(x)
#         # elif B>0 and A<0:
#         #     huice_dic["价值强组合"].append(x)
#         # elif A==0 and B== 0:
#         #     huice_dic["中等组合"].append(x)
#         # elif A == 0 and B<0:
#         #     huice_dic["交易中组合"].append(x)
#         # elif A <0 and B == 0:
#         #     huice_dic["价值中组合"].append(x)
#         # else:
#         #     huice_dic["弱势组合"].append(x)
        
        
#         # if A>0:
#         #     huice_dic["交易强组合"].append(x)
#         # elif A==0:
#         #     huice_dic["交易中组合"].append(x)
#         # else:
#         #     huice_dic["交易弱组合"].append(x)
        
#         if B>0:
#             huice_dic["价值强组合"].append(x)
#         elif B==0:
#             huice_dic["价值中组合"].append(x)
#         else:
#             huice_dic["价值弱组合"].append(x)
    
#     # 各组合净值序列
#     startT = tempDic[x].iloc[i,0].split('-')[1]
#     startT = datetime.datetime.strptime(startT, "%Y%m%d")
#     # 计算下一期
#     startT = reportPeriod(datetime.timedelta(days = 10) + startT)
#     endT = reportPeriod(datetime.timedelta(days = 10) + startT)
#     panel = a.matrix
#     panel = panel[panel.iloc[:,0]>=startT]
#     panel = panel[panel.iloc[:,0]<=endT]
#     priceSeries = pd.DataFrame({"时间" : panel.iloc[:,0]})
#     for key in huice_dic.keys():
#         p = np.dot((panel[huice_dic[key]])/(panel[huice_dic[key]].iloc[0,:]),np.ones((len(huice_dic[key]),1)))/len(huice_dic[key])
#         priceSeries[key] = np.array(p,dtype=np.float64)
    
#     result[startT.strftime("%Y%m%d")] = priceSeries
#     # result[startT.strftime("%Y%m%d")] = huice_dic
#     # result2[startT.strftime("%Y%m%d")] = [len(huice_dic["价值强组合"]),len(huice_dic["价值中组合"]),len(huice_dic["价值弱组合"])]
#     # result2[startT.strftime("%Y%m%d")] = [len(huice_dic["交易强组合"]),len(huice_dic["交易中组合"]),len(huice_dic["交易弱组合"])]

# fileSave = r'C:\Users\tangheng\Dropbox\summerIntern\代码\mutual-fund-analysis\研报备份\2014年以来没换过基金经理的基金指标按月回测2222(偏移一年，交易3分类).xlsx'
# with pd.ExcelWriter(fileSave) as writer:
#     for key in result.keys(): 
#         result[key].to_excel(writer,sheet_name = key)

# # kk = pd.DataFrame(result2)
# # kk.index = ["价值强组合","价值中组合","价值弱组合"]
# # kk = kk.T
# # fileSave = r'C:\Users\tangheng\Dropbox\summerIntern\代码\mutual-fund-analysis\研报备份\2014年以来没换过基金经理的基金各期价值胜率.xlsx'
# # with pd.ExcelWriter(fileSave) as writer:
# #         kk.to_excel(writer,sheet_name = "Sheet1")

# # kk = pd.DataFrame(result2)
# # kk.index = ["交易强组合","交易中组合","交易弱组合"]
# # kk = kk.T
# # fileSave = r'C:\Users\tangheng\Dropbox\summerIntern\代码\mutual-fund-analysis\研报备份\2014年以来没换过基金经理的基金各期交易胜率.xlsx'
# # with pd.ExcelWriter(fileSave) as writer:
# #         kk.to_excel(writer,sheet_name = "Sheet1")

        

    
