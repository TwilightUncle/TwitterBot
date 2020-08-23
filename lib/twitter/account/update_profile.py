import re
from lib.twitter.base import TwitterApiBaseInput, TwitterApiBaseOutput, TwitterApiBaseClient
from lib.twitter.exception import TwitterAPIInputError, TwitterAPIClientError
from lib.twitter.object.users import ResponseObjectUsers


class TwitterApiAccountUpdateProfileInput(TwitterApiBaseInput):
    '''account/update_profileエンドポイントのパラメータの入力クラス
    '''
    def __init__(self):
        super().__init__()

        # define send parameters
        self.__name                 = None
        self.__url                  = None
        self.__location             = None
        self.__description          = None
        self.__profile_link_color   = None
        self.__include_entities     = None
        self.__skip_status          = None

        self.__param_set_count      = 0
    
    
    def setName(self, name:str):
        '''プロフィールに表示する名前をセット
        '''
        super()._checkStringLength(name, 20)
        self.__name = name
        self.__param_set_count += 1

    
    def setUrl(self, url:str):
        '''プロフィールに関連付けるurlをセット
        '''
        super()._checkStringLength(url, 100)
        self.__url = url
        self.__param_set_count += 1
    

    def setLocation(self, location:str):
        '''プロフィールのロケーションに表示する文字列をセット
        '''
        super()._checkStringLength(location, 30)
        self.__location = location
        self.__param_set_count += 1
    

    def setDescription(self, description:str):
        '''自己紹介欄
        '''
        super()._checkStringLength(description, 160)
        self.__description = description
        self.__param_set_count += 1
    

    def setProfileLinkColor(self, color:str):
        '''プロフィールのリンクの色を調整できる。
        \n 3桁または6桁の16新数で指定(文字列)
        '''
        super()._checkStringLength(color, 6)
        color   = color.upper()
        p       = re.compile('([A-F0-9]{3}){1,2}')
        if p.fullmatch(color):
            raise TwitterAPIInputError('Only 3 or 6 digit hexadecimal string can be specified')
        self.__profile_link_color = color
        self.__param_set_count += 1
    

    def setIncludeEntities(self, is_include:bool):
        if is_include is not None:
            self.__include_entities = 'true' if is_include else 'false'
            self.__param_set_count += 1
    

    def setSkipStatus(self, is_skip:bool):
        if is_skip is not None:
            self.__skip_status = 'true' if is_skip else 'false'
            self.__param_set_count += 1


    def _checkInputCorrectness(self):
        if self.__param_set_count == 0:
            raise TwitterAPIInputError('Set at least one parameter.')

        super()._setQueryParam('name'               , self.__name) 
        super()._setQueryParam('url'                , self.__url)
        super()._setQueryParam('location'           , self.__location)
        super()._setQueryParam('description'        , self.__description)
        super()._setQueryParam('profile_link_color' , self.__profile_link_color)
        super()._setQueryParam('include_entities'   , self.__include_entities)
        super()._setQueryParam('skip_status'        , self.__skip_status)


class TwitterApiAccountUpdateProfileOutput(TwitterApiBaseOutput):
    '''レスポンスのオブジェクト化とドキュメンテーション
    '''
    def __init__(self, results):
        super().__init__(results)
        self.__user = ResponseObjectUsers(super().getContents())
    

    def getUser(self) -> ResponseObjectUsers:
        return self.__user


class TwitterApiAccountUpdateProfileClient(TwitterApiBaseClient):
    '''対象エンドポイントにhttp通信する際のクライアント
    '''
    def __init__(self, api_key='', api_secret='', access_token='', access_secret=''):
        super().__init__(api_key, api_secret, access_token, access_secret)
    

    # --------------------------
    # override functions
    # --------------------------


    def exec(self, inp:TwitterApiAccountUpdateProfileInput) -> TwitterApiAccountUpdateProfileOutput:
        if not isinstance(inp, TwitterApiAccountUpdateProfileInput):
            raise TwitterAPIClientError('invaild argment.')
        # set endpoint
        super()._addPath('account/update_profile')
        super()._addExtension('json')
        # execute
        results = super().exec(inp)
        return TwitterApiAccountUpdateProfileOutput(results)


    def _requestMethod(self):
        '''エンドポイントごとにGETかPOSTを指定'''
        return 'POST'
    

    def _useDefaultAccessToken(self) -> bool:
        '''コンストラクタの引数で、アクセストークンに空文字が渡された時、
        \n 設定ファイルに記述してあるデフォルトのアクセストークンを利用しようとするか否か。
        \n アクセストークンを取得するエンドポイントにおいては、空文字のまま通さないといけないためFalse。
        '''
        return True


def accountUpdateProfile(
    name='',
    url='',
    location='',
    description='',
    profile_link_color='',
    access_token='',
    access_secret=''
) -> TwitterApiAccountUpdateProfileOutput:
    '''プロフィールを更新する
    \n -- params --
    \n * name                   ... プロフィールに表示される名前
    \n * url                    ... プロフィールに関連付けるURL
    \n * location               ... 住んでいる場所とかに表示されるやつ
    \n * description            ... 自己紹介
    \n * profile_link_color     ... プロフィールのリンクの色を設定
    \n * access_token           ... 認証ユーザーのアクセストークン。
    \n * access_secret          ... 認証ユーザーのアクセスシークレット
    \n -- exceptions --
    \n * TwitterAPIInputError   ... 主に入力値の検証に失敗したとき投げられる
    \n * TwitterAPIClientError  ... 主にリクエストの実行前に発生する例外。api key等が空の時などに投げられる
    '''
    # set input
    inp = TwitterApiAccountUpdateProfileInput()
    if not name == '':
        inp.setName(name)
    if not url == '':
        inp.setUrl(url)
    if not location == '':
        inp.setLocation(location)
    if not description == '':
        inp.setDescription(description)
    if not profile_link_color == '':
        inp.setProfileLinkColor(profile_link_color)
    
    # execute
    client = TwitterApiAccountUpdateProfileClient(
        access_token=access_token,
        access_secret=access_secret
    )
    return client.exec(inp)
