# -*- coding: utf-8 -*-
"""diabetes_early.ipynb
Automatically generated by Colaboratory.
Original file is located at
    https://colab.research.google.com/drive/1J0T17f7pcYn2cJeXLq-fFFfj_XKX4xFs
"""

#import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import pickle

#close warnings
import warnings
warnings.filterwarnings('ignore')

#read data
data = pd.read_csv("diabetes_data_upload.csv")
data.head()

#check data types
data.info()
#only age is numeric, other cols are categorical

#check missing values
data.isnull().sum()

#Class countplot
sn.countplot(data["class"])

sn.countplot(data['Gender'],hue=data['class'], data=data)

agekde = sn.kdeplot(data['Age'][(data["class"] == "Positive")])
agekde = sn.kdeplot(data['Age'][(data["class"] == "Negative")])

agekde = agekde.legend(["Positive","Negative"])

#Label encoding to categorical cols
data['Gender'] = data['Gender'].map({'Male':1,'Female':0})
data['class'] = data['class'].map({'Positive':1,'Negative':0})
data['Polyuria'] = data['Polyuria'].map({'Yes':1,'No':0})
data['Polydipsia'] = data['Polydipsia'].map({'Yes':1,'No':0})
data['sudden weight loss'] = data['sudden weight loss'].map({'Yes':1,'No':0})
data['weakness'] = data['weakness'].map({'Yes':1,'No':0})
data['Polyphagia'] = data['Polyphagia'].map({'Yes':1,'No':0})
data['Genital thrush'] = data['Genital thrush'].map({'Yes':1,'No':0})
data['visual blurring'] = data['visual blurring'].map({'Yes':1,'No':0})
data['Itching'] = data['Itching'].map({'Yes':1,'No':0})
data['Irritability'] = data['Irritability'].map({'Yes':1,'No':0})
data['delayed healing'] = data['delayed healing'].map({'Yes':1,'No':0})
data['partial paresis'] = data['partial paresis'].map({'Yes':1,'No':0})
data['muscle stiffness'] = data['muscle stiffness'].map({'Yes':1,'No':0})
data['Alopecia'] = data['Alopecia'].map({'Yes':1,'No':0})
data['Obesity'] = data['Obesity'].map({'Yes':1,'No':0})

#min max scaling to age col
from sklearn.preprocessing import MinMaxScaler
min_max_scaler = MinMaxScaler()
data["Age"] = min_max_scaler.fit_transform(data[["Age"]])

#correlation
corrdata = data.corr()
ax,fig = plt.subplots(figsize=(15,9))
sn.heatmap(corrdata,annot=True)

y = data["class"]
X = data.drop(["class"],axis = 1)

X.corrwith(y).sort_values()

#feature selection
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2


select = SelectKBest(score_func=chi2, k=8)
z = select.fit_transform(X,y)

print("After selecting best 8 features:", z.shape)

filter = select.get_support()
features = np.array(X.columns)
 
print("All features:")
print(features)
 
print("Selected best 8:")
print(features[filter])

print(z)

from collections import Counter
from sklearn.datasets import make_classification
from imblearn.over_sampling import RandomOverSampler

print(Counter(y))
oversample = RandomOverSampler(sampling_strategy='minority')
# fit and apply the transform
X, y = oversample.fit_resample(X, y)
# summarize class distribution
print(Counter(y))

y.describe()

X_fea = X[features[filter]]

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X_fea, y, test_size = 0.2, random_state = 42)

#Logistic Regression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.model_selection import KFold

lr_model = LogisticRegression()

lr_model.fit(X_train,y_train)
pred = lr_model.predict(X_test)

lrscore = lr_model.score(X_test,y_test)
lrcm = confusion_matrix(y_test,pred)
lrcr = classification_report(y_test,pred)
kf = KFold(n_splits=5, shuffle=True, random_state=42)
crvlsc = cross_val_score(lr_model, X_fea, y, cv=kf)                 

print('Logistic Regression')
print('*******************')
print('Testscore')
print('---------')
print(lrscore)
print('\n')
print('confusion Matrix')
print('----------------')
print(lrcm)
print('\n')
print('Classification Report')
print('---------------------')
print(lrcr)
print('Cross Validation Scores')
print('---------------------')
print(f'Min:{crvlsc.min()}')
print(f'Max:{crvlsc.max()}') 
print(f'Avg:{crvlsc.mean()}\n')

#Random Forest
from sklearn.ensemble import RandomForestClassifier

rf_model = RandomForestClassifier(n_estimators=10)

rf_model.fit(X_train,y_train)
pred = rf_model.predict(X_test)

rfscore = rf_model.score(X_test,y_test)
rfcm = confusion_matrix(y_test,pred)
rfcr = classification_report(y_test,pred)
kf = KFold(n_splits=5, shuffle=True, random_state=42)
crvlsc = cross_val_score(rf_model, X_fea, y, cv=kf)                 

print('Random Forest')
print('*******************')
print('Testscore')
print('---------')
print(rfscore)
print('\n')
print('confusion Matrix')
print('----------------')
print(rfcm)
print('\n')
print('Classification Report')
print('---------------------')
print(rfcr)
print('Cross Validation Scores')
print('---------------------')
print(f'Min:{crvlsc.min()}')
print(f'Max:{crvlsc.max()}') 
print(f'Avg:{crvlsc.mean()}\n')



pickle_out = open("model.pkl", "wb")
pickle.dump(rf_model, pickle_out)
pickle_out.close()