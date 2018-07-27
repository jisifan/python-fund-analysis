# coding=utf-8
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import matplotlib
import datetime

# print('Python version ' + sys.version)
# print('Pandas version: ' + pd.__version__)
# print('Matplotlib version ' + matplotlib.__version__)

# # 建立pandas
# a = np.array([["hello",1, 2, 3, 4, 5],["hello1",2, 3, 4, 5, 6]])
# b = pd.DataFrame(data=a,index = [1,2],columns=[2,3,4,5,6,7])
# c = pd.Series(list(a),index = [1,2])

# data = [
#         ["2017-10-18",  11.53,  11.69,  11.70,  11.51,   871365.0,  "000001"],
#         ["2017-10-19",  11.64,  11.63,  11.72,  11.57,   722764.0,  "000001"],
#         ["2017-10-20",  11.59,  11.48,  11.59,  11.41,   461808.0,  "000001"],
#         ["2017-10-23",  11.39,  11.19,  11.40,  11.15,  1074465.0,  "000001"]]
# series = pd.Series(data, index=['a', 'b', 'c', 'd'])
# # 建立随机矩阵
# x = np.random.rand(100,10)
# # 1矩阵
# a = np.ones((3,1),dtype=int)
# # 0矩阵
# b = np.zeros((3,1),dtype=int)
# # 单位阵
# c = np.eye(2)
# # 横向合并
# result = np.hstack((a,b))
# # 纵向合并
# result = np.vstack((a,b))
# # 转化我行向量
# result = np.random.rand(3,3)
# result = result.reshape(9,1)
# # 转置
# result.transpose()
# result.T
# # 逆矩阵
# result = np.random.rand(3,3)
# result_inv = np.linalg.inv(result)
# np.dot(result,result_inv)
# # 矩阵乘法
# result = np.dot(a,a.transpose())
# # 矩阵的迹
# result = np.trace(result)
# # 矩阵的解
# A = np.random.rand(3,3)
# b = np.random.rand(3,1)
# c = np.linalg.solve(A,b)
# # 构造对角阵
# np.diag(A)
# np.diag(np.diag(A))
# # 矩阵特征向量
# b = np.linalg.eig(A)
# np.dot(A,b[1]) - np.dot(b[1],np.diag(b[0]))

####################################
# 正式开始
# 假设有N支股票，P个行业因子，Q个其他因子，1个国家因子, T期
# 假设股票的因子暴露矩阵为x(N*(1+P+Q)),
# 假设股票实际收益为r_all(N*T)
# 假设v是股票权重矩阵v(N*N)
# 假设s是行业权重，s通过v和X计算得到 temp = ones(1*N)*v.T*v*X(N*P),s = temp/temp.sum()
# 假设R是约束矩阵，通过s计算
# 假设omega是待求解的纯因子投资组合权重矩阵omega((1+P+Q)*N)
# 假设因子的收益率为f((1+P+Q)*T)
# 其中X、r_all、v都是提前给定的，先计算s,再计算omega,v
####################################
N = 100
P = 10
Q = 11
T = 60

K = 1+P+Q

# 构造虚拟的v
v = np.random.rand(1,N)
v = (v/v.sum()).reshape(N,) #写法很关键
v = np.diag(v)

# 构造虚拟的r_all
r_all = np.random.randn(N,T)
r_all = r_all/100

# 构造虚拟的x(N*P)，即行业暴露因子
t1 = int(np.floor(N/P))
t2 = int(N - t1 * P)
X = np.hstack((np.eye(t2),np.zeros((t2,P))))
for i in range(0,t1):
    X = np.vstack((X,np.eye(P)))
# 构造虚拟的x(N,Q)，即其他因子暴露
temp = np.random.rand(N,Q)
# 构造X，即所有暴露
X = np.hstack((np.ones((N,1)),X))
X = np.hstack((X,temp))

# 计算行业权重s
XP = X[:,1:(P+1)] #行业因子暴露
s = np.dot(np.dot(np.ones((1,N)),np.dot(v.T,v)), XP)
s = s/s.sum()

# 构造约束R
R1 = np.eye(P)
R1 = np.vstack((R1,np.hstack((0,s[0,0:(P-1)]/(-s[0,P-1])))))
R1 = np.vstack((R1,np.zeros((Q,P))))
R2 = np.vstack((np.zeros((1+P,Q)),np.eye(Q)))
R = np.hstack((R1,R2))

# 计算omega
omega = np.dot(R,np.linalg.inv(np.dot(np.dot(np.dot(np.dot(R.T,X.T),v),X),R)))
omega = np.dot(omega,np.dot(R.T,np.dot(X.T,v)))

# 检查因子是否提纯
check = np.dot(omega,X)

# 计算因子收益率
f = np.dot(omega,r_all)