import sys
from lib.twitter.base import TwitterApiBaseClient, TwitterApiBaseInput
from lib.twitter.exception import TwitterAPIInputError


class TwitterApiSearchInput(TwitterApiBaseInput):
    '''tweet検索apiパラメタ入力'''


    def __init__(self):
        self.__search_query = None
    

    def setSearchQuery(self, query:str):
        self.__search_query = query
        super()._setQueryParam('q', query)
    

    def _checkInputCorrectness(self):
        if self.__search_query is None:
            raise TwitterAPIInputError('rquired parameter is not input.')
        super()._setQueryParam('q', self.__search_query)


class TwitterApiSearchClient(TwitterApiBaseClient):
    '''tweet検索apiクライアント
    \n http://westplain.sakuraweb.com/translate/twitter/Documentation/REST-APIs/Public-API/GET-search-tweets.cgi
    '''


    def __init__(self, api_key='', api_secret='', access_token='', access_secret=''):
        super().__init__(api_key, api_secret, access_token, access_secret)
        super()._addPath('search/tweets')
        super()._addExtension('json')
    

    # --------------------------
    # override functions
    # --------------------------
    

    def _requestMethod(self) -> str:
        return 'GET'

    
    def _getRequiredParameterKeys(self) -> list:
        return ['q']
