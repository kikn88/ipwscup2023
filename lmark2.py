# wrote by Hiroaki Kikuchi, 2021
#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import sys

def lmark(dfE, dfX):
	reid = (dfE == dfX).sum()[0]
	return 1 - reid/len(dfE)

if __name__== "__main__":
	args = sys.argv
	if len(args) <= 2:
		print(args[0], 'E.csv X.csv')
	
	dfE = pd.read_csv(args[1], header=None)
	dfX = pd.read_csv(args[2], header=None)
	
	privacy_score = lmark(dfE, dfX)
	print(privacy_score)
	
