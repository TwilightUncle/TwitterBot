import re
from lib.twitter.base import TwitterApiBaseClient, TwitterApiBaseInput, TwitterApiBaseOutput
from lib.twitter.exception import TwitterAPIInputError, TwitterAPIClientError
from lib.twitter.object.tweets import ResponseObjectTweets


class TwitterApiStatusesUpdateInput(TwitterApiBaseInput):
    '''tweet投稿入力'''


    def __init__(self):
        super().__init__()
        self.__tweet            = None
        self.__reply_target_id  = None
        self.__is_sensitive     = None
        self.__media_ids        = None
        self.__media_count      = 0
    

    def setTweet(self, tweet:str):
        '''投稿するtweet文
        '''
        MAX_LENGTH = 140
        if len(tweet) > MAX_LENGTH:
            raise TwitterAPIInputError('Too many characters. Excess:{}'.format(len(tweet) - MAX_LENGTH))
        self.__tweet = tweet
    

    def setReplyTargetId(self, id:str):
        '''リプする場合の対象tweet idをセット
        '''
        if id is None:
            return
        p = re.compile('\d+')
        if p.fullmatch(id) is None:
            raise TwitterAPIInputError('Only numbers can be specified in the argument.')
        self.__reply_target_id = id
    

    def setIsSensitive(self, is_sensitive:bool):
        self.__is_sensitive = 'true' if is_sensitive else 'false'
    

    def setMediaId(self, id:str):
        '''アップロード済みのmedia idをひとつづつ指定する'''
        p = re.compile('\d+')
        if p.fullmatch(id) is None:
            raise TwitterAPIInputError('Only numbers can be specified in the argument.')
        if self.__media_count >= 4:
            raise TwitterAPIInputError('You can specify up to 4')
        if self.__media_ids is None:
            self.__media_ids = []
        self.__media_ids.append(id)
        self.__media_count += 1
    

    def _checkInputCorrectness(self):
        if self.__tweet is None:
            raise TwitterAPIInputError('rquired parameter is not input.')
        super()._setQueryParam('status', self.__tweet)
        super()._setQueryParam('in_reply_to_status_id', self.__reply_target_id)
        super()._setQueryParam('possibly_sensitive', self.__is_sensitive)

        if self.__media_ids is not None:
            super()._setQueryParam('media_ids', ','.join(self.__media_ids))


class TwitterApiStatusesUpdateOutput(TwitterApiBaseOutput):
    def __init__(self, results):
        super().__init__(results)
        self.__tweet = ResponseObjectTweets(super().getContents())
    

    def getTweet(self) -> ResponseObjectTweets:
        return self.__tweet


class TwitterApiStatusesUpdateClient(TwitterApiBaseClient):
    '''tweet検索apiクライアント
    \n http://westplain.sakuraweb.com/translate/twitter/Documentation/REST-APIs/Public-API/GET-search-tweets.cgi
    '''


    def __init__(self, api_key='', api_secret='', access_token='', access_secret=''):
        super().__init__(api_key, api_secret, access_token, access_secret)
    

    # --------------------------
    # override functions
    # --------------------------


    def exec(self, inp:TwitterApiStatusesUpdateInput) -> TwitterApiStatusesUpdateOutput:
        if not isinstance(inp, TwitterApiStatusesUpdateInput):
            raise TwitterAPIClientError('invaild argment.')
        super()._addPath('statuses/update')
        super()._addExtension('json')
        results = super().exec(inp)
        return TwitterApiStatusesUpdateOutput(results)
    

    def _requestMethod(self) -> str:
        return 'POST'


def statusesUpdate(
    tweet:str,
    reply_target_id=None,
    is_sensitive=False,
    media_ids=None,
    access_token='',
    access_secret=''
) -> TwitterApiStatusesUpdateOutput:
    '''ツイートを投稿する。
    \n -- params --
    \n * tweet                  ... ツイート本文
    \n * reply_target_id        ... 投稿するツイートがリプライの時、対象のツイートIDを指定
    \n * is_sensitive           ... センシティブな画像と思われるものを投稿するときTrue
    \n * media_ids              ... 投稿するツイートに表示する画像等のメディアがあるとき利用。media/uploadエンドポイントでupload済みのメディアのIDをリストで最大4つまで指定
    \n * access_token           ... 認証ユーザーのアクセストークン。
    \n * access_secret          ... 認証ユーザーのアクセスシークレット
    \n -- exceptions --
    \n * TwitterAPIInputError   ... 主に入力値の検証に失敗したとき投げられる
    \n * TwitterAPIClientError  ... 主にリクエストの実行前に発生する例外。api key等が空の時などに投げられる
    '''
    # set input
    inp = TwitterApiStatusesUpdateInput()
    inp.setTweet(tweet)
    inp.setReplyTargetId(reply_target_id)
    inp.setIsSensitive(is_sensitive)
    if type(media_ids) is list:
        for id in media_ids:
            inp.setMediaId(id)
    
    # execute
    client = TwitterApiStatusesUpdateClient(
        access_token=access_token,
        access_secret=access_secret
    )
    return client.exec(inp)
