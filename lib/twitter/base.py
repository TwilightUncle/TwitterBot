import os
import abc
import time
import urllib.parse
import urllib.request
import hmac
import hashlib
import base64
import json
import configparser
import copy

import random, string
from lib.twitter.exception import TwitterRequiredParameterError


def generateRandomString(n:int) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


class TwitterApiBaseClient(object, metaclass=abc.ABCMeta):
    '''Twitter APIクライアントの基底クラス
    \n# 署名作成参考記事
    \nhttp://westplain.sakuraweb.com/translate/twitter/Documentation/OAuth/Overview/Creating-a-signature.cgi
    \n# 認証ヘッダ作成参考記事
    \nhttp://westplain.sakuraweb.com/translate/twitter/Documentation/OAuth/Overview/Authorizing-a-request.cgi
    '''


    __BASE_URL = 'https://api.twitter.com/1.1/'
    __CONFIG_PATH = './instance/twitter_api.cfg' # 必要に応じて書き換える


    def __init__(self, api_key='', api_secret='', access_token='', access_secret=''):
        # if argments is not set, the constructor reads config and set default parameter.
        if api_key == '' or api_secret == '' or access_token == '' or access_secret == '':
            if not os.path.exists(self.__class__.__CONFIG_PATH):
                raise IOError(self.__class__.__CONFIG_PATH)

            cfg = configparser.ConfigParser()
            cfg.read(self.__class__.__CONFIG_PATH, 'UTF-8')

            if api_key == '':
                api_key         = cfg.get('default', 'TWITTER_API_CONSUMER_KEY')
            if api_secret == '':
                api_secret      = cfg.get('default', 'TWITTER_API_CONSUMER_KEY_SECRET')
            if access_token == '':
                access_token    = cfg.get('default', 'TWITTER_API_ACCESS_TOKEN')
            if access_secret == '':
                access_secret   = cfg.get('default', 'TWITTER_API_ACCESS_TOKEN_SECRET')
            
        self.__API_KEY          = api_key
        self.__API_SECRET       = api_secret
        self.__ACCESS_TOKEN     = access_token
        self.__ACCESS_SECRET    = access_secret
        self.__ENDPOINT         = self.__class__.__BASE_URL + self._endpoint()
        self.__REQUEST_METHOD   = self._requestMethod().upper()

        self.__request_params   = None
        self.__request_params_raw = {}

        # response
        self.__status           = None
        self.__headers          = None
        self.__contents         = None
    

    def setParam(self, key:str, value:str):
        self.__request_params_raw[key] = value


    def exec(self) -> str:
        '''リクエスト実行
        '''
        endpoint = self.__ENDPOINT
        req = None
        if self.__REQUEST_METHOD == 'GET':
            query_param_string  = urllib.parse.urlencode(self.__getRequestParams())
            endpoint           += '?' + query_param_string
            req                 = urllib.request.Request(endpoint)
        elif self.__REQUEST_METHOD == 'POST':
            encoded_params      = json.dumps(self.__getRequestParams()).encode()
            req                 = urllib.request.Request(endpoint, encoded_params)
            req.add_header('Content-Type', 'application/json')
        else:
            # invaild Http method
            return None
        
        req.add_header('Authorization', self.__buildOAuthHeader())
        response = None
        with urllib.request.urlopen(req) as res:
            self.__status   = res.status
            self.__headers  = res.getheaders()
            response        = res.read().decode('utf-8')
            self.__contents = json.loads(response)
        

    def getStatus(self):
        return self.__status
    

    def getHeaders(self):
        return self.__headers
    

    def getContents(self):
        return self.__contents


    def __buildOAuthHeader(self) -> str:
        signature_params = {
            'oauth_token'               : self.__ACCESS_TOKEN,
            'oauth_consumer_key'        : self.__API_KEY,
            'oauth_signature_method'    : 'HMAC-SHA1',
            'oauth_timestamp'           : str(int(time.time())),
            'oauth_nonce'               : generateRandomString(32),
            'oauth_version'             : '1.0'
        }
        auth_header_params = copy.copy(signature_params)
        # join request params
        signature_params.update(self.__getRequestParams())
        # sort and urlencode
        sorted_params           = sorted(signature_params.items(),key=lambda x:x[0])
        encoded_params          = urllib.parse.urlencode(sorted_params)
        encoded_params          = urllib.parse.quote(encoded_params) # 更にエンコードが必要
        encoded_key             = urllib.parse.quote(self.__API_SECRET) + '&' + urllib.parse.quote(self.__ACCESS_SECRET)
        encoded_url             = urllib.parse.quote(self.__ENDPOINT, safe='')
        # make base string
        signature_base_string   = self.__REQUEST_METHOD + '&' + encoded_url + '&' + encoded_params
        # make signature
        signature_hash          = hmac.new(
            encoded_key.encode('utf-8'), 
            signature_base_string.encode('utf-8'), 
            hashlib.sha1
        ).digest()
        signature               = base64.b64encode(signature_hash)
        # header params
        auth_header_params['oauth_signature'] = signature.strip().decode('utf-8')
        sorted_auth_params = sorted(auth_header_params.items(), key=lambda  x:x[0])
        # make auth header
        str_list = []
        for k, v in sorted_auth_params:
            str_list.append('{}="{}"'.format(urllib.parse.quote(k), urllib.parse.quote(v)))

        return 'OAuth ' + ', '.join(str_list)
    

    def __getRequestParams(self) -> dict:
        if self.__request_params is None:
            # check required params
            for key in self._getRequiredParameterKeys():
                try:
                    no_use = self.__request_params_raw[key]
                except KeyError:
                    # 例外を置き換える
                    raise TwitterRequiredParameterError("Required request parameter '{}' is not set".format(key))
            
            self.__request_params = self.__request_params_raw
        
        return self.__request_params


    @abc.abstractmethod
    def _endpoint(self) -> str:
        raise NotImplementedError()


    @abc.abstractmethod
    def _requestMethod(self) -> str:
        raise NotImplementedError()


    @abc.abstractmethod
    def _getRequiredParameterKeys(self) -> list:
        '''必須パラメータのキー一覧'''
        raise NotImplementedError()
