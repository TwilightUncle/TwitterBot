from lib.twitter.base import TwitterApiBaseInput, TwitterApiBaseOutput, TwitterApiBaseClient
from lib.twitter.exception import TwitterAPIInputError, TwitterAPIClientError
from lib.twitter.object.users import ResponseObjectUsers


class TwitterApiAccountUpdateProfileImageInput(TwitterApiBaseInput):
    def __init__(self):
        super().__init__()
        self.__image_file_path  = None
        self.__include_entities = None
        self.__skip_status      = None
    

    def setImageFilePath(self, path:str):
        self.__image_file_path = path
    

    def setIncludeEntities(self, is_include:bool):
        if is_include is not None:
            self.__include_entities = 'true' if is_include else 'false'
    

    def setSkipStatus(self, is_skip:bool):
        if is_skip is not None:
            self.__skip_status = 'true' if is_skip else 'false'
    

    def _checkInputCorrectness(self):
        if self.__image_file_path is None:
            raise TwitterAPIInputError('rquired parameter is not input.')

        image_type = super()._checkImageFile(self.__image_file_path)
        # media/uploadとは違いエンコード済みの画像はツイッター側で認識されなかったため、生データを送信
        # super()._setEncodeMediaPath('image', self.__image_file_path, 'image/' + image_type)
        super()._setMediaPath('image', self.__image_file_path, 'image/' + image_type)
        super()._setPostParam('include_entities', self.__include_entities)
        super()._setPostParam('skip_status', self.__skip_status)


class TwitterApiAccountUpdateProfileImageOutput(TwitterApiBaseOutput):
    def __init__(self, results):
        super().__init__(results)
        self.__user = ResponseObjectUsers(super().getContents())
    

    def getUser(self) -> ResponseObjectUsers:
        return self.__user


class TwitterApiAccountUpdateProfileImageClient(TwitterApiBaseClient):
    def __init__(self, api_key='', api_secret='', access_token='', access_secret=''):
        super().__init__(api_key, api_secret, access_token, access_secret)
        super()._setMediaUploadMode()
    

    # --------------------------
    # override functions
    # --------------------------


    def exec(self, inp:TwitterApiAccountUpdateProfileImageInput) -> TwitterApiAccountUpdateProfileImageOutput:
        if not isinstance(inp, TwitterApiAccountUpdateProfileImageInput):
            raise TwitterAPIClientError('invaild argment.')
        super()._addPath('account/update_profile_image')
        super()._addExtension('json')
        results = super().exec(inp)
        return TwitterApiAccountUpdateProfileImageOutput(results)
    

    def _requestMethod(self):
        return 'POST'


def updateProfileImage(
    image_file_path:str, 
    is_include_entities=True,
    is_skip_status=False,
    access_token='',
    access_secret=''
) -> TwitterApiAccountUpdateProfileImageOutput:
    '''Twitterプロフィール画像を更新する
    \n -- params --
    \n * image_file_path        ... 更新したい画像のファイルパスを指定
    \n * is_include_entities    ... Falseを設定すると、レスポンスのユーザーオブジェクトにentitiesが含まれなくなる
    \n * is_skip_status         ... Trueを設定するとレスポンスのユーザーオブジェクトにツイートが含まれなくなる
    \n * access_token           ... 認証ユーザーのアクセストークン。
    \n * access_secret          ... 認証ユーザーのアクセスシークレット
    \n -- exceptions --
    \n * TwitterAPIInputError   ... 主に入力値の検証に失敗したとき投げられる
    \n * TwitterAPIClientError  ... 主にリクエストの実行前に発生する例外。api key等が空の時などに投げられる
    '''
    # set input
    inp = TwitterApiAccountUpdateProfileImageInput()
    inp.setImageFilePath(image_file_path)
    inp.setIncludeEntities(is_include_entities)
    inp.setSkipStatus(is_skip_status)

    # execute
    client = TwitterApiAccountUpdateProfileImageClient(
        access_token=access_token, 
        access_secret=access_secret
    )
    return client.exec(inp)
