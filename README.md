# iPWS Cup 2023 - *Diabets Challenge*

The data anonymization competition, iPWS Cup 2023, aims to explore the practical anonymization technologies designed for healthcare big data and accurate prediction of future diabetes based on the current healthcare data. The competition will be held as a part of the international conference, [IWSEC 2023](https://www.iwsec.org/2023/), organized by IPSJ (Information Processing Society of Japan) and IEICE (the Institute of Electronics, Information, and Communication Engineers). 

[TOC]

## Requirement

- Python 3.6 
- Numpy
- pandas 1.1.5
- statsmodels v0.12.2

## Data

- [paper: Physical Activity Levels and Diabetes Prevalence in US Adults: Findings from NHANES 2015–2016](https://link.springer.com/content/pdf/10.1007/s13300-020-00817-x.pdf)
- [NHANES 2017-2018](https://wwwn.cdc.gov/nchs/nhanes/continuousnhanes/default.aspx?BeginYear=2017)


## Programs

### Generating Dataset

- `activ_diabet10_csv.py` download a required healthcare date from US CDC NHANES. The data consists of 12 attributes, indicating gender, age, race, educational level, marital status, BMI (body mass index) depressed state, poverty level, and physical variables for 4,190 participants in NHANES 2017-2018. Note that attributes labeled as 'gh' and 'mets' are not used for the competition. The diabetes patients are indicated as attributes labeled as 'dia'.  The downloaded file is stored in A.csv as, 

  ```
  python activ_diabet10_csv.py A.csv
  ```

  | gen  | age  | race  | edu        | mar      | bmi  | dep  | pir  | gh   | mets | qm   | dia  |
  | ---- | ---- | ----- | ---------- | -------- | ---- | ---- | ---- | ---- | ---- | ---- | ---- |
  | Male | 62   | White | Graduate   | Married  | 27.8 | 0    | 0    | 0    | 0    | Q2   | 1    |
  | Male | 53   | White | HighSchool | Divorced | 30.8 | 0    | 1    | 0    | 0    | Q1   | 0    |
  | Male | 78   | White | HighSchool | Married  | 28.8 | 0    | 0    | 0    | 0    | Q3   | 1    |

### Anonymizing Data (sample codes)

You can use any data anonymization algorithms in the competition.

Here, we present a couple of sample data anonymization scripts for your reference.

- `rr.py` Randomized Response

  It replaces values at specified attributes in input data B.csv by randomly chosen values with probability 1-p (retains the original value with probability p) and outputs to C.csv.  The target attributes are specified by a string of column indexes concatenated with an underscore. Any type of value can be randomized but discrete values such as gender and race are expected. 

  ```
  usage: rr.py B.csv p C.csv attributes_list
  (example) rr.py B.csv  0.9 C.csv  0_2_3_4_6_7_10
  ```

  The example generates the randomized data C.csv for columns 0, 2, 3, 4, 6, 7, and 10 with 1-0.9 probability. 

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

### Calculating Utility Score

The followings are the explanation of how the data utility is calculated with the associated scripts.

- `umark2.py` **u**tility bench**mark** 

  It calculates the overall utility score based on the utility loss of several perspectives: cross count  `ccount.py`, covariance matrix `cor.py`, odds ratio `odds6.py`, and information loss `iloss2`. These distances are multiplicatively aggregated.  

  Executing the following

  ```
  python umark2.py B.csv C.csv
  ```

  will give the table like this one:


  |      | cnt       | rate       | Coef       | OR         | pvalue     | cor        | 1          | 5          | cat        | max        | utility    |
  | ---- | --------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- | ---------- |
  | max  | 191       | 0.04558473 | 0.20702854 | 0.12078671 | 0.3405941  | 0.05519111 | 0.5        | 0.225      | 0.5        | 0.5        | 0.73181766 |
  | mean | 26.921875 | 0.00642527 | 0.04763524 | 0.04075512 | 0.09900669 | 0.00914453 | 0.05447494 | 0.03569332 | 0.05790573 | 0.05790573 | 0.96572577 |

  where the last column **utility** indicates the overall utility score. Namely, the perturbed data `C.csv` retains its utility as 0.73181766 through the processing for anonymizations (meaning that the data loses its utility by 0.26818234 due to the anonymization).

The followings are a detailed description of the metrics used for calculating the overall utility scores.

- `ccount.py` Cross Count

  It computes the counts of patients with diabetes with regards to all of the other attributes from the 0 to 11th columns. Continuous values such as age and BMI are divided into several bins.  

  Executing the following

  ```
  python ccount.py C.csv
  ```

  will generate a table of the counts of patients and the fraction of the counts for each of the possible combinations of values and diabetes. 

  |          | 11   | cnt  | rate       |
  | -------- | ---- | ---- | ---------- |
  | Female   | 0    | 1557 | 0.37159905 |
  | Female   | 1    | 531  | 0.12673031 |
  | Male     | 0    | 1530 | 0.36515513 |
  | Male     | 1    | 572  | 0.13651551 |
  | (19, 44] | 0    | 1400 | 0.33412888 |

  This shows that there are 531 and 572 patients with diabetes for females and males, respectively.  

- `cor.py` covariance matrix

  Executing the following

  ```
  python cor.py C.csv
  ```

  will give the correlation matrix of the domains, where the element is the Pearson correlation coefficient between values in all attributes. 
  
  For instance, the sample NHANES data generates a 26 x 26 matrix 

  |              | 0_Female   | 0_Male     | 1          | 2_White    |
  | ------------ | ---------- | ---------- | ---------- | ---------- |
  | **0_Female** | 0          | -1         | -0.0048204 | -0.036091  |
  | **0_Male**   | -1         | 0          | 0.00482043 | 0.03609103 |
  | **1**        | -0.0048204 | 0.00482043 | 0          | 0.09262846 |
  | **2_White**  | -0.036091  | 0.03609103 | 0.09262846 | 0          |

  where **0_Female** represents the value 'Female' in the 0-th column and **1** shows the 1st column (age). The male and female are excluded and hence the correlation is -1. There is a weak negative correlation (-0.0048204) between 'female' and age. 
  
- `odds6.py` Odds Ratio

  It performs the multiple logistic regression for given data B and C and outputs the mean absolute error in odds ratios (OR) and p-values between them. 

  Executing the following

  ```
  python odds6.py B.csv C.csv
  ```

  will give the table of ORs showing the risk of disease prevention with regard to demographic information (gender, age, and race), and the health status (BMI, depression).
  
  For example, OR for B gives the following table

  |             | Coef       | OR         | pvalue     |
  | ----------- | ---------- | ---------- | ---------- |
  | Intercept   | -5.0089095 | 0.00667818 | 4.44E-57   |
  | gen[T.Male] | 0.17144809 | 1.18702253 | 0.02343354 |
  | age         | 0.03690635 | 1.03759585 | 5.60E-54   |
  | bmi         | 0.06199413 | 1.06395609 | 1.04E-23   |

  where OR = 1.18 (T.Male) represents that male has a higher risk of diabetes than female with statistical significance (pvalue = 0.023). The good anonymized data preserves the ORs as exactly the same as the original data. 
  
- `iloss2.py` **I**nformation **Loss**

  It quantifies the loss of information between the original and the perturbed data. The distance between values x and y varies with the type of attributes:  |x - y| for numerical values such as age and BMI, and the Hamming weight, i.e., the number of inconsistent values for categorical values such as gender, and marital status. Note that the distances are normalized by dividing constants and the ranges are [0,1]. 

  Executing the following

  ```
  python iloss2.py B.csv C.csv
  ```

  will generate the information loss incurred by anonymization performed for C from B, like the following:

  |      | 1 (age)  | 5 (BMI)  | cat      | max      |
  | ---- | -------- | -------- | -------- | -------- |
  | max  | 0.500000 | 0.225000 | 0.500000 | 0.500000 |
  | mean | 0.054475 | 0.035693 | 0.057906 | 0.057906 |

  where column cat provides the Hamming distance of an 8-dimensional vector for categorical values, including gender, race, education, marital status, depression, poor index, quantified METS, and diabetes. 

### Sampling Anonymized Data

- `Pick2.py` sampling records

  ```
  python pick2.py C.csv D.csv X.csv
  ```

  It generates the challenge data `D.csv` that contains 100 records randomly sampled from the perturbed `C.csv`. The sampled record indexes are shuffled and then stored in the correct indexes file `X.csv`.
  
  This code is basically run by the judge to perform the sampling and generate `D.csv`.  `D.csv` will be made available to all attackers whereas the correct `X.csv` will be kept secret. 

### Attacking Data (sample code)

You can use any re-identification algorithms in the competition.

Here, we present a sample re-identification script for your reference.

- `rlink2.py` record linkage attack sample

  Executing the following 

  ```
  python rlink2.py B.csv D.csv E.csv
  ```

  will attempt to link the records in the original data `B.csv` with the perturbed records in `D.csv` and write the corresponding records in the `B.csv` to `E.csv`. `E.csv` consists of the estimated indexes of the records b* in B for each record d in D that has the smallest Euclid distance between b* and d.
  
  For example, 

  ```
  1605
  2580
  3142
  ..
  ```

  means that rows 0, 1, and 2 in `D.csv` are estimated as anonymized records of the row 1605, 2580, and 3142 in `B.csv`. 

  The discrete values e.g. gender and education are converted into numerical values represented with one-hot encoding. Note that historical attributes (8th gh and 9th mets) are not used. The attack.py, coded by Mr. Satoshi Hasegawa, uses the KDTree in sklearn to search the shortest vectors. 

### Calculating Privacy Score


- `lmark2.py` **L**inkage bench**mark** 

  It evaluates the privacy score of perturbated data. The score indicates how well the data withstood the re-identification attack.

  ```
  lmark2.py E.csv X.csv
  ```

   It computes the fraction of falsely estimated record indexes in E.csv computed with the correct indexes in X.csv.  



### Others

- `checkD.py `   format check of the anonymized records 

  It checks if the value of the perturbed data belongs to the specified range as follows. 

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
      checkvalues(dfC, 4, {'Divorced', 'Married', 'Never', 'Partner', 'Separated', 'Widowed'})
      checkvalues(dfC, 10, {'Q1', 'Q2', 'Q3', 'Q4'})
  ```

  Numerical data (1,5,6,7,11) must be either integer or real values.  For example, 13 <= age (1) <= 87.  

  Categorical values (0,2,3,4, 10) must be in the ranges in the original data. It alerts any invalid values. 



### Sample scripts

All steps in the competition can be performed in some sample shell scripts. Run the test script as following steps: 1, 3 for anonymizing phrases, and 5 for attacking phrases. Steps 2 and 4 are for the competition organizer (judge)

1. `bash test-1setup.sh` downloads NHANES 2017 data from CDC and converts the SAS format to CSV.  You can customize `test-0config.sh` where the team ID (00) and the target team IDs (00),  the default path, and all necessary file names are specified. Note it takes a few minutes. You don't have to execute it because the Judge uses it to synthesize B.csv distributed to every team. 
2. Judge synthesizes B.csv based on A.csv (NHAENS 2017). The source is not available. 
3. `bash test-3anonymize.sh` performs sample anonymizations using `rr.py` and `lap.py` and generates perturbed data `C.csv`. The utility score will be reported here. 
4. `bash test-4pick.sh` is performed by the judge and stores the sampled records `D.csv` and the corresponding indexes `X.csv`. 
5. `test-5rlink.sh` performs a record linkage attack to the target C.csv and evaluates the privacy score.
