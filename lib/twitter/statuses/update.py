import re
from lib.twitter.base import TwitterApiBaseClient, TwitterApiBaseInput, TwitterApiBaseOutput
from lib.twitter.exception import TwitterValidateParamaterError, TwitterAPIInputError
from lib.twitter.object.tweets import ResponseObjectTweets


class TwitterApiStatusesUpdateInput(TwitterApiBaseInput):
    '''tweet投稿入力'''


    def __init__(self):
        super().__init__()
        self.__tweet            = None
        self.__reply_target_id  = None
        self.__is_sensitive     = None
    

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
        p = re.compile('\d+')
        if p.fullmatch(id) is None:
            raise TwitterAPIInputError('Only numbers can be specified in the argument.')
        self.__reply_target_id = id
    

    def setIsSensitive(self, is_sensitive:bool):
        self.__is_sensitive = 'true' if is_sensitive else 'false'
    

    def _checkInputCorrectness(self):
        if self.__tweet is None:
            raise TwitterAPIInputError('rquired parameter is not input.')
        super()._setQueryParam('status', self.__tweet)

        if self.__reply_target_id is not None:
            super()._setQueryParam('in_reply_to_status_id', self.__reply_target_id)
        
        if self.__is_sensitive is None:
            super()._setQueryParam('possibly_sensitive', self.__is_sensitive)


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
        super()._addPath('statuses/update')
        super()._addExtension('json')
        results = super().exec(inp)
        return TwitterApiStatusesUpdateOutput(results)
    

    def _requestMethod(self) -> str:
        return 'POST'
