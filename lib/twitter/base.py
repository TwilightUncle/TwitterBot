import os
import sys
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
from lib.twitter.exception import TwitterRequiredParameterError, TwitterAPIClientError


def generateRandomString(n:int) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


class TwitterApiBaseClient(object, metaclass=abc.ABCMeta):
    '''Twitter APIクライアントの基底クラス
    \n# 署名作成参考記事
    \nhttp://westplain.sakuraweb.com/translate/twitter/Documentation/OAuth/Overview/Creating-a-signature.cgi
    \n# 認証ヘッダ作成参考記事
    \nhttp://westplain.sakuraweb.com/translate/twitter/Documentation/OAuth/Overview/Authorizing-a-request.cgi
    '''


    __BASE_URL = 'https://api.twitter.com/1.1'
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
        self.__REQUEST_METHOD   = self._requestMethod().upper()

        self.__request_params   = None
        self.__request_params_raw = {}

        self.__endpoint         = self.__class__.__BASE_URL

        self.__method_call_counter  = {}
        self.__method_call_rules    = self.__getMethodCallRules()
        self.__method_call_rules.update(self._getFunctionsCallRule())
        self.__is_executed          = False

        # response
        self.__status           = None
        self.__headers          = None
        self.__contents         = None
    

    # -----------------------------------------------------------------------
    # public methods
    # -----------------------------------------------------------------------


    def setParam(self, key:str, value:str):
        self._validateMethodCallCorrectness(sys._getframe().f_code.co_name)
        self.__request_params_raw[key] = value


    def exec(self) -> str:
        '''リクエスト実行
        '''
        self._validateMethodCallCorrectness(sys._getframe().f_code.co_name)
        self.__validateMethodCallCorrectness()

        query_param_string  = ''
        if len(self.__getRequestParams()) > 0:
            query_param_string  = '?' + urllib.parse.urlencode(self.__getRequestParams())
        
        endpoint            = self.__endpoint + query_param_string
        req                 = urllib.request.Request(endpoint, method=self.__REQUEST_METHOD)
        req.add_header('Authorization', self.__buildOAuthHeader())

        with urllib.request.urlopen(req) as res:
            self.__status   = res.status
            self.__headers  = res.getheaders()
            response        = res.read().decode('utf-8')
            self.__contents = json.loads(response)
        
        self.__is_executed = True
        

    def getStatus(self):
        '''exec実行後呼び出し(結果)'''
        self._validateMethodCallCorrectness(sys._getframe().f_code.co_name)
        return self.__status
    

    def getHeaders(self):
        '''exec実行後呼び出し(結果)'''
        self._validateMethodCallCorrectness(sys._getframe().f_code.co_name)
        return self.__headers
    

    def getContents(self):
        '''exec実行後呼び出し(結果)'''
        self._validateMethodCallCorrectness(sys._getframe().f_code.co_name)
        return self.__contents
    

    # -------------------------------------------------------------------------
    # private methods
    # -------------------------------------------------------------------------


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
        encoded_url             = urllib.parse.quote(self.__endpoint, safe='')
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
    

    def __getMethodCallRules(self) -> dict:
        return {
            'setParam' : {
                'callable' : 'before_exec'
            },
            'exec' : {
                'callable' : 'before_exec'
            },
            'getStatus' : {
                'callable' : 'after_exec'
            },
            'getHeaders' : {
                'callable' : 'after_exec'
            },
            'getContents' : {
                'callable' : 'after_exec'
            }
        }

    
    def __validateMethodCallCorrectness(self):
        '''execの最初に呼び出すことのみを想定。関数呼び出しの正当性の検証
        '''
        for k, v in self.__method_call_rules.items():
            call_count  = self.__method_call_counter.get(k)

            # required check
            required    = v.get('required')
            if required == True and (call_count is None or call_count <  1):
                raise TwitterAPIClientError('"{}" must be called before "exec" call'.format(k))

            # validation number of calls
            count_rule  = b.get('call_count')
            if count_rule:
                min_count = count_rule.get('min')
                if min_count and (call_count is None or call_count < min_count):
                    raise TwitterAPIClientError('"{}" must be called at least {} times'.format(k, min_count))

    

    # -------------------------------------------------------------------------
    # protedted methods
    # -------------------------------------------------------------------------
    

    def _addPath(self, path:str):
        '''前後のスラッシュは削除, 後ろに再度追加
        '''
        self.__endpoint += '/' + path.strip('/')
    

    def _addExtension(self, ext:str):
        '''エンドポイントの拡張子を指定
        '''
        self.__endpoint += '.' + ext
    

    def _validateMethodCallCorrectness(self, method_name:str):
        '''呼び出しに条件があるメソッドはこれを呼びだす(検証対象の関数呼び出し時点で分かるものは呼び出しの段階で例外)
        '''
        # count number of call
        if self.__method_call_counter.get(method_name) is None:
            self.__method_call_counter[method_name] = 0
        
        self.__method_call_counter[method_name] += 1

       # get rule 
        rule = self.__method_call_rules.get(method_name)
        if rule is None:
            return
        
        # validation callable
        callable_rule = rule.get('callable')
        if callable_rule:
            if callable_rule == 'before_exec' and self.__is_executed == True:
                raise TwitterAPIClientError('"{}" cannot be called after executing exec.'.format(method_name))
            if callable_rule == 'after_exec' and self.__is_executed == False:
                raise TwitterAPIClientError('"{}" cannot be called before executing exec.'.format(method_name))
        
        # validation number of calls
        count_rule = rule.get('call_count')
        if count_rule:
            if self.__is_executed == True:
                raise TwitterAPIClientError('"{}" cannot be called after executing exec.'.format(method_name))
            max_count = count_rule.get('max')
            if max_count and max_count < self.__method_call_counter[method_name]:
                raise TwitterAPIClientError('"{}" can be called up to {} times.'.format(method_name, max_count))
        
        # required check
        required = rule.get('required')
        if required == True:
            if self.__is_executed == True:
                raise TwitterAPIClientError('"{}" cannot be called after executing exec.'.format(method_name))

    
    # -------------------------------------------------------------------------
    # abstract methods
    # -------------------------------------------------------------------------


    @abc.abstractmethod
    def _requestMethod(self) -> str:
        raise NotImplementedError(sys._getframe().f_code.co_name)


    @abc.abstractmethod
    def _getRequiredParameterKeys(self) -> list:
        '''必須パラメータのキー一覧'''
        raise NotImplementedError(sys._getframe().f_code.co_name)


    @abc.abstractmethod
    def _getFunctionsCallRule(self) -> dict:
        '''関数呼び出しのルール定義'''
        raise NotImplementedError(sys._getframe().f_code.co_name)
