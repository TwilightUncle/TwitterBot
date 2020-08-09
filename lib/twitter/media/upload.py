import os
from lib.twitter.base import TwitterApiBaseInput, TwitterApiBaseOutput, TwitterApiBaseClient
from lib.twitter.exception import TwitterAPIInputError, TwitterAPIClientError


class TwitterApiMediaUploadInput(TwitterApiBaseInput):
    '''現状は画像ファイルのみ対応'''
    def __init__(self):
        super().__init__()
        self.__media_file_path = None
    
    
    def setMediaFilePath(self, path:str):
        self.__media_file_path = path
    

    def _checkInputCorrectness(self):
        if self.__media_file_path is None:
            raise TwitterAPIInputError('rquired parameter is not input.')

        image_type = super()._checkImageFile(self.__media_file_path)
        super()._setEncodeMediaPath('media_data', self.__media_file_path, 'image/' + image_type)


class TwitterApiMediaUploadOutput(TwitterApiBaseOutput):
    def __init__(self, results):
        super().__init__(results)

        self.__media_id     = None
        self.__size         = None
        self.__width        = None
        self.__height       = None
        self.__image_type   = None
        
        contents            = super().getContents()
        self.__media_id     = contents.get('media_id_string')
        self.__size         = contents.get('size')

        image = contents.get('image')
        if image is not None:
            self.__width        = image.get('w')
            self.__height       = image.get('h')
            self.__image_type   = image.get('image_type')
    

    def getMediaId(self) -> str:
        return self.__media_id
    

    def getSize(self) -> int:
        return self.__size
    

    def getWidth(self) -> int:
        return self.__width
    

    def getHeight(self) -> int:
        return self.__height
    

    def getImageType(self) -> str:
        return self.__image_type
    

class TwitterApiMediaUploadClient(TwitterApiBaseClient):
    def __init__(self, api_key='', api_secret='', access_token='', access_secret=''):
        super().__init__(api_key, api_secret, access_token, access_secret)
        super()._setMediaUploadMode()
    

    # --------------------------
    # override functions
    # --------------------------


    def exec(self, inp:TwitterApiMediaUploadInput) -> TwitterApiMediaUploadOutput:
        if not isinstance(inp, TwitterApiMediaUploadInput):
            raise TwitterAPIClientError('invaild argment')

        super()._setEndPoint('https://upload.twitter.com/1.1/media/upload.json')
        results = super().exec(inp)
        return TwitterApiMediaUploadOutput(results)


    def _requestMethod(self):
        return 'POST'
