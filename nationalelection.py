# -*- coding: utf-8 -*-
"""NationalElection.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ii5vYmeaW812XGic8XTvvATopHqH4sd3

**India Nation Election** form 1977, 1980, 1984, 1989, 1991, 1996, 1998, 1999, 2004, 2009, 2014
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('/content/indian-national-level-election.csv')

"""st_name : State  --
Year : General election year --
pc_no : Parliamentary constituency number --
pc_name : Parliamentary constituency name --
pc_type : Parliamentary constituency reservation status --
cand_name : Candidate name --
cand_sex : Candidate sex --
partyname:  Party name --
partyabbre : Party abbreviation --
totvotpoll :  Votes received --
electors : Number of registered voters
"""

df.head()

df.info()

df.isna().sum()

df['pc_type'].value_counts()

df['pc_type'].replace({'SC ':'SC'}, inplace=True)

df['pc_type'] = df['pc_type'].fillna('GEN')

sns.set_theme()
sns.countplot(x='pc_type', data = df)
plt.title('Parliamentary constituency reservation status')

plt.figure(dpi=300)
df['pc_type'].value_counts().plot(kind='pie', autopct='%2.0f%%')
plt.title('Parliamentary constituency reservation status distribution')
plt.show()

df['cand_sex'] = df['cand_sex'].fillna('M')

sns.countplot(x='cand_sex', data=df)
plt.title('Candidate sex')

df.isna().sum()

df['partyname'].value_counts()

df['st_name'].replace({'Chattisgarh':'Chhattisgarh', 'Orissa':'Odisha', 'Pondicherry':'Puducherry' }, inplace=True)
df['st_name'].replace({'National Capital Territory Of Delhi':'Delhi','Nct Of Delhi':'Delhi'}, inplace=True)
df['st_name'].replace({'Goa Daman & Diu': 'Daman & Diu','Goa, Daman & Diu':'Daman & Diu'},inplace=True)

"""# Independents and IND denotes Independent canditate"""

df['partyname'].replace({'Independents':'Independent', 'IND':'Independent'}, inplace=True)

df['partyname'].replace({'INC':'Indian National Congress'}, inplace=True)
df['partyname'].replace({'BJP':'Bharatiya Janata Party'}, inplace=True)
df['partyname'].replace({'BSP':'Bahujan Samaj Party'}, inplace=True)

plt.figure(dpi=300, figsize=(10,8))
party_count = df['partyname'].value_counts().head(9)
party_count.plot.pie(autopct='%2.0f%%')
plt.show()

stateName_pollCount = df.groupby(df['st_name'])['totvotpoll'].sum()
plt.figure(dpi=300, figsize=(10,8))
stateName_pollCount.plot(kind='bar')
plt.xticks(rotation=90)
plt.title('Total votes polled over state of India')
plt.xlabel('State')
plt.ylabel('Votes polled')
plt.show()

year_pollCount = df.groupby('year')['electors'].sum().reset_index() #.reset_index(): Converts the groupby result back into a DataFrame and resets the index.
year_pollCount.columns = ['year', 'electors']  # Renaming the columns if needed

plt.figure(dpi=300, figsize=(10,8))
plt.plot(year_pollCount['year'], year_pollCount['electors'],marker='o',markerfacecolor='red')
plt.title('Total voter')
plt.xlabel('Years')
plt.ylabel('Votes polled')
plt.grid(axis='both')
plt.show()

year_pollCount = df.groupby('year')['totvotpoll'].sum().reset_index() #.reset_index(): Converts the groupby result back into a DataFrame and resets the index.
year_pollCount.columns = ['year', 'pollcount']  # Renaming the columns if needed

plt.figure(dpi=300, figsize=(10,8))
plt.plot(year_pollCount['year'], year_pollCount['pollcount'],marker='o',markerfacecolor='red')
plt.title('Votes polled over the year in Lok Sabha election')
plt.xlabel('Years')
plt.ylabel('Votes polled')
plt.grid(axis='both')
plt.show()

total_voter = df.groupby('st_name')['electors'].sum().reset_index()
polled_vote = df.groupby('st_name')['totvotpoll'].sum().reset_index()


plt.figure(dpi=300, figsize=(10,8))
plt.barh(total_voter['st_name'], total_voter['electors'], label='Total voter')
plt.barh(polled_vote['st_name'],polled_vote['totvotpoll'], label='Polled voter')
plt.legend()
plt.show()

year = df['year'].unique()
male = df[df['cand_sex'] == 'M']['year'].value_counts().sort_index(ascending=True)
female = df[df['cand_sex'] == 'F']['year'].value_counts().sort_index(ascending=True)

x_axis = np.arange(len(year))

plt.figure(dpi=300, figsize=(10,8))
plt.xticks(x_axis, year)
plt.bar(x_axis - 0.2, male,0.4, label='Male')
plt.bar(x_axis + 0.2, female,0.4, label='Female')
plt.title('Male & Female Candidate')
plt.xlabel("Year")
plt.ylabel("Number of Candidates")
plt.legend()
plt.show()

c = df[df['partyname'] == 'IND']
d = df.groupby(df['partyname'] == 'IND')['st_name']
#z = list(filter(lambda x: x == 'Tamil Nadu', d))
'''
for group_name, group_data in d:
    print(group_name)
    print(group_data)
    print()
'''
l = df[(df['partyname'] == 'IND') & (df['st_name'] == 'Tamil Nadu')]['cand_name']
l.head()

i = df[df['st_name'] == 'Tamil Nadu']['pc_name'].unique()

print(len(i), ' ' ,i)

i = df[df['st_name'] == 'Tamil Nadu']['pc_name']
i

#df.drop('Poll_Percentage', axis=1, inplace=True)
pc = df.groupby('st_name')['pc_name']
pc.first()

data = df.groupby(['year', 'pc_name'])['totvotpoll']
data.groups

df['winner'] = df.groupby(['year', 'pc_name'])['totvotpoll'].transform(lambda x: x == x.max()).astype(int)

sns.barplot(x='cand_sex', y='winner',hue='pc_type', data=df)

df.head()

sns.countplot(x='winner', data=df)

"""Encoding st_name, pc_name, partyabbre

OneHotEncoder
"""

X = df[['st_name', 'pc_name', 'partyabbre', 'totvotpoll','electors']]
y = df['winner']
X

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

ct = ColumnTransformer(transformers = [('encoder', OneHotEncoder(),[0, 1, 2])],remainder='passthrough')
X_transformed = ct.fit_transform(X)

X_transformed = X_transformed.toarray()

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test = train_test_split(X_transformed, y, test_size=0.2, random_state=0)

from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression()
classifier.fit(x_train, y_train)

y_pred = classifier.predict(x_test)

print(y_pred)

train_score = classifier.score(x_train,y_train)

test_score = classifier.score(x_test,y_test)

plt.figure(dpi=300,figsize=(8,6))
accuracy_data = {'Train Accuracy':train_score, 'Test Accuracy':test_score}
plt.bar(accuracy_data.keys(), accuracy_data.values(), color=['blue', 'orange'])
plt.title('Accuracy Score')
plt.ylabel('Score')
plt.show()

"""# confusion matrix"""

from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

acc = (sum(np.diag(cm)))/len(y_test)
acc

"""# K-fold cross validation"""

# New data
new_data = pd.DataFrame({
    'st_name': ['Tamil Nadu'],
    'pc_name': ['Salem'],
    'partyabbre': ['INC'],
    'totvotpoll': [254138],
    'electors': [677947]
})

# Transform the new data using the same ColumnTransformer
new_data_transformed = ct.transform(new_data)

# Predict using the classifier
prediction = classifier.predict(new_data_transformed)

print("Predicted Winner:", prediction)

value = df[(df['st_name']=='Tamil Nadu') & (df['pc_name']=='Salem')]
value.head(50)

from sklearn.model_selection import StratifiedKFold,cross_val_score

kfold = StratifiedKFold(n_splits=50, shuffle=True, random_state=0)

accuracies = cross_val_score(estimator = classifier, X=X_transformed, y=y, cv=kfold, scoring='r2')

