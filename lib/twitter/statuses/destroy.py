import re
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


    def exec(self, inp:TwitterApiStatusesDestoryInput) -> TwitterApiStatusesDestoryOutput:
        if not isinstance(inp, TwitterApiStatusesDestoryInput):
            raise TwitterAPIClientError('invaild argment.')
        # make endpoint
        super()._addPath('statuses/destroy')
        super()._addPath(inp.getDestroyId())
        super()._addExtension('json')
        # execute
        results = super().exec(inp)
        return TwitterApiStatusesDestoryOutput(results)
    

    def _requestMethod(self) -> str:
        return 'POST'


def statusesDestroy(
    destroy_id:str,
    access_token='',
    access_secret=''
) -> TwitterApiStatusesDestoryOutput:
    '''destroy_idで指定した投稿済みのツイートを削除します。
    \n -- params --
    \n * destroy_id             ... 削除するツイートID
    \n * access_token           ... 認証ユーザーのアクセストークン。
    \n * access_secret          ... 認証ユーザーのアクセスシークレット
    \n -- exceptions --
    \n * TwitterAPIInputError   ... 主に入力値の検証に失敗したとき投げられる
    \n * TwitterAPIClientError  ... 主にリクエストの実行前に発生する例外。api key等が空の時などに投げられる
    '''
    # set input
    inp = TwitterApiStatusesDestoryInput()
    inp.setDestroyId(destroy_id)

    # execute
    client = TwitterApiStatusesDestoryClient(
        access_token=access_token,
        access_secret=access_secret
    )
    return client.exec(inp)
