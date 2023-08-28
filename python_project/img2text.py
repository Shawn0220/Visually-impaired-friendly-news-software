import copy
import hmac
import time
import urllib.parse
from hashlib import sha1
from hashlib import sha256
import requests
import json
import re
import uuid

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


def getimg2text(img_base64_src):
    '''with open(file_path_src, mode='rb') as f:
        img_base64_src = str(base64.b64encode(f.read()), encoding='utf8')'''
    data = {
        "image": str(img_base64_src),
    }

    return json.dumps(data)


# file_path = r'C:\Users\52954\Desktop\test.png'

def headers():  # 公共请求头参数
    headers = {
        'Content-Type': 'application/json',
    }
    return headers


def request_example(method, servlet_path, data=None, params=None, headers=None):
    url = RESOURCE_URL + servlet_path

    pub_params = fetch_public_params(method, access_key=AK, secret_key=SK, servlet_path=servlet_path, params=params)

    # post/get 请求，此处为了调用方便已忽略ssl安全验证
    token_response = requests.request(method=method, url=url, params=pub_params,
                                      data=data, headers=headers, verify=False)

    url = urllib.parse.unquote(token_response.url, 'ISO-8859-1')
    # print('url : %s' % url)
    # print(json.dumps(token_response.json(), indent=4, ensure_ascii=False))
    return token_response.json()


def imgtotext(img_base64_src):
    servlet_path = '/api/ocr/v1/general'
    sender_response = request_example('POST', servlet_path=servlet_path,
                                      data=getimg2text(img_base64_src), headers=headers())

    print(sender_response)
    try:
        mystring = str(sender_response["items"])
    except:
        print("图片未识别到文字")
        return "您的照片中未识别到文字，请重新拍摄哟"
    # 正则表达式提取文字串
    reP = re.compile(r"itemstring'(.+?)itemcoord", re.S)
    textArr = re.findall(reP, mystring)
    text = ''
    for mystr in textArr:
        text = text + mystr
    r = '[’"#$%&\'()*+-./:;<=>?@[\\]\b\r^_`{|}~\n\0，\t]+'
    line = re.sub(r, '', text)
    line.replace(" ", "")
    print(line)
    return str(line)
