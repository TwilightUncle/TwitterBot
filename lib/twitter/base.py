import abc
import time
import urllib.parse
import urllib.request
import hmac
import hashlib
import base64

import random, string


def generateRandomString(n:int) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


class TwitterApiBaseClient(object, metaclass=abc.ABCMeta):
    '''Twitter APIクライアントの基底クラス
    '''


    __BASE_URL = 'https://api.twitter.com/1.1/'


    def __init__(self, api_key:str, api_secret:str, access_token:str, access_secret:str):
        self.__API_KEY          = api_key
        self.__API_SECRET       = api_secret
        self.__ACCESS_TOKEN     = access_token
        self.__ACCESS_SECRET    = access_secret
        self.__ENDPOINT         = self.__class__.__BASE_URL + self._endpoint()
        self.__REQUEST_METHOD   = self._requestMethod().upper()


    def __oauth(self):
        pass


    def __buildOAuthHeader(self) -> str:
        signature_key = urllib.parse.quote(self.__API_SECRET) + '&' + urllib.parse.quote(self.__ACCESS_SECRET)
        signature_params = {
            'oauth_token'               : self.__ACCESS_TOKEN,
            'oauth_consumer_key'        : self.__API_KEY,
            'oauth_signature_method'    : 'HMAC-SHA1',
            'oauth_timestamp'           : int(time.time()),
            'oauth_nonce'               : generateRandomString(16),
            'oauth_version'             : '1.0'
        }
        # join request params
        signature_params.update(self._buildParams())
        # sort and urlencode
        sorted_params           = sorted(signature_params.items(),key=lambda x:x[0])
        encoded_params          = urllib.parse.urlencode(sorted_params)
        encoded_url             = urllib.parse.quote(self.__ENDPOINT, safe='')
        # make base string
        signature_base_string   = self.__REQUEST_METHOD + '&' + encoded_url + '&' + encoded_params
        # make signature
        signature_hash          = hmac.new(signature_key, signature_base_string, hashlib.sha1).digest()
        signature               = base64.b64encode(signature_hash)
        signature_params['oauth_signature'] = signature.strip()
        # to string list
        str_list = []
        for k, v in signature_params.items():
            str_list.append(k + '=' + v)

        return 'Authorization: OAuth ' + ','.join(str_list)


    @abc.abstractmethod
    def _endpoint() -> str:
        pass


    @abc.abstractmethod
    def _requestMethod() -> str:
        pass


    @abc.abstractmethod
    def _buildParams() -> dict:
        pass
