#!/usr/bin/env python
# coding: utf-8


from Dataloader import *
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import pkuseg
import gensim
import pickle

def train():
    # 加载数据
    data = pd.read_csv('QA.csv', sep='\t')
    loader = data.drop('answer',axis=1)

    #处理加载的数据，建立索引，去重
    sentince_list = []
    sentince_index = []

    for st in loader.values:
        sentince_list.append(st[0])
        sentince_list.append(st[1])
        sentince_index.append((st[0],st[2]))
        sentince_index.append((st[1],st[2]))
    sentince_list = list(set(sentince_list))
    sentince_index = list(set(sentince_index))
    sentince_index = {each[0]:each[1] for each in sentince_index}



    #使用TF-IDF将句子转化为向量形式,形成矩阵
    seg = pkuseg.pkuseg()           # 以默认配置加载模型
    tfidf_vectorizer = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b", max_df=0.7)

    real_documents = []
    for item_text in sentince_list:
        item_str = seg.cut(item_text)
        real_documents.append(item_str)
    document = [" ".join(sent0) for sent0 in real_documents]

    tfidf_model = tfidf_vectorizer.fit(document)
    #print(tfidf_model.vocabulary_)

    #print(tfidf_vectorizer.idf_) #特征对应的权重
    #print(tfidf_vectorizer.get_feature_names())#特征词
    #print(real_vec.toarray()) #上面对话对应的向量表示
    sparse_result = tfidf_model.transform(document).todense()
    pickle.dump(tfidf_model,open("model.plk",'wb'))
    pickle.dump(sparse_result, open("vec.plk",'wb'))
    pickle.dump((sentince_list,sentince_index,data['answer'].values),open("list.plk",'wb'))

def predict(test_sentices):
    #测试句子转换

    tfidf_model = pickle.load(open("model.plk",'rb'))
    sparse_result = pickle.load(open("vec.plk",'rb'))
    saveList = pickle.load(open("list.plk",'rb'))
    test_documents = []
    seg = pkuseg.pkuseg()
    for item_text in test_sentices:
        item_str = seg.cut(item_text)
        test_documents.append(item_str)
    test_document = [" ".join(sent0) for sent0 in test_documents]
    result = tfidf_model.transform(test_document).todense()

    sentince_list = saveList[0]
    sentince_index = saveList[1]
    data = saveList[2]
    # data = pd.read_csv('QA.csv', sep='\t')
    # loader = data.drop('answer',axis=1)
    # for st in loader.values:
    #     sentince_list.append(st[0])
    #     sentince_list.append(st[1])
    #     sentince_index.append((st[0],st[2]))
    #     sentince_index.append((st[1],st[2]))
    # sentince_list = list(set(sentince_list))
    # sentince_index = list(set(sentince_index))
    # sentince_index = {each[0]:each[1] for each in sentince_index}

    #结果测试
    ans = result*sparse_result.T
    ans = ans.argmax(axis=1)
    answer = sentince_list[ans.tolist()[0][0]]
    answer = data[sentince_index[answer]]
    print(answer)
    return answer


if __name__ == "__main__":
    #train()
    predict(['刘玉老师是谁'])

