import sys
from lib.twitter.base import TwitterApiBaseClient, TwitterApiBaseInput, TwitterApiBaseOutput
from lib.twitter.exception import TwitterAPIInputError


class TwitterApiSearchInput(TwitterApiBaseInput):
    '''tweet検索apiパラメタ入力'''


    def __init__(self):
        super().__init__()
        self.__search_query = None
        self.__count        = None
    

    def setSearchQuery(self, query:str):
        MAX_LEN = 500
        if len(tweet) > MAX_LENGTH:
            raise TwitterAPIInputError('Too many characters. Excess:{}'.format(len(tweet) - MAX_LENGTH))
        self.__search_query = query
    

    def setCount(self, num:int):
        MAX_COUNT = 100
        MIN_COUNT = 1
        if num > MAX_COUNT:
            TwitterAPIInputError('Input value is too large. max: {}'.format(MAX_COUNT))
        if num < MIN_COUNT:
            TwitterAPIInputError('Input value is too small. max: {}'.format(MIN_COUNT))
        self.__count = str(num)
    

    def _checkInputCorrectness(self):
        if self.__search_query is None:
            raise TwitterAPIInputError('rquired parameter is not input.')
        super()._setQueryParam('q', self.__search_query)

        if self.__count is not None:
            super()._setQueryParam('count', self.__count)


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
    

    # --------------------------
    # override functions
    # --------------------------
    

    def exec(self, inp) -> TwitterApiSearchOutput:
        super()._addPath('search/tweets')
        super()._addExtension('json')
        results = super().exec(inp)
        return TwitterApiSearchOutput(results)
    

    def _requestMethod(self) -> str:
        return 'GET'
