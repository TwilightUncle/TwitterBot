import sys
from lib.twitter.base import TwitterApiBaseClient, TwitterApiBaseInput, TwitterApiBaseOutput
from lib.twitter.exception import TwitterAPIInputError


class TwitterApiSearchInput(TwitterApiBaseInput):
    '''tweet検索apiパラメタ入力'''


    def __init__(self):
        super().__init__()
        self.__search_query = None
    

    def setSearchQuery(self, query:str):
        self.__search_query = query
    

    def _checkInputCorrectness(self):
        if self.__search_query is None:
            raise TwitterAPIInputError('rquired parameter is not input.')
        super()._setQueryParam('q', self.__search_query)


class TwitterApiSearchOutput(TwitterApiBaseOutput):
    '''tweet検索api出力'''


    def __init__(self, results):
        super().__init__(results)


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
    

    def exec(self, inp) -> TwitterApiSearchOutput:
        results = super().exec(inp)
        return TwitterApiSearchOutput(results)
    

    def _requestMethod(self) -> str:
        return 'GET'
