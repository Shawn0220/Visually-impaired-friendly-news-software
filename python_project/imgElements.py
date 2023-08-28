import urllib.parse
import copy
import hmac
import time
import urllib.parse
from hashlib import sha1
from hashlib import sha256
import base64
import requests
import json
import uuid
import wave
import os

RESOURCE_URL = u'https://api-wuxi-1.cmecloud.cn:8443'  # 调用ecloud API源URL，RESOURCE_URL + query_servlet_path = 调用API的URL

AK = 'c37f8556d0e74165b2404a1407fb21ea'
SK = 'c083b63dc5564fe5bdccd55aafd618db'


def percent_encode(encode_str):
    """
    encode string to url code
    :param encode_str:  str
    :return:
    """
    encode_str = str(encode_str)
    res = urllib.parse.quote(encode_str.encode('utf-8'), '')
    res = res.replace('+', '%20')
    res = res.replace('*', '%2A')
    res = res.replace('%7E', '~')
    return res


def sign(http_method, playlocd, servlet_path, secret_key):
    parameters = copy.deepcopy(playlocd)
    parameters.pop('Signature')
    sorted_parameters = sorted(parameters.items(), key=lambda parameters: parameters[0])
    canonicalized_query_string = ''
    for (k, v) in sorted_parameters:
        canonicalized_query_string += '&{}={}'.format(percent_encode(k), percent_encode(v))

    string_to_sign = '{}\n{}\n{}'.format(http_method, percent_encode(servlet_path),
                                         sha256(canonicalized_query_string[1:].encode('utf-8')).hexdigest())

    key = ("BC_SIGNATURE&" + secret_key).encode('utf-8')

    string_to_sign = string_to_sign.encode('utf-8')
    signature = hmac.new(key, string_to_sign, sha1).hexdigest()
    return signature


def fetch_public_params(http_method, access_key, secret_key, servlet_path, params=None):
    """
    通过AK、SK获取密钥（密钥具有时效性）
    PS：此处为了调用方便已忽略ssl安全验证
    :return: access token
    """
    time_str = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime())
    random_uuid = str(uuid.uuid4())
    param = {
        'Version': '2016-12-05',
        'AccessKey': access_key,
        'Timestamp': time_str,
        'Signature': '',
        'SignatureMethod': 'HmacSHA1',
        'SignatureNonce': random_uuid,
        'SignatureVersion': 'V2.0',
    }

    if params is not None:
        for (k, v) in params.items():
            param.setdefault(k, v)

    param['Signature'] = sign(http_method, param, servlet_path, secret_key)

    return param


def fetch_img(imgbase64):  # 读取图片文件，返回json数据
    """
    构建输入样例
    :return:    example data
    """
    data = {
        "image": imgbase64,
    }
    return json.dumps(data)


# file_path = r'C:\Users\52954\Desktop\test.png'

def fetch_headers():  # 公共请求头参数
    headers = {
        'Content-Type': 'application/json',
    }
    return headers


def myRequest(method, servlet_path, data=None, params=None, headers=None):
    url = RESOURCE_URL + servlet_path

    pub_params = fetch_public_params(method, access_key=AK, secret_key=SK, servlet_path=servlet_path, params=params)

    token_response = requests.request(method=method, url=url, params=pub_params,
                                      data=data, headers=headers, verify=False)

    url = urllib.parse.unquote(token_response.url, 'ISO-8859-1')
    return token_response.json()


def imgclass(imgbase64):
    # URI
    query_servlet_path = '/api/generalimgrecog/v1/generalImageDetect'
    response = myRequest('POST', servlet_path=query_servlet_path,
                         data=fetch_img(imgbase64), headers=fetch_headers())
    # print(response)
    classes = response['body'][0]['classes']
    print(classes)
    x = classes
    return "您照片里的东西包括" + x + "本次识别结束"


def base64towav(base64_str):
    wav_out = "cache.wav"
    data_raw = base64.b64decode(base64_str)
    with wave.open(wav_out, 'wb') as wav_file:
        wav_file.setframerate(16000)
        wav_file.setsampwidth(2)
        wav_file.setnchannels(1)
        wav_file.writeframes(data_raw)
    with open(wav_out, "rb") as wav_file:
        wav_data = base64.b64encode(wav_file.read())
    os.remove("cache.wav")
    return wav_data


def voice_sender(text):
    data = {
        "text": text,
        "sessionParam": {
            "sid": "3",
            "frame_size": 640,
            "audio_coding": "raw",
            "native_voice_name": "yiping",
            "speed": 75,
            "volume": 0,
            "read_all_marks": 0,
            "read_number": 0,
            "read_english": 0
        },
    }
    return json.dumps(data)


def getVoice(imgbase64):
    # a = datetime.datetime.now()
    text = imgclass((imgbase64))
    send_query_servlet_path = '/api/lingxiyun/cloud/tts/v1'
    sender_response = myRequest('POST', servlet_path=send_query_servlet_path,
                                data=voice_sender(text), headers=fetch_headers())
    base64_str = sender_response['body']['data']
    return "data:audio/wav;base64," + str(base64towav(base64_str), 'ascii', 'ignore')
