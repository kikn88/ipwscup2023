# iPWS Cup 2023 - *Diabets Challenge*

Data anonymization competition, iPWS Cup 2023, aims to exlpre the practical anonymization technologies designed for health care big data and accurate prediction of future diabates based on the current health care data. The competion will be held as a part of international conference, [IWSEC 2023](https://www.iwsec.org/2023/), organized by IPSJ (Information Processing Society of Japan) and IEICE (the Institute of Electronics, Informaion and Commucation Engineers). 

[TOC]

### Requirement

- Python 3.6 
- Numpy
- pandas 1.1.5
- statsmodels v0.12.2

## Data

- [paper: Physical Activity Levels and Diabetes Prevalence in US Adults: Findings from NHANES 2015–2016](https://link.springer.com/content/pdf/10.1007/s13300-020-00817-x.pdf)
- [NHANES 2017-2018](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?BeginYear=2017)


## Programs

### Dataset Generation

- `activ_diabet10_csv.py` download a required healthcare date from US CDC NHANES. The data consists of 12 attributes, indicating gender, age, race, educational level, marital status, BMI (body mass index) depressed state, poverty level and physical variables for 4,190 participants in NHANES 2017-2018. Note that attributes labled as 'gh' and 'mets' are not used for the competion. The diabets patients are indicated as attribute labled as 'dia'.  The downloaded file is stored A.csv as, 

  ```
  python activ_diabet10_csv.py A.csv
  ```

  | gen  | age  | race  | edu        | mar      | bmi  | dep  | pir  | gh   | mets | qm   | dia  |
  | ---- | ---- | ----- | ---------- | -------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
  | Male | 62   | White | Graduate   | Married  | 27.8 | 0    | 0    | 0    | 0    | Q2   | 1    |
  | Male | 53   | White | HighSchool | Divorced | 30.8 | 0    | 1    | 0    | 0    | Q1   | 0    |
  | Male | 78   | White | HighSchool | Married  | 28.8 | 0    | 0    | 0    | 0    | Q3   | 1    |

### Anonymizing

Arbitrary algorithm can be used for data anonymization. Here are some samples. 

- `rr.py` Randomized Response
  It replaces values at specified attributes in input data B.csv by randomly choosen values with probability 1-p (retains the original value with probability p) and outputs to C.csv.  The target attributes are specified by a string of column indexes concatnated with underscore. Any types of values can be reandomized but the discreate values such as gender and race are expected. 

  ```
  usage: rr.py B.csv p C.csv attributes_list
  (example) rr.py B.csv  0.9 C.csv  0_2_3_4_6_7_10
  ```

  The example generates the randomized data C.csv for columns 0, 2, 3, 4, 6, 7 and 10 with 1-0.9 probability. 

- `lap.py`  adds Laprace noise
  It adds the Laprace noise to the specified list of attributes that take numerical values, e.g., age and BMI. 

  ```
  usage: dp2.py input.csv attributes_list epsilon_list output.csv
  (example) dp2.py B.csv 1_5 1.0_2.0 C.csv
  ```

  The example adds Laplace noises with epsilon = 1 and 2 for the 1st and 5th attributes. The noise with the privacy budget epsilon and sensitivity = 1 follows the Laplace distribution defined as  
  $$
  \frac{\epsilon}{2} e^{-\epsilon |x|}
  $$



### Utility Metrics 

The followings are the metrics for the utility loss inccured by anonymizations. 

- `ccount.py`　Cross Count

  It computes the counts of patients of diabetes with regards to all of other attributes from 0 to 11th columns. Continuous values such as age and BMI are divided into several bins.  

  ```
  ccount.py C.csv
  ```

  This generates a table of the counts of patients and the fraction of the counts for each of possible combinations of values and the diabetes. 

  |          | 11   | cnt  | rate       |
  | -------- | ---- | ---- | ---------- |
  | Female   | 0    | 1557 | 0.37159905 |
  | Female   | 1    | 531  | 0.12673031 |
  | Male     | 0    | 1530 | 0.36515513 |
  | Male     | 1    | 572  | 0.13651551 |
  | (19, 44] | 0    | 1400 | 0.33412888 |

  This shows that there are 531 and 572 patients in diabetes for female and male, respectively.  

- `cor.py` covariance matrix

  ```
  cor.py		C.csv
  ```

  It gives the correlation matrix of the domains, where element is the Pearson correlation coefficients between values in all attrbutes. For instance, the sample NHANES data generates 26 x 26 matrix 

  |              | 0_Female   | 0_Male     | 1          | 2_White    |
  | ------------ | ---------- | ---------- | ---------- | ---------- |
  | **0_Female** | 0          | -1         | -0.0048204 | -0.036091  |
  | **0_Male**   | -1         | 0          | 0.00482043 | 0.03609103 |
  | **1**        | -0.0048204 | 0.00482043 | 0          | 0.09262846 |
  | **2_White**  | -0.036091  | 0.03609103 | 0.09262846 | 0          |

  where **0_Female** represents value 'Female' in 0-th column and **1** shows 1st column (age). The male and female are excluded and hence the correlation is -1. There is a weak negative correlation (-0.0048204) between 'female' and age. 
  
- `odds6.py`　Odds Ratio

  It performs the mutiple logistic regression for given data B and C and outputs the mean absoute error in odds ratios (OR) and p-values between them. 

  ```
  odds6.py B.csv C.csv
  ```

  ORs show the risk of disease prevention with regards to demographic information (gender, age, and race), and the health status (BMI, depression).  For example, OR for B gives the following table

  |             | Coef       | OR         | pvalue     |
  | ----------- | ---------- | ---------- | ---------- |
  | Intercept   | -5.0089095 | 0.00667818 | 4.44E-57   |
  | gen[T.Male] | 0.17144809 | 1.18702253 | 0.02343354 |
  | age         | 0.03690635 | 1.03759585 | 5.60E-54   |
  | bmi         | 0.06199413 | 1.06395609 | 1.04E-23   |

  , where OR = 1.18 (T.Male) represents that male has higher risk in diabets than female with statistical significant (pvalue = 0.023). The good anonymized data preserves the ORs  as exactly same to the original data. 
  
- `iloss2.py` **I**nformation **Loss**
  It quantifies the loss of information between the orignal and the pertubted data. The distance between values x and y varies with type of attributes:  |x - y| for numerical values such as age and BMI, and the Hamming weight, i.e., the number of inconsistent values for categorical values such as gender, and marital status. Note that the distances are normalized by dividing constants and the ranges are [0,1]. 

  ```
  iloss2.py B.csv C.csv
  ```

  It generates the information loss incurred by anonymization performed for C from B. 

  |      | 1 (age)  | 5 (BMI)  | cat      | max      |
  | ---- | -------- | -------- | -------- | -------- |
  | max  | 0.500000 | 0.225000 | 0.500000 | 0.500000 |
  | mean | 0.054475 | 0.035693 | 0.057906 | 0.057906 |

  where column cat provides the Hamming distance of 8-dimensional vector for categorical values, including gender, race, education, marital status, depression, poor index, quantified METS, and diabetes. 

- `umark2.py` **u**tility bench**mark** 

  It provides the overall loss of utility metrics defined from several perspectives: cross count  `ccount.py`, corvariance matrix `cor.py`, odds ratio `odds6.py`, and informtion loss `iloss2`. These distances are multiplicatively aggregated.  

  ```
  umark B.csv C.csv
  ```

  gives the following table

  |      | cnt       | rate       | Coef       | OR         | pvalue     | cor        | 1          | 5          | cat        | max        | uloss      |
  | ---- | --------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- |
  | max  | 191       | 0.04558473 | 0.20702854 | 0.12078671 | 0.3405941  | 0.05519111 | 0.5        | 0.225      | 0.5        | 0.5        | 0.26818234 |
  | mean | 26.921875 | 0.00642527 | 0.04763524 | 0.04075512 | 0.09900669 | 0.00914453 | 0.05447494 | 0.03569332 | 0.05790573 | 0.05790573 | 0.03427423 |

  where the last column **uloss** indicates the overall utility loss score aggregated all metrics. Namely, the pertubted data `C.csv` loses its utility as 0.26818234 through the processing for anonymizations. 

### Risk Metrics

- `Pick2.py` sampling records

  ```
  pick2.py C.csv D.csv X.csv
  ```

  It generates the challenge data `D.csv` that contains 100 records randomly sampled from the pertubted `C.csv`. The sampled record indexes are  suffuled and then stored into the correct indexes file `X.csv`.  Typically, a judge performs the sampling and makes `D.csv` available to all attackers without the correct `X.csv`. 

- rlink2.py record linkage 

  ```
  rlink2.py  B.csv D.csv  E.csv
  ```

  It attempts to link the records in the original data `B.csv` with the pertubted records in `D.csv` and write the corresponging records in the `B.csv` to `E.csv`. `E.csv` consists of the estimated indexes of the records b* in B for each record d in D that has the smallest Euclid distance between b* and d.  For example, 

  ```
  1605
  2580
  3142
  ..
  ```

  means that the 1st, 2nd and 3rd records in `D.csv` are estimated as anonymized from 1605-th, 2580-th and 3142-th records in `B.csv`. 

  The discrete values e.g. gender and educations are converted into numerical values represented with one-hot encording. Note that historical attributes (8th gh and 9th mets) are not used. The attack.py, coded by Mr. Satoshi Hasegawa, uses the KDTree in sklearn to search the shortest vectors. 

- `lmark2.py`　**L**inkage bench**mark** 

  It evaulates the re-identified risk of a perturbted data. 

  ```
  lmark2.py E.csv X.csv
  ```

   It computes the fraction of correctly estimated record indexes in E.csv computed with the correct indexes X.csv.  



### Others

- `checkD.py `   format check of the anonymized records　
  It checks if the value of the pertubted data belongs the specified range as follows. 

  ```
      # Numerical data range check
      checkrange(dfC, 1, 13, 87)
      checkrange(dfC, 5, 8, 52)
      checkrange(dfC, 6, 0, 1)
      checkrange(dfC, 7, 0, 1)
      checkrange(dfC, 11, 0, 1)
  
      # Categorical data check
      checkvalues(dfC, 0, {'Female', 'Male'})
      checkvalues(dfC, 2, {'Black', 'Hispanic', 'Mexican', 'Other', 'White'})
      checkvalues(dfC, 3, {'11th', '9th', 'College', 'Graduate', 'HighSchool', 'Missing', np.nan})
      checkvalues(dfC, 4, {'Divorced', 'Married', 'Never', 'Parther', 'Separated', 'Widowed'})
      checkvalues(dfC, 10, {'Q1', 'Q2', 'Q3', 'Q4'})
  ```

  Numerical date (1,5,6,7,11) must be either integer or real values.  For example, 13 <= age (1) <= 87.  

  Categorical values (0,2,3,4, 10) must be in the ranges in the original data. It alarts any invalid values. 



### Sample scripts

All steps in the competition can be performed in some sample shell scripts. Run  test-script as following steps: 1, 3 for anonymizing  pharse and 5 for attacking phrases. Step 2 and 4 are for the competiton organizer (judge)

1. `bash test-1setup.sh` downloads NHANES 2017 data from CDC and converts the SAS format to CSV.  You can customize `test-0config.sh` where  the team ID (00) and the target team IDs (00) ,  the default path and all necessary file names are specified. Note it takes few minutes. You don't have to execute it because the Judge uses it to synthsize B.csv distributed to every teams. 
2. Judge synthesizes B.csv based on A.csv (NHAENS 2017). The source is not available. 
3. `bash test-3anonymize.sh` performs sample anonymizations using `rr.py` and `lap.py` and generates pertubuted data `C.csv`. Utility loss score are reported here. 
4. ``bash test-4pick.sh`　is performed by the judge and stores the sampled records `D.csv` and the corresponding indexes `X.csv`. 
5. `test-5rlink.sh` performs record linkage attack to the target C.csv and evaulates the re-identified risk score. 















