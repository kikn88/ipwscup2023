# wrote by Hiroaki Kikuchi, 2021
import pandas as pd
import sys

seed = 528  # a new and hidden seed will be chosen by the organizer at the game

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(sys.argv[0], 'C.csv D.csv X.csv')
        sys.exit(0)
        # sample random 100 records from C and write the sampled records to D
        # and the row index to X
     
    dfC = pd.read_csv(sys.argv[1], header=None)
    dfD = dfC.sample(n = 100, random_state = seed)
    dfX = dfD.index.to_series()
    #dfc, ea = pick(df, ex.index)
    
    dfD.to_csv(sys.argv[2], header=None, index = None)
    dfX.to_csv(sys.argv[3], header=None, index = None)

