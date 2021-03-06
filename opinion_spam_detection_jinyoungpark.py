# -*- coding: utf-8 -*-
"""Opinion Spam Detection_JinYoungPark.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZO2_SutTafVUpqYJdnPWJk5qexvK8-KG

# Final Projection: Opinion Spam Detection

TCSS 535

Name: Jin Young Park

Student ID number: 1971490
"""

# Commented out IPython magic to ensure Python compatibility.
from google.colab import drive
import os
import fnmatch
import pandas as pd
import regex as re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
# %matplotlib inline
import nltk
from nltk.corpus import stopwords
import seaborn as sns
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
import numpy as np
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
import time

"""## 1. File Upload"""

drive.mount('/content/drive')

path = '/content/drive/My Drive/TCSS_535_FinalProject/op_spam_v1.4'

config_files = [os.path.join(subdir,f)
for subdir, dirs, files in os.walk(path)
    for f in fnmatch.filter(files, '*.txt')]

truth_or_deceptive = []
for f in config_files:
    c = re.search('(trut|deceptiv)\w',f)
    truth_or_deceptive.append(c.group())
labels_ToD = pd.DataFrame(truth_or_deceptive, columns = ['Labels'])

polarity = []
for f in config_files:
    c = re.search('(positiv|negativ)\w',f)
    polarity.append(c.group())
polarities = pd.DataFrame(polarity, columns = ['Polarity'])

source = []
for f in config_files:
    c = re.search('(MTur|TripAdviso|We)\w',f)
    source.append(c.group())
sources = pd.DataFrame(source, columns = ['Source'])

hotel = []
for f in config_files:
    c = re.search('(affini|allegr|amalf|ambassado|conra|fairmon|hardroc|hilto|homewoo|hyat|intercontinenta|jame|knickerbocke|monac|omn|palme|sherato|sofite|swissote|talbot)\w',f)
    hotel.append(c.group())
hotels = pd.DataFrame(hotel, columns = ['Hotel'])

review = []
directory =os.path.join("/content/drive/My Drive/TCSS_535_FinalProject/op_spam_v1.4")
for subdir,dirs ,files in os.walk(directory):
    for file in files:
        if fnmatch.filter(files, '*.txt'):
            f=open(os.path.join(subdir, file),'r')
            a = f.read()
            review.append(a)
reviews = pd.DataFrame(review, columns = ['Reviews'])

hotelreview_df= pd.merge(reviews, polarities,right_index=True,left_index = True)
hotelreview_df= pd.merge(hotelreview_df, sources,right_index=True,left_index = True)
hotelreview_df= pd.merge(hotelreview_df, hotels,right_index=True,left_index = True)
hotelreview_df= pd.merge(hotelreview_df, labels_ToD,right_index=True,left_index = True)
hotelreview_df.head()

"""## 2. Analyze the given data set"""

hotelreview_df.shape

hotelreview_df.info()

hotelreview_df.isnull().sum()

hotelreview_df.describe()

hotelreview_df.Labels.value_counts()

hotelreview_df.Source.value_counts()

hotelreview_df.Polarity.value_counts()

hotelreview_df.Hotel.value_counts()

"""## 3. Compute Statistic / Visualization"""

hotelreview_df[800:1200]

hotelreview_df.Reviews[0:400]

"""### Word Cloud

Word Cloud is a visualization technique where the size of each word indicates the frequency or importance of text data.
"""

stopword_list=[]
def displayWordCloud(data = None, backgroundcolor = 'black', width=800, height=600 ): 
  wordcloud = WordCloud(stopwords= stopword_list, background_color = backgroundcolor, width = width, height = height).generate(data) 
  print(wordcloud.words_) 
  plt.figure(figsize = (15, 10)) 
  plt.imshow(wordcloud) 
  plt.axis("off") 
  plt.show()

"""Negative Deceptive"""

displayWordCloud(''.join(hotelreview_df.Reviews[0:400]))

"""Nagative Truth"""

displayWordCloud(''.join(hotelreview_df.Reviews[400:800]))

"""Postive Truth"""

displayWordCloud(''.join(hotelreview_df.Reviews[800:1200]))

"""Positive Deceptive"""

displayWordCloud(''.join(hotelreview_df.Reviews[1200:1600]))

"""### N-grams model visualization

N-Grams is a contiguous word of n items from text data.
I visualized each of the text data using a bar chart with the frequencies of 1-gram, 2-grams, and 3-grams in ascending order of 10 each.
"""

#This is a function that splits text data one word .
def TexttoWords (data = None):
  for char in '-.,\n':
    data=data.replace(char,' ')
    data = data.lower()
  words = data.split()
  return words

"""Negative Deceptive"""

ND_words = TexttoWords(''.join(hotelreview_df.Reviews[0:400]))
ND_1_words = (pd.Series(nltk.ngrams(ND_words, 1)).value_counts())[:10]
ND_2_words = (pd.Series(nltk.ngrams(ND_words, 2)).value_counts())[:10]
ND_3_words = (pd.Series(nltk.ngrams(ND_words, 3)).value_counts())[:10]

"""This is a bar chart with the frequencies of 1-gram in the Negative Deceptive data."""

ND_1_words.sort_values().plot.barh(color='blue', width=.9, figsize=(6, 4))

"""This is a bar chart with the frequencies of 2-gram in the Negative Deceptive data."""

ND_2_words.sort_values().plot.barh(color='Orange', width=.9, figsize=(6, 4))

"""This is a bar chart with the frequencies of 3-gram in the Negative Deceptive data."""

ND_3_words.sort_values().plot.barh(color='green', width=.9, figsize=(6, 4))

"""Negative Truth"""

NT_words = TexttoWords(''.join(hotelreview_df.Reviews[400:800]))
NT_1_words = (pd.Series(nltk.ngrams(NT_words, 1)).value_counts())[:10]
NT_2_words = (pd.Series(nltk.ngrams(NT_words, 2)).value_counts())[:10]
NT_3_words = (pd.Series(nltk.ngrams(NT_words, 3)).value_counts())[:10]

"""This is a bar chart with the frequencies of 1-gram in the Negative Truth data."""

NT_1_words.sort_values().plot.barh(color='blue', width=.9, figsize=(6, 4))

"""This is a bar chart with the frequencies of 2-gram in the Negative Truth data."""

NT_2_words.sort_values().plot.barh(color='Orange', width=.9, figsize=(6, 4))

"""This is a bar chart with the frequencies of 3-gram in the Negative Truth data."""

NT_3_words.sort_values().plot.barh(color='green', width=.9, figsize=(6, 4))

"""Positive Truth"""

PT_words = TexttoWords(''.join(hotelreview_df.Reviews[800:1200]))
PT_1_words = (pd.Series(nltk.ngrams(PT_words, 1)).value_counts())[:10]
PT_2_words = (pd.Series(nltk.ngrams(PT_words, 2)).value_counts())[:10]
PT_3_words = (pd.Series(nltk.ngrams(PT_words, 3)).value_counts())[:10]

"""This is a bar chart with the frequencies of 1-gram in the Positive Truth data."""

PT_1_words.sort_values().plot.barh(color='blue', width=.9, figsize=(6, 4))

"""This is a bar chart with the frequencies of 2-gram in the Positive Truth data."""

PT_2_words.sort_values().plot.barh(color='Orange', width=.9, figsize=(6, 4))

"""This is a bar chart with the frequencies of 3-gram in the Positive Truth data."""

PT_3_words.sort_values().plot.barh(color='green', width=.9, figsize=(6, 4))

"""Positive Deceptive"""

PD_words = TexttoWords(''.join(hotelreview_df.Reviews[1200:1600]))
PD_1_words = (pd.Series(nltk.ngrams(PD_words, 1)).value_counts())[:10]
PD_2_words = (pd.Series(nltk.ngrams(PD_words, 2)).value_counts())[:10]
PD_3_words = (pd.Series(nltk.ngrams(PD_words, 3)).value_counts())[:10]

"""This is a bar chart with the frequencies of 1-gram in the Positive Deceptive data."""

PD_1_words.sort_values().plot.barh(color='blue', width=.9, figsize=(6, 4))

"""This is a bar chart with the frequencies of 2-gram in the Positive Deceptive data."""

PD_2_words.sort_values().plot.barh(color='Orange', width=.9, figsize=(6, 4))

"""This is a bar chart with the frequencies of 3-gram in the Positive Deceptive data."""

PD_3_words.sort_values().plot.barh(color='green', width=.9, figsize=(6, 4))

"""## 4. Pre-process Data : Perform Data Cleaning

Remove non-alphabetic words
"""

hotelreview_df['CleanedReviews'] = hotelreview_df['Reviews'].apply(lambda x: ' '.join([word for word in x.split() if word.isalpha()]))

"""Remove Stopwords"""

nltk.download('stopwords')
stop_words = stopwords.words('english')
new_stop_words = ['i', 'I', 'the', 'The' ' hotel', 'room', 'rooms']
stop_words.extend(new_stop_words)
hotelreview_df['CleanedReviews'] = hotelreview_df['CleanedReviews'].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in stop_words]))
hotelreview_df

"""## 5. Result of Cleaned Data

## Bar Chart 
Comparison of the number of words in the original data and the cleaned data
"""

num_total_word = len(TexttoWords(''.join(hotelreview_df.Reviews)))
num_total_Cleaned_word = len(TexttoWords(''.join(hotelreview_df.CleanedReviews)))
num_total_Deceptive_word = len(TexttoWords(''.join(hotelreview_df.Reviews[0:400])))+len(TexttoWords(''.join(hotelreview_df.Reviews[1200:1600])))
num_total_Truthful_word = len(TexttoWords(''.join(hotelreview_df.Reviews[400:1200])))
num_total_Cleaned_Deceptive_word = len(TexttoWords(''.join(hotelreview_df.CleanedReviews[0:400])))+len(TexttoWords(''.join(hotelreview_df.CleanedReviews[1200:1600])))
num_total_Cleaned_Truthful_word = len(TexttoWords(''.join(hotelreview_df.CleanedReviews[400:1200])))
total_num=pd.DataFrame({'Type':['Total_num','Total_num', 'Deceptive_num', 'Deceptive_num', 'Truthful_num', 'Truthful_num'],
                             'OorC':['Original_Data', 'Cleaned_Data','Original_Data', 'Cleaned_Data','Original_Data', 'Cleaned_Data'],
                             'Num':[num_total_word, num_total_Cleaned_word, num_total_Deceptive_word, num_total_Cleaned_Deceptive_word, num_total_Truthful_word, num_total_Cleaned_Truthful_word]})
total_num

sns.barplot(x='Type', y='Num', hue='OorC', data=total_num) # default : dodge=True
plt.title('Comparison of the number of words in the original data and the cleaned data', fontsize=18)
plt.legend(fontsize=12)
plt.show()

"""### Word Cloud

Negative Deceptive
"""

displayWordCloud(''.join(hotelreview_df.CleanedReviews[0:400]))

"""Nagative Truth"""

displayWordCloud(''.join(hotelreview_df.CleanedReviews[400:800]))

"""Postive Truth"""

displayWordCloud(''.join(hotelreview_df.CleanedReviews[800:1200]))

"""Positive Deceptive"""

displayWordCloud(''.join(hotelreview_df.CleanedReviews[1200:1600]))

"""### N-grams model visualization

Negative Deceptive
"""

ND_cleaned_words = TexttoWords(''.join(hotelreview_df.CleanedReviews[0:400]))
ND_1_cleaned_words = (pd.Series(nltk.ngrams(ND_cleaned_words, 1)).value_counts())[:10]
ND_2_cleaned_words = (pd.Series(nltk.ngrams(ND_cleaned_words, 2)).value_counts())[:10]
ND_3_cleaned_words = (pd.Series(nltk.ngrams(ND_cleaned_words, 3)).value_counts())[:10]

"""This is a bar chart with the frequencies of 1-gram in the Negative Deceptive data."""

ND_1_cleaned_words.sort_values().plot.barh(color='blue', width=.9, figsize=(6, 4))

"""This is a bar chart with the frequencies of 2-gram in the Negative Deceptive data."""

ND_2_cleaned_words.sort_values().plot.barh(color='Orange', width=.9, figsize=(6, 4))

"""This is a bar chart with the frequencies of 3-gram in the Negative Deceptive data."""

ND_3_cleaned_words.sort_values().plot.barh(color='green', width=.9, figsize=(6, 4))

"""Negative Truth"""

NT_cleaned_words = TexttoWords(''.join(hotelreview_df.CleanedReviews[400:800]))
NT_1_cleaned_words = (pd.Series(nltk.ngrams(NT_cleaned_words, 1)).value_counts())[:10]
NT_2_cleaned_words = (pd.Series(nltk.ngrams(NT_cleaned_words, 2)).value_counts())[:10]
NT_3_cleaned_words = (pd.Series(nltk.ngrams(NT_cleaned_words, 3)).value_counts())[:10]

"""This is a bar chart with the frequencies of 1-gram in the Negative Truth data."""

NT_1_cleaned_words.sort_values().plot.barh(color='blue', width=.9, figsize=(6, 4))

"""This is a bar chart with the frequencies of 2-gram in the Negative Truth data."""

NT_2_cleaned_words.sort_values().plot.barh(color='Orange', width=.9, figsize=(6, 4))

"""This is a bar chart with the frequencies of 3-gram in the Negative Truth data."""

NT_3_cleaned_words.sort_values().plot.barh(color='green', width=.9, figsize=(6, 4))

"""Positive Truth"""

PT_cleaned_words = TexttoWords(''.join(hotelreview_df.CleanedReviews[800:1200]))
PT_1_cleaned_words = (pd.Series(nltk.ngrams(PT_cleaned_words, 1)).value_counts())[:10]
PT_2_cleaned_words = (pd.Series(nltk.ngrams(PT_cleaned_words, 2)).value_counts())[:10]
PT_3_cleaned_words = (pd.Series(nltk.ngrams(PT_cleaned_words, 3)).value_counts())[:10]

"""This is a bar chart with the frequencies of 1-gram in the Positive Truth data."""

PT_1_cleaned_words.sort_values().plot.barh(color='blue', width=.9, figsize=(6, 4))

"""This is a bar chart with the frequencies of 2-gram in the Positive Truth data."""

PT_2_cleaned_words.sort_values().plot.barh(color='Orange', width=.9, figsize=(6, 4))

"""This is a bar chart with the frequencies of 3-gram in the Positive Truth data."""

PT_3_cleaned_words.sort_values().plot.barh(color='green', width=.9, figsize=(6, 4))

"""Positive Deceptive"""

PD_cleaned_words = TexttoWords(''.join(hotelreview_df.CleanedReviews[1200:1600]))
PD_1_cleaned_words = (pd.Series(nltk.ngrams(PD_cleaned_words, 1)).value_counts())[:10]
PD_2_cleaned_words = (pd.Series(nltk.ngrams(PD_cleaned_words, 2)).value_counts())[:10]
PD_3_cleaned_words = (pd.Series(nltk.ngrams(PD_cleaned_words, 3)).value_counts())[:10]

"""This is a bar chart with the frequencies of 1-gram in the Positive Deceptive data."""

PD_1_cleaned_words.sort_values().plot.barh(color='blue', width=.9, figsize=(6, 4))

"""This is a bar chart with the frequencies of 2-gram in the Positive Deceptive data."""

PD_2_cleaned_words.sort_values().plot.barh(color='Orange', width=.9, figsize=(6, 4))

"""This is a bar chart with the frequencies of 3-gram in the Positive Deceptive data."""

PD_3_cleaned_words.sort_values().plot.barh(color='green', width=.9, figsize=(6, 4))

"""## 6. Pre-process Data : Feature Selection & Engineering

Convert the text of the data to numeric values

TfidfVectorizer

TfidfVectorizer is a tool that automatically calculates TF-IDF provided by sklearn. And TF-IDF is a method of weighting the importance of each word in the Document-Term Metrix using word frequency and inverse document frequency.
"""

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(hotelreview_df['CleanedReviews'])
X.toarray()

"""Label Encoder

Label Encoder is encode target labels with values between 0 and n_classes-1.
"""

encoder = LabelEncoder()
encoder.fit(hotelreview_df['Labels'])
y = encoder.transform(hotelreview_df['Labels'])
y

"""## 7. Train-Test Split

Split the data into Train (80% of entire data) and Test (20% of entire data)
"""

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 101)

"""## 8. Logistic Regression

Training Logistic Regression
"""

LogisticRegressionmodel = LogisticRegression()
start = time.time()
LogisticRegressionmodel.fit(X_train, y_train)
print("Train Time :", time.time() - start)

"""Evaluation Metrics"""

LogisticRegressionpred = LogisticRegressionmodel.predict(X_test)

print("Train Score:",LogisticRegressionmodel.score(X_train, y_train))
print("Test Score:", LogisticRegressionmodel.score(X_test,y_test))
target_names = ['Deceptive', 'Truthful']
print(classification_report(y_test, LogisticRegressionpred, target_names=target_names))

"""Fine Tuning"""

C = np.logspace(-4, 4, 50)
param_grid = { 'C': C,
              'max_iter': [20, 50, 100, 200, 500, 1000]}
gcv = GridSearchCV(LogisticRegression(penalty='l2'), param_grid)
gcv.fit(X_train, y_train)
print('final params', gcv.best_params_, 'best score', gcv.best_score_)
means = gcv.cv_results_['mean_test_score']
stds = gcv.cv_results_['std_test_score']
params = gcv.cv_results_['params']
for mean, stdev, param in zip(means, stds, params):
    print("%f (%f) with: %r" % (mean, stdev, param))

TunedLogisticRegressionmodel = LogisticRegression(C=1.2067926406393288, max_iter=50)
start = time.time()
TunedLogisticRegressionmodel.fit(X_train, y_train)
print("Train Time :", time.time() - start)
TunedLogisticRegressionpred = TunedLogisticRegressionmodel.predict(X_test)

print("Train Score:",TunedLogisticRegressionmodel.score(X_train, y_train))
print("Test Score:",TunedLogisticRegressionmodel.score(X_test,y_test))
target_names = ['Deceptive', 'Truthful']
print(classification_report(y_test, TunedLogisticRegressionpred, target_names=target_names))

"""## 9. SVM

Training SVM
"""

SVMmodel = SVC()
start = time.time()
SVMmodel.fit(X_train, y_train) 
print("Train Time :", time.time() - start)

"""Evaluation Metrics"""

SVMpred = SVMmodel.predict(X_test)

print("Train Score:",SVMmodel.score(X_train, y_train))
print("Test Score:", SVMmodel.score(X_test,y_test))
target_names = ['Deceptive', 'Truthful']
print(classification_report(y_test, SVMpred, target_names=target_names))

"""Fine Tuning"""

C_SVM = [50, 10, 1.0, 0.1, 0.01]
param_grid_SVM = { 'C': C_SVM,
              'kernel':['linear', 'poly', 'rbf', 'sigmoid']}
gcv_SVM = GridSearchCV(SVC(), param_grid_SVM)
gcv_SVM.fit(X_train, y_train)
print('final params', gcv_SVM.best_params_, 'best score', gcv_SVM.best_score_)
means_SVM = gcv_SVM.cv_results_['mean_test_score']
stds_SVM = gcv_SVM.cv_results_['std_test_score']
params_SVM = gcv_SVM.cv_results_['params']
for mean_SVM, stdev_SVM, param_SVM in zip(means_SVM, stds_SVM, params_SVM):
    print("%f (%f) with: %r" % (mean_SVM, stdev_SVM, param_SVM))

TunedSVMmodel = SVC(C=50, kernel='rbf')
start = time.time()
TunedSVMmodel.fit(X_train, y_train)
print("Train Time :", time.time() - start)
TunedSVMpred = TunedSVMmodel.predict(X_test)

print("Train Score:",TunedSVMmodel.score(X_train, y_train))
print("Test Score:",TunedSVMmodel.score(X_test,y_test))
target_names = ['Deceptive', 'Truthful']
print(classification_report(y_test, TunedSVMpred, target_names=target_names))

"""## 10. Random Forest

Training Random Forest
"""

RandomForestmodel = RandomForestClassifier(n_estimators=10)
start = time.time()
RandomForestmodel.fit(X_train, y_train) 
print("Train Time :", time.time() - start)

"""Evaluation Metrics"""

RandomForestpred = RandomForestmodel.predict(X_test)

print("Train Score:",RandomForestmodel.score(X_train, y_train))
print("Test Score:", RandomForestmodel.score(X_test,y_test))
target_names = ['Deceptive', 'Truthful']
print(classification_report(y_test, RandomForestpred, target_names=target_names))

"""Fine Tuning"""

param_grid_RandomForest = { 'n_estimators': [10, 20, 50, 100, 500, 1000],
                  'max_features': ['sqrt', 'log2']}
gcv_RandomForest = GridSearchCV(RandomForestClassifier(), param_grid_RandomForest)
gcv_RandomForest.fit(X_train, y_train)
print('final params', gcv_RandomForest.best_params_, 'best score', gcv_RandomForest.best_score_)
means_RandomForest = gcv_RandomForest.cv_results_['mean_test_score']
stds_RandomForest = gcv_RandomForest.cv_results_['std_test_score']
params_RandomForest = gcv_RandomForest.cv_results_['params']
for mean_RandomForest, stdev_RandomForest, param_RandomForest in zip(means_RandomForest, stds_RandomForest, params_RandomForest):
    print("%f (%f) with: %r" % (mean_RandomForest, stdev_RandomForest, param_RandomForest))

TunedRandomForestmodel = RandomForestClassifier(n_estimators=1000, max_features='log2')
start = time.time()
TunedRandomForestmodel.fit(X_train, y_train)
print("Train Time :", time.time() - start)
TunedRandomForestpred = TunedRandomForestmodel.predict(X_test)

print("Train Score:",TunedRandomForestmodel.score(X_train, y_train))
print("Test Score:",TunedRandomForestmodel.score(X_test,y_test))
target_names = ['Deceptive', 'Truthful']
print(classification_report(y_test, TunedRandomForestpred, target_names=target_names))

"""## Reference:

How to Design A Spam Filtering System with Machine Learning Algorithms: https://towardsdatascience.com/email-spam-detection-1-2-b0e06a5c0472

Generate word cloud in Python: https://www.geeksforgeeks.org/generating-word-cloud-python/

From DataFrame to N-Grams: https://towardsdatascience.com/from-dataframe-to-n-grams-e34e29df3460

How to Clean Text for Machine Learning with Python: https://machinelearningmastery.com/clean-text-machine-learning-python/

Logistic Regression - Detailed Overview: https://towardsdatascience.com/logistic-regression-detailed-overview-46c4da4303bc

Support Vector Machine: https://scikit-learn.org/stable/modules/svm.html

Understanding Random Forest: https://towardsdatascience.com/understanding-random-forest-58381e0602d2

sklearn.linear_model.LogisticRegression: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html

sklearn.model_selection.GridSearchCV: https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html

sklearn.svm.SVC: https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html

sklearn.ensemble.RandomForestClassifier: https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html


"""