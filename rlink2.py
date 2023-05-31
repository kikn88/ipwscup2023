# wrote by Hiroaki Kikuchi, 2021
# coding: utf-8
import pandas as pd
import numpy as np
import attack
import sys

def rlink(dfC, dfD):
	a = attack.RecordLinkageAttack(dfD, dfC)
	dist, index = a.execute(k = 3)
	di = pd.DataFrame(np.hstack((index,dist)))
	di.loc[di[3] > di[3].median(), 0:2] = -1	
	return di.iloc[:, 0:3].astype(int)

if __name__ == "__main__":
	if  len(sys.argv) < 2:
		print(sys.argv[0], 'B.csv D.csv E.csv')
		sys.exit(0)
		# reidentify D and write the identified index in B to E
	
	dfB = pd.read_csv(sys.argv[1], header = None)
	dfD = pd.read_csv(sys.argv[2], header = None)
	dfB.loc[:,8:9] = 0		# drop 8 (gh), 9 (mets)
	dfD.loc[:,8:9] = 0
	#es = rlink(dfC, dfD)
	#es.to_csv(sys.argv[3], header = None, index = None)

	a = attack.RecordLinkageAttack(dfB, dfD)
	dist, index = a.execute(k = 3)
	di = pd.DataFrame(np.hstack((index,dist)))
	#di.loc[di[3] > di[3].median(), 0:2] = -1
	di.iloc[:, 0].astype(int).to_csv(sys.argv[3], header = None, index = None)
	'''
	'''
