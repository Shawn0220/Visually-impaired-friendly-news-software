import os
import pickle
import tensorflow as tf
import re
from my_bert_ner.utils import create_model, get_logger
from my_bert_ner.model import Model
from my_bert_ner.loader import input_from_line
from my_bert_ner.train import FLAGS, load_config


os.environ['CUDA_VISIBLE_DEVICES'] = '0'
config = load_config(FLAGS.config_file)
logger = get_logger(FLAGS.log_file)
# limit GPU memory
tf_config = tf.ConfigProto()
tf_config.gpu_options.allow_growth = True
f = open(FLAGS.map_file, "rb")
tag_to_id, id_to_tag = pickle.load(f)
sess = tf.Session(config=tf_config)
model = create_model(sess, Model, FLAGS.ckpt_path, config, logger)


def getentity(sentence):
    line = sentence
    result = model.evaluate_line(sess, input_from_line(line, FLAGS.max_seq_len, tag_to_id), id_to_tag)
    #print(result['entities'])
    entityArr = []
    for entity in result['entities']:
        entityArr.append(entity['word'])
        print(entity['word'])
    print(entityArr)


    for i in range(1,len(entityArr)+1):
    # 正则表达式提取文字串
        mystring = entityArr[i-1]
        r = '[’"#$%&\'()*+-./:;<=>?@[\\]\b\r^_`{|}~\n\0，\t]+'
        line = re.sub(r, '', mystring)
        line.replace(" ", "")
        entityArr[i-1] = line

    entityArr = list(set(entityArr))
    return str(entityArr)


if __name__ == '__main__':
    out = getentity('我在常州遇到了章节')
    out0 = getentity('我在南通遇到了刘翔')
    # print(out)
    # print(out0)