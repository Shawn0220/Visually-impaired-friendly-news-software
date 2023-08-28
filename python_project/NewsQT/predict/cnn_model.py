# coding: utf-8

import tensorflow as tf


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
            self.attention_W = tf.Variable(tf.random_uniform([self.config.embedding_dim, attention_hidden_dim], 0.0, 1.0),name="attention_W")
            self.attention_U = tf.Variable(tf.random_uniform([self.config.embedding_dim, attention_hidden_dim], 0.0, 1.0),name="attention_U")
            self.attention_V = tf.Variable(tf.random_uniform([attention_hidden_dim, 1], 0.0, 1.0),name="attention_V")
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
                input_conv = tf.reshape(tf.concat(self.output_att, axis=1),[-1, self.config.seq_length, self.config.embedding_dim * 2],name="input_convolution")
            self.input_conv_expanded = input_conv
        else:
            self.input_conv_expanded = embedding_inputs
        # dim_input_conv = self.input_conv_expanded.shape[-2].value

        with tf.name_scope("cnn"):
            conv1 = tf.layers.conv1d(self.input_conv_expanded, self.config.num_filters, self.config.kernel_size, name='conv1')
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
