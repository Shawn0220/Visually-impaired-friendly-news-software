# coding: utf-8

from __future__ import print_function

import os
import tensorflow as tf
import re
import tensorflow.contrib.keras as kr

from predict.cnn_model import TCNNConfig, TextCNN
from predict.data.cnews_loader import read_category, read_vocab

try:
    bool(type(unicode))
except NameError:
    unicode = str

base_dir = os.path.abspath(os.path.dirname(__file__))
vocab_dir = base_dir + '\\data\\vocab.txt'

save_path = base_dir + '\\checkpoints\\textcnn\\best_validation' # 最佳验证结果保存路径

# def loadtestdemo(filepath):
#     filenames = os.listdir(filepath)
#     result=[]
#     for filename in filenames:
#         f=open(os.path.join(filepath,filename), 'r', encoding='utf-8', errors='ignore')
#         str=f.read()
#         f.close()
#         result.append(str)
#     return result


class CnnModel:
    def __init__(self):
        self.config = TCNNConfig()
        self.categories, self.cat_to_id = read_category()
        self.words, self.word_to_id = read_vocab(vocab_dir)
        self.config.vocab_size = len(self.words)
        self.model = TextCNN(self.config)

        self.session = tf.Session()
        self.session.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        saver.restore(sess=self.session, save_path=save_path)  # 读取保存的模型

    def predict(self, message):
        # 支持不论在python2还是python3下训练的模型都可以在2或者3的环境下运行
        content = unicode(message)
        data = [self.word_to_id[x] for x in content if x in self.word_to_id]

        feed_dict = {
            self.model.input_x: kr.preprocessing.sequence.pad_sequences([data], self.config.seq_length),
            self.model.keep_prob: 1.0
        }

        y_pred_cls = self.session.run(self.model.y_pred_cls, feed_dict=feed_dict)
        return self.categories[y_pred_cls[0]]


cnn_model = CnnModel()  # 创建神经网络实例


def main(data):
    if not isinstance(data, str):
        data = str(data)
    r = re.compile(u"[^\u4e00-\u9fa5]+").sub('', data)
    result = cnn_model.predict(r)
    print(result)
    return result


def main2(data):
    d = data
    print(d)
    results = []       # 用于保存结果
    print("遍历新闻")
    for i in d:     # 遍历新闻
        if not isinstance(i, str):
            i = str(i)
        r = re.compile(u"[^\u4e00-\u9fa5]+").sub('', i)
        result = cnn_model.predict(r)  # 调用神经网络预测
        results.append(result)       # 保存结果
    print("返回结果")
    return results
