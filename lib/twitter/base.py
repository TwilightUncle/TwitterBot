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
import imghdr

from lib.utils import generateRandomString
from lib.twitter.exception import TwitterRequiredParameterError, TwitterAPIClientError


# ==========================================================================
# クライアントクラス
# ==========================================================================
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

            if self._useDefaultAccessToken():
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
        self.__media_params     = None
        self.__auth_extentions  = None
        self.__endpoint         = None
        self.__is_media_upload  = False

        self.__initializeParams()
    

    # -----------------------------------------------------------------------
    # public methods
    # -----------------------------------------------------------------------


    def exec(self, inp) -> dict:
        '''リクエスト実行(他に必要な処理あればオーバーライド想定)
        '''
        if not isinstance(inp, TwitterApiBaseInput):
            raise TwitterAPIClientError('invaild argment.')
        
        # get params
        inp._checkInputCorrectness()
        self.__request_params   = inp._getQueryParams()
        self.__media_params     = inp._getPostParams()
        self.__auth_extentions  = inp._getAuthHeaderExtentionParams()

        # make request
        query_param_string  = ''
        if len(self.__getRequestParams()) > 0:
            query_param_string  = '?' + urllib.parse.urlencode(self.__getRequestParams())
        endpoint            = self.__endpoint + query_param_string

        req = None
        if self.__is_media_upload:
            content_type, body  = self.__buildMediaData()
            req             = urllib.request.Request(endpoint, method=self.__REQUEST_METHOD, data=body)
            req.add_header('Content-Type', content_type)
            req.add_header('Content-Length', str(len(body)))
        else:
            req             = urllib.request.Request(endpoint, method=self.__REQUEST_METHOD)
        req.add_header('Authorization', self.__buildOAuthHeader())

        # request execute
        try:
            results = {}
            with urllib.request.urlopen(req) as res:
                results['status']   = res.status
                results['headers']  = res.getheaders()
                response            = res.read().decode('utf-8')
                if self._responseType() == 'json':
                    results['contents'] = json.loads(response)
                elif self._responseType() == 'http_query':
                    results['contents'] = urllib.parse.parse_qs(response)
                else:
                    results['contents'] = response
        except urllib.error.HTTPError as err:
            # レスポンスを表示させて、そのまま投げる
            print(err.read().decode('utf-8'))
            raise err
        
        # パラメータ等を初期化して、インスタンスを再利用できるようにする
        self.__initializeParams()
        return results
    

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
        signature_params.update(self.__getAuthHeaderExtentionParams())
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
    

    def __buildMediaData(self) -> (str, bytes):
        '''画像送信等に対応
        \n Content-Type: multipart/form-data;のリクエストを作成
        '''
        body = []
        # boundary
        boundary = 'k-u-r-u-m-i-------------' + generateRandomString(32)
        content_type = 'multipart/form-data; boundary=' + boundary
        delimiter = ('--' + boundary).encode()

        for param_name, value in self.__getMediaParams().items():
            # get value
            data = None
            if type(value) is str:
                data = value.encode()
            
            if type(value) is dict:
                file_path = value.get('file_path')
                if file_path:
                    with open(file_path, 'rb') as media_file:
                        data = media_file.read()
                    if value.get('is_encode') == True:
                        data = base64.b64encode(data)
            
            if data is None:
                raise TwitterAPIClientError('incorrect input parameter type.')

            # build data
            param = []
            param.append(delimiter)
            param.append(f'Content-Disposition: form-data; name="{param_name}"; '.encode())
            if type(value) is dict and value.get('is_encode') == True:
                param.append(f'Content-Type: {value.get("mime_type")}'.encode())
                param.append('Content-Transfer-Encoding: base64'.encode())
            param.append(b'')
            param.append(data)

            # append params
            body.append(b"\r\n".join(param))
        
        body.append(delimiter + b"--\r\n\r\n")
        return content_type, b"\r\n".join(body)
    

    def __getRequestParams(self) -> dict:
        return self.__request_params
    

    def __getMediaParams(self) -> dict:
        return self.__media_params
    

    def __getAuthHeaderExtentionParams(self) -> dict:
        return self.__auth_extentions
    

    def __initializeParams(self):
        self.__request_params   = None
        self.__media_params     = None
        self.__auth_extentions  = None
        self.__endpoint         = self.__class__.__BASE_URL
    

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
    

    def _setEndPoint(self, url:str):
        '''endpointにそのまま代入する
        '''
        self.__endpoint = url
    

    def _setMediaUploadMode(self):
        '''メディアアップロード系のエンドポイントではこれをコンストラクタで呼び出す
        '''
        self.__is_media_upload = True


    # -------------------------------------------------------------------------
    # abstract methods
    # -------------------------------------------------------------------------


    @abc.abstractmethod
    def _requestMethod(self) -> str:
        raise NotImplementedError(sys._getframe().f_code.co_name)


    def _useDefaultAccessToken(self) -> bool:
        '''コンストラクタの引数で、アクセストークンに空文字が渡された時、
        \n 設定ファイルに記述してあるデフォルトのアクセストークンを利用しようとするか否か。
        \n アクセストークンを取得するエンドポイントにおいては、空文字のまま通さないといけないため。
        '''
        return True
    

    def _responseType(self) -> str:
        '''レスポンスがjson以外だったら、以下のいずれかを指定
        \n http_query
        '''
        return 'json'


# ==========================================================================
# 入力クラス
# ==========================================================================
class TwitterApiBaseInput(object, metaclass=abc.ABCMeta):
    '''入力値設定基底クラス
    \n 基底クラスの関数は基本的に外で呼び出されることを想定されていません。
    '''


    def __init__(self):
        self.__get_params       = {}
        self.__post_params      = {}
        self.__auth_extentions  = {}
    

    def _setQueryParam(self, key:str, value):
        if value is None:
            return
        self.__get_params[key] = value
    

    def _setQueryEncodeFilePath(self, key:str, path:str):
        '''get parameterにファイルの64エンコードバイナリデータを追加する'''
        if path is None:
            return
        with open(path, 'rb') as file:
            data = file.read()
        data = base64.b64encode(data)
        data = data.decode('utf-8')
        self._setQueryParam(key, data)
    

    def _setPostParam(self, key:str, value):
        if value is None:
            return
        self.__post_params[key] = value
    

    def _setEncodeMediaPath(self, key:str, path:str, mime_type:str):
        if path is None:
            return
        self._setPostParam(key, {'is_encode' : True, 'file_path' : path, 'mime_type' : mime_type})
    

    def _setMediaPath(self, key:str, path:str, mime_type:str):
        if path is None:
            return
        self._setPostParam(key, {'is_encode' : False, 'file_path' : path, 'mime_type' : mime_type})
    

    def _setAuthHeaderExtentionParam(self, key:str, value:str):
        if value is None:
            return
        self.__auth_extentions[key] = value
    

    def _getQueryParams(self) -> dict:
        return self.__get_params
    

    def _getPostParams(self) -> dict:
        return self.__post_params
    

    def _getAuthHeaderExtentionParams(self) -> dict:
        return self.__auth_extentions
    

    def _checkImageFile(self, file_path:str) -> str:
        if file_path is None:
            raise TwitterAPIInputError('path is None.')

        if not os.path.isfile(file_path):
            raise TwitterAPIInputError('The specified file does not exist.')

        image_type = imghdr.what(file_path)
        if image_type is None:
            raise TwitterAPIInputError('Please specify the image file')
        return image_type
    

    @abc.abstractmethod
    def _checkInputCorrectness(self):
        '''入力値の正当性チェック。駄目だったら例外を投げる'''
        raise NotImplementedError(sys._getframe().f_code.co_name)


# ==========================================================================
# 出力クラス
# ==========================================================================
class TwitterApiBaseOutput(object, metaclass=abc.ABCMeta):
    '''出力基底クラス
    '''


    def __init__(self, results):
        self.__status   = results.get('status')
        self.__headers  = results.get('headers')
        self.__contents = results.get('contents')
    

    def getStatus(self):
        '''http status code'''
        return self.__status
    

    def getHeaders(self):
        '''http headers'''
        return self.__headers
    

    def getContents(self) -> dict:
        '''contents'''
        return self.__contents
