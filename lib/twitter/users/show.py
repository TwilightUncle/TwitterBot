import re
from lib.twitter.base import TwitterApiBaseInput, TwitterApiBaseOutput, TwitterApiBaseClient
from lib.twitter.exception import TwitterAPIInputError, TwitterAPIClientError
from lib.twitter.object.users import ResponseObjectUsers


class TwitterApiUsersShowInput(TwitterApiBaseInput):
    def __init__(self):
        super().__init__()

        self.__user_id          = None
        self.__screen_name      = None
        self.__include_entities = None
    
    
    def setUserId(self, id:str):
        p = re.compile('\d+')
        if p.fullmatch(id) is None:
            raise TwitterAPIClientError('Only numbers can be specified in the argument.')
        self.__user_id = id
    

    def setScreenName(self, name:str):
        self.__screen_name = name
    

    def setIncludeEntities(self, is_include:bool):
        self.__include_entities = 'true' if is_include else 'false'


    def _checkInputCorrectness(self):
        if self.__user_id is None and self.__screen_name is None:
            raise TwitterAPIInputError('rquired parameter is not input.')

        super()._setQueryParam('user_id', self.__user_id)
        super()._setQueryParam('screen_name', self.__screen_name)
        super()._setQueryParam('include_entities', self.__include_entities)


class TwitterApiUsersShowOutput(TwitterApiBaseOutput):
    def __init__(self, results):
        super().__init__(results)
        contents = super().getContents()

        self.__user = ResponseObjectUsers(contents)
    

    def getUser(self) -> ResponseObjectUsers:
        return self.__user


class TwitterApiUsersShowClient(TwitterApiBaseClient):
    def __init__(self, api_key='', api_secret='', access_token='', access_secret=''):
        super().__init__(api_key, api_secret, access_token, access_secret)
    

    # --------------------------
    # override functions
    # --------------------------


    def exec(self, inp:TwitterApiUsersShowInput) -> TwitterApiUsersShowOutput:
        if not isinstance(inp, TwitterApiUsersShowInput):
            raise TwitterAPIClientError('invaild argment.')
        # set endpoint
        super()._addPath('users/show')
        super()._addExtension('json')
        # execute
        results = super().exec(inp)
        return TwitterApiUsersShowOutput(results)


    def _requestMethod(self):
        '''エンドポイントごとにGETかPOSTを指定'''
        return 'GET'
    

    def _useDefaultAccessToken(self) -> bool:
        '''コンストラクタの引数で、アクセストークンに空文字が渡された時、
        \n 設定ファイルに記述してあるデフォルトのアクセストークンを利用しようとするか否か。
        \n アクセストークンを取得するエンドポイントにおいては、空文字のまま通さないといけないためFalse。
        '''
        return True
