# wrote by Makoto Iguchi, 2023
import pandas as pd
import numpy as np
import sys

throwExceptionFlag = 1
    
def checkvalues(df, i, vals):
    if set(df[i].values).issubset(vals):
        print(i, 'OK')
    else:
        print(i, 'Invalid')
        if (throwExceptionFlag):
            raise Exception(str(i) + ' Invalid')

def checkrange(df, i, vmin, vmax):
    if (df[i].min() >= vmin and df[i].max() <= vmax):
        print(i, 'OK')
    else:
        print(i, 'Invalid')
        if (throwExceptionFlag):
            raise Exception(str(i) + ' Invalid')

def checkC(dfB, dfC):
    # Type check
    if dfC.dtypes[[1,5,6,7,11]].isin([np.dtype('int32'), np.dtype('int64'), np.dtype(float)]).all():
        if dfC.dtypes[[0,2,3,4,10]].isin([np.dtype(object)]).all():
            print("C: num, obj OK")
        else:
            print("C: obj INVALID")
            if (throwExceptionFlag):
                raise Exception("C: obj INVALID")
    else:
        print("C: num INVALID")
        if (throwExceptionFlag):
            raise Exception("C: num INVALID")

    # Numerical data range check
    checkrange(dfC, 1, 13, 87)
    checkrange(dfC, 5, 8, 91)
    checkrange(dfC, 6, 0, 1)
    checkrange(dfC, 7, 0, 1)
    checkrange(dfC, 11, 0, 1)

    # Categorical data check
    checkvalues(dfC, 0, {'Female', 'Male'})
    checkvalues(dfC, 2, {'Black', 'Hispanic', 'Mexican', 'Other', 'White'})
    checkvalues(dfC, 3, {'11th', '9th', 'College', 'Graduate', 'HighSchool'})
    checkvalues(dfC, 4, {'Divorced', 'Married', 'Never', 'Parther', 'Separated', 'Widowed'})
    checkvalues(dfC, 10, {'Q1', 'Q2', 'Q3', 'Q4'})
    
    # Row & Column check
    if (dfC.shape == dfB.shape):
        print(dfC.shape, 'OK')
    else:
        print(dfC.shape, "Invalid")
        if (throwExceptionFlag):
            raise Exception(str(dfC.shape) + " Invalid")

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        print('Usage : ', sys.argv[0], 'B.csd C.csv')
        sys.exit(0)

    dfB = pd.read_csv(sys.argv[1], header=None) # Original health data
    dfC = pd.read_csv(sys.argv[2], header=None) # Anonymized health data (to be checked)

    throwExceptionFlag = 0
    checkC(dfB, dfC)
 