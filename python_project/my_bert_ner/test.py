from bottle import route,run
@route('/')
def home():
    return "it's my homepage"


run(host='localhost',port=9999)