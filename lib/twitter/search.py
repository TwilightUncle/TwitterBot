import sys
from lib.twitter.base import TwitterApiBaseClient


class TwitterApiSearchClient(TwitterApiBaseClient):
    '''tweet検索apiクライアント
    \n http://westplain.sakuraweb.com/translate/twitter/Documentation/REST-APIs/Public-API/GET-search-tweets.cgi
    '''


    def __init__(self, api_key='', api_secret='', access_token='', access_secret=''):
        super().__init__(api_key, api_secret, access_token, access_secret)
        super()._addPath('search/tweets')
        super()._addExtension('json')


    def setSearchQuery(self, query:str):
        super()._validateMethodCallCorrectness(sys._getframe().f_code.co_name)
        super().setParam('q', query)
    

    # --------------------------
    # override functions
    # --------------------------
    

    def _requestMethod(self) -> str:
        return 'GET'

    
    def _getRequiredParameterKeys(self) -> list:
        return ['q']
    

    def _getFunctionsCallRule(self) -> dict:
        return {
            'setSearchQuery' : {
                'required' : True
            }
        }
