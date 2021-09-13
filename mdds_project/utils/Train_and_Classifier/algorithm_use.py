#!/usr/bin/env python
# -*- coding: utf-8 -*-


import os
import re
import gensim
from numpy import *
from sklearn import metrics
import numpy as np
from sklearn.model_selection import *
from sklearn.metrics import classification_report
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, AdaBoostClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import scale
import time
import datetime
from utils.common import Logger
from utils.config_parser import ConfigParser
from sklearn.neural_network import MLPClassifier
from random import shuffle


class ClusteringMixData:
    def __init__(self, theConfigFilePath, theLogger=Logger()):
        # parse config file
        self.configParser = ConfigParser()
        self.configParser.parseFile(theConfigFilePath)
        # self.configParser.generateDirectories()
        self.log = theLogger
        
    def _createLogDir(self, logDir):
        if not os.path.exists(logDir):
            try:
                os.makedirs(logDir)
            except OSError, e:
                print e
    
    def _getLogDir(self):
        """
        logRootDir = self.configParser.getLogDir()
        logDir = '%s/%s' % (logRootDir, 'Log') #'%s/%s-%s' % (logRootDir, 
        return logDir
        """
        return 'Log'
    
    
    def testModel(self, X, y, size=0.25):
        classifiers = [
                 KNeighborsClassifier(),
                 SVC(kernel="linear", C=0.025, probability=True),
                 SVC(gamma=2, C=1, probability=True),
                 DecisionTreeClassifier(),
                 RandomForestClassifier(),
                 AdaBoostClassifier(),
                 LogisticRegression(),
                 GradientBoostingClassifier(),
                 MLPClassifier(solver='lbfgs', 
                               alpha=1e-5,
                               hidden_layer_sizes=(5, 2),
                               random_state=1)
             ]

        names = ["Nearest Neighbors", "Linear SVM", "RBF SVM",
                 "Decision Tree", "Random Forest", "AdaBoost",
                 "LogisticRegression", "GradientBoostingClassifier", "MLPClassifier"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=size)
        DicResult = {}
        for name, clf in zip(names, classifiers):
            d1 = datetime.datetime.now()
            clf.fit(X_train, y_train)

            import pickle
            clf.fit(X_train, y_train)
            with open('models\\' + name + '.txt', 'wb') as f:
                pickle.dump(clf, f)
            '''
            with open('models\\' + name+'.txt', 'rb') as f:
                clf = pickle.load(f)
            '''
            
            y_true, y_pred = y_test, clf.predict(X_test)
            self.log.info('testModel: %s' %name)
            
            result = classification_report(y_true, y_pred, digits=4)
            self.log.info('----------------classification report:----------------\n%s' %result)
            
            confusion = metrics.confusion_matrix(y_true, y_pred)
            TP = confusion[1,1]
            TN = confusion[0,0]
            FP = confusion[0,1]
            FN = confusion[1,0]
            accuracy = (TP+TN) / float(TP+TN+FN+FP)
            self.log.info('classfication accuracy: %f' %accuracy)

            error = (FP+FN) / float(TP+TN+FN+FP)
            self.log.info('Classification Error: %f' %error)

            recall = TP / float(TP+FN)
            self.log.info('Sensitivity Recall: %f' %recall)

            specificity = TN / float(TN+FP)
            self.log.info('Specificity: %f' %specificity)

            false_positive_rate = FP / float(TN+FP)
            self.log.info('False Positive Rate: %f' %false_positive_rate)
            
            precision = TP / float(TP+FP)
            self.log.info('Precision: %f' %precision)
            
            auc = metrics.roc_auc_score(y_true, y_pred)
            self.log.info('auc: %f' %auc)
            
            d2 = datetime.datetime.now()
            interval = d2 - d1
            self.log.info("time: %dseconds" %(interval.seconds))
            self.log.info("------------------------------------------------------------")
            resultList = []
            resultList.append(y_true)
            resultList.append(y_pred)
            DicResult[name] = resultList
        return DicResult
    
