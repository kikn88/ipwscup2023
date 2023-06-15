
# wrote by Makoto Iguchi, 2023
import pandas as pd
import numpy as np
import sys

throwExceptionFlag = 1
    
def checkE(dfE):
    rows = 100
    n = 3985 

    # Format check
    if dfE.shape == (100, 1):
        print(dfE.shape, "OK")
    else:
        print(dfE.shape, "INVALID")
        if (throwExceptionFlag):
            raise Exception(str(dfE.shape) + " INVALID")
        
    # Index value check
    if dfE.dtypes.isin([np.dtype('int32'), np.dtype('int64')]).item():
        print("E: int OK")
        if dfE.max().item() < n and dfE.min().item() >= 0:
            print("E: value OK")
        else:
            message = "E: value Invalid (max:" + str(dfE.max().item()) + ", min:" + str(dfE.min().item()) + ")"
            print(message)
            if (throwExceptionFlag):
                raise Exception(message)
    else:
        print("E: int Invalid")
        if (throwExceptionFlag):
            raise Exception("E: int Invalid")

if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print('Usage : ', sys.argv[0], 'E.csv')
        sys.exit(0)

    dfE = pd.read_csv(sys.argv[1], header=None) # Estimated indexes

    throwExceptionFlag = 0
    checkE(dfE)
 