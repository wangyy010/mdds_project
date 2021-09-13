#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
import numpy as np
from algorithm_use import ClusteringMixData
from utils.common import Logger, LogLevel, LogMode, Utils
from sklearn.metrics import classification_report
from sklearn import metrics

class MyVModelConst:
    CONFIG_FILE_PATH = "myVModel.ini"

    
def sensitveInfoTest(rate):
    d1 = datetime.datetime.now()
    # set my model
    model = ClusteringMixData(MyVModelConst.CONFIG_FILE_PATH, theLogger=Logger())
    model.startTime = datetime.datetime.now()
    
    # Build logger
    model._createLogDir(model._getLogDir())
    logLevel = LogLevel.INFO
    logger = Logger(theLevel=logLevel,
                    theMode=LogMode.FILE,
                    theLogFile='%s/%s-MyVModel-run.log' \
                    % (model._getLogDir(), \
                    Utils.getTimeAsString(model.startTime)),
                    thePrintAlwaysFlag=True)
    model.log = logger

    model.log.info("#################### Experimental description ###################")
    model.log.info("Test model size: %f" %rate)
    model.log.info("Classing algorithm: "+"from gensim")
    model.log.info("Show best results!")
    model.log.info("Add more action after analysis raw data")
    model.log.info("#################### Experimental description ####################")
    
    blacklist_file = open('12000_bad_pdfs.txt')
    whitelist_file = open('12000_good_pdfs.txt')
    pos_data = []
    neg_data = []
    pos_set = set()
    neg_set = set()
    for line in blacklist_file.readlines():
        nodes = line.strip('\n').split(',')
        tempList = []
        flag = None
        for index in range(len(nodes)):
            flag = nodes[index]
            tempList.append(int(nodes[index]))
        pos_data.append(tempList)
        pos_set.add(line)
    print 'pos_set_length: %d' %(len(pos_set))
        
    for line in whitelist_file.readlines():
        nodes = line.strip('\n').split(',')
        tempList = []
        for index in range(len(nodes)):
            flag = nodes[index]
            tempList.append(int(nodes[index]))
        neg_data.append(tempList) 	
        neg_set.add(line)
    print 'neg_set_length: %d' %(len(neg_set))
        
    model.log.info("The length of pos_data is:"+str(len(pos_data)))
    model.log.info("The length of neg_data is:"+str(len(neg_data)))
        
    if len(pos_data)==0 or len(neg_data)==0: return
        
    dimension = len(pos_data[0])
    model.log.info('The length of dimension is: %d' %(dimension))
        
    X = np.concatenate((pos_data, neg_data))
    X_vec = []
    for item in X:
        X_vec.append(tuple(item.tolist()))
 
    d2 = datetime.datetime.now()
    interval = d2 - d1
    model.log.info("preprocessing time: %dseconds" %(interval.seconds))
        
    y = np.concatenate((np.ones(len(pos_data)), np.zeros(len(neg_data))))
    dictResult = model.testModel(X_vec, y, rate)
    
    names = ["Nearest Neighbors", "Linear SVM", "RBF SVM",
             "Decision Tree", "Random Forest", "AdaBoost",
             "LogisticRegression", "GradientBoostingClassifier", "MLPClassifier"]
    
    # Select best results
    model.log.info('\n\n')
    model.log.info('*********************** Best result: ***********************') 
    totalY_true = []
    totalY_pred = []
    totalWhiteDistri = []
    totalBlackDistri = []


    tmpY_true = []
    tmpY_pred = []
    bestOverall_accuracy = 0
    bestMethod = ''
    for name in names:
        y_true = dictResult[name][0]
        y_pred = dictResult[name][1]
        overall_accuracy = metrics.accuracy_score(y_true, y_pred)
        if (overall_accuracy > bestOverall_accuracy):
            bestMethod = name
            bestOverall_accuracy = overall_accuracy
            tmpY_true = y_true
            tmpY_pred = y_pred
            
    model.log.info('Best method: ' + bestMethod)
    model.log.info('Best accuracy: '+str(bestOverall_accuracy))
    totalY_true = tmpY_true.tolist()
    totalY_pred = tmpY_pred.tolist() 
    
    totalY_trueA = np.array(totalY_true)
    totalY_predA = np.array(totalY_pred)
    
    result = classification_report(totalY_trueA, totalY_pred,digits=4)
    model.log.info('----------------classification report:----------------\n%s' %result)

    confusion = metrics.confusion_matrix(totalY_trueA, totalY_predA)
    TP = confusion[1,1]
    TN = confusion[0,0]
    FP = confusion[0,1]
    FN = confusion[1,0]
    accuracy = (TP+TN) / float(TP+TN+FN+FP)
    model.log.info('classfication accuracy: %f' %accuracy)

    error = (FP+FN) / float(TP+TN+FN+FP)
    model.log.info('Classification Error: %f' %error)

    recall = TP / float(TP+FN)
    model.log.info('Sensitivity Recall: %f' %recall)

    specificity = TN / float(TN+FP)
    model.log.info('Specificity: %f' %specificity)

    false_positive_rate = FP / float(TN+FP)
    model.log.info('False Positive Rate: %f' %false_positive_rate)
			
    precision = TP / float(TP+FP)
    model.log.info('Precision: %f' %precision)
            
    auc = metrics.roc_auc_score(y_true, y_pred)
    model.log.info('auc: %f' %auc)
            
    d2 = datetime.datetime.now()
    interval = d2 - d1
    model.log.info("time: %dseconds" %(interval.seconds))
    model.log.info("------------------------------------------------------------")
    model.log.log.close()

if __name__ == "__main__":
    sensitveInfoTest(rate=0.5)
