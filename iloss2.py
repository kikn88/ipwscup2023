# wrote by Hiroaki Kikuchi, 2021
# coding: utf-8
import pandas as pd
import sys

def iloss(dfC, dfD0):
	dfD = dfD0
	dfD.index = list(range(dfD.shape[0]))
	cat = [0,2,3,4,6,7,10,11] 	# categorical属性の列．
	dn = (dfC[[1,5]] - dfD[[1,5]]).abs()
	vmax = 20.0 # 差分の上限
	dn[dn > vmax] = vmax
	dn = dn/vmax
	dc = (dfC[cat] != dfD[cat]).sum(axis = 1)/8
	il = dn.aggregate(['max','mean'])
	il['cat'] = dc.aggregate(['max','mean'])
	il['max'] = il.max(axis = 1)
	return il

if __name__== "__main__":
	if len(sys.argv) <= 2:
		print(sys.argv[0], ' C.csv D.csv')
		sys.exit(1)
	# 有用性評価．CとDのinformation loss 情報損失を評価する．
	
	dfC = pd.read_csv(sys.argv[1], header=None)
	dfD = pd.read_csv(sys.argv[2], header=None)

	'''
	cat = [0,2,3,4,6,7,10,11] 	# categorical属性の列．
	dn = (dfC[[1,5]] - dfD[[1,5]]).abs()
	vmax = 20.0 # 差分の上限
	dn[dn > vmax] = vmax
	dn = dn/vmax
	dc = (dfC[cat] != dfD[cat]).sum(axis = 1)/8
	il = dn.aggregate(['max','mean'])
	il['cat'] = dc.aggregate(['max','mean'])
	il['mean'] = il.mean(axis = 1)
	print(il)
	'''
	il = iloss(dfC, dfD)
	print(il)
	
