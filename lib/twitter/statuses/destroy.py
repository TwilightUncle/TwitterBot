from lib.twitter.base import TwitterApiBaseClient
from lib.twitter.exception import TwitterValidateParamaterError


class TwitterApiStatusesDestoryClient(TwitterApiBaseClient):
    '''tweet検索apiクライアント
    \n http://westplain.sakuraweb.com/translate/twitter/Documentation/REST-APIs/Public-API/POST-statuses-destroy-id.cgi
    '''


    def __init__(self, api_key='', api_secret='', access_token='', access_secret=''):
        super().__init__(api_key, api_secret, access_token, access_secret)


    def setDestroyId(self, id:str):
        # id の数値型チェックで失敗させる
        super()._addPath('statuses/destroy')
        super()._addPath(id)
        super()._addExtension('json')
    

    def setIsTrimUser(self, is_trim:bool):
        if is_trim:
            super().setParam('trim_user', 'true')
    

    # --------------------------
    # override functions
    # --------------------------
    

    def _requestMethod(self) -> str:
        return 'POST'

    
    def _getRequiredParameterKeys(self) -> list:
        return []
    

    def _getFunctionsCallRule(self) -> dict:
        return {
            'setDestroyId' : ['required', 'once']
        }
