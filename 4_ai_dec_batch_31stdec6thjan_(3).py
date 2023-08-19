# -*- coding: utf-8 -*-
"""4. AI Dec Batch 31stDec6thJan (3).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XH4VhqZUV9Q3rkzehmSIe2cHuU3hYZkU

# Min/Max Scaling

In min/max scaling, you subtract each value by the minimum value and then divide the result
by the difference of minimum and maximum value in the dataset.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

titanic_data= sns.load_dataset('titanic')
titanic_data.head()

titanic_data= titanic_data[["age","fare","pclass"]]
titanic_data.head()

from sklearn.preprocessing import MinMaxScaler

scaler=MinMaxScaler()
scaler.fit(titanic_data)

titanic_data_scaled= scaler.transform(titanic_data)

titanic_data_scaled= pd.DataFrame(titanic_data_scaled, columns=titanic_data.columns)
titanic_data_scaled.head()

"""# Handling Missing Data

Missing values are those observations that do not contain any value.

Missing values can totally change data patterns, and therefore it is extremely important to understand
why missing values occur in the dataset and how to handle them.

One of the most commonly occuring data types is numeric data, which consists of numbers.

The use of statsitical techniques or algorithms to replace missing values is called as imputation.
"""

titanic_data= sns.load_dataset('titanic')
titanic_data.head()

titanic_data= titanic_data[["survived","pclass","age","fare"]]
titanic_data.head()

titanic_data.isnull().mean()

titanic_data.isnull().sum()

median= titanic_data.age.median()
print(median)

mean=titanic_data.age.mean()
print(mean)

titanic_data['Median_Age']=titanic_data.age.fillna(median)

titanic_data['Mean_Age']=titanic_data.age.fillna(mean)

titanic_data['Mean_Age']=np.round(titanic_data['Mean_Age'],1)

titanic_data.head(20)

"""Frequent Category Imputation

One of the most common ways of handling missing values in a categorical column is to replace the missing values
with the most frequently occuring values, i.e. the mode of the column.
"""

titanic_data= sns.load_dataset('titanic')
titanic_data.head()

titanic_data= titanic_data[["embark_town","age","fare"]]
titanic_data.head()

titanic_data.isnull().sum()

titanic_data.embark_town.value_counts().sort_values(ascending=False).plot.bar()
plt.xlabel('Emabrk Town')
plt.ylabel('Number of Passengers')

titanic_data.embark_town.mode()

titanic_data.embark_town.fillna('Southampton',inplace=True)

titanic_data.isnull().sum()

"""# Categorical Data Encoding

A dataset can contain numerical, categroical, datetime and mixed variables.

A mechanism is needed to convert categorical data to its numeric counterparts so that
the data can be used to build statistical models.

The technique used to convert numeric data into categorical data are called categorical data encoding
schemes.

# One Hot Encoding

One hot encoding is one of the most commonly used categorical encoding schemes.

In one hot encoing, for each unique value in the categorical column, a new column is added. Integer 1 is added
to the column that corresponds to original label, and all the remaining columns are filled with zeros.
"""

titanic_data= sns.load_dataset('titanic')
titanic_data.head()

titanic_data=titanic_data[["sex","class","embark_town"]]
titanic_data.head()

temp= pd.get_dummies(titanic_data['sex'])
temp.head()

pd.concat([titanic_data['sex'],pd.get_dummies(titanic_data['sex'])],axis=1).head()

temp=pd.get_dummies(titanic_data['embark_town'])
temp.head()

"""# Label Encoding

In label encoding, labels are replaced by intergers. This is why label encoding is also called as integer encoding.
"""

from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings("ignore")

le=LabelEncoder()

le.fit(titanic_data['class'])

titanic_data['le_class']=le.transform(titanic_data['class'])

titanic_data.head()

"""# Data Discretization

The process of converting continuous numeric values, such as price, age and weight into discrete intervals
is called as discretization or binning.

Discretization is helpful in cases where you have a skewed distribution of data.

Equal Width Discretization
"""

diamond_data= sns.load_dataset('diamonds')
diamond_data.head()

sns.distplot(diamond_data['price'])

price_range= diamond_data['price'].max()-diamond_data['price'].min()
print(price_range)

price_range/10

lower_interval= int(np.floor(diamond_data['price'].min()))

upper_interval= int(np.ceil(diamond_data['price'].max()))

interval_length= int(np.round(price_range/10))

print(lower_interval)
print(upper_interval)
print(interval_length)

total_bins= [i for i in range(lower_interval, upper_interval+interval_length, interval_length)]
print(total_bins)

bin_labels=['Bin_no_'+str(i) for i in range(1,len(total_bins))]
print(bin_labels)

diamond_data['price_bins']=pd.cut(x=diamond_data['price'], bins=total_bins, labels=bin_labels, include_lowest=True)
diamond_data.head(10)

diamond_data.groupby('price_bins')['price'].count().plot().bar()
plt.xticks(rotation=45)

"""# Handling Outliers

Outliers are the values that are too far from the rest of the observations in the columns.

OUtliers can occur due to various reasons.

# Outlier Trimming

Outlier Trimming refers to simply removing the outliers beyond a certain threshold values.
"""

titanic_data= sns.load_dataset('titanic')
titanic_data.head()

sns.boxplot(y='age',data=titanic_data)

IQR= titanic_data["age"].quantile(0.75)-titanic_data["age"].quantile(0.25)

lower_age_limit= titanic_data["age"].quantile(0.25)-(IQR*1.5)

upper_age_limit=titanic_data["age"].quantile(0.75)+(IQR*1.5)

print(lower_age_limit)
print(upper_age_limit)

age_outliers= np.where(titanic_data["age"]>upper_age_limit,True,
                      np.where(titanic_data["age"]<lower_age_limit,True,False))

age_outliers[:10]

titanic_without_age_outliers= titanic_data.loc[~(age_outliers),]

titanic_data.shape, titanic_without_age_outliers.shape

sns.boxplot(y="age",data=titanic_without_age_outliers)

"""# Feature Selection

Machine Learning algorithms learn from datasets. A dataset consists of features.

A feature refers to single characterisitic or dimension of data. Features are also known as attributes.

For instance, a dataset of cars has features like car model, car color, seating capacity, mileage etc.

Selecting the right set of features not only improves the performance of your machine learning model
but also speed up the training time of your algorithm.

# Feature Selection based on Variance

Features that are very similar should be removed from the dataset. There are various ways to remove
very similar features from the dataset.

One of the ways is to find the variance for a particular feature and remove features having variance less
than a certain threshold.
"""

wine_data= pd.read_csv("winequality-red.csv")
wine_data.head()

"""Dividing data into features and labels"""

features= wine_data.drop(["quality"],axis=1)
labels=wine_data.filter(["quality"],axis=1)

features.var()

from sklearn.feature_selection import VarianceThreshold

var_sel= VarianceThreshold(threshold=(0.1))
var_sel.fit(features)

attributes_to_retain= features.columns[var_sel.get_support()]
attributes_to_retain

attributes_to_filter=[attr for attr in features.columns
                     if attr not in features.columns[var_sel.get_support()]]
attributes_to_filter

filtered_dataset= features.drop(attributes_to_filter,axis=1)
filtered_dataset.head()

"""# Feature Selection based on Correlation"""

correlation_matrix= features.corr()
correlation_matrix

sns.heatmap(correlation_matrix)

correlated_features_matrix=set()
for i in range(len(correlation_matrix.columns)):
    for j in range(i):
        if abs(correlation_matrix.iloc[i,j])>0.6:
            corr_col=correlation_matrix.columns[i]
            correlated_features_matrix.add(corr_col)

len(correlated_features_matrix)

print(correlated_features_matrix)

"""# Machine Learning Concepts

Machine Learning is a branch of Artificial Intelligence that enables computer programs to automatically learn
and imporve from experience.

Supervised Learning and Unsupervised Learning

Supervised Machine Learning algorithms are those algorithms where the input dataset and the corresponding output or true
prediction is available and the algorithms try to find the relationship between inputs and outputs.

Unsupervised Machine Learning algorithms are those where the true labels for the outputs are not known.

Clustering algorithms are a typical of unsupervised learning.

Supervised learning algorithms are further divided into two types: Regression and Classification algorithms.
    
Regression algorithms predict a continuous value. Example Price of a house or car.

Classification algorithms predict a discrete value, such whether the email is Ham/Spam.
"""

import pandas as pd
import numpy as np
import seaborn as sns

sns.get_dataset_names()

tips_df= sns.load_dataset("tips")

tips_df.head()

"""Divide data into features and labels"""

#extracting features
X=tips_df.drop(["tip"],axis=1)

#extracting labels
y=tips_df["tip"]

X.head()

y.head()

"""Converting Categorical Data to Numbers"""

numerical= X.drop(['sex','smoker','day','time'],axis=1)
numerical.head()

categorical= X.filter(['sex','smoker','day','time'])
categorical.head()

# perfroming one-hot encoding
import pandas as pd
cat_numerical=pd.get_dummies(categorical)
cat_numerical.head()

X=pd.concat([numerical, cat_numerical],axis=1)
X.head()

"""Dividing Data into Training and Test Sets

After a Machine Learning algorithm has been trained, it needs to be evaluated to see how well it performs on unseen data.

Therefore, we divide the dataset into two sets i.e. train and test set. The model is trained via the train set and
evaluated on the test set.
"""

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test= train_test_split(X,y,test_size=0.20, random_state=0)

"""Data Scaling/Normalization

It is better to convert all values to a uniform scale.
"""

from sklearn.preprocessing import StandardScaler
sc=StandardScaler()
X_train=sc.fit_transform(X_train)
X_test=sc.transform(X_test)

"""Linear Regression

Linear Regression is a linear model that assumes a linear relationship between inputs and outputs and
minimizes the cost of error between the predicted and actual output using functions like mean absolute error.

Advantages

1. Linear regression is a simple to implement and easily interpretable algorithm.

2. Takes less training time to train, even for huge datasets.

3. Linear regression coefficients are easy to interpret.
"""

from sklearn.linear_model import LinearRegression

lin_reg= LinearRegression()

regressor= lin_reg.fit(X_train, y_train)

y_pred=regressor.predict(X_test)

"""Once you have trained a model and have made predictions on the test set, the next step is to know how well
your model has performed for making predictions on the unknown test set.

Mean Absolute Error(MAE)- Mean Absolute Error(MAE) is calculated by taking the average of absolute error obtained
by subtracting real values from predicted values.

Mean Squared Error(MSE)- It is similar to MAE. However, the error for each record is squared in the case of MSE.

Root Mean Squared Error(RMSE)- It is under the root of MSE
"""

from sklearn import metrics

print('Mean Absolute Error:',metrics.mean_absolute_error(y_test, y_pred))

print('Mean Squared Error:',metrics.mean_squared_error(y_test, y_pred))

print('Root Mean Squared Error:',np.sqrt(metrics.mean_squared_error(y_test,y_pred)))

"""By looking at the Mean Absolute Error, it can be concluded that on average there is an error of 0.70 for prediction,
which means that ion average the predicted tip values are 0.70$ more or less than the actual tip values.

# Random Forest Regression

Random Forest is a tree-based algorithm that converts features in to tree nodes and then uses entropy loss to make
prediction.

Advantages

1. It is useful when you have lots of missing data or an imbalanced data.

2. With a large number of trees, you can avoid overfitting while training. Overfitting occurs
when the machine learning models perform better on the training set but worse on the test set.

3. Through cross-validation, the random forest can return higher accuracy.
"""

from sklearn.ensemble import RandomForestRegressor

rf_reg=RandomForestRegressor(random_state=42, n_estimators=500)

regressor= rf_reg.fit(X_train, y_train)
y_pred=regressor.predict(X_test)

from sklearn import metrics

print('Mean Absolute Error:',metrics.mean_absolute_error(y_test, y_pred))

print('Mean Squared Error:',metrics.mean_squared_error(y_test, y_pred))

print('Root Mean Squared Error:',np.sqrt(metrics.mean_squared_error(y_test,y_pred)))

"""# Classification

Classification problems are the type of problems where you have to predict a discrete value (0 or 1)
e.g whether email is spam/ham
"""

import pandas as pd
import numpy as np

churn_df=pd.read_csv("Churn_Modelling.csv")
churn_df.head()

"""This dataset contains records of customers who left the bank six months after various information about them
is recorded.
"""

churn_df=churn_df.drop(['RowNumber','CustomerId','Surname'],axis=1)
churn_df.head()

"""Dividing Data into Features and Labels"""

X=churn_df.drop(['Exited'],axis=1)
y=churn_df['Exited']

X.head()

y.head()

"""Converting Categorical Data to Numbers"""

numerical=X.drop(['Geography','Gender'],axis=1)
numerical.head()

categorical=X.filter(['Geography','Gender'])
categorical.head()

import pandas as pd

cat_numerical=pd.get_dummies(categorical)
cat_numerical.head()

X= pd.concat([numerical, cat_numerical],axis=1)
X.head()

"""Dividing data into Training and Test sets"""

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test= train_test_split(X,y,test_size=0.20, random_state=0)

"""Data Scaling/Normalization"""

from sklearn.preprocessing import StandardScaler

sc=StandardScaler()
X_train=sc.fit_transform(X_train)
X_test=sc.transform(X_test)

"""Logistic Regression

Logistic Regression is a linear model, which makes classification by passing the output of linear regression
through a sigmoid function.
"""

from sklearn.linear_model import LogisticRegression

log_clf=LogisticRegression()

classifier=log_clf.fit(X_train, y_train)

y_pred=classifier.predict(X_test)

"""There are various metrics to evaluate a classification model. Some of the most commonly used classification
metircs are F1 score, precision, recall, accuracy and confusion matrix.

True Negatives: (TN/tn)- True Negatives are those output labels that are actually false and model also predicted them
as False

True Positive: True positives are those labels that are actually true and also predicted as True by the model.
    
False negative: False negatives are labels that are actually true but predicted as false by the machine learning
model.

False Positive: Labels that are actually false but predicted as true by the model are called false positive.

Confusion Matrix

Precision- It is obtained by dividing true positives by the sum of true positive and false positive.

Precision= tp/(tp+fp)

Recall- Recall is calculated by dividing true positives by the sum of true positive and false negative.

Recall= tp/(tp+fn)

F1- measure- F1 measure is simply the harmonic mean of precision and recall.

Accuracy- It refers to the number of correctly predicted labels divided by the total number of observations in a
dataset.

Accuracy= (tp+tn)/(tp+tn+fp+fn)
"""

# evaluating the model performance

from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

print(confusion_matrix(y_test,y_pred))
print("-"*50)
print(classification_report(y_test, y_pred))
print("-"*50)
print(accuracy_score(y_test, y_pred))

"""The output shows that for 81 percent of the records in the test set, logistic regression correctly predicted
whether or not a customer will leave the bank.
"""

