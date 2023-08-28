from bottle import Bottle, run, request, response
import json
import mypredict


app = Bottle()


# 提取文本中的任命、地点、机构实体
@app.post('/mypredict')
def newsentities():
    text = json.load(request.body)
    print("Bert实体识别启动")
    data = {
        "entities": mypredict.getentity(text["text"])
    }
    print(data)
    response.content_type = 'application/json'
    return json.dumps(data)


app.run(host='10.11.12.22', port=18081, reloader=True)