import sys
import datetime
import calendar
from lib.twitter.base import TwitterApiBaseClient, TwitterApiBaseInput, TwitterApiBaseOutput
from lib.twitter.exception import TwitterAPIInputError


class TwitterApiSearchInput(TwitterApiBaseInput):
    '''tweet検索apiパラメタ入力'''


    def __init__(self):
        super().__init__()
        self.__search_query = None
        self.__count        = None
        self.__until        = None
        self.__result_type  = None
    

    def setSearchQuery(self, query:str):
        '''ツイートの検索文字列
        '''
        MAX_LEN = 500
        if len(tweet) > MAX_LENGTH:
            raise TwitterAPIInputError('Too many characters. Excess:{}'.format(len(tweet) - MAX_LENGTH))
        self.__search_query = query
    

    def setCount(self, num:int):
        '''取得するツイートの個数。
        \n 指定できる範囲は 1 ～ 100
        '''
        MAX_COUNT = 100
        MIN_COUNT = 1
        if num > MAX_COUNT:
            raise TwitterAPIInputError('Input value is too large. max: {}'.format(MAX_COUNT))
        if num < MIN_COUNT:
            raise TwitterAPIInputError('Input value is too small. max: {}'.format(MIN_COUNT))
        self.__count = str(num)
    

    def setUntil(self, year:int, month:int, day:int):
        '''指定した年月日以前のツイートを取得する。遡れない場合もあるらしい
        '''
        current_date = datetime.date.today()
        if year < 1 or year > current_date.year:
            raise TwitterAPIInputError('invaild input year.')
        if month < 1 or month > 12 or (year == current_date.year and month > current_date.month):
            raise TwitterAPIInputError('invaild input month.')
        if (
            day < 1 or day > calendar.monthrange(year, month) or 
            (year == current_date.year and month == current_date.month and day > current_date.day)
        ):
            raise TwitterAPIInputError('invaild input day')
        self.__until = '{:0=4}-{:0=2}-{:0=2}'.format(year, month, day)
    

    def setResultType(self, result_type:str):
        '''以下のいずれかを指定
        \n mixed    ... 混合
        \n recent   ... 最近のツイートのみ取得
        \n popular  ... 人気のあるツイートのみ取得
        '''
        types = ['mixed', 'recent', 'popular']
        if result_type not in types:
            raise TwitterAPIInputError('invaild input param')
        self.__result_type = result_type
    

    def _checkInputCorrectness(self):
        if self.__search_query is None:
            raise TwitterAPIInputError('rquired parameter is not input.')
        super()._setQueryParam('q', self.__search_query)

        if self.__count is not None:
            super()._setQueryParam('count', self.__count)
        
        if self.__until is not None:
            super()._setQueryParam('until', self.__until)
        
        if self.__result_type is not None:
            super()._setQueryParam('result_type', self.__result_type)


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
