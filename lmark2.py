# wrote by Hiroaki Kikuchi, 2021
#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import sys

if __name__== "__main__":
	args = sys.argv
	if len(args) <= 3:
		print(args[0], 'E.csv X.csv')
	
	dfE = pd.read_csv(args[1], header=None)
	dfX = pd.read_csv(args[2], header=None)
	
	reid = (dfE == dfX).sum()[0]
	print(reid/100)
	#df = pd.DataFrame([{'recall': rcall, 'prec': prec, 'topk': topk.sum()/supp.sum()}])
	