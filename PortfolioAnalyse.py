# coding=utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import matplotlib
import datetime
import math as ma

from WindPy import w

w.start()


# 返回报告期
# 参数：datetime对象
def reportPeriod(date1):
    if date1.month <= 12 and date1.month > 6:
        return datetime.datetime(date1.year,12,31,0,0)
    else:
        return datetime.datetime(date1.year,6,30,0,0)

# 模拟持仓分析
class PortfolioAnalyse:
    def __init__(self,fundCode,indexCode,startTime,endTime):
        '''
        初始化对象时直接生成self.matrix，一共六列，分别代表：基金模拟持仓前六个月收益、基金模拟持仓后六个月收益、 
            对标指数前六个月收益、对标指数后六个月收益、基金前六个月单位净值收益、基金后六个月单位净值收益。
        每行代表一个报告期
        '''
        self.fundcode = fundCode
        self.fundname = w.wss(fundCode, "sec_name").Data[0][0]
        fundSetup = w.wss(fundCode, "fund_setupdate").Data[0][0]
        # 往前移半年，并获取交易日期
        startDate = max(fundSetup-datetime.timedelta(weeks=24),startTime-datetime.timedelta(weeks=24))
        endDate = min(endTime,datetime.datetime.now())
        startDate_str = startDate.strftime("%Y-%m-%d")
        endDate_str = endDate.strftime("%Y-%m-%d")
        tradeDays = w.tdays(startDate_str, endDate_str, "Period=S").Data[0][0:-1]
        
        # 各期模拟持仓计算结果
        simulation_return = pd.DataFrame()
        
        #各期持仓组合
        self.portfolio = {}
        
        # range(1,len(tradeDays))倒过来
        for i in range(len(tradeDays)-1,0,-1):
            tradeday = tradeDays[i]
            reporttime = reportPeriod(tradeday).strftime("%Y%m%d")
            # 取出报告期持仓详情
            command = "rptdate="+ reporttime +";windcode="+fundCode+";field=stock_code,proportiontototalstockinvestments"
            stockHolds = w.wset("allstockhelddetaill3",command).Data
            # 如果持仓为空则跳过
            if len(stockHolds) <2:
                continue
            # 如果持仓披露不全则跳过
            if sum(stockHolds[1])<90:
                continue
            
            # 持仓股票列表
            stockList_str = ""
            firstTry = True
            for stockID in stockHolds[0]:
                if firstTry:
                    stockList_str = stockList_str + stockID
                    firstTry = False
                else:
                    stockList_str = stockList_str +","+ stockID
            
            command = "tradeDate=" + tradeday.strftime("%Y%m%d") + ";priceAdj=U;cycle=D"
            stockprice = w.wss(stockList_str, "close,adjfactor",command).Data
            stockprice = np.array(stockprice,dtype = np.float64)
            stockprice_now = stockprice[0,:] * stockprice[1,:]
            
            # 半年前价格
            tradedaytemp = tradeDays[i-1]
            command = "tradeDate=" + tradedaytemp.strftime("%Y%m%d") + ";priceAdj=U;cycle=D"
            stockprice = w.wss(stockList_str, "close,adjfactor",command).Data
            stockprice = np.array(stockprice,dtype = np.float64)
            stockprice_previous = stockprice[0,:] * stockprice[1,:]
            
            stockprice_after = np.array([np.nan]*stockprice_previous.shape[0]).reshape(stockprice_previous.shape[0],)
            # 半年后价格
            if i < len(tradeDays) - 1:
                after_Halfyear = tradeDays[i+1]
                command = "tradeDate=" + after_Halfyear.strftime("%Y%m%d") + ";priceAdj=U;cycle=D"
                stockprice = w.wss(stockList_str, "close,adjfactor",command).Data
                stockprice = np.array(stockprice,dtype = np.float64)
                stockprice_after = stockprice[0,:] * stockprice[1,:]
            
            # 基金持仓前六个月收益
            growth_previous = stockprice_now / stockprice_previous
            growth_previous[np.isnan(growth_previous)] = 0
            previous_return = sum(np.array(stockHolds[1],dtype=np.float64)*growth_previous)/100 - 1
            
            # 基金持仓后六个月收益
            growth_after = stockprice_after / stockprice_now
            growth_after[np.isnan(growth_after)] = 0
            after_return = sum(np.array(stockHolds[1],dtype=np.float64)*growth_after)/100 - 1
            
            # 对标指数前后六个月收益
            command = "tradeDate=" + tradeday.strftime("%Y%m%d") + ";priceAdj=U;cycle=D"
            indexPrice_now = w.wss(indexCode, "close,adjfactor", command).Data[0][0]
            command = "tradeDate=" + tradeDays[i-1].strftime("%Y%m%d") + ";priceAdj=U;cycle=D"
            indexPrice_previous = w.wss(indexCode, "close,adjfactor", command).Data[0][0]
            indexPrice_after = np.nan
            if i < len(tradeDays) - 1:
                command = "tradeDate=" + tradeDays[i+1].strftime("%Y%m%d") + ";priceAdj=U;cycle=D"
                indexPrice_after = w.wss(indexCode, "close,adjfactor", command).Data[0][0]
            indexReturn_previous = indexPrice_now/indexPrice_previous - 1
            indexReturn_after = indexPrice_after/indexPrice_now - 1
            
            # 基金单位净值前后六个月收益
            command = "tradeDate=" + tradeday.strftime("%Y%m%d")
            fundPrice_now = w.wss(fundCode, "NAV_adj", command).Data[0][0]
            command = "tradeDate=" + tradeDays[i-1].strftime("%Y%m%d")
            fundPrice_previous = w.wss(fundCode, "NAV_adj", command).Data[0][0]
            if fundPrice_previous is None:
                fundPrice_previous = np.nan
            fundPrice_after = np.nan
            if i < len(tradeDays) - 1:
                command = "tradeDate=" + tradeDays[i+1].strftime("%Y%m%d")
                fundPrice_after = w.wss(fundCode, "NAV_adj", command).Data[0][0]
                
            fundReturn_previous = fundPrice_now/fundPrice_previous - 1
            fundReturn_after = fundPrice_after/fundPrice_now - 1
            
            # 对结果基金赋值
            simulation_return[reporttime] = [previous_return,after_return,indexReturn_previous, \
                indexReturn_after,fundReturn_previous,fundReturn_after]
            self.portfolio[reporttime] = stockHolds
        
        # 组装返回值
        simulation_return = simulation_return.T
        indexName = w.wss(indexCode, "sec_name").Data[0][0]
        if simulation_return.shape[0]>0:
            simulation_return.columns = ["基金模拟持仓前六个月收益","基金模拟持仓后六个月收益", \
                indexName+"指数前六个月收益",indexName+"指数后六个月收益","基金前六个月单位净值收益", \
                "基金后六个月单位净值收益"]
        
        # 赋值结果
        self.matrix = simulation_return
        self.portfolio = self.portfolio


        
    def score(self):
        if self.matrix.shape[0] <= 0:
            return pd.DataFrame()
        datas = self.matrix
        N = datas.shape[0]
        # 交易能力指标
        jyzhibiao = pd.DataFrame()
        # 价值投资能力指标
        jztzzhibiao = pd.DataFrame()
        for i in range(N-1):
            A = datas.iloc[i+1,1]
            B = datas.iloc[i,0]
            C = datas.iloc[i+1,5]
            D = datas.iloc[i+1,3]
            
            jiaoyinengli = 0
            if (C > B and C < A) or (C > A and C < B):
                jiaoyinengli = 0
            elif C > B and C > A:
                jiaoyinengli = 1
            elif C < B and C < A:
                jiaoyinengli = -1
            
            jiazhitouzinengli = 0
            if A < D:
                jiazhitouzinengli = -1
            elif A > D and A < B:
                jiazhitouzinengli = 0
            elif A > D and A > B:
                jiazhitouzinengli = 1
            
            jztzzhibiao[datas.index[i+1]] = [jiazhitouzinengli]
            jyzhibiao[datas.index[i+1]+"-"+datas.index[i]] = [jiaoyinengli]
                
        jyzhibiao = jyzhibiao.T
        jztzzhibiao = jztzzhibiao.T
        
        result = pd.DataFrame()
        result["时间区间"] = jyzhibiao.index
        result["交易能力"] = jyzhibiao.iloc[:,0].values
        result["报告期"] = jztzzhibiao.index
        result["价值投资能力"] = jztzzhibiao.iloc[:,0].values
        
        return result


# 批量导出
def batch_process(stockList,indexCode,startTime,endTime,outputFile = r'C:\Users\tangheng\Dropbox\summerIntern\代码\mutual-fund-analysis\研报备份\2014年以来没换过基金经理的基金指标计算2.xlsx'):
    jiemian_t = pd.DataFrame()
    zhibiao_t = pd.DataFrame()
    jiemian_Dict = {}
    zhibiao_Dict = {}
    # obj = PortfolioAnalyse("090015.OF",indexCode,startTime,endTime)
    
    for x in stockList:
        #test
        obj = PortfolioAnalyse(x,indexCode,startTime,endTime)
        #截面数据
        jiemian = obj.matrix
        #持仓数据
        chicang = obj.portfolio
        #指标计算
        zhibiao = obj.score()
        
        k = pd.DataFrame()
        k2 = pd.DataFrame()
        i = 0
        for x in jiemian.columns:
            if i == 0:
                k[x] = [obj.fundcode]
            elif i == 1:
                k[x] = [obj.fundname]
            else:
                k[x] = [""]
            
            k2[x] = [""]
            i=i+1
        
        t = pd.DataFrame()
        t2 = pd.DataFrame()
        i = 0
        for x in zhibiao.columns:
            if i == 0:
                t[x] = [obj.fundcode]
            elif i == 1:
                t[x] = [obj.fundname]
            else:
                t[x] = [""]
        
            t2[x] = [""]
            i = i + 1
        
        
        
        jiemian_t = pd.concat([jiemian_t,k,jiemian,k2])
        zhibiao_t = pd.concat([zhibiao_t,t,zhibiao,t2])
        zhibiao_Dict[obj.fundcode] = zhibiao
        jiemian_Dict[obj.fundcode] = jiemian
        print(obj.fundcode)
    
    with pd.ExcelWriter(outputFile) as writer:
        jiemian_t.to_excel(writer,sheet_name = '截面')
        zhibiao_t.to_excel(writer,sheet_name = '指标')
    
    return [jiemian_Dict,jiemian_t,zhibiao_Dict,zhibiao_t,]

# 批量计算
startTime = datetime.datetime(2005,1,1,0,0)
endTime = datetime.datetime(2018,7,24,0,0)
indexCode = "000300.SH"
# inputFile = r'C:\Users\tangheng\Dropbox\summerIntern\代码\mutual-fund-analysis\研报备份\回测数据（中证800、没换过基金经理）.xlsm'
# data = pd.read_excel(inputFile,sheet_name="Sheet1")
# stockList = data.iloc[:,0]
stockList = ["161005.OF","000527.OF","540006.OF","000172.OF","161017.OF","000311.OF", \
        "001878.OF","163406.OF","110011.OF","570005.OF","206007.OF","180031.OF"]
outputFile = r'C:\Users\tangheng\Dropbox\summerIntern\代码\mutual-fund-analysis\研报备份\明星基金经理.xlsx'
batch_process(stockList,indexCode,startTime,endTime,outputFile)







