# coding: utf-8

from __future__ import print_function

import os
import re
import tensorflow.contrib.keras as kr

# coding: utf-8

import tensorflow as tf
# coding: utf-8

import sys
from collections import Counter

import numpy as np
#import pandas as pd
import tensorflow.keras as kr

if sys.version_info[0] > 2:
    is_py3 = True
else:
    reload(sys)
    sys.setdefaultencoding("utf-8")
    is_py3 = False

cat=['财经', '房产', '教育', '科技', '军事', '汽车', '体育', '游戏', '娱乐', '其他']

def native_word(word, encoding='utf-8'):
    """如果在python2下面使用python3训练的模型，可考虑调用此函数转化一下字符编码"""
    if not is_py3:
        return word.encode(encoding)
    else:
        return word


def native_content(content):
    if not is_py3:
        return content.decode('utf-8')
    else:
        return content


def open_file(filename, mode='r'):
    """
    常用文件操作，可在python2和python3间切换.
    mode: 'r' or 'w' for read or write
    """
    if is_py3:
        return open(filename, mode, encoding='utf-8', errors='ignore')
    else:
        return open(filename, mode)

def read_tsvfile(filename):
    contents, labels = [], []
    with open_file(filename) as f:
        for line in f:
            try:
                label, content = line.strip().split('\t')
                if content:
                    contents.append(native_content(content))
                    labels.append(native_content(label))
            except:
                pass
    return contents, labels

def read_file(filename):
    """读取文件数据"""
    contents, labels = [], []
    with open_file(filename) as f:
        for line in f:
            try:
                label, content = line.strip().split('\t')
                if content:
                    contents.append(list(native_content(content)))
                    labels.append(native_content(label))
            except:
                pass
    return contents, labels


def build_vocab(train_dir, vocab_dir, vocab_size=6000):
    """根据训练集构建词汇表，存储"""
    data_train, _ = read_file(train_dir)

    all_data = []
    for content in data_train:
        all_data.extend(content)

    counter = Counter(all_data)
    count_pairs = counter.most_common(vocab_size - 1)
    words, _ = list(zip(*count_pairs))
    # 添加一个 <PAD> 来将所有文本pad为同一长度
    words = ['<PAD>'] + list(words)
    open_file(vocab_dir, mode='w').write('\n'.join(words) + '\n')


def read_vocab(vocab_dir):
    """读取词汇表"""
    # words = open_file(vocab_dir).read().strip().split('\n')
    with open_file(vocab_dir) as fp:
        # 如果是py2 则每个值都转化为unicode
        words = [native_content(_.strip()) for _ in fp.readlines()]
    word_to_id = dict(zip(words, range(len(words))))
    return words, word_to_id


def read_category():
    """读取分类目录，固定"""

    categories = cat

    categories = [native_content(x) for x in categories]

    cat_to_id = dict(zip(categories, range(len(categories))))

    return categories, cat_to_id

def to_words(content, words):
    """将id表示的内容转换为文字"""
    return ''.join(words[x] for x in content)


def process_file(filename, word_to_id, cat_to_id, max_length=600):
    """将文件转换为id表示"""
    contents, labels = read_file(filename)

    data_id, label_id = [], []
    for i in range(len(contents)):
        data_id.append([word_to_id[x] for x in contents[i] if x in word_to_id])
        label_id.append(cat_to_id[labels[i]])

    # 使用keras提供的pad_sequences来将文本pad为固定长度
    x_pad = kr.preprocessing.sequence.pad_sequences(data_id, max_length)
    y_pad = kr.utils.to_categorical(label_id, num_classes=len(cat_to_id))  # 将标签转换为one-hot表示

    return x_pad, y_pad


def batch_iter(x, y, batch_size=64):
    """生成批次数据"""
    data_len = len(x)
    num_batch = int((data_len - 1) / batch_size) + 1

    indices = np.random.permutation(np.arange(data_len))
    x_shuffle = x[indices]
    y_shuffle = y[indices]

    for i in range(num_batch):
        start_id = i * batch_size
        end_id = min((i + 1) * batch_size, data_len)
        yield x_shuffle[start_id:end_id], y_shuffle[start_id:end_id]



class TCNNConfig(object):
    """CNN配置参数"""

    embedding_dim = 64  # 词向量维度
    seq_length = 600  # 序列长度
    num_classes = 10  # 类别数
    num_filters = 256  # 卷积核数目
    kernel_size = 5  # 卷积核尺寸
    vocab_size = 6000  # 词汇表达小

    hidden_dim = 128  # 全连接层神经元
    hidden_dim2 = 64  # 全连接层神经元

    dropout_keep_prob = 0.5  # dropout保留比例
    learning_rate = 1e-3  # 学习率

    batch_size = 64  # 每批训练大小
    num_epochs = 10  # 总迭代轮次

    print_per_batch = 50  # 每多少轮输出一次结果
    save_per_batch = 10  # 每多少轮存入tensorboard

    use_attention = False
    attention_dim = 10


class TextCNN(object):
    """文本分类，CNN模型"""

    def __init__(self, config):
        self.config = config

        # 三个待输入的数据
        self.input_x = tf.placeholder(tf.int32, [None, self.config.seq_length], name='input_x')
        self.input_y = tf.placeholder(tf.float32, [None, self.config.num_classes], name='input_y')
        self.keep_prob = tf.placeholder(tf.float32, name='keep_prob')

        self.cnn()

    def attention(self, x_i, x, index):
        """
        Attention model for Neural Machine Translation
        :param x_i: the embedded input at time i
        :param x: the embedded input of all times(x_j of attentions)
        :param index: step of time
        """
        e_i = []
        c_i = []
        for output in x:
            output = tf.reshape(output, [-1, self.config.embedding_dim])
            atten_hidden = tf.tanh(tf.add(tf.matmul(x_i, self.attention_W), tf.matmul(output, self.attention_U)))
            e_i_j = tf.matmul(atten_hidden, self.attention_V)
            e_i.append(e_i_j)
        e_i = tf.concat(e_i, axis=1)
        # e_i = tf.exp(e_i)
        alpha_i = tf.nn.softmax(e_i)
        alpha_i = tf.split(alpha_i, self.config.seq_length, 1)
        # i!=j
        for j, (alpha_i_j, output) in enumerate(zip(alpha_i, x)):
            if j == index:
                continue
            else:
                output = tf.reshape(output, [-1, self.config.embedding_dim])
                c_i_j = tf.multiply(alpha_i_j, output)
                c_i.append(c_i_j)
        c_i = tf.reshape(tf.concat(c_i, axis=1), [-1, self.config.seq_length - 1, self.config.embedding_dim])
        c_i = tf.reduce_sum(c_i, 1)
        return c_i

    def cnn(self):
        """CNN模型"""
        # 词向量映射
        with tf.device('/cpu:0'):
            embedding = tf.get_variable('embedding', [self.config.vocab_size, self.config.embedding_dim])
            embedding_inputs = tf.nn.embedding_lookup(embedding, self.input_x)

        if self.config.use_attention:
            attention_hidden_dim = self.config.attention_dim
            # Wa = [attention_W  attention_U]
            self.attention_W = tf.Variable(
                tf.random_uniform([self.config.embedding_dim, attention_hidden_dim], 0.0, 1.0), name="attention_W")
            self.attention_U = tf.Variable(
                tf.random_uniform([self.config.embedding_dim, attention_hidden_dim], 0.0, 1.0), name="attention_U")
            self.attention_V = tf.Variable(tf.random_uniform([attention_hidden_dim, 1], 0.0, 1.0), name="attention_V")
            # attention layer before convolution
            self.output_att = list()
            with tf.name_scope("attention"):
                input_att = tf.split(embedding_inputs, self.config.seq_length, axis=1)
                for index, x_i in enumerate(input_att):
                    x_i = tf.reshape(x_i, [-1, self.config.embedding_dim])
                    if index % 10 == 0:
                        print("*********" + str(index) + "**********")
                    c_i = self.attention(x_i, input_att, index)
                    inp = tf.concat([x_i, c_i], axis=1)
                    self.output_att.append(inp)
                input_conv = tf.reshape(tf.concat(self.output_att, axis=1),
                                        [-1, self.config.seq_length, self.config.embedding_dim * 2],
                                        name="input_convolution")
            self.input_conv_expanded = input_conv
        else:
            self.input_conv_expanded = embedding_inputs
        # dim_input_conv = self.input_conv_expanded.shape[-2].value

        with tf.name_scope("cnn"):
            conv1 = tf.layers.conv1d(self.input_conv_expanded, self.config.num_filters, self.config.kernel_size,
                                     name='conv1')
            # pool1 = tf.layers.max_pooling1d(conv1, pool_size=2,strides=2,name='pooling1')
            # conv2 = tf.layers.conv1d(pool1, self.config.num_filters, self.config.kernel_size+3, name='conv2')
            pool1 = tf.reduce_max(conv1, reduction_indices=[1], name='pooling2')

        with tf.name_scope("score"):
            # 全连接层，后面接dropout以及relu激活
            fc1 = tf.layers.dense(pool1, self.config.hidden_dim, name='fc1')
            fc1 = tf.contrib.layers.dropout(fc1, self.keep_prob)
            fc1 = tf.nn.tanh(fc1)
            # 分类器
            self.logits = tf.layers.dense(fc1, self.config.num_classes, name='fc3')
            self.y_pred_cls = tf.argmax(tf.nn.softmax(self.logits), 1)  # 预测类别

        with tf.name_scope("optimize"):
            # 损失函数，交叉熵
            cross_entropy = tf.nn.softmax_cross_entropy_with_logits(logits=self.logits, labels=self.input_y)
            self.loss = tf.reduce_mean(cross_entropy)
            # 优化器
            self.optim = tf.train.AdamOptimizer(learning_rate=self.config.learning_rate).minimize(self.loss)

        with tf.name_scope("accuracy"):
            # 准确率
            correct_pred = tf.equal(tf.argmax(self.input_y, 1), self.y_pred_cls)

            self.acc = tf.reduce_mean(tf.cast(correct_pred, tf.float32))


base_dir = os.path.abspath(os.path.dirname(__file__))

vocab_dir = base_dir + '\\data\\vocab.txt'

save_path = base_dir + '\\checkpoints\\textcnn\\best_validation'  # 最佳验证结果保存路径

try:
    bool(type(unicode))
except NameError:
    unicode = str

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

def newsclass(textstring):
    data = textstring
    print(data)
    if not isinstance(data, str):
        data = str(data)
    r = re.compile(u"[^\u4e00-\u9fa5]+").sub('', data)
    result = cnn_model.predict(r)
    print(result)
    return result


if __name__ == '__main__':
    x = newsclass('教培行业受到冲击，新东方何去何从')
    print(x)