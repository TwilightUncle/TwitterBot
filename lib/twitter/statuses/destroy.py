import re
import sys
from lib.twitter.base import TwitterApiBaseClient, TwitterApiBaseInput, TwitterApiBaseOutput
from lib.twitter.exception import TwitterAPIClientError, TwitterAPIInputError
from lib.twitter.object.tweets import ResponseObjectTweets


class TwitterApiStatusesDestoryInput(TwitterApiBaseInput):
    def __init__(self):
        super().__init__()
        self.__destroy_id = ''
        self.__is_trim_user = None
    

    def setDestroyId(self, id:str):
        '''削除する対象のツイートidを指定
        \n エンドポイントの確定もあるので一度だけの呼び出しとする
        '''
        p = re.compile('\d+')
        if p.fullmatch(id) is None:
            raise TwitterAPIClientError('Only numbers can be specified in the argument.')
        self.__destroy_id = id
    

    def setIsTrimUser(self, is_trim:bool):
        if is_trim:
            self.__is_trim_user = 'true'
    

    def getDestroyId(self):
        return self.__destroy_id
    

    def _checkInputCorrectness(self):
        if self.__destroy_id == '':
            raise TwitterAPIInputError('rquired parameter is not input.')

        if self.__is_trim_user is not None:
            super()._setQueryParam('trim_user', self.__is_trim_user)


class TwitterApiStatusesDestoryOutput(TwitterApiBaseOutput):
    def __init__(self, results):
        super().__init__(results)
        self.__deleted_tweet = ResponseObjectTweets(super().getContents())
    

    def getDeletedTweet(self) -> ResponseObjectTweets:
        return self.__deleted_tweet


class TwitterApiStatusesDestoryClient(TwitterApiBaseClient):
    '''tweet検索apiクライアント
    \n http://westplain.sakuraweb.com/translate/twitter/Documentation/REST-APIs/Public-API/POST-statuses-destroy-id.cgi
    '''


    def __init__(self, api_key='', api_secret='', access_token='', access_secret=''):
        super().__init__(api_key, api_secret, access_token, access_secret)
    

    # --------------------------
    # override functions
    # --------------------------


    def exec(self, inp) -> TwitterApiStatusesDestoryOutput:
        # make endpoint
        super()._addPath('statuses/destroy')
        super()._addPath(inp.getDestroyId())
        super()._addExtension('json')
        # execute
        results = super().exec(inp)
        return TwitterApiStatusesDestoryOutput(results)
    

    def _requestMethod(self) -> str:
        return 'POST'
