
import numpy as np
import pandas as pd
import math
import itertools

from matplotlib import pyplot as plt
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import roc_curve, roc_auc_score



def main():

    # 1. Data Load
    data_path = "/Users/minwookim/Dropbox/05_Duke/Machine Learning/HW03/"
    data = load(data_path)

    header = data.columns.tolist()

    # 2. Run cross validation and obtain roc curves and auc
    auc0=cross_validation_features(data, 10, plot=True)
    auc1=cross_validation(data, 10, algorithm=naive_bayes, plot=True)
    auc2=cross_validation(data, 10, algorithm=linear_regression, plot=True)
    auc3=nested_cross_validation(data, 10, algorithm=logistic_regression, list_of_parameters=[0.01,0.1,1,10,100],plot=True)
    auc4=cross_validation(data, 10, algorithm=decision_tree, plot=True)
    auc5=nested_cross_validation(data, 10, algorithm=randomforest, list_of_parameters=[5,10,20,50,100], plot=True)


    # 3. Print out auc values
    print "\n 1. AUC for individual features :"
    for i in range(0, 4):
        print "\t {} : Mean={}, Standard dev={}".format(header[i+1],np.mean(auc0[i]), np.std(auc0[i]))

    print "\n 2. AUC for Naive Bayes :"
    print "\t Mean={}, Standard dev={}".format(np.mean(auc1), np.std(auc1))
    print "\n 3. AUC for linear regression :"
    print "\t Mean={}, Standard dev={}".format(np.mean(auc2), np.std(auc2))
    print "\n 4. AUC for logistic regression :"
    print "\t Mean={}, Standard dev={}".format(np.mean(auc3), np.std(auc3))
    print "\n 5. AUC for decision tree :"
    print "\t Mean={}, Standard dev={}".format(np.mean(auc4), np.std(auc4))
    print "\n 6. AUC for random forest :"
    print "\t Mean={}, Standard dev={}".format(np.mean(auc5), np.std(auc5))


    # 4. AUC interval plot
    yticks = ['Temperature','Humidity','Light','CO2','Naive Bayes','Linear Regression','Logistic Regression','Decision Tree',
             'RandomForest']

    for i in range(0,4):
        plt.plot([np.mean(auc0[i])-np.std(auc0[i]),np.mean(auc0[i])+np.std(auc0[i])], [0.1*(10-i)]*2, linewidth=6)
    plt.plot([np.mean(auc1) - np.std(auc1), np.mean(auc1) + np.std(auc1)], [0.1 * 6] * 2, linewidth=6)
    plt.plot([np.mean(auc2) - np.std(auc2), np.mean(auc2) + np.std(auc2)], [0.1 * 5] * 2, linewidth=6)
    plt.plot([np.mean(auc3) - np.std(auc3), np.mean(auc3) + np.std(auc3)], [0.1 * 4] * 2, linewidth=6)
    plt.plot([np.mean(auc4) - np.std(auc4), np.mean(auc4) + np.std(auc4)], [0.1 * 3] * 2, linewidth=6)
    plt.plot([np.mean(auc5) - np.std(auc5), np.mean(auc5) + np.std(auc5)], [0.1 * 2] * 2, linewidth=6)

    plt.yticks([x / 10.0 for x in range(10, 0, -1)], yticks)
    plt.xlim([0.5,1])
    plt.ylim([0.1,1.1])
    plt.grid(True)
    plt.show()


# Naive bayes classifier based on gaussian distribution
def naive_bayes(data, train_index, test_index):
    train = data.iloc[train_index,:]
    test = data.iloc[test_index,:]
    nb = GaussianNB()
    # train the model
    nb.fit(train.iloc[:, [1,2,4]], train.iloc[:, 6])
    # predict the labels and report accuracy
    hard_pred = nb.predict(test.iloc[:, [1,2,4]])
    acc = 1.0 * np.isclose(hard_pred, test.iloc[:, 6]).sum() / len(hard_pred)
    # use predicted probabilities to construct ROC curve and AUC score\n",
    soft_pred = nb.predict_proba(test.iloc[:, [1,2,4]])
    fpr, tpr, thresh = roc_curve(test.iloc[:, 6], soft_pred[:, 1], drop_intermediate=False)
    auc = roc_auc_score(test.iloc[:, 6], soft_pred[:, 1])
    return acc, auc, fpr, tpr


# Linear regression
def linear_regression(data, train_index, test_index):
    train = data.iloc[train_index,:]
    test = data.iloc[test_index,:]
    linear = LinearRegression()
    # train the model
    linear.fit(train.iloc[:, [1,2,4]], train.iloc[:, 6])
    # predict the labels
    hard_pred = (linear.predict(test.iloc[:, [1,2,4]])>0.5)*1
    acc = 1.0 * np.isclose(hard_pred, test.iloc[:, 6]).sum() / len(hard_pred)
    # Construct ROC curve and AUC score
    soft_pred = linear.predict(test.iloc[:, [1,2,4]])
    fpr, tpr, thresh = roc_curve(test.iloc[:, 6], soft_pred, drop_intermediate=False)
    auc = roc_auc_score(test.iloc[:, 6], soft_pred)
    return acc, auc, fpr, tpr


# Logistic regression
def logistic_regression(param, data, train_index, test_index):
    train = data.iloc[train_index,:]
    test = data.iloc[test_index,:]
    logistic = LogisticRegression(C=param)
    # train the model
    logistic.fit(train.iloc[:, [1,2,4]], train.iloc[:, 6])
    # predict the labels and report accuracy
    hard_pred = logistic.predict(test.iloc[:, [1,2,4]])
    acc = 1.0 * np.isclose(hard_pred, test.iloc[:, 6]).sum() / len(hard_pred)
    # use predicted probabilities to construct ROC curve and AUC score
    soft_pred = logistic.predict_proba(test.iloc[:, [1,2,4]])
    fpr, tpr, thresh = roc_curve(test.iloc[:, 6], soft_pred[:, 1], drop_intermediate=False)
    auc = roc_auc_score(test.iloc[:, 6], soft_pred[:, 1])
    return acc, auc, fpr, tpr


# Decision tree
def decision_tree(data, train_index, test_index):
    train = data.iloc[train_index,:]
    test = data.iloc[test_index,:]
    dt = DecisionTreeClassifier()
    # train the model
    dt.fit(train.iloc[:, [1,2,4]], train.iloc[:, 6])
    # predict the labels and report accuracy
    hard_pred = dt.predict(test.iloc[:, [1,2,4]])
    acc = 1.0 * np.isclose(hard_pred, test.iloc[:, 6]).sum() / len(hard_pred)
    # use predicted probabilities to construct ROC curve and AUC score",
    soft_pred = dt.predict_proba(test.iloc[:, [1,2,4]])
    fpr, tpr, thresh = roc_curve(test.iloc[:, 6], soft_pred[:, 1], drop_intermediate=False)
    auc = roc_auc_score(test.iloc[:, 6], soft_pred[:, 1])
    return acc, auc, fpr, tpr


# Randomforest
def randomforest(param, data, train_index, test_index):
    train = data.iloc[train_index,:]
    test = data.iloc[test_index,:]
    rf = RandomForestClassifier(n_estimators=param)
    # train the model
    rf.fit(train.iloc[:, [1,2,4]], train.iloc[:, 6])
    # predict the labels and report accuracy
    hard_pred = rf.predict(test.iloc[:, [1,2,4]])
    acc = 1.0 * np.isclose(hard_pred, test.iloc[:, 6]).sum() / len(hard_pred)
    # use predicted probabilities to construct ROC curve and AUC score
    soft_pred = rf.predict_proba(test.iloc[:, [1,2,4]])
    fpr, tpr, thresh = roc_curve(test.iloc[:, 6], soft_pred[:, 1], drop_intermediate=False)
    auc = roc_auc_score(test.iloc[:, 6], soft_pred[:, 1])
    return acc, auc, fpr, tpr


# Support Vector Machine(with kernel = poly)
def support_vector(param, data,train_index, test_index):
    train = data.iloc[train_index,:]
    test = data.iloc[test_index,:]
    sv = SVC(C=param, probability=True, kernel = 'poly', degree=3, gamma=0.3, tol=0.5)
    # train the model
    sv.fit(train.iloc[:, [1,2,4]], train.iloc[:, 6])
    # predict the labels and report accuracy
    hard_pred = sv.predict(test.iloc[:, [1,2,4]])
    acc = 1.0 * np.isclose(hard_pred, test.iloc[:, 6]).sum() / len(hard_pred)
    # use predicted probabilities to construct ROC curve and AUC score\n",
    soft_pred = sv.predict_proba(test.iloc[:, [1,2,4]])
    fpr, tpr, thresh = roc_curve(test.iloc[:, 6], soft_pred[:, 1], drop_intermediate=False)
    auc = roc_auc_score(test.iloc[:, 6], soft_pred[:, 1])
    return acc, auc, fpr, tpr


# Nested cross validation + ROC curve plot
def nested_cross_validation(data, n_folds, algorithm, list_of_parameters, plot=False):
    assert isinstance(list_of_parameters, list)
    if n_folds<3 :
        print "Need at least 3 folds"
        return

    # Divide the set into k fold
    groups = kfold(len(data), n_folds)
    auc_list = []
    plt.figure("Algorithm={}".format(algorithm))

    for i in range(0, n_folds):

        # First, find the optimal parameter using validation sets
        test_index = groups[i] # Test set
        acc_table = pd.DataFrame(np.matrix([[1,]*n_folds]*(len(list_of_parameters)))) #Accuracy table
        for j in range(0, n_folds):
            if j==i : continue
            validation_index = groups[j] # Validation set
            train_index = [] # Train set
            # Merge train_index into a single list
            for k in range(0, n_folds):
                if k==j or k==i : continue
                else : train_index.append(groups[k])
            train_index = list(itertools.chain(*train_index))
            for p in range(0, len(list_of_parameters)):
                acc, auc, fpr, tpr = algorithm(list_of_parameters[p], data, train_index, validation_index)
                acc_table.iloc[p, j] = acc

        average_acc = acc_table.mean(axis=1)
        optimal_param = list_of_parameters[average_acc.index[max(average_acc)]]

        # Next, use the optimal parameter to fit the algorithm
        train_index = []  # Train index
        for k in range(0, n_folds):
            if k == i:
                continue
            else:
                train_index.append(groups[k])
        train_index = list(itertools.chain(*train_index))
        acc, auc, fpr, tpr = algorithm(optimal_param, data, train_index, test_index)
        plt.plot(fpr, tpr, label='Test fold={}'.format(i))
        plt.legend(loc=4, borderaxespad=0.)
        auc_list.append(auc)

    plt.plot([-0.01, 1.01], [-0.01, 1.01], "r--", alpha=.5)

    if plot==True:
        plt.show()
    return auc_list


# Cross validation + ROC curve plot
def cross_validation(data, n_folds, algorithm=None, plot=False):
    if n_folds<2 :
        print "Need at least 2 folds"
        return

    # Divide the set into k fold
    groups = kfold(len(data),n_folds)
    auc_list = []
    plt.figure("Algorithm={}".format(algorithm))

    for i in range(0, n_folds):
        test_index = groups[i]
        train_index = []
        for k in range(0, n_folds):
            if k==i : continue
            else : train_index.append(groups[k])
        # Merge train_index into a single list
        train_index = list(itertools.chain(*train_index))
        acc, auc, fpr, tpr = algorithm(data, train_index, test_index)
        plt.plot(fpr, tpr, label='Test fold={}'.format(i))
        plt.legend(loc=4, borderaxespad=0.)
        auc_list.append(auc)
    plt.plot([-0.01, 1.01], [-0.01, 1.01], "r--", alpha=.5)

    if plot==True:
        plt.show()
    return auc_list


# ROC curve plot for each individual feature, on all 10 test folds
def cross_validation_features(data, n_folds, plot=False):
    if n_folds<2 :
        print "Need at least 2 folds"
        return

    groups = kfold(len(data),n_folds)
    auc_list = [[] for p in range(1,5)]
    header=data.columns.tolist()

    for i in range(0, n_folds):
        test_index = groups[i]
        for p in range(1, 5):
            fpr, tpr, thresh = roc_curve(data.iloc[test_index, 6], data.iloc[test_index, p])
            auc = roc_auc_score(data.iloc[test_index, 6], data.iloc[test_index, p])
            plt.figure("features={}".format(header[p]))
            plt.plot(fpr, tpr, label='Test fold={}'.format(i))
            plt.plot([-0.01, 1.01], [-0.01, 1.01], "r--", alpha=.5)
            plt.legend(loc=4, borderaxespad=0.)
            auc_list[p-1].append(auc)

    if plot==True:
        plt.show()
    return auc_list


def kfold(n_list, n_group):
    result = [[] for i in range(n_group)]
    for i in range(0, n_list):
        result[i%n_group].append(i)
    return result


def load(data_path):
    data1 = pd.read_csv(data_path+"datatraining.txt")
    data2 = pd.read_csv(data_path+"datatest.txt")
    data3 = pd.read_csv(data_path+"datatest2.txt")
    data = data1.append(data2).append(data3)
    return data


if __name__ == '__main__': main()