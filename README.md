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



### Statistics Analysis 

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

### Recode Linking

- Pick.py テストレコードのサンプリング

  ```
  pick.py B.csv Ex.csv C.csv Ea.csv
  例）pick.py B.csv e-x.csv c-100.csv e-a.csv
  ```

- attack.py レコードリンケージによるメンバーシップ攻撃．ユークリッド距離によるKDTreeを構築して探索している (PWS Cup 2020参照)

- rlink.py 

  ```
  rlink.py  C.csv D.csv E.csv
  例)rlink.py c-100.csv d-xrrdp.csv e-100xrrdp.csv
  ```

  テストデータCの各行が匿名化データDに属さないときは-1（非メンバーシップ），属するときは何行目かを上位k(=3)位まで予測して，Eに出力する．各列のメジアンよりも距離がある行を，-1と推測する（丁度50行を-1と推測する）．レコード間距離は，One Hot Encodingしてユークリッド距離を用いる．列8 (gh), 9 (mets)は用いない．
  sklearnのKDTree関数を用いたattack.py を呼んでいる．
  
  

### 有用性評価 Utility Metirics 
- `umark.py`		**U**tlity bench**mark** 

  ```
  umark B.csv D.csv
  ```

  有用性評価．BとDの，クロス集計(cnt, rate), オッズ比(Coef,OR,pvalue), 共分散cor の最大値と平均値を出力．

  |      | cnt   | rate  | Coef  | OR    | pvalue | cor   |
  | ---- | ----- | ----- | ----- | ----- | ------ | ----- |
  | max  | 69    | 0.020 | 0.309 | 0.061 | 0.159  | 0.006 |
  | mean | 2.530 | 0.001 | 0.031 | 0.017 | 0.028  | 8E-05 |

- `Iloss.py` **I**nformation **Loss**

  ```
  iloss.py C.csv D.csv
  ```
  
  有用性評価．CとDの，行を対応させたL1距離の最大値を評価する．(Max列のMax行の値)
  例）

	|      | 1    | 5    | cat  | Max  |
  | ---- | ---- | ---- | ---- | ---- |
  |mean |1.085297| 0.723084| 0.443483| 1.085297|
	|max  |8.000000| 4.400000| 4.000000| 8.000000|




### 安全性評価 Privacy Metrics 
- `lmark.py`　**L**inkage bench**mark** 

  ```
  lmark     Ea.csv  E.csv [out.csv]
  例) lmark.py e-a.csv e-100xrrdp.csv
  ```

  正解行番号Ea.csv と推定行番号E.csv を検査して，次の安全性 recall, precision, top-k を評価する．
  $$
  recall = \frac{|E_a \cap E|}{|E_a|}, \, prec = \frac{|E_a \cap E|}{|E|}, top_k = \frac{|\{x \in E_a| x \in E[x]\}|}{k}
  $$
  ここで，E_a とEは`Ea.csv` と`E.csv` の中の正の行番号(＝排除されていない行）からなる集合とする．$E[x]$​​ は行xに対応する推測行番号の上位k位までの集合．
  
  

### フォーマットチェッカー

- `checkDX.py`　
  加工フェーズの提出物(匿名化データD, 排除行データX)の形式チェック

  ```
  checkDX.py B.csv D.csv X.csv
  例）python3 checkDX.py Csv/B.csv Csv/d-xrrdp.csv Csv/e-x.csv 
  D: num OK
  D: obj OK
  0 OK
  2 OK
  3 OK
  4 OK
  10 OK
  (2724, 12) OK
  X: int OK
  X: unique OK
  (695, 1) OK
  ```

  Dに関しては，

  1. 数値列(1,5,6,7,11)が整数または実数であるか
  2. 名義列(0,2,3,4,10)がオブジェクトであるか
  3. 列1(年齢)，列5(BMI)が，値域[13, 85], [13, 75]にあるか，列6(鬱病)，列7(貧困), 列11(糖尿病)が{0,1}の値か．
  4. 列0 (性別)，列2(人種)，列3(学歴)，列4(既婚歴)，列10(活動量)がB.csv の値域の中にあるかどうか
  5. Dの行数が$|B|/2 = 1709$行以上あり，12 列あるか．
  
  をそれぞれ検査します．Xに関しては，
  
  1. 整数型であるか
  2. 重複する行を指定していないか
  3. $|X|_{行数}+|D|_{行数} = |B|_{行数}$​ になっているか
  
  を検査しています．全てに OK が出れば合格です．



### 実行スクリプト

`bash スクリプト名`で実行する．（OSによってshが使えない時は，スクリプト内のpytest の部分だけを順に実行）

1. `test-0config.sh` 自分のチーム番号Team, 攻撃先チーム番号You，pythonのパス，生成ファイル格納ディレクトリCsvなどを設定する．

2. `test-1setup.sh` ヘルスケアデータをCDCからダウンロードする．最初に一度だけ実行する．全ファイルを落とすのに数秒かかる．

3. `test-2anonymize.sh` （匿名化フェーズ）加工から有用性評価を実行する．Category_encodersのwarningが出ることもある．rr, dp はランダム要素があり，毎回結果が違う．

     ```
     $ bash test-2anonymize.sh
     top2.py Csv/B.csv 1_5 75_50 Csv/e-top.csv
     bottom2.py Csv/B.csv 1_5 22_20 Csv/e-bot.csv
     kanony2.py Csv/B.csv 7 2_3_4 Csv/e-ka.csv
     exclude.py Csv/B.csv Csv/pre_anony_00_x.csv Csv2/C.csv Csv2/e-in2.csv
     umark.py Csv/B.csv Csv/C.csv
                  cnt      rate      Coef        OR    pvalue       cor
     max   519.000000  0.061190  0.749521  0.288657  0.383715  0.135895
     mean  114.106061  0.007815  0.101983  0.072791  0.086014  0.012597
     uniqrt.py Csv/C.csv
     2360 0.7038473009245452 0.5632458233890215
     rr.py Csv/C.csv 0.9 Csv/d-xrr2.csv 0_2_3_4_6_7_10
     dp2.py Csv/d-xrr2.csv 1_5 1.0_2.0 Csv2/pre_anony_00_d.csv
     umark.py Csv/B.csv Csv/pre_anony_00_d.csv
                  cnt      rate      Coef        OR    pvalue       cor
     max   596.000000  0.065067  0.385540  0.218689  0.455050  0.182816
     mean  114.606061  0.010027  0.102278  0.082985  0.129358  0.015871
     ```

4. `test-3pick.sh`　評価データをBからテストデータCTをサンプリングする．事務局が行なう処理．

5. `test-4rlink.sh` （攻撃フェーズ）メンバーシップ推定とレコードリンクを試み，推定結果を出力する．

   ```
   $ bash test-4rlink.sh 
   rlink.py Csv/pre_anony_00_c.csv Csv/pre_anony_00_d.csv Csv/pre_attack_00_from_00.csv
   lmark.py Csv/pre_anony_00_ea.csv Csv/pre_attack_00_from_00.csv
   lmark.py Ea.csv E.csv out.csv
   recall    0.84
   prec      0.84
   topk      0.74
   dtype: float64
   ```

6. Test-5check.sh 提出ファイル(D, X, E)のフォーマット検査を行なう．全てにOK が出れば良い．















