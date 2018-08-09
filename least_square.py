# from cvxopt import solvers, matrix
import numpy as np
import sys
def least_square6(data_train, label_train):
	'''
	帶約束的回归方程计算，包含重仓股因子
	'''
	
	# 时间窗口长度
	N = data_train.shape[0]
	
	for i in range(N):
	    if data_train[i,0] is None:
	        data_train = data_train[:,1:]
	        break
	    
	data_train = np.hstack((np.ones((N,1)),data_train))
	
	# 防止类型错误
	data_train = np.array(data_train,dtype=np.float64)
	label_train = np.array(label_train,dtype=np.float64)
	
	# 解出序数，列向量
	W = np.dot(np.dot(np.linalg.inv(np.dot(data_train.T,data_train)),data_train.T),label_train)
	
	# 残差
	epsilon = label_train - np.dot(data_train,W)
	SSE = np.dot(epsilon.T,epsilon)

	ybar = label_train - np.dot(1/N * np.ones((1,N)),label_train)
	SST = np.dot(ybar.T,ybar)
	
	r_square = float(1 - SSE/SST)

	#返回前将W转为行向量
	return W.T, r_square


#test
X =  np.random.rand(20,5)
X =  np.hstack((np.array([None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None]).reshape(20,1),X))
Y =  np.random.rand(20,1)
result = least_square6(X,Y)
