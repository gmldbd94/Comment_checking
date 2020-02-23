import os
import random


from konlpy.tag import Twitter, Okt
import gensim
from smart_open import open
import tensorflow as tf
import numpy as np
import codecs


def read_data(filename):
    with open(filename, 'r', encoding='utf-16') as f:
        data = [line.split('\t') for line in f.read().splitlines()]
        data = data[1:]  # header 제외 #
    return data

# 데이터 전처리 과정
data = read_data('train.txt')
random.shuffle(data)
# 데이터 길이 확인
length = data.__len__();
print(length)

train_data = []
test_data =[]
for i in range(0, 3000):
    train_data.append(data[i])
for i in range(3001, 4228):
    test_data.append(data[i])
#train_set 생성
f = open("train_set.txt", 'a')
for i in range(0, 3000):
    f.writelines(['\n', train_data[i][1]+'\t'+train_data[i][2]])
f.close

#test_set 생성
p = open("test_set.txt", 'a')
for i in range(0,1227):
    p.writelines(['\n', test_data[i][1]+'\t'+test_data[i][2]])
p.close

# print(train_data)
# print(test_data)
pos_tagger = Okt()

os.getcwd()
os.chdir("model")
def tokenize(doc):
    return ['/'.join(t) for t in pos_tagger.pos(doc, norm=True, stem=True)]

## training Word2Vec model using skip-gram
tokens = [tokenize(row[1]) for row in train_data]
model = gensim.models.Word2Vec(size=300, sg=1, alpha=0.025, min_alpha=0.025, seed=1234)
model.build_vocab(tokens)

for epoch in range(30):
    model.train(tokens, total_examples=model.corpus_count, epochs=model.iter)
    model.alpha -= 0.002
    model.min_alpha = model.alpha

model.save("Word2vec.model")