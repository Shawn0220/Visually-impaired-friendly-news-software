from bottle import Bottle, run, request, response
import json
import text2voice
import imgElements
import img2text
import voice2text
import recommender
import NewsQT.predict.newsclass
import NewsQT.predict.cnn_model
import NewsQT.predict.cnews_loader

app = Bottle()


# 文本转语音
@app.post('/text2voice')
def textToVoice():
    text = json.load(request.body)
    # print(text)
    print("文本转语音启动")
    data = {
        "voice": text2voice.getVoice(text["text"])
    }
    response.content_type = 'application/json'
    return json.dumps(data)

    # return "hello"


# 获取图片中物品的类别
@app.post('/imgElements')
def imgclasses():
    img = json.load(request.body)
    # print(img["img_base64"])
    print("图像识别启动")
    data = {
        "text": imgElements.imgclass(img["img_base64"]),
        "classes": imgElements.getVoice(img["img_base64"])
    }
    response.content_type = 'application/json'
    return json.dumps(data)


# 获取新闻分类
@app.post('/NewsQT/predict/newsclass')
def newsclasses():
    textstring = json.load(request.body)
    #print(textstring)
    # print(textstring["text"])
    print("新闻分类启动")
    data = {
        "class": NewsQT.predict.newsclass.newsclass(textstring["text"])
    }
    print(data)
    response.content_type = 'application/json;charset=utf-8'
    return json.dumps(data)


# 提取图片中文字
@app.post('/img2text')
def imgtotext():
    img = json.load(request.body)
    # print(img["img_base64"])
    print("图片文字识别启动")
    data = {
        "text": img2text.imgtotext(img["img_base64"])
    }
    response.content_type = 'application/json'
    return json.dumps(data)


# 音频转文本
@app.post('/voice2text')
def voicetotext():
    wav = json.load(request.body)
    # print(img["img_base64"])
    print("音频转文本启动")
    data = {
        "text": voice2text.voicetotext(wav["pcm_base64"])
    }
    # print(data["text"])
    response.content_type = 'application/json'
    return json.dumps(data)



# 新闻推荐
@app.post('/recommender')
def recmd():
    user = json.load(request.body)
    print("新闻推荐启动")
    data = {
        "news": recommender.myrecommender(user["user_id"], user["how_many"])
    }
    response.content_type = 'application/json'
    return json.dumps(data)


'''# 提取文本中的任命、地点、机构实体
@app.post('/my_bert_ner/mypredict')
def newsentities():
    text = json.load(request.body)
    data = {
        "entities":my_bert_ner.mypredict.getentity(text["text"])
    }
    response.content_type = 'application/json'
    return json.dumps(data)'''

app.run(host=' 10.6.150.214', port=18080, reloader=True)
