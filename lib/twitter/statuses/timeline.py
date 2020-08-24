import re
from lib.twitter.base import TwitterApiBaseInput, TwitterApiBaseOutput, TwitterApiBaseClient
from lib.twitter.exception import TwitterAPIInputError, TwitterAPIClientError
from lib.twitter.object.tweets import ResponseObjectTweets


class TwitterTimelineType(object):
    USER        = 'user'        # 指定したユーザーのホームを見たときに表示されるタイムライン
    MENTIONS    = 'mentions'    # 認証ユーザーへのメンションがついたツイートのタイムライン
    HOME        = 'home'        # トップページと同様


class TwitterApiStatusesTimelineInput(TwitterApiBaseInput):
    '''タイムラインのパラメータ入力クラス。各パラメータについては以下を参照
    \n http://westplain.sakuraweb.com/translate/twitter/Documentation/REST-APIs/Public-API/GET-statuses-mentions_timeline.cgi
    \n http://westplain.sakuraweb.com/translate/twitter/Documentation/REST-APIs/Public-API/GET-statuses-user_timeline.cgi
    \n http://westplain.sakuraweb.com/translate/twitter/Documentation/REST-APIs/Public-API/GET-statuses-home_timeline.cgi
    '''


    def __init__(self):
        super().__init__()
        self.__timeline_type        = TwitterTimelineType.HOME
        # users only
        self.__user_id              = None
        self.__screen_name          = None
        self.__include_rts          = None
        # users and home
        self.__exclude_replies      = None
        # common
        self.__count                = None
        self.__since_id             = None
        self.__max_id               = None
        self.__trim_user            = None
        self.__contributor_details  = None
        self.__include_entities     = None
    

    def setTimelineType(self, timeline_type:str):
        '''必須'''
        if timeline_type == TwitterTimelineType.USER or timeline_type == TwitterTimelineType.MENTIONS:
            self.__timeline_type = timeline_type
        else:
            self.__timeline_type = TwitterTimelineType.HOME
    

    def setUserId(self, id:str):
        p = re.compile('\d+')
        if p.fullmatch(id) is None:
            raise TwitterAPIClientError('Only numbers can be specified in the argument.')
        self.__user_id = id
    

    def setUserScreenName(self, name:str):
        self.__screen_name = name
    

    def setCount(self, num:int):
        '''取得するツイートの個数。
        \n 指定できる範囲は 1 ～ 200
        '''
        MAX_COUNT = 200
        MIN_COUNT = 1
        if num > MAX_COUNT:
            raise TwitterAPIInputError('Input value is too large. max: {}'.format(MAX_COUNT))
        if num < MIN_COUNT:
            raise TwitterAPIInputError('Input value is too small. max: {}'.format(MIN_COUNT))
        self.__count = str(num)
    

    def setSinceId(self, id:str):
        '''これに指定したIDよりも大きい(より新しい)IDの検索結果を取得
        '''
        p = re.compile('\d+')
        if p.fullmatch(id) is None:
            raise TwitterAPIClientError('Only numbers can be specified in the argument.')
        self.__since_id = id
    

    def setMaxId(self, id:str):
        '''これに指定したID以下(より古い)のIDの検索結果を取得
        '''
        p = re.compile('\d+')
        if p.fullmatch(id) is None:
            raise TwitterAPIClientError('Only numbers can be specified in the argument.')
        self.__max_id = id
    

    def setIsTrimUser(self, is_trim:bool):
        if is_trim:
            self.__is_trim_user = 'true'
    

    def setIsExcludeReplies(self, is_exclude:bool):
        if is_exclude:
            self.__exclude_replies = 'true'
    

    def setIsContributorDetails(self, is_get_detail:bool):
        if is_get_detail:
            self.__contributor_details = 'true'
    

    def setIsExcludeEntities(self, is_exclude:bool):
        if is_exclude:
            self.__include_entities = 'false'
    

    def setIsExcludeRetweet(self, is_exclude:bool):
        '''リツイート除外
        '''
        if is_exclude:
            self.__include_rts = 'false'
    

    def getTimelineType(self) -> str:
        '''clientでエンドポイント確定するのに必要'''
        return self.__timeline_type
    

    def _checkInputCorrectness(self):
        if self.__timeline_type == TwitterTimelineType.USER:
            if self.__user_id is None and self.__screen_name is None:
                raise TwitterAPIInputError('user_id or screen_name must be set')
            super()._setQueryParam('user_id', self.__user_id)
            super()._setQueryParam('screen_name', self.__screen_name)
            super()._setQueryParam('include_rts', self.__include_rts)
        
        if (
            self.__timeline_type == TwitterTimelineType.USER or
            self.__timeline_type == TwitterTimelineType.HOME
        ):
            super()._setQueryParam('exclude_replies', self.__exclude_replies)
        
        super()._setQueryParam('count', self.__count)
        super()._setQueryParam('since_id', self.__since_id)
        super()._setQueryParam('max_id', self.__max_id)
        super()._setQueryParam('trim_user', self.__trim_user)
        super()._setQueryParam('contributor_details', self.__contributor_details)
        super()._setQueryParam('include_entities', self.__include_entities)
    

class TwitterApiStatusesTimelineOutput(TwitterApiBaseOutput):
    def __init__(self, results):
        super().__init__(results)

        self.__tweets = []
        self.__result_count = 0

        tweets = super().getContents()
        for tweet in tweets:
            self.__tweets.append(ResponseObjectTweets(tweet))
        self.__result_count = len(self.__tweets)
    

    def getTweetList(self) -> [ResponseObjectTweets]:
        return self.__tweets
    

    def getResultTweetsCount(self):
        return self.__result_count


class TwitterApiStatusesTimelineClient(TwitterApiBaseClient):
    '''タイムライン取得APIクライアント
    '''

    
    def __init__(self, api_key='', api_secret='', access_token='', access_secret=''):
        super().__init__(api_key, api_secret, access_token, access_secret)
    

    # --------------------------
    # override functions
    # --------------------------


    def exec(self, inp:TwitterApiStatusesTimelineInput) -> TwitterApiStatusesTimelineOutput:
        if not isinstance(inp, TwitterApiStatusesTimelineInput):
            raise TwitterAPIClientError('invaild argment.')

        endpoint = 'statuses/home_timeline'
        if inp.getTimelineType() == TwitterTimelineType.USER:
            endpoint = 'statuses/user_timeline'
        if inp.getTimelineType() == TwitterTimelineType.MENTIONS:
            endpoint = 'statuses/mentions_timeline'
        
        super()._addPath(endpoint)
        super()._addExtension('json')
        results = super().exec(inp)
        return TwitterApiStatusesTimelineOutput(results)
    

    def _requestMethod(self) -> str:
        return 'GET'


def __commonInput(
    time_line_type:str,
    count=0,
    since_id='',
    max_id=''
) -> TwitterApiStatusesTimelineInput:
    '''共通の入力値をセットする処理を行う。非公開想定
    '''
    inp = TwitterApiStatusesTimelineInput()
    inp.setTimelineType(time_line_type)
    if count > 0:
        inp.setCount(count)
    if not since_id == '':
        inp.setSinceId(since_id)
    if not max_id == '':
        inp.setMaxId(max_id)
    return inp


def __commonExecute(
    inp:TwitterApiStatusesTimelineInput,
    access_token='',
    access_secret=''
) -> TwitterApiStatusesTimelineOutput:
    '''共通の実行処理。非公開想定。
    '''
    client = TwitterApiStatusesTimelineClient(
        access_token=access_token,
        access_secret=access_secret
    )
    return client.exec(inp)


def statusesMentionsTimeline(
    count=0,
    since_id='',
    max_id='',
    access_token='',
    access_secret=''
) -> TwitterApiStatusesTimelineOutput:
    '''認証ユーザーのメンションのタイムラインを取得する
    \n -- params --
    \n * count                  ... 取得するツイートの数
    \n * since_id               ... ここに指定したIDのツイートよりもより新しいツイートを取得する
    \n * max_id                 ... ここに指定したIDのツイートよりもより古いツイートを取得する
    \n * access_token           ... 認証ユーザーのアクセストークン。
    \n * access_secret          ... 認証ユーザーのアクセスシークレット
    \n -- exceptions --
    \n * TwitterAPIInputError   ... 主に入力値の検証に失敗したとき投げられる
    \n * TwitterAPIClientError  ... 主にリクエストの実行前に発生する例外。api key等が空の時などに投げられる
    '''
    # set input
    inp = __commonInput(
        time_line_type=TwitterTimelineType.MENTIONS,
        count=count, 
        since_id=since_id, 
        max_id=max_id
    )

    # execute
    response = __commonExecute(
        inp=inp,
        access_token=access_token,
        access_secret=access_secret
    )
    return response


def statusesHomeTimeline(
    count=0,
    since_id='',
    max_id='',
    exclude_replies=False,
    access_token='',
    access_secret=''
) -> TwitterApiStatusesTimelineOutput:
    '''認証ユーザーのホームで表示されるタイムラインを取得する
    \n -- params --
    \n * count                  ... 取得するツイートの数
    \n * since_id               ... ここに指定したIDのツイートよりもより新しいツイートを取得する
    \n * max_id                 ... ここに指定したIDのツイートよりもより古いツイートを取得する
    \n * exclude_replies        ... Trueを指定すると、取得するタイムラインにリプライツイートを含まないようにする
    \n * access_token           ... 認証ユーザーのアクセストークン。
    \n * access_secret          ... 認証ユーザーのアクセスシークレット
    \n -- exceptions --
    \n * TwitterAPIInputError   ... 主に入力値の検証に失敗したとき投げられる
    \n * TwitterAPIClientError  ... 主にリクエストの実行前に発生する例外。api key等が空の時などに投げられる
    '''
    # set input
    inp = __commonInput(
        time_line_type=TwitterTimelineType.HOME,
        count=count, 
        since_id=since_id, 
        max_id=max_id
    )
    inp.setIsExcludeReplies(exclude_replies)

    # execute
    response = __commonExecute(
        inp=inp,
        access_token=access_token,
        access_secret=access_secret
    )
    return response


def statusesUserTimeline(
    user_id='',
    screen_name='',
    count=0,
    since_id='',
    max_id='',
    exclude_replies=False,
    exclude_rts=True
) -> TwitterApiStatusesTimelineOutput:
    '''指定ユーザーのホームで表示されるタイムラインを取得する
    \n -- params --
    \n * user_id                ... タイムラインを表示したい対象ユーザーのID
    \n * screen_name            ... タイムラインを表示したい対象ユーザーのスクリーン名("@"以下のユーザー名)
    \n * count                  ... 取得するツイートの数
    \n * since_id               ... ここに指定したIDのツイートよりもより新しいツイートを取得する
    \n * max_id                 ... ここに指定したIDのツイートよりもより古いツイートを取得する
    \n * exclude_replies        ... Trueを指定すると、取得するタイムラインにリプライツイートを含まないようにする
    \n * exclude_rts            ... Trueを指定すると、取得するタイムラインにリツイートを含まないようにする
    \n -- exceptions --
    \n * TwitterAPIInputError   ... 主に入力値の検証に失敗したとき投げられる
    \n * TwitterAPIClientError  ... 主にリクエストの実行前に発生する例外。api key等が空の時などに投げられる
    '''
    # set input
    inp = __commonInput(
        time_line_type=TwitterTimelineType.USER,
        count=count, 
        since_id=since_id, 
        max_id=max_id
    )
    if not user_id == '':
        inp.setUserId(user_id)
    if not screen_name == '':
        inp.setUserScreenName(screen_name)
    inp.setIsExcludeReplies(exclude_replies)
    inp.setIsExcludeRetweet(exclude_rts)

    # execute
    response = __commonExecute(inp=inp)
    return response
