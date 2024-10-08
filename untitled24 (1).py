import numpy as np
import pandas as pd
df = pd.read_csv('/content/drive/MyDrive/Datasets/heart_2020_cleaned.csv')
pd.set_option('display.max_columns', None)
df

df.head()

df.tail()

df.sample(15)

df.shape

df.info()

df.describe().style.background_gradient(cmap='bone').set_properties(**{'font-size': '12pt', 'font-family': 'Calibri'})

df.describe(include=[object, 'float64']).T.style.set_properties(**{'background-color': '#f4f4f9', 'font-size': '14px'})

import pandas as pd

# Assuming df is your DataFrame
styled_df = df.describe(include='all').T.style.set_properties(**{'background-color': '#f4f4f9', 'font-size': '14px'})

# To display the styled DataFrame
styled_df

df.duplicated().sum()

total_duplicates = df.duplicated().sum()
percentage_duplicates = round((total_duplicates / df.shape[0]) * 100, 2)
print(f"Total duplicates: {total_duplicates}, Percentage: {percentage_duplicates}%")

df.drop_duplicates(inplace = True)
total_duplicates = df.duplicated().sum()
percentage_duplicates = round((total_duplicates / df.shape[0]) * 100, 2)
print(f"Total duplicates: {total_duplicates}, Percentage: {percentage_duplicates}%")

import missingno as msno
import matplotlib.pyplot as plt

msno.bar(df, figsize=(12, 6), color=(0.24, 0.5, 0.6), fontsize=12, labels=True)
plt.show()

import missingno as msno
import matplotlib.pyplot as plt

msno.bar(df, figsize=(12, 6), color='skyblue', fontsize=12, sort='ascending')

plt.title('Completeness of Data in Each Column', fontsize=14)  # Increased title font size
plt.xlabel('Columns', fontsize=12)  # Added x-axis label for clarity
plt.ylabel('Number of Non-Missing Values', fontsize=12)  # Added y-axis label
plt.show()

for i in df.columns:
    if df[i].dtype == 'object':
        print(f"Column: {i}")  # Clearly indicates which column's data is being printed
        print(df[i].value_counts(dropna=False))  # Includes counts of all values, including NaNs
        print('*' * 40)

mappings = {
    'Sex': {'Female': 0, 'Male': 1},
    'GenHealth': {'Poor': 1, 'Fair': 2, 'Good': 3, 'Very good': 4, 'Excellent': 5},
    'PhysicalActivity': {'No': 0, 'Yes': 1},
    'Stroke': {'No': 0, 'Yes': 1},
    'Asthma': {'No': 0, 'Yes': 1},
    'SkinCancer': {'No': 0, 'Yes': 1},
    'Diabetic': {'No': 0, 'No, borderline diabetes': 1, 'Yes (during pregnancy)': 2, 'Yes': 3},
    'AlcoholDrinking': {'No': 0, 'Yes': 1},
    'AgeCategory': {
        '18-24': 0, '25-29': 1, '30-34': 2, '35-39': 3, '40-44': 4,
        '45-49': 5, '50-54': 6, '55-59': 7, '60-64': 8, '65-69': 9,
        '70-74': 10, '75-79': 11, '80 or older': 12
    },
    'KidneyDisease': {'No': 0, 'Yes': 1},
    'Smoking': {'No': 0, 'Yes': 1},
    'DiffWalking': {'No': 0, 'Yes': 1},
    'Race' : {'White' : 0, 'Black' : 1, 'Asian': 2, 'American Indian/Alaskan Native': 3, 'Other': 4, 'Hispanic': 5},
    'HeartDisease' : {'No' : 0, 'Yes' : 1},
    'Race' : {'White' : 0, 'Black' : 1, 'Asian': 2, 'American Indian/Alaskan Native': 3, 'Other': 4, 'Hispanic': 5}
}

# Applying the mappings to the dataframe
for col, mapping in mappings.items():
    df[col] = df[col].map(mapping)

df.head(5)

import pandas as pd

def find_outliers(col):
    Q1 = col.quantile(0.25)
    Q3 = col.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return col[(col < lower_bound) | (col > upper_bound)]

outliers = {}
for column in df.select_dtypes(include=['number']).columns:
    outliers_in_column = find_outliers(df[column])
    if not outliers_in_column.empty:
        outliers[column] = outliers_in_column

for column, outlier_values in outliers.items():
    print(f"Outliers in {column}:")
    print(outlier_values)
    print("*" * 40)

ax = df.plot(kind='box', figsize=(15, 15), subplots=True, layout=(5, 5))

# Improve the spacing between the plots
plt.tight_layout()

# Display the plot
plt.show()

import seaborn as sns

# Create a larger figure to accommodate the dimensions of the heatmap
plt.figure(figsize=(15, 15))

# Generate a heatmap for the correlation matrix
corr_matrix = df.corr()
sns.heatmap(corr_matrix, annot=True, cmap='inferno', fmt=".2f")

# Show the plot
plt.show()

df.dropna(inplace=True)
df.dropna(subset=['HeartDisease'], inplace=True)
df.shape

from sklearn.model_selection import train_test_split
from sklearn.feature_selection import mutual_info_classif
from sklearn.feature_selection import SelectKBest

X_df = df.drop(['HeartDisease'], axis=1)
X = X_df.values
y = df['HeartDisease'].values

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=42)
print(x_train.shape)

mi = mutual_info_classif(X, y)

k = 10
selector = SelectKBest(mutual_info_classif, k=k)
X_new = selector.fit_transform(X, y)

selected_features = X_df.columns[selector.get_support()]
print(selected_features)

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.bar(X_df.columns, mi)
plt.xticks(rotation=90)
plt.xlabel('Features')
plt.ylabel('Mutual Information Score')
plt.title('Mutual Information Scores for Features')
plt.tight_layout()
plt.show()

plt.figure(figsize=(5,5))

HeartDisease_rate = pd.Series(y_train).value_counts()

plt.pie(HeartDisease_rate.values, labels= HeartDisease_rate.index, autopct="%.1f%%",
        wedgeprops=dict(width=0.45, edgecolor='w'), shadow = True, explode = [0, 0.1], )
plt.title("HeartDisease Rate", fontsize = 18, weight='bold')

plt.show();

plt.figure(figsize=(5,5))
plt.title("Gender Distribution", fontsize = 18, weight='bold')

# Assuming 'df' is your DataFrame and 'Sex' is the column for gender
gender_count = df['Sex'].value_counts()  # Calculate gender counts

plt.pie(gender_count,labels=gender_count.index,radius=1, autopct='%.2f%%',
       wedgeprops=dict(width=0.45, edgecolor='w'), shadow = True, explode = [0, 0.1])

plt.show()

plt.figure(figsize=(6, 6))

ax = sns.countplot(data=df, x='HeartDisease', hue='Sex')

ax.set_title("HeartDisease Among Different Genders", fontsize=16,  weight='bold')
ax.set_xlabel("Had Heart Disease", fontsize=14)
ax.set_ylabel("count", fontsize=14)

for c in ax.containers:
    ax.bar_label(c)

plt.show()

def plot_pie_chart(data, column, title, explode=[0, 0.1], figsize=(5, 5)):
    plt.figure(figsize=figsize)
    values = data[column].value_counts()
    plt.pie(values.values, labels=values.index, autopct="%.1f%%",
            wedgeprops=dict(width=0.45, edgecolor='w'), shadow=True, explode=explode)
    plt.title(title, fontsize=18, weight='bold')
    plt.show()

def plot_countplot(data, x, hue, title, xlabel, ylabel, figsize=(6, 6)):
    plt.figure(figsize=figsize)
    ax = sns.countplot(data=data, x=x, hue=hue)
    ax.set_title(title, fontsize=16, weight='bold')
    ax.set_xlabel(xlabel, fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    for c in ax.containers:
        ax.bar_label(c)
    plt.show()

plot_pie_chart(df, 'HeartDisease', "HeartDisease Rate")
plot_countplot(df, 'HeartDisease', 'Sex', "HeartDisease Among Different Genders", "Had Heart Disease", "Count")

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(16, 16), dpi=120)
risk_factors = ['PhysicalActivity', 'Smoking']

sns.set_style("whitegrid")

for i, risk_factor in enumerate(risk_factors, 1):
    plt.subplot(2, 1, i)
    x = sns.countplot(data=df, x=risk_factor, hue='Sex', palette="Set2")
    plt.title(f"{risk_factor} Among Different Genders", fontsize=16, weight='bold')
    plt.xlabel(risk_factor, fontsize=16)
    plt.ylabel("Individuals", fontsize=16)
    plt.xticks(size=10, rotation=25, horizontalalignment='right', fontweight='light')
    for c in x.containers:
        x.bar_label(c)

plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(14, 6))
sns.set_style("darkgrid")

age_counts = df['AgeCategory'].value_counts().sort_index()

plt.bar(age_counts.index, age_counts.values, color='skyblue')

plt.title('Distribution of Age Category', fontsize=16, weight='bold')
plt.xlabel('Age Category', fontsize=14)
plt.ylabel('Count', fontsize=14)
plt.xticks(rotation=0)

for i, count in enumerate(age_counts.values):
    plt.text(i, count, str(count), ha='center', va='bottom')

plt.tight_layout()
plt.show()

plt.figure(figsize=(13, 25))
risk_factors = ['PhysicalActivity' ,'Smoking','AlcoholDrinking']

sns.set_style("ticks")

for i, risk_factor in enumerate(risk_factors, 1):
    plt.subplot(5, 1, i)
    x = sns.countplot(data=df, x='AgeCategory', hue=risk_factor,
                     order = df['AgeCategory'].value_counts().sort_index().index.values)
    plt.title(f"{risk_factor} Among Different Age Groups", fontsize=16, weight='bold')
    plt.xlabel("Age Category", fontsize=14)
    plt.ylabel("Individuals", fontsize=14)
    for c in x.containers:
        x.bar_label(c)
plt.tight_layout()

plt.show()

HeartDisease_rate = df["Diabetic"].value_counts()

# Set the style to 'whitegrid'
sns.set_style("whitegrid")

# Create a bar plot
ax = sns.barplot(x=HeartDisease_rate.index, y=HeartDisease_rate.values)

# Add labels to the bars
for p in ax.patches:
    height = p.get_height()
    ax.text(p.get_x() + p.get_width() / 2., height + 0.05, f'{int(height)}', ha="center")

plt.title("Diabetic Distribution")
plt.xlabel("Diabetes (0 = No, 3 = Yes, No, borderline diabetes =  1, Yes (during pregnancy) = 2)")
plt.ylabel("Count")
plt.show();

x_train_new = selector.transform(x_train)
x_test_new = selector.transform(x_test)

x_train_select_df = pd.DataFrame(x_train_new, columns=selected_features)
x_test_select_df = pd.DataFrame(x_test_new, columns=selected_features)

from sklearn.tree import DecisionTreeClassifier
dt = DecisionTreeClassifier(max_depth = 4 , max_features = 9 )
dt.fit(x_train_new , y_train)

dt.score(x_train_new , y_train)

dt.score(x_test_new , y_test)

from matplotlib import pyplot as plt

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.figure(figsize=(10, 0.5 * top))
    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('Feature Importances')
    plt.xlabel('Importance Score')
    plt.ylabel('Features')
    plt.show()

features_names = x_train_select_df.columns
f_importances(abs(dt.feature_importances_), features_names, top=6)

y_pre_dt = dt.predict(x_test_new)
y_pre_dt

from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=8 , max_depth = 4 , max_features = 11)
rf.fit(x_train_new , y_train)

rf.score(x_train_new , y_train)

rf.score(x_test_new , y_test)

from matplotlib import pyplot as plt

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.figure(figsize=(10, 0.5 * top))
    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('Feature Importances')
    plt.xlabel('Importance Score')
    plt.ylabel('Features')
    plt.show()

features_names = x_train_select_df.columns
f_importances(abs(rf.feature_importances_), features_names, top=6)

y_pre_rf = rf.predict(x_test_new)
y_pre_rf

import xgboost as xgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

dtrain = xgb.DMatrix(x_train_new, label=y_train)
dtest = xgb.DMatrix(x_test_new, label=y_test)


param = {
    'max_depth': 4,
    'learning_rate': 0.1,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'reg_alpha': 0.1,
    'reg_lambda': 1.0,
    'objective': 'binary:logistic',  # Assuming binary classification
    'eval_metric': 'logloss',  # Or other suitable metric
    'seed': 42
}


watchlist = [(dtrain, 'train'), (dtest, 'eval')]


num_round = 1000  # Maximum number of boosting rounds
early_stopping_rounds = 10
bst = xgb.train(param, dtrain, num_round, watchlist, early_stopping_rounds=early_stopping_rounds, verbose_eval=True)

y_pred = bst.predict(dtest)

y_pred_binary = [1 if p >= 0.5 else 0 for p in y_pred]

y_pred_train = bst.predict(xgb.DMatrix(x_train_new))
y_pred_train_binary = [1 if p >= 0.5 else 0 for p in y_pred_train]

# Calculating accuracy on training data
accuracy = accuracy_score(y_train, y_pred_train_binary)
print("Training Accuracy:", accuracy)

y_pred_test = bst.predict(xgb.DMatrix(x_test_new))
y_pred_test_binary = [1 if p >= 0.5 else 0 for p in y_pred_test]

accuracy = accuracy_score(y_test, y_pred_test_binary)
print("Test Accuracy:", accuracy)

from matplotlib import pyplot as plt

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.figure(figsize=(10, 0.5 * top))
    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('Feature Importances')
    plt.xlabel('Importance Score')
    plt.ylabel('Features')
    plt.show()

features_names = x_train_select_df.columns

importance_scores = bst.get_score(importance_type='gain')

importance_list = [importance_scores.get(str(i), 0) for i in range(len(features_names))]

f_importances(importance_list, features_names, top=6)

y_pred_bst = bst.predict(xgb.DMatrix(x_test_new))
y_pred_bst

from sklearn.metrics import confusion_matrix
import seaborn as sns

con_dt = confusion_matrix(y_test, y_pre_dt)
con_rf = confusion_matrix(y_test, y_pre_rf)
y_pred_bst_binary = [1 if p >= 0.5 else 0 for p in y_pred_bst]

con_bst = confusion_matrix(y_test, y_pred_bst_binary)

fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(21,7))

sns.heatmap(con_dt,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax1 , cmap = 'Blues')
ax1.set_ylabel('Prediction',fontsize=13)
ax1.set_xlabel('Actual',fontsize=13)
ax1.set_title('Decision Tree',fontsize=17)


sns.heatmap(con_rf,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax2 , cmap = 'YlOrBr')
ax2.set_ylabel('Prediction',fontsize=13)
ax2.set_xlabel('Actual',fontsize=13)
ax2.set_title('Random Forest',fontsize=17)

sns.heatmap(con_bst,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax3 , cmap = 'Greens')
ax3.set_ylabel('Prediction',fontsize=13)
ax3.set_xlabel('Actual',fontsize=13)
ax3.set_title('XGBoost',fontsize=17)
plt.show()

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


y_pred_bst_binary = [1 if p >= 0.5 else 0 for p in y_pred_bst]


ls_scores = np.array([accuracy_score(y_test , y_pre_dt),
                       accuracy_score(y_test , y_pre_rf),
                       accuracy_score(y_test, y_pred_bst_binary), # Use binary predictions
                       precision_score(y_test , y_pre_dt), # Use binary predictions
                       precision_score(y_test , y_pre_rf),
                       precision_score(y_test , y_pred_bst_binary), # Use binary predictions
                       recall_score(y_test , y_pre_dt),
                       recall_score(y_test , y_pre_rf),
                       recall_score(y_test , y_pred_bst_binary), # Use binary predictions
                       f1_score(y_test , y_pre_dt),
                       f1_score(y_test , y_pre_rf),
                       f1_score(y_test , y_pred_bst_binary)]) # Use binary predictions

index1 = ['Accuracy' , 'Precision' , 'Recall' , 'F1-score']
cols1 = ['Decision Tree' , 'Random Forest', 'XGBClassifier']
eval = pd.DataFrame(ls_scores.reshape(4,3) , columns = cols1 , index = index1)
eval

from matplotlib import pyplot as plt

eval['Decision Tree'].plot(kind='line', figsize=(8, 4), title='Decision Tree')
plt.gca().spines[['top', 'right']].set_visible(False)

eval['Random Forest'].plot(kind='line', figsize=(8, 4), title='Random Forest')
plt.gca().spines[['top', 'right']].set_visible(False)

eval['XGBClassifier'].plot(kind='line', figsize=(8, 4), title='XGBClassifier')
plt.gca().spines[['top', 'right']].set_visible(False)

plt.figure(figsize=(14, 10))  # Set the figure size

# Plot Accuracy
plt.subplot(2, 2, 1)
plt.bar(eval.columns, eval.loc['Accuracy'], color=['skyblue', 'lightgreen', 'salmon'])
plt.title('Comparison of Accuracy')
plt.ylabel('Accuracy')
plt.ylim(0, 1)  # Assuming the metric is between 0 and 1
plt.xticks(rotation=45)

# Plot Precision
plt.subplot(2, 2, 2)
plt.bar(eval.columns, eval.loc['Precision'], color=['skyblue', 'lightgreen', 'salmon'])
plt.title('Comparison of Precision')
plt.ylabel('Precision')
plt.ylim(0, 1)
plt.xticks(rotation=45)

# Plot Recall
plt.subplot(2, 2, 3)
plt.bar(eval.columns, eval.loc['Recall'], color=['skyblue', 'lightgreen', 'salmon'])
plt.title('Comparison of Recall')
plt.ylabel('Recall')
plt.ylim(0, 1)
plt.xticks(rotation=45)

# Plot F1-score
plt.subplot(2, 2, 4)
plt.bar(eval.columns, eval.loc['F1-score'], color=['skyblue', 'lightgreen', 'salmon'])
plt.title('Comparison of F1-score')
plt.ylabel('F1-score')
plt.ylim(0, 1)
plt.xticks(rotation=45)

plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint

param_dist = {
    'max_depth': randint(3, 15),
    'max_features': randint(5, x_train.shape[1])
}

random_search = RandomizedSearchCV(estimator=DecisionTreeClassifier(),
                                   param_distributions=param_dist,
                                   n_iter=10,
                                   cv=5)

random_search.fit(x_train_new, y_train)

print("Best Parameters:", random_search.best_params_)

best_dt_model = random_search.best_estimator_

best_dt_model = DecisionTreeClassifier(max_depth=6, max_features=16)
best_dt_model.fit(x_train_new, y_train)

best_dt_model.score(x_train_new , y_train)

best_dt_model.score(x_test_new , y_test)

from matplotlib import pyplot as plt

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.figure(figsize=(10, 0.5 * top))
    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('Feature Importances')
    plt.xlabel('Importance Score')
    plt.ylabel('Features')
    plt.show()

features_names = x_train_select_df.columns
f_importances(abs(best_dt_model.feature_importances_), features_names, top=6)

y_pre_best_dt_model = dt.predict(x_test_new)
y_pre_best_dt_model

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint

param_dist = {
    'n_estimators': randint(50, 200),
    'max_depth': randint(3, 15),
    'max_features': ['auto', 'sqrt', 'log2'],
    'min_samples_split': randint(2, 10),
    'min_samples_leaf': randint(1, 5),
    'bootstrap': [True, False]
}

random_search_rf = RandomizedSearchCV(estimator=RandomForestClassifier(),
                                   param_distributions=param_dist,
                                   n_iter=10,
                                   cv=5,
                                   n_jobs=-1,
                                   verbose=2,
                                   random_state=42)

random_search_rf.fit(x_train_new, y_train)

print("Best Parameters for Random Forest:", random_search_rf.best_params_)

best_rf_model = random_search_rf.best_estimator_

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score

best_rf_model = RandomForestClassifier(bootstrap=False,
                                       max_depth=7,
                                       max_features='sqrt',
                                       min_samples_leaf=4,
                                       min_samples_split=5,
                                       n_estimators=87,
                                       random_state=42)

# Fit the model to the training data
best_rf_model.fit(x_train_new, y_train)

# Make predictions on the test set
y_pred_rf = best_rf_model.predict(x_test_new)

from matplotlib import pyplot as plt

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.figure(figsize=(10, 0.5 * top))
    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('Feature Importances')
    plt.xlabel('Importance Score')
    plt.ylabel('Features')
    plt.show()

features_names = x_train_select_df.columns
f_importances(abs(best_rf_model.feature_importances_), features_names, top=6)

y_pre_best_rf_model = dt.predict(x_test_new)
y_pre_best_rf_model

import xgboost as xgb
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

param_dist = {
    'n_estimators': randint(50, 200),
    'learning_rate': uniform(0.01, 0.3),
    'max_depth': randint(3, 10),
    'subsample': uniform(0.6, 0.4),
    'colsample_bytree': uniform(0.6, 0.4),
    'gamma': uniform(0, 10),
    'reg_alpha': uniform(0, 1),
    'reg_lambda': uniform(0, 1)
}

random_search_xgb = RandomizedSearchCV(estimator=xgb.XGBClassifier(objective='binary:logistic'),
                                   param_distributions=param_dist,
                                   n_iter=10,
                                   cv=5,
                                   n_jobs=-1,
                                   verbose=2,
                                   random_state=42)

random_search_xgb.fit(x_train_new, y_train)

print("Best Parameters for XGBoost:", random_search_xgb.best_params_)

best_xgb_model = random_search_xgb.best_estimator_

import xgboost as xgb
from sklearn.metrics import accuracy_score, precision_score, recall_score

best_xgb_model = xgb.XGBClassifier(objective='binary:logistic',
                                   colsample_bytree=0.8650089137415928,
                                   gamma=3.1171107608941098,
                                   learning_rate=0.16602040635334325,
                                   max_depth=4,
                                   n_estimators=53,
                                   reg_alpha=0.18485445552552704,
                                   reg_lambda=0.9695846277645586,
                                   subsample=0.9100531293444458,
                                   random_state=42)  # Set random state for reproducibility

# Fit the model to the training data
best_xgb_model.fit(x_train_new, y_train)

# Make predictions on the test set
y_pred_xgb = best_xgb_model.predict(x_test_new)

from matplotlib import pyplot as plt

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.figure(figsize=(10, 0.5 * top))
    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('Feature Importances')
    plt.xlabel('Importance Score')
    plt.ylabel('Features')
    plt.show()

features_names = x_train_select_df.columns

f_importances(abs(best_xgb_model.feature_importances_), features_names, top=6)

y_pre_best_xgb_model = dt.predict(x_test_new)
y_pre_best_xgb_model

from sklearn.metrics import confusion_matrix
import seaborn as sns

con_best_dt_model = confusion_matrix(y_test, y_pre_best_dt_model)
con_best_rf_model = confusion_matrix(y_test, y_pre_best_rf_model)
y_pred_bst_binary = [1 if p >= 0.5 else 0 for p in y_pred_bst]

con_best_xgb_model = confusion_matrix(y_test, y_pre_best_xgb_model)

fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(21,7))

sns.heatmap(con_best_dt_model,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax1 , cmap = 'Blues')
ax1.set_ylabel('Prediction',fontsize=13)
ax1.set_xlabel('Actual',fontsize=13)
ax1.set_title('Decision Tree',fontsize=17)


sns.heatmap(con_best_rf_model,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax2 , cmap = 'YlOrBr')
ax2.set_ylabel('Prediction',fontsize=13)
ax2.set_xlabel('Actual',fontsize=13)
ax2.set_title('Random Forest',fontsize=17)

sns.heatmap(con_best_xgb_model,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax3 , cmap = 'Greens')
ax3.set_ylabel('Prediction',fontsize=13)
ax3.set_xlabel('Actual',fontsize=13)
ax3.set_title('XGBoost',fontsize=17)
plt.show()

y_pred_bst_binary = [1 if p >= 0.5 else 0 for p in y_pred_bst]


ls_scores = np.array([accuracy_score(y_test , y_pre_best_dt_model),
                       accuracy_score(y_test , y_pre_best_rf_model),
                       accuracy_score(y_test, y_pre_best_xgb_model),
                       precision_score(y_test , y_pre_best_dt_model),
                       precision_score(y_test , y_pre_best_rf_model),
                       precision_score(y_test , y_pre_best_xgb_model),
                       recall_score(y_test , y_pre_best_dt_model),
                       recall_score(y_test , y_pre_best_rf_model),
                       recall_score(y_test , y_pre_best_xgb_model),
                       f1_score(y_test , y_pre_best_dt_model),
                       f1_score(y_test , y_pre_best_rf_model),
                       f1_score(y_test , y_pre_best_xgb_model)])

index1 = ['Accuracy' , 'Precision' , 'Recall' , 'F1-score']
cols1 = ['Decision Tree' , 'Random Forest', 'XGBClassifier']
eval = pd.DataFrame(ls_scores.reshape(4,3) , columns = cols1 , index = index1)
eval

from sklearn.utils import resample
df_majority = df[df['HeartDisease'] == 0]
df_minority = df[df['HeartDisease'] == 1]

df_majority_downsampled = resample(df_majority,
                                 replace=False,
                                 n_samples=len(df_minority),
                                 random_state=1234)

df1 = pd.concat([df_majority_downsampled, df_minority])

df1['HeartDisease'].value_counts()

plt.figure(figsize = (8,5))
sns.countplot(data = df1 , x= 'HeartDisease')
plt.title('After Under Sampling')

X_2 = df1.drop(['HeartDisease'] , axis = 1).values
y_2 = df1['HeartDisease'].values
x_train_new , x_test_new , y_train , y_test = train_test_split(X_2,y_2,test_size = 0.30 , random_state=42)

dt2= DecisionTreeClassifier(max_depth = 6 , max_features = 9 )

dt2.fit(x_train_new , y_train)

dt2.score(x_train_new , y_train)

dt2.score(x_test_new , y_test)

from matplotlib import pyplot as plt

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('feature importances')
    plt.show()

features_names = x_train_select_df.columns
f_importances(abs(dt2.feature_importances_), features_names, top=6)

y_pre_dt2 = dt2.predict(x_test_new)
y_pre_dt2

from sklearn.impute import SimpleImputer
# Creating an imputer to replace NaN with the mean of each column
imputer = SimpleImputer(strategy='mean')

# Fitting the imputer on the training data and transform both training and test data
x_train_imputed2 = imputer.fit_transform(x_train_new)

rf2 = RandomForestClassifier(bootstrap=True,
                                       max_depth=14,
                                       max_features='sqrt',
                                       min_samples_leaf=2,
                                       min_samples_split=3,
                                       n_estimators=58,
                                       random_state=42)

rf2.fit(x_train_imputed2, y_train)

x_train_imputed2 = imputer.transform(x_train_new)
rf2.score(x_train_imputed2, y_train)

x_test_imputed2 = imputer.transform(x_test_new)
rf2.score(x_test_imputed2, y_test)

from matplotlib import pyplot as plt

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('feature importances')
    plt.show()

features_names = x_train_select_df.columns
f_importances(abs(rf2.feature_importances_), features_names, top=6)

x_test_imputed2 = imputer.transform(x_test_new)
y_pre_rf2 = rf2.predict(x_test_imputed2)
y_pre_rf2

import xgboost as xgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

dtrain2 = xgb.DMatrix(x_train_new, label=y_train)
dtest2 = xgb.DMatrix(x_test_new, label=y_test)

param = {
    'objective': 'binary:logistic',
    'colsample_bytree': 0.9439761626945282,
    'gamma': 6.803075385877797,
    'learning_rate': 0.1451497755908629,
    'max_depth': 4,
    'n_estimators': 181,
    'reg_alpha': 0.9422017556848528,
    'reg_lambda': 0.5632882178455393,
    'subsample': 0.7541666010159664,
    'random_state': 42
}

watchlist2 = [(dtrain2, 'train'), (dtest2, 'eval')]

num_round = 1000
early_stopping_rounds = 10
bst2 = xgb.train(param, dtrain2, num_round, watchlist2,
                 early_stopping_rounds=early_stopping_rounds,
                 verbose_eval=True)

y_pred_2 = bst2.predict(dtest2)

y_pred_binary2 = [1 if p >= 0.5 else 0 for p in y_pred_2]

y_pred_2_train = bst2.predict(xgb.DMatrix(x_train_new))
y_pred_train_binary2 = [1 if p >= 0.5 else 0 for p in y_pred_2_train]

accuracy = accuracy_score(y_train, y_pred_train_binary2)
print("Training Accuracy:", accuracy)

y_pred_2_test = bst2.predict(xgb.DMatrix(x_test_new))
y_pred_test_binary2 = [1 if p >= 0.5 else 0 for p in y_pred_2_test]

accuracy = accuracy_score(y_test, y_pred_test_binary2)
print("Test Accuracy:", accuracy)

from sklearn.metrics import confusion_matrix

con_dt2 = confusion_matrix(y_test, y_pre_dt2)
con_rf2 = confusion_matrix(y_test, y_pre_rf2)
y_pred_bst_binary2 = [1 if p >= 0.5 else 0 for p in y_pred_2]

con_bst2 = confusion_matrix(y_test, y_pred_bst_binary2)

fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(21,7))

sns.heatmap(con_dt,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax1 , cmap = 'Blues')
ax1.set_ylabel('Prediction',fontsize=13)
ax1.set_xlabel('Actual',fontsize=13)
ax1.set_title('Decision Tree',fontsize=17)


sns.heatmap(con_rf,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax2 , cmap = 'YlOrBr')
ax2.set_ylabel('Prediction',fontsize=13)
ax2.set_xlabel('Actual',fontsize=13)
ax2.set_title('Random Forest',fontsize=17)

sns.heatmap(con_bst2,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax3 , cmap = 'Greens')
ax3.set_ylabel('Prediction',fontsize=13)
ax3.set_xlabel('Actual',fontsize=13)
ax3.set_title('XGBoost',fontsize=17)
plt.show()

y_pred_bst_binary2 = [1 if p >= 0.5 else 0 for p in y_pred_2]

ls_scores = np.array([accuracy_score(y_test , y_pre_dt2),
                       accuracy_score(y_test , y_pre_rf2),
                       accuracy_score(y_test, y_pred_bst_binary2),
                       precision_score(y_test , y_pre_dt2),
                       precision_score(y_test , y_pre_rf2),
                       precision_score(y_test , y_pred_bst_binary2),
                       recall_score(y_test , y_pre_dt2),
                       recall_score(y_test , y_pre_rf2),
                       recall_score(y_test , y_pred_bst_binary2),
                       f1_score(y_test , y_pre_dt2),
                       f1_score(y_test , y_pre_rf2),
                       f1_score(y_test , y_pred_bst_binary2)])

index1 = ['Accuracy' , 'Precision' , 'Recall' , 'F1-score']
cols1 = ['Decision Tree' , 'Random Forest', 'XGBClassifier']
eval2 = pd.DataFrame(ls_scores.reshape(4,3) , columns = cols1 , index = index1)
eval2

from imblearn.under_sampling import RandomUnderSampler
rus = RandomUnderSampler(random_state=42)
X_resampled, y_resampled = rus.fit_resample(x_train_new, y_train)

dt_model = DecisionTreeClassifier()

param_dist = {
    'max_depth': randint(3, 15),
    'max_features': randint(5, x_train_new.shape[1])
}

random_search = RandomizedSearchCV(
    estimator=dt_model,
    param_distributions=param_dist,
    n_iter=50,
    cv=5,
    scoring='f1',
    n_jobs=-1,
    verbose=2,
    random_state=42
)

random_search.fit(X_resampled, y_resampled)

print("Best Parameters:", random_search.best_params_)

best_dt_model_2 = random_search.best_estimator_

best_dt_model_2= DecisionTreeClassifier(max_depth = 5 , max_features = 10)

best_dt_model_2.fit(x_train_new , y_train)

best_dt_model_2.score(x_train_new , y_train)

best_dt_model_2.score(x_test_new , y_test)

from matplotlib import pyplot as plt

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('feature importances')
    plt.show()

features_names = x_train_select_df.columns

f_importances(abs(best_dt_model_2.feature_importances_), features_names, top=6)

y_pre_best_dt_model_2 = best_dt_model_2.predict(x_test_new)
y_pre_best_dt_model_2

param_dist = {
    'n_estimators': randint(50, 200),
    'max_depth': randint(3, 15),
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 10),
    'max_features': ['auto', 'sqrt', 'log2'],
    'bootstrap': [True, False]
}
rf = RandomForestClassifier()

random_search_rf = RandomizedSearchCV(estimator=rf,
                                   param_distributions=param_dist,
                                   n_iter=10,
                                   cv=5,
                                   n_jobs=-1,
                                   verbose=2,
                                   random_state=42)

random_search_rf.fit(x_train_new, y_train)

print("Best Parameters for Random Forest:", random_search_rf.best_params_)

best_rf_model_2 = random_search_rf.best_estimator_

imputer = SimpleImputer(strategy='mean')

x_train_imputed2 = imputer.fit_transform(x_train_new)

best_rf_model_2 = RandomForestClassifier(bootstrap=True,
                                       max_depth=9,
                                       max_features='log2',
                                       min_samples_leaf=8,
                                       min_samples_split=5,
                                       n_estimators=153,
                                       random_state=42)

best_rf_model_2.fit(x_train_imputed2, y_train)

x_train_imputed2 = imputer.transform(x_train_new)

best_rf_model_2.score(x_train_imputed2, y_train)

x_test_imputed2 = imputer.transform(x_test_new)

best_rf_model_2.score(x_test_imputed2, y_test)

from matplotlib import pyplot as plt

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('feature importances')
    plt.show()

features_names = x_train_select_df.columns

f_importances(abs(best_rf_model_2.feature_importances_), features_names, top=6)

x_test_imputed2 = imputer.transform(x_test_new)

y_pre_best_rf_model_2 = best_rf_model_2.predict(x_test_imputed2) # Use x_test_imputed instead of x_test
y_pre_best_rf_model_2

from scipy.stats import randint, uniform

param_dist = {
    'n_estimators': randint(50, 200),
    'learning_rate': uniform(0.01, 0.3),
    'max_depth': randint(3, 10),
    'subsample': uniform(0.6, 0.4),
    'colsample_bytree': uniform(0.6, 0.4),
    'gamma': uniform(0, 10),
    'reg_alpha': uniform(0, 1),
    'reg_lambda': uniform(0, 1)
}

random_search_xgb = RandomizedSearchCV(estimator=xgb.XGBClassifier(objective='binary:logistic'),
                                   param_distributions=param_dist,
                                   n_iter=10,
                                   cv=5,
                                   n_jobs=-1,
                                   verbose=2,
                                   random_state=42)

random_search_xgb.fit(x_train_new, y_train)

print("Best Parameters for XGBoost:", random_search_xgb.best_params_)

best_xgb_model_2 = random_search_xgb.best_estimator_

import xgboost as xgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

dtrain2 = xgb.DMatrix(x_train_new, label=y_train)
dtest2 = xgb.DMatrix(x_test_new, label=y_test)

param = {
    'objective': 'binary:logistic',
    'colsample_bytree': 0.6063865008880857,
    'gamma': 2.3089382562214897,
    'learning_rate': 0.0823076398078035,
    'max_depth': 6,
    'n_estimators': 57,
    'reg_alpha': 0.034388521115218396,
    'reg_lambda': 0.9093204020787821,
    'subsample': 0.7035119926400067,
    'random_state': 42
}

watchlist2 = [(dtrain2, 'train'), (dtest2, 'eval')]

num_round = 1000
early_stopping_rounds = 10
best_xgb_model_2 = xgb.train(param, dtrain2, num_round, watchlist2,
                 early_stopping_rounds=early_stopping_rounds,
                 verbose_eval=True)

y_pred_best_xgb_model_2 = best_xgb_model_2.predict(dtest2)

y_pred_binary_best_xgb_model_2 = [1 if p >= 0.5 else 0 for p in y_pred_best_xgb_model_2]

from matplotlib import pyplot as plt

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.figure(figsize=(10, 0.5 * top))
    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('Feature Importances')
    plt.xlabel('Importance Score')
    plt.ylabel('Features')
    plt.show()

features_names = x_train_select_df.columns

# f_importances(abs(best_xgb_model_2.feature_importances_), features_names, top=6)
best_xgb_model_estimator = random_search_xgb.best_estimator_  # Assuming you used RandomizedSearchCV
f_importances(abs(best_xgb_model_estimator.feature_importances_), features_names, top=6)

dtest_new = xgb.DMatrix(x_test_new)
y_pred_best_xgb_model_2 = best_xgb_model_2.predict(dtest_new)
y_pred_best_xgb_model_2

con_best_dt_model_2 = confusion_matrix(y_test, y_pre_best_dt_model_2)
con_best_rf_model_2 = confusion_matrix(y_test, y_pre_best_rf_model_2)

y_pred_binary_best_xgb_model_2 = [1 if p >= 0.5 else 0 for p in y_pred_best_xgb_model_2]


con_best_xgb_model_2 = confusion_matrix(y_test, y_pred_binary_best_xgb_model_2)


#Plot the confusion matrix.
fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(21,7))

sns.heatmap(con_best_dt_model_2,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax1 , cmap = 'Blues')
ax1.set_ylabel('Prediction',fontsize=13)
ax1.set_xlabel('Actual',fontsize=13)
ax1.set_title('Decision Tree',fontsize=17)


sns.heatmap(con_best_rf_model_2,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax2 , cmap = 'YlOrBr')
ax2.set_ylabel('Prediction',fontsize=13)
ax2.set_xlabel('Actual',fontsize=13)
ax2.set_title('Random Forest',fontsize=17)

sns.heatmap(con_best_xgb_model_2,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax3 , cmap = 'Greens')
ax3.set_ylabel('Prediction',fontsize=13)
ax3.set_xlabel('Actual',fontsize=13)
ax3.set_title('XGBoost',fontsize=17)
plt.show()

y_pred_binary_best_xgb_model_2 = [1 if p >= 0.5 else 0 for p in y_pred_binary_best_xgb_model_2]

ls_scores = np.array([accuracy_score(y_test , y_pre_best_dt_model_2),
                       accuracy_score(y_test , y_pre_best_rf_model_2),
                       accuracy_score(y_test, y_pred_binary_best_xgb_model_2),
                       precision_score(y_test , y_pre_best_dt_model_2),
                       precision_score(y_test ,y_pre_best_rf_model_2),
                       precision_score(y_test , y_pred_binary_best_xgb_model_2),
                       recall_score(y_test , y_pre_best_dt_model_2),
                       recall_score(y_test , y_pre_best_rf_model_2),
                       recall_score(y_test , y_pred_binary_best_xgb_model_2),
                       f1_score(y_test , y_pre_best_dt_model_2),
                       f1_score(y_test , y_pre_best_rf_model_2),
                       f1_score(y_test ,y_pred_binary_best_xgb_model_2)])

index1 = ['Accuracy' , 'Precision' , 'Recall' , 'F1-score']
cols1 = ['Decision Tree' , 'Random Forest', 'XGBClassifier']
eval_2 = pd.DataFrame(ls_scores.reshape(4,3) , columns = cols1 , index = index1)
eval_2

plt.figure(figsize=(14, 10))  # Set the figure size


plt.subplot(2, 2, 1)
plt.bar(eval.columns, eval.loc['Accuracy'], color=['skyblue', 'lightgreen', 'salmon'])
plt.title('Comparison of Accuracy')
plt.ylabel('Accuracy')
plt.ylim(0, 1)
plt.xticks(rotation=45)


plt.subplot(2, 2, 2)
plt.bar(eval.columns, eval.loc['Precision'], color=['skyblue', 'lightgreen', 'salmon'])
plt.title('Comparison of Precision')
plt.ylabel('Precision')
plt.ylim(0, 1)
plt.xticks(rotation=45)


plt.subplot(2, 2, 3)
plt.bar(eval.columns, eval.loc['Recall'], color=['skyblue', 'lightgreen', 'salmon'])
plt.title('Comparison of Recall')
plt.ylabel('Recall')
plt.ylim(0, 1)
plt.xticks(rotation=45)

plt.subplot(2, 2, 4)
plt.bar(eval.columns, eval.loc['F1-score'], color=['skyblue', 'lightgreen', 'salmon'])
plt.title('Comparison of F1-score')
plt.ylabel('F1-score')
plt.ylim(0, 1)
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

!pip install imblearn
from imblearn.under_sampling import RandomUnderSampler
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import mutual_info_classif, SelectKBest
import pandas as pd


X_df = df.drop(['HeartDisease'], axis=1)
X = X_df.values
y = df['HeartDisease'].values


u_s = RandomUnderSampler()
X_under, y_under = u_s.fit_resample(X, y)


x_train, x_test, y_train, y_test = train_test_split(X_under, y_under, test_size=0.30, random_state=42)


print("Shape of training data:", x_train.shape)


selector = SelectKBest(mutual_info_classif, k=10)
x_train_new = selector.fit_transform(x_train, y_train)

# Step 7: Apply the same feature selection to the test set
x_test_new = selector.transform(x_test)

# Step 8: Get the selected feature names (use X_df which is still a DataFrame)
selected_features = X_df.columns[selector.get_support()]
print("Selected features:", selected_features)

# Optional: Create DataFrames with the selected features for both training and test sets
x_train_select_df = pd.DataFrame(x_train_new, columns=selected_features)
x_test_select_df = pd.DataFrame(x_test_new, columns=selected_features)

plt.figure(figsize=(10, 6))

mean_scores = x_train_select_df.mean()

plt.bar(mean_scores.index, mean_scores.values)
plt.xticks(rotation=90)
plt.xlabel('Features')
plt.ylabel('Mean Mutual Information Score')
plt.title('Mean Mutual Information Scores for Features')
plt.tight_layout()
plt.show()

X_under.shape

dt3= DecisionTreeClassifier(max_depth = 6 , max_features = 9 )

dt3.fit(x_train_new,y_train)

dt3.score(x_train_new,y_train)

dt3.score(x_test_new,y_test)

from matplotlib import pyplot as plt

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('feature importances')
    plt.show()

features_names = x_train_select_df.columns

f_importances(abs(dt3.feature_importances_), features_names, top=6)

y_pre_dt3=dt3.predict(x_test_new)
y_pre_dt3

from sklearn.impute import SimpleImputer

imputer = SimpleImputer(strategy='mean')

x_train_imputed3 = imputer.fit_transform(x_train_new)

rf3 = RandomForestClassifier(bootstrap=True,
                                       max_depth=14,
                                       max_features='sqrt',
                                       min_samples_leaf=2,
                                       min_samples_split=3,
                                       n_estimators=58,
                                       random_state=42)
rf3.fit(x_train_imputed3, y_train)

x_train_imputed3 = imputer.transform(x_train_new)

rf3.score(x_train_imputed3, y_train)

x_test_imputed3 = imputer.transform(x_test_new)

rf3.score(x_test_imputed3, y_test)

from matplotlib import pyplot as plt

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('feature importances')
    plt.show()

features_names = x_train_select_df.columns

f_importances(abs(rf3.feature_importances_), features_names, top=6)

x_test_imputed3 = imputer.transform(x_test_new)

y_pre_rf3 = rf3.predict(x_test_imputed3)
y_pre_rf3

dtrain3 = xgb.DMatrix(x_train_new, label=y_train)
dtest3 = xgb.DMatrix(x_test_new, label=y_test)

param = {
    'objective': 'binary:logistic',
    'colsample_bytree': 0.9439761626945282,
    'gamma': 6.803075385877797,
    'learning_rate': 0.1451497755908629,
    'max_depth': 4,
    'n_estimators': 181,
    'reg_alpha': 0.9422017556848528,
    'reg_lambda': 0.5632882178455393,
    'subsample': 0.7541666010159664,
    'random_state': 42
}

watchlist3 = [(dtrain3, 'train'), (dtest3, 'eval')]

num_round = 1000
early_stopping_rounds = 10
bst3 = xgb.train(param, dtrain3, num_round, watchlist3,
                 early_stopping_rounds=early_stopping_rounds,
                 verbose_eval=True)

y_pred_3 = bst3.predict(dtest3)

y_pred_binary3 = [1 if p >= 0.5 else 0 for p in y_pred_3]

y_pred_3_train = bst3.predict(xgb.DMatrix(x_train_new))
y_pred_train_binary3 = [1 if p >= 0.5 else 0 for p in y_pred_3_train]

accuracy = accuracy_score(y_train, y_pred_train_binary3)
print("Training Accuracy:", accuracy)

y_pred_3_test = bst3.predict(xgb.DMatrix(x_test_new))
y_pred_test_binary3 = [1 if p >= 0.5 else 0 for p in y_pred_3_test]

accuracy = accuracy_score(y_test, y_pred_test_binary3)
print("Test Accuracy:", accuracy)

con_dt3 = confusion_matrix(y_test, y_pre_dt3)
con_rf3 = confusion_matrix(y_test, y_pre_rf3)

y_pred_bst_binary3 = [1 if p >= 0.5 else 0 for p in y_pred_3]

con_bst3 = confusion_matrix(y_test, y_pred_bst_binary3)

fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(21,7))

sns.heatmap(con_dt3,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax1 , cmap = 'Blues')
ax1.set_ylabel('Prediction',fontsize=13)
ax1.set_xlabel('Actual',fontsize=13)
ax1.set_title('Decision Tree',fontsize=17)


sns.heatmap(con_rf3,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax2 , cmap = 'YlOrBr')
ax2.set_ylabel('Prediction',fontsize=13)
ax2.set_xlabel('Actual',fontsize=13)
ax2.set_title('Random Forest',fontsize=17)

sns.heatmap(con_bst3,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax3 , cmap = 'Greens')
ax3.set_ylabel('Prediction',fontsize=13)
ax3.set_xlabel('Actual',fontsize=13)
ax3.set_title('XGBoost',fontsize=17)
plt.show()

y_pred_bst_binary3 = [1 if p >= 0.5 else 0 for p in y_pred_3]

ls_scores = np.array([accuracy_score(y_test , y_pre_dt3),
                       accuracy_score(y_test , y_pre_rf3),
                       accuracy_score(y_test, y_pred_bst_binary3),
                       precision_score(y_test , y_pre_dt3),
                       precision_score(y_test , y_pre_rf3),
                       precision_score(y_test , y_pred_bst_binary3),
                       recall_score(y_test , y_pre_dt3),
                       recall_score(y_test , y_pre_rf3),
                       recall_score(y_test , y_pred_bst_binary3),
                       f1_score(y_test , y_pre_dt3),
                       f1_score(y_test , y_pre_rf3),
                       f1_score(y_test , y_pred_bst_binary3)])

index1 = ['Accuracy' , 'Precision' , 'Recall' , 'F1-score']
cols1 = ['Decision Tree' , 'Random Forest', 'XGBClassifier']
eval3 = pd.DataFrame(ls_scores.reshape(4,3) , columns = cols1 , index = index1)
eval3

rus = RandomUnderSampler(random_state=42)
X_resampled, y_resampled = rus.fit_resample(x_train_new, y_train)


dt_model = DecisionTreeClassifier()

param_dist = {
    'max_depth': randint(3, 15),
    'max_features': randint(5, x_train_new.shape[1])
}


random_search = RandomizedSearchCV(
    estimator=dt_model,
    param_distributions=param_dist,
    n_iter=50,  # Number of random combinations to try
    cv=5,       # Number of cross-validation folds
    scoring='f1',  # Use F1-score as the evaluation metric (adjust as needed)
    n_jobs=-1,   # Use all available cores for parallel processing
    verbose=2,   # Print progress updates
    random_state=42  # Set random state for reproducibility
)

random_search.fit(X_resampled, y_resampled)

print("Best Parameters:", random_search.best_params_)

best_dt_model_3 = random_search.best_estimator_

best_dt_model_3= DecisionTreeClassifier(max_depth = 8 , max_features = 9 )

best_dt_model_3.fit(x_train_new,y_train)

best_dt_model_3.score(x_train_new,y_train)

best_dt_model_3.score(x_test_new,y_test)

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('feature importances')
    plt.show()

features_names = x_train_select_df.columns

f_importances(abs(best_dt_model_3.feature_importances_), features_names, top=6)

y_pre_best_dt_model_3=dt3.predict(x_test_new)
y_pre_best_dt_model_3

param_dist = {
    'n_estimators': randint(50, 200),
    'max_depth': randint(3, 15),
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 10),
    'max_features': ['auto', 'sqrt', 'log2'],
    'bootstrap': [True, False]
}


rf = RandomForestClassifier()

random_search_rf = RandomizedSearchCV(estimator=rf,
                                   param_distributions=param_dist,
                                   n_iter=10,
                                   cv=5,
                                   n_jobs=-1,
                                   verbose=2,
                                   random_state=42)

random_search_rf.fit(x_train_new, y_train)

print("Best Parameters for Random Forest:", random_search_rf.best_params_)

best_rf_model_3 = random_search_rf.best_estimator_

imputer = SimpleImputer(strategy='mean')

x_train_imputed3 = imputer.fit_transform(x_train_new)

best_rf_model_3 = RandomForestClassifier(bootstrap=True,
                                       max_depth=9,
                                       max_features='log2',
                                       min_samples_leaf=8,
                                       min_samples_split=5,
                                       n_estimators=153,
                                       random_state=42)
best_rf_model_3.fit(x_train_imputed3, y_train)

x_train_imputed3 = imputer.transform(x_train_new)

best_rf_model_3.score(x_train_imputed3, y_train)

x_test_imputed3 = imputer.transform(x_test_new)

best_rf_model_3.score(x_test_imputed3, y_test)

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('feature importances')
    plt.show()

features_names = x_train_select_df.columns

f_importances(abs(best_rf_model_3.feature_importances_), features_names, top=6)

x_test_imputed3 = imputer.transform(x_test_new)

y_pre_best_rf_model_3 = best_rf_model_3.predict(x_test_imputed3)
y_pre_best_rf_model_3

param_dist = {
    'n_estimators': randint(50, 200),
    'learning_rate': uniform(0.01, 0.3),
    'max_depth': randint(3, 10),
    'subsample': uniform(0.6, 0.4),
    'colsample_bytree': uniform(0.6, 0.4),
    'gamma': uniform(0, 10),
    'reg_alpha': uniform(0, 1),
    'reg_lambda': uniform(0, 1)
}

random_search_xgb = RandomizedSearchCV(estimator=xgb.XGBClassifier(objective='binary:logistic'),
                                   param_distributions=param_dist,
                                   n_iter=10,
                                   cv=5,
                                   n_jobs=-1,
                                   verbose=2,
                                   random_state=42)

random_search_xgb.fit(x_train_new, y_train)


print("Best Parameters for XGBoost:", random_search_xgb.best_params_)

best_xgb_model_3 = random_search_xgb.best_estimator_

dtrain3 = xgb.DMatrix(x_train_new, label=y_train)
dtest3 = xgb.DMatrix(x_test_new, label=y_test)

param = {
    'objective': 'binary:logistic',
    'colsample_bytree': 0.9439761626945282,
    'gamma': 6.803075385877797,
    'learning_rate': 0.1451497755908629,
    'max_depth': 4,
    'n_estimators': 181,
    'reg_alpha': 0.9422017556848528,
    'reg_lambda':  0.5632882178455393,
    'subsample': 0.7541666010159664,
    'random_state': 42
}

watchlist3 = [(dtrain3, 'train'), (dtest3, 'eval')]

num_round = 1000
early_stopping_rounds = 10
best_xgb_model_3 = xgb.train(param, dtrain3, num_round, watchlist3,
                 early_stopping_rounds=early_stopping_rounds,
                 verbose_eval=True)

y_pred_best_xgb_model_3 = best_xgb_model_3.predict(dtest3)

y_pred_binary_best_xgb_model_3 = [1 if p >= 0.5 else 0 for p in y_pred_best_xgb_model_3]

from matplotlib import pyplot as plt

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.figure(figsize=(10, 0.5 * top))
    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('Feature Importances')
    plt.xlabel('Importance Score')
    plt.ylabel('Features')
    plt.show()

features_names = x_train_select_df.columns

best_xgb_model_estimator = random_search_xgb.best_estimator_
f_importances(abs(best_xgb_model_estimator.feature_importances_), features_names, top=6)

dtest_new = xgb.DMatrix(x_test_new)
y_pred_best_xgb_model_3 = best_xgb_model_3.predict(dtest_new)
y_pred_best_xgb_model_3

con_best_dt_model_3 = confusion_matrix(y_test, y_pre_best_dt_model_3)
con_best_rf_model_3 = confusion_matrix(y_test, y_pre_best_rf_model_3)

y_pred_binary_best_xgb_model_3 = [1 if p >= 0.5 else 0 for p in y_pred_best_xgb_model_3]


con_best_xgb_model_3 = confusion_matrix(y_test, y_pred_binary_best_xgb_model_3)


#Plot the confusion matrix.
fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(21,7))

sns.heatmap(con_best_dt_model_3,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax1 , cmap = 'Blues')
ax1.set_ylabel('Prediction',fontsize=13)
ax1.set_xlabel('Actual',fontsize=13)
ax1.set_title('Decision Tree',fontsize=17)


sns.heatmap(con_best_rf_model_3,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax2 , cmap = 'YlOrBr')
ax2.set_ylabel('Prediction',fontsize=13)
ax2.set_xlabel('Actual',fontsize=13)
ax2.set_title('Random Forest',fontsize=17)

sns.heatmap(con_best_xgb_model_3,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax3 , cmap = 'Greens')
ax3.set_ylabel('Prediction',fontsize=13)
ax3.set_xlabel('Actual',fontsize=13)
ax3.set_title('XGBoost',fontsize=17)
plt.show()

y_pred_binary_best_xgb_model_3 = [1 if p >= 0.5 else 0 for p in y_pred_binary_best_xgb_model_3]

ls_scores = np.array([accuracy_score(y_test , y_pre_best_dt_model_3),
                       accuracy_score(y_test , y_pre_best_rf_model_3),
                       accuracy_score(y_test, y_pred_binary_best_xgb_model_3),
                       precision_score(y_test , y_pre_best_dt_model_3),
                       precision_score(y_test , y_pre_best_rf_model_3),
                       precision_score(y_test , y_pred_binary_best_xgb_model_3),
                       recall_score(y_test , y_pre_best_dt_model_3),
                       recall_score(y_test , y_pre_best_rf_model_3),
                       recall_score(y_test , y_pred_binary_best_xgb_model_3),
                       f1_score(y_test , y_pre_best_dt_model_3),
                       f1_score(y_test , y_pre_best_rf_model_3),
                       f1_score(y_test ,y_pred_binary_best_xgb_model_2)])

index1 = ['Accuracy' , 'Precision' , 'Recall' , 'F1-score']
cols1 = ['Decision Tree' , 'Random Forest', 'XGBClassifier']
eval_3 = pd.DataFrame(ls_scores.reshape(4,3) , columns = cols1 , index = index1)
eval_3

plt.figure(figsize=(12, 8))  # Set the figure size

# Plot Accuracy
plt.subplot(2, 2, 1)
plt.bar(eval.columns, eval.loc['Accuracy'], color=['skyblue', 'lightgreen'])
plt.title('Comparison of Accuracy')
plt.ylabel('Accuracy')
plt.ylim(0, 1)  # Assuming the metric is between 0 and 1
plt.xticks(rotation=45)

# Plot Precision
plt.subplot(2, 2, 2)
plt.bar(eval.columns, eval.loc['Precision'], color=['skyblue', 'lightgreen'])
plt.title('Comparison of Precision')
plt.ylabel('Precision')
plt.ylim(0, 1)
plt.xticks(rotation=45)

# Plot Recall
plt.subplot(2, 2, 3)
plt.bar(eval.columns, eval.loc['Recall'], color=['skyblue', 'lightgreen'])
plt.title('Comparison of Recall')
plt.ylabel('Recall')
plt.ylim(0, 1)
plt.xticks(rotation=45)

# Plot F1-score
plt.subplot(2, 2, 4)
plt.bar(eval.columns, eval.loc['F1-score'], color=['skyblue', 'lightgreen'])
plt.title('Comparison of F1-score')
plt.ylabel('F1-score')
plt.ylim(0, 1)
plt.xticks(rotation=45)

plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

from imblearn.under_sampling import NearMiss
from sklearn.model_selection import train_test_split
from sklearn.feature_selection import mutual_info_classif, SelectKBest
import pandas as pd

# Step 3: Assuming 'df' is your DataFrame and already loaded with data including the 'HeartDisease' column
X_df = df.drop(['HeartDisease'], axis=1)  # Keep the DataFrame for column names later
X = X_df.values  # Extract values for calculations
y = df['HeartDisease'].values

# Step 4: Perform NearMiss undersampling to balance the dataset
nm = NearMiss(version=1)
X_under3, y_under3 = nm.fit_resample(X, y)

# Step 5: Split the undersampled data into training and test sets
x_train, x_test, y_train, y_test = train_test_split(X_under3, y_under3, test_size=0.30, random_state=42)

# Output the shape of the training data
print("Shape of training data:", x_train.shape)

# Step 6: Perform feature selection using mutual information on the training data
selector = SelectKBest(mutual_info_classif, k=10)  # Adjust k as needed
x_train_new = selector.fit_transform(x_train, y_train)  # Fit and transform on the training data

# Step 7: Apply the same feature selection to the test set
x_test_new = selector.transform(x_test)

# Step 8: Get the selected feature names (use X_df which is still a DataFrame)
selected_features = X_df.columns[selector.get_support()]
print("Selected features:", selected_features)

# Optional: Create DataFrames with the selected features for both training and test sets
x_train_select_df = pd.DataFrame(x_train_new, columns=selected_features)
x_test_select_df = pd.DataFrame(x_test_new, columns=selected_features)

plt.figure(figsize=(10, 6))

mean_scores = x_train_select_df.mean()

plt.bar(mean_scores.index, mean_scores.values)
plt.xticks(rotation=90)
plt.xlabel('Features')
plt.ylabel('Mean Mutual Information Score')
plt.title('Mean Mutual Information Scores for Features')
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 6))
sns.countplot(x=y_under3, palette="Set2")
plt.title('Distribution of HeartDisease After NearMiss Undersampling')
plt.xlabel('HeartDisease')
plt.ylabel('Count')
plt.show()

plt.figure(figsize=(8, 6))
sns.countplot(x=y_train, palette="Set1")
plt.title('Distribution of HeartDisease in Training Set')
plt.xlabel('HeartDisease')
plt.ylabel('Count')
plt.show()

plt.figure(figsize=(8, 6))
sns.countplot(x=y_test, palette="Set3")
plt.title('Distribution of HeartDisease in Test Set')
plt.xlabel('HeartDisease')
plt.ylabel('Count')
plt.show()

x_train_new.shape

dt5 = DecisionTreeClassifier(max_depth = 6 , max_features = 9)

dt5.fit(x_train_new , y_train)

dt5.score(x_train_new , y_train)

dt5.score(x_test_new , y_test)

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('feature importances')
    plt.show()

features_names = x_train_select_df.columns

f_importances(abs(dt5.feature_importances_), features_names, top=6)

y_pre_dt5 = dt5.predict(x_test_new)
y_pre_dt5

rf5 = RandomForestClassifier(bootstrap=True,
                                       max_depth=14,
                                       max_features='sqrt',
                                       min_samples_leaf=2,
                                       min_samples_split=3,
                                       n_estimators=58,
                                       random_state=42)

rf5.fit(x_train_new , y_train)

rf5.score(x_train_new , y_train)

rf5.score(x_test_new , y_test)

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('feature importances')
    plt.show()


features_names = x_train_select_df.columns

f_importances(abs(rf5.feature_importances_), features_names, top=6)

y_pre_rf5 = rf5.predict(x_test_new)
y_pre_rf5

dtrain5 = xgb.DMatrix(x_train_new, label=y_train)
dtest5 = xgb.DMatrix(x_test_new, label=y_test)

param = {
    'objective': 'binary:logistic',
    'colsample_bytree': 0.9439761626945282,
    'gamma': 6.803075385877797,
    'learning_rate': 0.1451497755908629,
    'max_depth': 4,
    'n_estimators': 181,
    'reg_alpha': 0.9422017556848528,
    'reg_lambda': 0.5632882178455393,
    'subsample': 0.7541666010159664,
    'random_state': 42
}

watchlist5 = [(dtrain5, 'train'), (dtest5, 'eval')]

num_round = 1000
early_stopping_rounds = 10
bst5 = xgb.train(param, dtrain5, num_round, watchlist5,
                 early_stopping_rounds=early_stopping_rounds,
                 verbose_eval=True)

y_pred_5 = bst5.predict(dtest5)

y_pred_binary5 = [1 if p >= 0.5 else 0 for p in y_pred_5]

y_pred_5_train = bst5.predict(xgb.DMatrix(x_train_new))
y_pred_train_binary5 = [1 if p >= 0.5 else 0 for p in y_pred_5_train]

accuracy = accuracy_score(y_train, y_pred_train_binary5)
print("Training Accuracy:", accuracy)

y_pred_5_test = bst5.predict(xgb.DMatrix(x_test_new))
y_pred_test_binary5 = [1 if p >= 0.5 else 0 for p in y_pred_5_test]

accuracy = accuracy_score(y_test, y_pred_test_binary5)
print("Test Accuracy:", accuracy)

con_dt5 = confusion_matrix(y_test, y_pre_dt5)
con_rf5 = confusion_matrix(y_test, y_pre_rf5)
y_pred_bst_binary5 = [1 if p >= 0.5 else 0 for p in y_pred_5]

con_bst5 = confusion_matrix(y_test, y_pred_bst_binary5)

fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(21,7))

sns.heatmap(con_dt5,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax1 , cmap = 'Blues')
ax1.set_ylabel('Prediction',fontsize=13)
ax1.set_xlabel('Actual',fontsize=13)
ax1.set_title('Decision Tree',fontsize=17)


sns.heatmap(con_rf5,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax2 , cmap = 'YlOrBr')
ax2.set_ylabel('Prediction',fontsize=13)
ax2.set_xlabel('Actual',fontsize=13)
ax2.set_title('Random Forest',fontsize=17)

sns.heatmap(con_bst5,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax3 , cmap = 'Greens')
ax3.set_ylabel('Prediction',fontsize=13)
ax3.set_xlabel('Actual',fontsize=13)
ax3.set_title('XGBoost',fontsize=17)
plt.show()

y_pred_bst_binary5 = [1 if p >= 0.5 else 0 for p in y_pred_5]

ls_scores = np.array([accuracy_score(y_test , y_pre_dt5),
                       accuracy_score(y_test , y_pre_rf5),
                       accuracy_score(y_test, y_pred_bst_binary5),
                       precision_score(y_test , y_pre_dt5),
                       precision_score(y_test , y_pre_rf5),
                       precision_score(y_test , y_pred_bst_binary5),
                       recall_score(y_test , y_pre_dt5),
                       recall_score(y_test , y_pre_rf5),
                       recall_score(y_test , y_pred_bst_binary5),
                       f1_score(y_test , y_pre_dt5),
                       f1_score(y_test , y_pre_rf5),
                       f1_score(y_test , y_pred_bst_binary5)])

index1 = ['Accuracy' , 'Precision' , 'Recall' , 'F1-score']
cols1 = ['Decision Tree' , 'Random Forest', 'XGBClassifier']
eval5 = pd.DataFrame(ls_scores.reshape(4,3) , columns = cols1 , index = index1)
eval5

# rus = RandomUnderSampler(random_state=42)
X_resampled, y_resampled = rus.fit_resample(x_train_new, y_train)

dt_model = DecisionTreeClassifier()

param_dist = {
    'max_depth': randint(3, 15),
    'max_features': randint(5, x_train_new.shape[1])
}

random_search = RandomizedSearchCV(
    estimator=dt_model,
    param_distributions=param_dist,
    n_iter=50,
    cv=5,
    scoring='f1',
    n_jobs=-1,
    verbose=2,
    random_state=42
)

random_search.fit(X_resampled, y_resampled)

print("Best Parameters:", random_search.best_params_)

best_dt_model_5 = random_search.best_estimator_

best_dt_model_5 = DecisionTreeClassifier(max_depth = 11 , max_features = 9)

best_dt_model_5.fit(x_train_new , y_train)

best_dt_model_5.score(x_train_new , y_train)

best_dt_model_5.score(x_test_new , y_test)

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('feature importances')
    plt.show()

features_names = x_train_select_df.columns

f_importances(abs(best_dt_model_5.feature_importances_), features_names, top=6)

y_pre_best_dt_model_5 = best_dt_model_5.predict(x_test_new)
y_pre_best_dt_model_5

param_dist = {
    'n_estimators': randint(50, 200),
    'max_depth': randint(3, 15),
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 10),
    'max_features': ['auto', 'sqrt', 'log2'],
    'bootstrap': [True, False]
}

rf = RandomForestClassifier()

random_search_rf = RandomizedSearchCV(estimator=rf,
                                   param_distributions=param_dist,
                                   n_iter=10,
                                   cv=5,
                                   n_jobs=-1,
                                   verbose=2,
                                   random_state=42)

random_search_rf.fit(x_train_new, y_train)

print("Best Parameters for Random Forest:", random_search_rf.best_params_)

best_rf_model_5 = random_search_rf.best_estimator_

best_rf_model_5  = RandomForestClassifier(bootstrap=True,
                                       max_depth=14,
                                       max_features='sqrt',
                                       min_samples_leaf=2,
                                       min_samples_split=10,
                                       n_estimators=139,
                                       random_state=42)

best_rf_model_5 .fit(x_train_new , y_train)

best_rf_model_5 .score(x_train_new , y_train)

best_rf_model_5.score(x_test_new , y_test)

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('feature importances')
    plt.show()

features_names = x_train_select_df.columns

f_importances(abs(best_rf_model_5.feature_importances_), features_names, top=6)

y_pre_best_rf_model_5 = best_rf_model_5.predict(x_test_new)
y_pre_best_rf_model_5

param_dist = {
    'n_estimators': randint(50, 200),
    'learning_rate': uniform(0.01, 0.3),
    'max_depth': randint(3, 10),
    'subsample': uniform(0.6, 0.4),
    'colsample_bytree': uniform(0.6, 0.4),
    'gamma': uniform(0, 10),
    'reg_alpha': uniform(0, 1),
    'reg_lambda': uniform(0, 1)
}

random_search_xgb = RandomizedSearchCV(estimator=xgb.XGBClassifier(objective='binary:logistic'),
                                   param_distributions=param_dist,
                                   n_iter=10,
                                   cv=5,
                                   n_jobs=-1,
                                   verbose=2,
                                   random_state=42)

random_search_xgb.fit(x_train_new, y_train)

print("Best Parameters for XGBoost:", random_search_xgb.best_params_)

best_xgb_model_5 = random_search_xgb.best_estimator_

dtrain5 = xgb.DMatrix(x_train_new, label=y_train)
dtest5 = xgb.DMatrix(x_test_new, label=y_test)

param = {
    'objective': 'binary:logistic',
    'colsample_bytree': 0.7693605922825478,
    'gamma': 3.9488151817556973,
    'learning_rate': 0.09804645241541143,
    'max_depth': 9,
    'n_estimators': 188,
    'reg_alpha': 0.19884240408880516,
    'reg_lambda': 0.71134195274865,
    'subsample': 0.9160702162124823,
    'random_state': 42
}

watchlist5 = [(dtrain5, 'train'), (dtest5, 'eval')]

num_round = 1000
early_stopping_rounds = 10
best_xgb_model_5 = xgb.train(param, dtrain5, num_round, watchlist5,
                 early_stopping_rounds=early_stopping_rounds,
                 verbose_eval=True)

y_pred_best_xgb_model_5 = best_xgb_model_5.predict(dtest5)

y_pred_binary_best_xgb_model_5 = [1 if p >= 0.5 else 0 for p in y_pred_best_xgb_model_5]

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.figure(figsize=(10, 0.5 * top))
    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('Feature Importances')
    plt.xlabel('Importance Score')
    plt.ylabel('Features')
    plt.show()

features_names = x_train_select_df.columns


best_xgb_model_estimator = random_search_xgb.best_estimator_
f_importances(abs(best_xgb_model_estimator.feature_importances_), features_names, top=6)

dtest_new = xgb.DMatrix(x_test_new)
y_pred_best_xgb_model_5 = best_xgb_model_5.predict(dtest_new)
y_pred_best_xgb_model_5

con_best_dt_model_5 = confusion_matrix(y_test, y_pre_best_dt_model_5)
con_best_rf_model_5 = confusion_matrix(y_test, y_pre_best_rf_model_5)

y_pred_binary_best_xgb_model_5 = [1 if p >= 0.5 else 0 for p in y_pred_best_xgb_model_5]


con_best_xgb_model_5 = confusion_matrix(y_test, y_pred_binary_best_xgb_model_5)


#Plot the confusion matrix.
fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(21,7))

sns.heatmap(con_best_dt_model_5,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax1 , cmap = 'Blues')
ax1.set_ylabel('Prediction',fontsize=13)
ax1.set_xlabel('Actual',fontsize=13)
ax1.set_title('Decision Tree',fontsize=17)


sns.heatmap(con_best_rf_model_5,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax2 , cmap = 'YlOrBr')
ax2.set_ylabel('Prediction',fontsize=13)
ax2.set_xlabel('Actual',fontsize=13)
ax2.set_title('Random Forest',fontsize=17)

sns.heatmap(con_best_xgb_model_5,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax3 , cmap = 'Greens')
ax3.set_ylabel('Prediction',fontsize=13)
ax3.set_xlabel('Actual',fontsize=13)
ax3.set_title('XGBoost',fontsize=17)
plt.show()

y_pred_binary_best_xgb_model_5 = [1 if p >= 0.5 else 0 for p in y_pred_binary_best_xgb_model_5]

ls_scores = np.array([accuracy_score(y_test , y_pre_best_dt_model_5),
                       accuracy_score(y_test , y_pre_best_rf_model_5),
                       accuracy_score(y_test, y_pred_binary_best_xgb_model_5),
                       precision_score(y_test , y_pre_best_dt_model_5),
                       precision_score(y_test , y_pre_best_rf_model_5),
                       precision_score(y_test , y_pred_binary_best_xgb_model_5),
                       recall_score(y_test , y_pre_best_dt_model_5),
                       recall_score(y_test , y_pre_best_rf_model_5),
                       recall_score(y_test , y_pred_binary_best_xgb_model_5),
                       f1_score(y_test , y_pre_best_dt_model_5),
                       f1_score(y_test , y_pre_best_rf_model_5),
                       f1_score(y_test ,y_pred_binary_best_xgb_model_5)])

index1 = ['Accuracy' , 'Precision' , 'Recall' , 'F1-score']
cols1 = ['Decision Tree' , 'Random Forest', 'XGBClassifier']
eval_5 = pd.DataFrame(ls_scores.reshape(4,3) , columns = cols1 , index = index1)
eval_5

plt.figure(figsize=(12, 8))  # Set the figure size

# Plot Accuracy
plt.subplot(2, 2, 1)
plt.bar(eval.columns, eval.loc['Accuracy'], color=['skyblue', 'lightgreen'])
plt.title('Comparison of Accuracy')
plt.ylabel('Accuracy')
plt.ylim(0, 1)  # Assuming the metric is between 0 and 1
plt.xticks(rotation=45)

# Plot Precision
plt.subplot(2, 2, 2)
plt.bar(eval.columns, eval.loc['Precision'], color=['skyblue', 'lightgreen'])
plt.title('Comparison of Precision')
plt.ylabel('Precision')
plt.ylim(0, 1)
plt.xticks(rotation=45)

# Plot Recall
plt.subplot(2, 2, 3)
plt.bar(eval.columns, eval.loc['Recall'], color=['skyblue', 'lightgreen'])
plt.title('Comparison of Recall')
plt.ylabel('Recall')
plt.ylim(0, 1)
plt.xticks(rotation=45)

# Plot F1-score
plt.subplot(2, 2, 4)
plt.bar(eval.columns, eval.loc['F1-score'], color=['skyblue', 'lightgreen'])
plt.title('Comparison of F1-score')
plt.ylabel('F1-score')
plt.ylim(0, 1)
plt.xticks(rotation=45)

plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

from imblearn.under_sampling import ClusterCentroids
from sklearn.cluster import MiniBatchKMeans

X_df = df.drop(['HeartDisease'], axis=1)  # Keep the DataFrame for column names later
X = X_df.values  # Extract values for calculations
y = df['HeartDisease'].values

# Step 4: Perform undersampling using ClusterCentroids with MiniBatchKMeans
cc = ClusterCentroids(estimator=MiniBatchKMeans(n_init=1, random_state=0), random_state=42)
X_under4, y_under4 = cc.fit_resample(X, y)

# Step 5: Split the undersampled data into training and test sets
x_train, x_test, y_train, y_test = train_test_split(X_under4, y_under4, test_size=0.30, random_state=42)

# Output the shape of the training data
print("Shape of training data:", x_train.shape)

# Step 6: Perform feature selection using mutual information on the training data
selector = SelectKBest(mutual_info_classif, k=10)  # Adjust k as needed
x_train_new = selector.fit_transform(x_train, y_train)  # Fit and transform on the training data

# Step 7: Apply the same feature selection to the test set
x_test_new = selector.transform(x_test)

# Step 8: Get the selected feature names (use X_df which is still a DataFrame)
selected_features = X_df.columns[selector.get_support()]
print("Selected features:", selected_features)

# Optional: Create DataFrames with the selected features for both training and test sets
x_train_select_df = pd.DataFrame(x_train_new, columns=selected_features)
x_test_select_df = pd.DataFrame(x_test_new, columns=selected_features)

plt.figure(figsize=(10, 6))

mean_scores = x_train_select_df.mean()

plt.bar(mean_scores.index, mean_scores.values)
plt.xticks(rotation=90)
plt.xlabel('Features')
plt.ylabel('Mean Mutual Information Score')
plt.title('Mean Mutual Information Scores for Features')
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 6))
sns.countplot(x=y_under4, palette="Set2")
plt.title('Distribution of HeartDisease After ClusterCentroids Undersampling')
plt.xlabel('HeartDisease')
plt.ylabel('Count')
plt.show()

plt.figure(figsize=(8, 6))
sns.countplot(x=y_train, palette="Set1")
plt.title('Distribution of HeartDisease in Training Set')
plt.xlabel('HeartDisease')
plt.ylabel('Count')
plt.show()

plt.figure(figsize=(8, 6))
sns.countplot(x=y_test, palette="Set3")
plt.title('Distribution of HeartDisease in Test Set')
plt.xlabel('HeartDisease')
plt.ylabel('Count')
plt.show()

x_train_new.shape

dt6 = DecisionTreeClassifier(max_depth = 6 , max_features = 9)

dt6.fit(x_train_new , y_train)

dt6.score(x_train_new , y_train)

dt6.score(x_test_new , y_test)

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('feature importances')
    plt.show()

features_names = x_train_select_df.columns

f_importances(abs(dt6.feature_importances_), features_names, top=6)

y_pre_dt6 = dt6.predict(x_test_new)
y_pre_dt6

rf6 = RandomForestClassifier(bootstrap=True,
                                       max_depth=14,
                                       max_features='sqrt',
                                       min_samples_leaf=2,
                                       min_samples_split=3,
                                       n_estimators=58,
                                       random_state=42)

rf6.fit(x_train_new , y_train)

rf6.score(x_train_new , y_train)

rf6.score(x_test_new , y_test)

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('feature importances')
    plt.show()

features_names = x_train_select_df.columns

f_importances(abs(rf6.feature_importances_), features_names, top=6)

y_pre_rf6 = rf6.predict(x_test_new)
y_pre_rf6

dtrain6 = xgb.DMatrix(x_train_new, label=y_train)
dtest6 = xgb.DMatrix(x_test_new, label=y_test)


param = {
    'max_depth': 4,
    'learning_rate': 0.1,
    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'reg_alpha': 0.1,
    'reg_lambda': 1.0,
    'objective': 'binary:logistic',
    'eval_metric': 'logloss',
    'seed': 42
}


watchlist6 = [(dtrain6, 'train'), (dtest6, 'eval')]


num_round = 1000
early_stopping_rounds = 10
bst6 = xgb.train(param, dtrain6, num_round, watchlist6, early_stopping_rounds=early_stopping_rounds, verbose_eval=True)


y_pred_6 = bst6.predict(dtest6)


y_pred_binary6 = [1 if p >= 0.5 else 0 for p in y_pred_6]

y_pred_6_train = bst6.predict(xgb.DMatrix(x_train_new))
y_pred_train_binary6 = [1 if p >= 0.5 else 0 for p in y_pred_6_train]

accuracy = accuracy_score(y_train, y_pred_train_binary6)
print("Training Accuracy:", accuracy)

y_pred_6_test = bst6.predict(xgb.DMatrix(x_test_new))
y_pred_test_binary6 = [1 if p >= 0.5 else 0 for p in y_pred_6_test]

accuracy = accuracy_score(y_test, y_pred_test_binary6)
print("Test Accuracy:", accuracy)

con_dt6 = confusion_matrix(y_test, y_pre_dt6)
con_rf6 = confusion_matrix(y_test, y_pre_rf6)

y_pred_bst_binary6 = [1 if p >= 0.5 else 0 for p in y_pred_6]

con_bst6 = confusion_matrix(y_test, y_pred_bst_binary6)

fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(21,7))

sns.heatmap(con_dt6,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax1 , cmap = 'Blues')
ax1.set_ylabel('Prediction',fontsize=13)
ax1.set_xlabel('Actual',fontsize=13)
ax1.set_title('Decision Tree',fontsize=17)


sns.heatmap(con_rf6,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax2 , cmap = 'YlOrBr')
ax2.set_ylabel('Prediction',fontsize=13)
ax2.set_xlabel('Actual',fontsize=13)
ax2.set_title('Random Forest',fontsize=17)

sns.heatmap(con_bst6,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax3 , cmap = 'Greens')
ax3.set_ylabel('Prediction',fontsize=13)
ax3.set_xlabel('Actual',fontsize=13)
ax3.set_title('XGBoost',fontsize=17)
plt.show()

y_pred_bst_binary6 = [1 if p >= 0.5 else 0 for p in y_pred_6]

ls_scores = np.array([accuracy_score(y_test , y_pre_dt6),
                       accuracy_score(y_test , y_pre_rf6),
                       accuracy_score(y_test, y_pred_bst_binary6),
                       precision_score(y_test , y_pre_dt6),
                       precision_score(y_test , y_pre_rf6),
                       precision_score(y_test , y_pred_bst_binary6),
                       recall_score(y_test , y_pre_dt6),
                       recall_score(y_test , y_pre_rf6),
                       recall_score(y_test , y_pred_bst_binary6),
                       f1_score(y_test , y_pre_dt6),
                       f1_score(y_test , y_pre_rf6),
                       f1_score(y_test , y_pred_bst_binary6)])

index1 = ['Accuracy' , 'Precision' , 'Recall' , 'F1-score']
cols1 = ['Decision Tree' , 'Random Forest', 'XGBClassifier']
eval6 = pd.DataFrame(ls_scores.reshape(4,3) , columns = cols1 , index = index1)
eval6

rus = RandomUnderSampler(random_state=42)
X_resampled, y_resampled = rus.fit_resample(x_train_new, y_train)

dt_model = DecisionTreeClassifier()

param_dist = {
    'max_depth': randint(3, 15),
    'max_features': randint(5, x_train_new.shape[1])
}

random_search = RandomizedSearchCV(
    estimator=dt_model,
    param_distributions=param_dist,
    n_iter=50,
    cv=5,
    scoring='f1',
    n_jobs=-1,
    verbose=2,
    random_state=42
)

random_search.fit(X_resampled, y_resampled)

print("Best Parameters:", random_search.best_params_)

best_dt_model_6 = random_search.best_estimator_

best_dt_model_6  = DecisionTreeClassifier(max_depth = 7 , max_features = 7)

best_dt_model_6.fit(x_train_new , y_train)

best_dt_model_6.score(x_train_new , y_train)

best_dt_model_6.score(x_test_new , y_test)

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('feature importances')
    plt.show()

features_names = x_train_select_df.columns

f_importances(abs(best_dt_model_6.feature_importances_), features_names, top=6)

y_pre_best_dt_model_6 = best_dt_model_6.predict(x_test_new)
y_pre_best_dt_model_6

param_dist = {
    'n_estimators': randint(50, 200),
    'max_depth': randint(3, 15),
    'min_samples_split': randint(2, 20),
    'min_samples_leaf': randint(1, 10),
    'max_features': ['auto', 'sqrt', 'log2'],
    'bootstrap': [True, False]
}

rf = RandomForestClassifier()

random_search_rf = RandomizedSearchCV(estimator=rf,
                                   param_distributions=param_dist,
                                   n_iter=10,
                                   cv=5,
                                   n_jobs=-1,
                                   verbose=2,
                                   random_state=42)

random_search_rf.fit(x_train_new, y_train)

print("Best Parameters for Random Forest:", random_search_rf.best_params_)

best_rf_model_6 = random_search_rf.best_estimator_

best_rf_model_6 = RandomForestClassifier(bootstrap=True,
                                       max_depth=14,
                                       max_features='sqrt',
                                       min_samples_leaf=2,
                                       min_samples_split=10,
                                       n_estimators=139,
                                       random_state=42)

best_rf_model_6.fit(x_train_new , y_train)

best_rf_model_6.score(x_train_new , y_train)

best_rf_model_6.score(x_test_new , y_test)

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('feature importances')
    plt.show()

features_names = x_train_select_df.columns

f_importances(abs(best_rf_model_6.feature_importances_), features_names, top=6)

y_pre_best_rf_model_6 = best_rf_model_6.predict(x_test_new)
y_pre_best_rf_model_6

param_dist = {
    'n_estimators': randint(50, 200),
    'learning_rate': uniform(0.01, 0.3),
    'max_depth': randint(3, 10),
    'subsample': uniform(0.6, 0.4),
    'colsample_bytree': uniform(0.6, 0.4),
    'gamma': uniform(0, 10),
    'reg_alpha': uniform(0, 1),
    'reg_lambda': uniform(0, 1)
}


random_search_xgb = RandomizedSearchCV(estimator=xgb.XGBClassifier(objective='binary:logistic'),
                                   param_distributions=param_dist,
                                   n_iter=10,
                                   cv=5,
                                   n_jobs=-1,
                                   verbose=2,
                                   random_state=42)

random_search_xgb.fit(x_train_new, y_train)

print("Best Parameters for XGBoost:", random_search_xgb.best_params_)

best_xgb_model_6 = random_search_xgb.best_estimator_

dtrain6 = xgb.DMatrix(x_train_new, label=y_train)
dtest6= xgb.DMatrix(x_test_new, label=y_test)

param = {
    'objective': 'binary:logistic',
    'colsample_bytree': 0.6063865008880857,
    'gamma': 2.3089382562214897,
    'learning_rate': 0.0823076398078035,
    'max_depth': 6,
    'n_estimators': 57,
    'reg_alpha': 0.034388521115218396,
    'reg_lambda': 0.9093204020787821,
    'subsample': 0.7035119926400067,
    'random_state': 42
}

watchlist6 = [(dtrain6, 'train'), (dtest6, 'eval')]

num_round = 1000
early_stopping_rounds = 10
best_xgb_model_6 = xgb.train(param, dtrain6, num_round, watchlist6,
                 early_stopping_rounds=early_stopping_rounds,
                 verbose_eval=True)

y_pred_best_xgb_model_6 = best_xgb_model_6.predict(dtest6)

y_pred_binary_best_xgb_model_6 = [1 if p >= 0.5 else 0 for p in y_pred_best_xgb_model_6]

def f_importances(coef, names, top=-1):
    imp = coef
    imp, names = zip(*sorted(list(zip(imp, names))))


    if top == -1:
        top = len(names)

    plt.figure(figsize=(10, 0.5 * top))
    plt.barh(range(top), imp[::-1][0:top], align='center')
    plt.yticks(range(top), names[::-1][0:top])
    plt.title('Feature Importances')
    plt.xlabel('Importance Score')
    plt.ylabel('Features')
    plt.show()

features_names = x_train_select_df.columns

best_xgb_model_estimator = random_search_xgb.best_estimator_
f_importances(abs(best_xgb_model_estimator.feature_importances_), features_names, top=6)

dtest_new = xgb.DMatrix(x_test_new)
y_pred_best_xgb_model_6 = best_xgb_model_6.predict(dtest_new)
y_pred_best_xgb_model_6

con_best_dt_model_6 = confusion_matrix(y_test, y_pre_best_dt_model_6)
con_best_rf_model_6 = confusion_matrix(y_test, y_pre_best_rf_model_6)

y_pred_binary_best_xgb_model_6 = [1 if p >= 0.5 else 0 for p in y_pred_best_xgb_model_6]


con_best_xgb_model_6 = confusion_matrix(y_test, y_pred_binary_best_xgb_model_6)


#Plot the confusion matrix.
fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(21,7))

sns.heatmap(con_best_dt_model_6,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax1 , cmap = 'Blues')
ax1.set_ylabel('Prediction',fontsize=13)
ax1.set_xlabel('Actual',fontsize=13)
ax1.set_title('Decision Tree',fontsize=17)


sns.heatmap(con_best_rf_model_6,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax2 , cmap = 'YlOrBr')
ax2.set_ylabel('Prediction',fontsize=13)
ax2.set_xlabel('Actual',fontsize=13)
ax2.set_title('Random Forest',fontsize=17)

sns.heatmap(con_best_xgb_model_6,
            annot=True,
            fmt='d',
            xticklabels=['No','Yes'],
            yticklabels=['No','Yes'] , ax = ax3 , cmap = 'Greens')
ax3.set_ylabel('Prediction',fontsize=13)
ax3.set_xlabel('Actual',fontsize=13)
ax3.set_title('XGBoost',fontsize=17)
plt.show()

y_pred_binary_best_xgb_model_6 = [1 if p >= 0.5 else 0 for p in y_pred_binary_best_xgb_model_6]


ls_scores = np.array([accuracy_score(y_test , y_pre_best_dt_model_6),
                       accuracy_score(y_test , y_pre_best_rf_model_6),
                       accuracy_score(y_test, y_pred_binary_best_xgb_model_6),
                       precision_score(y_test , y_pre_best_dt_model_6),
                       precision_score(y_test , y_pre_best_rf_model_6),
                       precision_score(y_test , y_pred_binary_best_xgb_model_6),
                       recall_score(y_test , y_pre_best_dt_model_6),
                       recall_score(y_test , y_pre_best_rf_model_6),
                       recall_score(y_test , y_pred_binary_best_xgb_model_6),
                       f1_score(y_test , y_pre_best_dt_model_6),
                       f1_score(y_test , y_pre_best_rf_model_6),
                       f1_score(y_test ,y_pred_binary_best_xgb_model_6)])

index1 = ['Accuracy' , 'Precision' , 'Recall' , 'F1-score']
cols1 = ['Decision Tree' , 'Random Forest', 'XGBClassifier']
eval_6 = pd.DataFrame(ls_scores.reshape(4,3) , columns = cols1 , index = index1)
eval_6

plt.figure(figsize=(12, 8))


plt.subplot(2, 2, 1)
plt.bar(eval.columns, eval.loc['Accuracy'], color=['skyblue', 'lightgreen'])
plt.title('Comparison of Accuracy')
plt.ylabel('Accuracy')
plt.ylim(0, 1)
plt.xticks(rotation=45)


plt.subplot(2, 2, 2)
plt.bar(eval.columns, eval.loc['Precision'], color=['skyblue', 'lightgreen'])
plt.title('Comparison of Precision')
plt.ylabel('Precision')
plt.ylim(0, 1)
plt.xticks(rotation=45)

plt.subplot(2, 2, 3)
plt.bar(eval.columns, eval.loc['Recall'], color=['skyblue', 'lightgreen'])
plt.title('Comparison of Recall')
plt.ylabel('Recall')
plt.ylim(0, 1)
plt.xticks(rotation=45)


plt.subplot(2, 2, 4)
plt.bar(eval.columns, eval.loc['F1-score'], color=['skyblue', 'lightgreen'])
plt.title('Comparison of F1-score')
plt.ylabel('F1-score')
plt.ylim(0, 1)
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()

# Assuming you have the data for eval_2, create the DataFrame here
# For example:
eval_2_data = [[0.75, 0.76, 0.75], [0.72, 0.73, 0.73], [0.81, 0.82, 0.80], [0.76, 0.77, 0.76]]
eval_3_data = [[0.74, 0.75, 0.75], [0.70, 0.72, 0.73], [0.83, 0.81, 0.79], [0.76, 0.76, 0.76]]
eval_5_data = [[0.86, 0.87, 0.87], [0.88, 0.93, 0.92], [0.79, 0.79, 0.80], [0.83, 0.85, 0.86]]
eval_6_data = [[0.74, 0.75, 0.76], [0.71, 0.73, 0.73], [0.80, 0.81, 0.81], [0.75, 0.77, 0.77]]

eval_2 = pd.DataFrame(eval_2_data, columns=['Decision Tree', 'Random Forest', 'XGBClassifier'], index=['Accuracy', 'Precision', 'Recall', 'F1-score'])
eval_3 = pd.DataFrame(eval_3_data, columns=['Decision Tree', 'Random Forest', 'XGBClassifier'], index=['Accuracy', 'Precision', 'Recall', 'F1-score'])
eval_5 = pd.DataFrame(eval_5_data, columns=['Decision Tree', 'Random Forest', 'XGBClassifier'], index=['Accuracy', 'Precision', 'Recall', 'F1-score'])
eval_6 = pd.DataFrame(eval_6_data, columns=['Decision Tree', 'Random Forest', 'XGBClassifier'], index=['Accuracy', 'Precision', 'Recall', 'F1-score'])

# Now you can concatenate the DataFrames
metrics_all = pd.concat([eval_2, eval_3, eval_5, eval_6],
                        keys=['Manual Random Under-sampling',
                              'Automated Random Under-sampling',
                              'Near Miss Under-sampling',
                              'Cluster Centroids Under-sampling'])
print(metrics_all)

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Creating individual dataframes
eval_2_data = [[0.75, 0.76, 0.75], [0.72, 0.73, 0.73], [0.81, 0.82, 0.80], [0.76, 0.77, 0.76]]
eval_3_data = [[0.74, 0.75, 0.75], [0.70, 0.72, 0.73], [0.83, 0.81, 0.79], [0.76, 0.76, 0.76]]
eval_5_data = [[0.86, 0.87, 0.87], [0.88, 0.93, 0.92], [0.79, 0.79, 0.80], [0.83, 0.85, 0.86]]
eval_6_data = [[0.74, 0.75, 0.76], [0.71, 0.73, 0.73], [0.80, 0.81, 0.81], [0.75, 0.77, 0.77]]

eval_2 = pd.DataFrame(eval_2_data, columns=['Decision Tree', 'Random Forest', 'XGBClassifier'], index=['Accuracy', 'Precision', 'Recall', 'F1-score'])
eval_3 = pd.DataFrame(eval_3_data, columns=['Decision Tree', 'Random Forest', 'XGBClassifier'], index=['Accuracy', 'Precision', 'Recall', 'F1-score'])
eval_5 = pd.DataFrame(eval_5_data, columns=['Decision Tree', 'Random Forest', 'XGBClassifier'], index=['Accuracy', 'Precision', 'Recall', 'F1-score'])
eval_6 = pd.DataFrame(eval_6_data, columns=['Decision Tree', 'Random Forest', 'XGBClassifier'], index=['Accuracy', 'Precision', 'Recall', 'F1-score'])

# Concatenate the DataFrames
metrics_all = pd.concat([eval_2, eval_3, eval_5, eval_6],
                        keys=['Manual Random Under-sampling',
                              'Automated Random Under-sampling',
                              'Near Miss Under-sampling',
                              'Cluster Centroids Under-sampling'])

metrics_all.reset_index(inplace=True)
metrics_all.rename(columns={'level_0': 'Under-sampling Technique', 'level_1': 'Metric'}, inplace=True)
# Melting the DataFrame properly for plotting
melted_metrics = metrics_all.melt(id_vars=['Under-sampling Technique', 'Metric'],
                                  var_name='Model', value_name='Score')
# Plotting the melted DataFrame
plt.figure(figsize=(14, 8))
bar = sns.barplot(data=melted_metrics, x='Metric', y='Score', hue='Model', palette='deep', ci=None)

plt.title('Comparison of Tuned Model Metrics Across Different Under-sampling Techniques')
plt.ylabel('Score')
plt.xlabel('Metric')
plt.legend(title='Model', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

eval2_data = [[0.74, 0.75, 0.76], [0.71, 0.73, 0.73], [0.82, 0.80, 0.81], [0.76, 0.76, 0.77]]
eval3_data = [[0.74, 0.75, 0.75], [0.70, 0.72, 0.73], [0.83, 0.79, 0.80], [0.76, 0.76, 0.76]]
eval5_data = [[0.84, 0.87, 0.87], [0.88, 0.93, 0.92], [0.79, 0.79, 0.80], [0.83, 0.85, 0.86]]
eval6_data = [[0.73, 0.75, 0.76], [0.71, 0.73, 0.73], [0.80, 0.81, 0.81], [0.75, 0.77, 0.77]]

eval2 = pd.DataFrame(eval2_data, columns=['Decision Tree', 'Random Forest', 'XGBClassifier'], index=['Accuracy', 'Precision', 'Recall', 'F1-score'])
eval3 = pd.DataFrame(eval3_data, columns=['Decision Tree', 'Random Forest', 'XGBClassifier'], index=['Accuracy', 'Precision', 'Recall', 'F1-score'])
eval5 = pd.DataFrame(eval5_data, columns=['Decision Tree', 'Random Forest', 'XGBClassifier'], index=['Accuracy', 'Precision', 'Recall', 'F1-score'])
eval6 = pd.DataFrame(eval6_data, columns=['Decision Tree', 'Random Forest', 'XGBClassifier'], index=['Accuracy', 'Precision', 'Recall', 'F1-score'])

# Concatenate the DataFrames
metrics_all = pd.concat([eval2, eval3, eval5, eval6],
                        keys=['Manual Random Under-sampling',
                              'Automated Random Under-sampling',
                              'Near Miss Under-sampling',
                              'Cluster Centroids Under-sampling'])

metrics_all.reset_index(inplace=True)
metrics_all.rename(columns={'level_0': 'Under-sampling Technique', 'level_1': 'Metric'}, inplace=True)
# Melting the DataFrame properly for plotting
melted_metrics = metrics_all.melt(id_vars=['Under-sampling Technique', 'Metric'],
                                  var_name='Model', value_name='Score')
# Plotting the melted DataFrame
plt.figure(figsize=(14, 8))
bar = sns.barplot(data=melted_metrics, x='Metric', y='Score', hue='Model', palette='deep', ci=None)

plt.title('Comparison of Model Metrics Across Different Under-sampling Techniques')
plt.ylabel('Score')
plt.xlabel('Metric')
plt.legend(title='Model', bbox_to_anchor=(1.05, 1), loc='upper left')
plt.show()

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Creating individual dataframes
eval_2_data = [[0.75, 0.76, 0.75], [0.72, 0.73, 0.73], [0.81, 0.82, 0.80], [0.76, 0.77, 0.76]]
eval_3_data = [[0.74, 0.75, 0.75], [0.70, 0.72, 0.73], [0.83, 0.81, 0.79], [0.76, 0.76, 0.76]]
eval_5_data = [[0.86, 0.87, 0.87], [0.88, 0.93, 0.92], [0.79, 0.79, 0.80], [0.83, 0.85, 0.86]]
eval_6_data = [[0.74, 0.75, 0.76], [0.71, 0.73, 0.73], [0.80, 0.81, 0.81], [0.75, 0.77, 0.77]]

eval_2 = pd.DataFrame(eval_2_data, columns=['Decision Tree', 'Random Forest', 'XGBClassifier'], index=['Accuracy', 'Precision', 'Recall', 'F1-score'])
eval_3 = pd.DataFrame(eval_3_data, columns=['Decision Tree', 'Random Forest', 'XGBClassifier'], index=['Accuracy', 'Precision', 'Recall', 'F1-score'])
eval_5 = pd.DataFrame(eval_5_data, columns=['Decision Tree', 'Random Forest', 'XGBClassifier'], index=['Accuracy', 'Precision', 'Recall', 'F1-score'])
eval_6 = pd.DataFrame(eval_6_data, columns=['Decision Tree', 'Random Forest', 'XGBClassifier'], index=['Accuracy', 'Precision', 'Recall', 'F1-score'])

# Concatenate the DataFrames
metrics_all = pd.concat([eval_2, eval_3, eval_5, eval_6],
                        keys=['Manual Random Under-sampling',
                              'Automated Random Under-sampling',
                              'Near Miss Under-sampling',
                              'Cluster Centroids Under-sampling'])

metrics_all.reset_index(inplace=True)
metrics_all.rename(columns={'level_0': 'Under-sampling Technique', 'level_1': 'Metric'}, inplace=True)
# Melting the DataFrame properly for plotting
melted_metrics = metrics_all.melt(id_vars=['Under-sampling Technique', 'Metric'],
                                  var_name='Model', value_name='Score')

import seaborn as sns
import matplotlib.pyplot as plt

# Ensure the plotting setup is ready
sns.set(style="whitegrid")  # For a nicer grid style

unique_techniques = melted_metrics['Under-sampling Technique'].unique()  # Get unique techniques

# Plotting one figure per sampling technique
for technique in unique_techniques:
    # Filter the DataFrame for the current technique
    data_subset = melted_metrics[melted_metrics['Under-sampling Technique'] == technique]

    # Create a new figure for each technique
    plt.figure(figsize=(12, 6))
    bar = sns.barplot(data=data_subset, x='Metric', y='Score', hue='Model', palette='deep', ci=None)

    # Adding titles and labels
    plt.title(f'Comparison of Tuned Model Metrics - {technique}')
    plt.ylabel('Score')
    plt.xlabel('Metric')
    plt.legend(title='Model')
    plt.ylim(0, 1)  # Set a consistent Y-axis limit for comparability

    # Show the plot
    plt.show()

eval2_data = [[0.74, 0.75, 0.76], [0.71, 0.73, 0.73], [0.82, 0.80, 0.81], [0.76, 0.76, 0.77]]
eval3_data = [[0.74, 0.75, 0.75], [0.70, 0.72, 0.73], [0.83, 0.79, 0.80], [0.76, 0.76, 0.76]]
eval5_data = [[0.84, 0.87, 0.87], [0.88, 0.93, 0.92], [0.79, 0.79, 0.80], [0.83, 0.85, 0.86]]
eval6_data = [[0.73, 0.75, 0.76], [0.71, 0.73, 0.73], [0.80, 0.81, 0.81], [0.75, 0.77, 0.77]]
eval_2 = pd.DataFrame(eval_2_data, columns=['Decision Tree', 'Random Forest', 'XGBClassifier'], index=['Accuracy', 'Precision', 'Recall', 'F1-score'])
eval_3 = pd.DataFrame(eval_3_data, columns=['Decision Tree', 'Random Forest', 'XGBClassifier'], index=['Accuracy', 'Precision', 'Recall', 'F1-score'])
eval_5 = pd.DataFrame(eval_5_data, columns=['Decision Tree', 'Random Forest', 'XGBClassifier'], index=['Accuracy', 'Precision', 'Recall', 'F1-score'])
eval_6 = pd.DataFrame(eval_6_data, columns=['Decision Tree', 'Random Forest', 'XGBClassifier'], index=['Accuracy', 'Precision', 'Recall', 'F1-score'])

# Concatenate the DataFrames
metrics_all = pd.concat([eval_2, eval_3, eval_5, eval_6],
                        keys=['Manual Random Under-sampling',
                              'Automated Random Under-sampling',
                              'Near Miss Under-sampling',
                              'Cluster Centroids Under-sampling'])

metrics_all.reset_index(inplace=True)
metrics_all.rename(columns={'level_0': 'Under-sampling Technique', 'level_1': 'Metric'}, inplace=True)
# Melting the DataFrame properly for plotting
melted_metrics = metrics_all.melt(id_vars=['Under-sampling Technique', 'Metric'],
                                  var_name='Model', value_name='Score')
# Ensure the plotting setup is ready
sns.set(style="whitegrid")  # For a nicer grid style

unique_techniques = melted_metrics['Under-sampling Technique'].unique()  # Get unique techniques

# Plotting one figure per sampling technique
for technique in unique_techniques:
    # Filter the DataFrame for the current technique
    data_subset = melted_metrics[melted_metrics['Under-sampling Technique'] == technique]

    # Create a new figure for each technique
    plt.figure(figsize=(12, 6))
    bar = sns.barplot(data=data_subset, x='Metric', y='Score', hue='Model', palette='deep', ci=None)

    # Adding titles and labels
    plt.title(f'Comparison of Model Metrics - {technique}')
    plt.ylabel('Score')
    plt.xlabel('Metric')
    plt.legend(title='Model')
    plt.ylim(0, 1)  # Set a consistent Y-axis limit for comparability

    # Show the plot
    plt.show()

pip install graphviz

from graphviz import Digraph

dot = Digraph(comment='Machine Learning Project Flowchart', format='png')
dot.attr(rankdir='TB', size='10', bgcolor='transparent')

dot.attr('node', shape='rectangle', style='filled', color='darkblue', fillcolor='skyblue', fontname='Helvetica', fontcolor='white')

dot.node('Start', 'Start', shape='ellipse', fillcolor='lightgray')
dot.node('End', 'End', shape='ellipse', fillcolor='lightgray')

dot.node('A', 'Data Collection')
dot.node('B', 'Data Processing')
dot.node('C', 'Feature Engineering')
dot.node('D', 'Data Visualization')
dot.node('E', 'Model Training')
dot.node('F', 'Model Tuning')
dot.node('G', 'Model Evaluation')
dot.node('H', 'Under Sampling')

dot.edge('Start', 'A')
dot.edge('A', 'B')
dot.edge('B', 'C')
dot.edge('C', 'D')
dot.edge('D', 'E')
dot.edge('E', 'F')
dot.edge('F', 'G')

dot.edge('G', 'H')
for i in range(1, 5):
    dot.edge('H', f'E_{i}', label=f'Under Sampling {i}')
    dot.node(f'E_{i}', 'Model Training')
    dot.node(f'F_{i}', 'Model Tuning')
    dot.node(f'G_{i}', 'Model Evaluation')
    dot.edge(f'E_{i}', f'F_{i}')
    dot.edge(f'F_{i}', f'G_{i}')
    if i < 4:
        dot.edge(f'G_{i}', f'H', label=f'Next Cycle {i+1}')

dot.edge(f'G_{4}', 'End')

dot.render('output/ML_project_flowchart_complete', view=True)
