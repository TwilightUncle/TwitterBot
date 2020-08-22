from lib.twitter.base import TwitterApiBaseInput, TwitterApiBaseOutput, TwitterApiBaseClient
from lib.twitter.exception import TwitterAPIInputError, TwitterAPIClientError


class TwitterApiOauthRequestTokenInput(TwitterApiBaseInput):
    def __init__(self):
        super().__init__()
        self.__oauth_callback       = None
        self.__x_auth_access_type   = None
    

    def setOauthCallback(self, url:str):
        self.__oauth_callback = url
    

    def setXAuthAccessType(self, req_type:str):
        '''ユーザーアカウントに要求するアクセスレベル
        \n read ... 読み込み権限のみ
        \n write ... 書き込み権限も
        '''
        types = ['read', 'write']
        if req_type in types:
            self.__x_auth_access_type = req_type


    def _checkInputCorrectness(self):
        if self.__oauth_callback is None:
            raise TwitterAPIInputError('rquired parameter is not input.')

        super()._setAuthHeaderExtentionParam('oauth_callback', self.__oauth_callback) 
        super()._setQueryParam('x_auth_access_type', self.__x_auth_access_type)


class TwitterApiOauthRequestTokenOutput(TwitterApiBaseOutput):
    def __init__(self, results):
        super().__init__(results)
        contents = super().getContents()
        self.__oauth_token = contents.get('oauth_token')
        self.__oauth_token_secret = contents.get('oauth_token_secret')
        self.__oauth_callback_confirmed = contents.get('oauth_callback_confirmed')
        self.__oauth_redirect_every_time = 'https://api.twitter.com/oauth/authorize?oauth_token='
        self.__oauth_redirect_once = 'https://api.twitter.com/oauth/authenticate?oauth_token='

    
    def getOauthToken(self) str:
        '''取得できなかった場合、None'''
        return self.__oauth_token
    

    def getOauthTokenSeacret(self) -> str:
        '''取得できなかった場合、None'''
        return self.__oauth_token_secret
    

    def getOauthCallbackConfirmed(self) -> bool:
        '''取得できなかった場合、False'''
        if self.__oauth_callback_confirmed == 'true':
            return True
        return False
    

    def getOauthRedirectEveryTimeUrl(self) -> str:
        if not self.__oauth_token:
            return None
        return self.__oauth_redirect_every_time + self.__oauth_token
    

    def getOauthRedirectOnceUrl(self) -> str:
        if not self.__oauth_token:
            return None
        return self.__oauth_redirect_once + self.__oauth_token


class TwitterApiOauthRequestTokenClient(TwitterApiBaseClient):
    def __init__(self, api_key='', api_secret=''):
        super().__init__(api_key, api_secret)
    

    # --------------------------
    # override functions
    # --------------------------


    def exec(self, inp:TwitterApiOauthRequestTokenInput) -> TwitterApiOauthRequestTokenOutput:
        if not isinstance(inp, TwitterApiOauthRequestTokenInput):
            raise TwitterAPIClientError('invaild argment.')
        # set endpoint
        results = super().exec(inp)
        super()._addPath('oauth/request_token')
        super()._addExtension('json')
        return TwitterApiOauthRequestTokenOutput


    def _requestMethod(self):
        '''エンドポイントごとにGETかPOSTを指定'''
        return 'POST'
    

    def _useDefaultAccessToken(self) -> bool:
        '''コンストラクタの引数で、アクセストークンに空文字が渡された時、
        \n 設定ファイルに記述してあるデフォルトのアクセストークンを利用しようとするか否か。
        \n アクセストークンを取得するエンドポイントにおいては、空文字のまま通さないといけないためFalse。
        '''
        return False
    

    def __responseType(self) -> str:
        return 'http_query'


def oauthRequestToken(
    oauth_callback:str,
    auth_access_type='read'
) -> TwitterApiOauthRequestTokenOutput:
    '''認証を行うためのトークンと、twitterの認証画面へのリダイレクトURLを取得する
    \n -- params --
    \n * oauth_callback ... twitterの認証画面から帰ってきて、結果を処理するためのURLを指定
    \n * auth_access_type ... このapiが行うことができる権限の指定。'read': 読み込み専用。'write':ツイッターの投稿やプロフィールの変更も可。
    \n -- exceptions --
    \n * TwitterAPIInputError   ... 主に入力値の検証に失敗したとき投げられる
    \n * TwitterAPIClientError  ... 主にリクエストの実行前に発生する例外。api key等が空の時などに投げられる
    '''
    # set params
    inp = TwitterApiOauthRequestTokenInput()
    inp.setOauthCallback(oauth_callback)
    inp.setXAuthAccessType(auth_access_type)

    # execute
    client = TwitterApiOauthRequestTokenClient()
    return client.exec(inp)
