import os
import numpy as np
import pandas as pd
import pickle

os.chdir("C:\\Users\\sojeo\\OneDrive\\바탕 화면\\SJ_practice")

# Document Classifier
class NaiveBayesClassifier() :
    def __init__(self) :
        pass
    def _tokenize(self, docs) :
        return [d.split() for d in docs]

    # 사전확률, 우도 학습
    def train(self, docs, labels, k = 0.5, model='nbc.model'):

        #label별 인덱스 지정
        label2i = {k:i for i, k in enumerate(np.unique(labels))}
        self.i2label = {i:k for k, i in label2i.items()}
        label_prob = np.zeros(len(label2i))
        tokenized_docs = self._tokenize(docs)

        #label별 빈도 계산
        nbc_dic = {}
        for i, doc in enumerate(tokenized_docs) :
            for w in doc :
                if w in nbc_dic.keys() :
                    nbc_dic[w]['count'][label2i[labels[i]]] += 1
                else :
                    nbc_dic[w] = {'count' : np.zeros(len(label2i)), 'prob' : np.zeros(len(label2i)), 'log_prob' : np.zeros(len(label2i)) }
                    nbc_dic[w]['count'][label2i[labels[i]]] = 1
                label_prob[label2i[labels[i]]] += 1

        #확률 계산
        for w in nbc_dic.keys() :
            for label in label2i.keys() :
                nbc_dic[w]['prob'][label2i[label]] = (k + nbc_dic[w]['count'][label2i[label]]) / (2*k + label_prob[label2i[label]])
                nbc_dic[w]['log_prob'][label2i[label]] = np.log(nbc_dic[w]['prob'][label2i[label]] )

        self.nbc_dic = nbc_dic
        self.label2i = label2i
        self.label_prob = np.log(label_prob/label_prob.sum())

        with open(model, 'wb') as f :
            tmp = {'label_prob' : label_prob
            , 'nbc_dic' : self.nbc_dic
            , 'i2label' : self.i2label
            , 'label2i' : self.label2i}
            pickle.dump(tmp, f)

    # 새로운 문서 분류
    def predict(self, docs, model = None):
        if model :
            with open(model, 'rb') as f :
                tmp = pickle.load(f)
                self.label_prob = tmp['label_prob']
                self.nbc_dic = tmp['nbc_dic']
                self.i2label = tmp['i2label']
                self.label2i = tmp['label2i']

        tokenized_docs = self._tokenize(docs)
        results = []

        #라벨별 확률
        for d in tokenized_docs :
            prob_for_label = np.zeros(len(self.label2i))

            for w in d :
                for label, i in self.label2i.items() :
                    prob_for_label[i] += self.nbc_dic[w]['log_prob'][i]
            tmp = np.exp(prob_for_label + self.label_prob)
            prob = tmp / tmp.sum()

            results.append(self.i2label[prob.argsort()[::-1][0]])
        return results

    # 정확도 측정
    def score(self, docs, labels, model = None):
        predictions = self.predict(docs, model)
        return np.mean(np.array(predictions) == np.array(labels))

if __name__ == "__main__" :
    df_train = pd.read_csv("train.csv")
    df_test = pd.read_csv("test.csv")

    X_train, Y_train = df_train['mail'].tolist(), df_train['label'].tolist()
    X_test, Y_test = df_test['mail'].tolist(), df_test['label'].tolist()

    nbc = NaiveBayesClassifier()
    nbc.train(X_train, Y_train)
    #nbc.predict(X_test)
    # print(nbc.score(X_test, Y_test, model = 'nbc.model'))