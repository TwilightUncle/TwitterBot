import re
import sys
from lib.twitter.base import TwitterApiBaseClient
from lib.twitter.exception import TwitterValidateParamaterError, TwitterAPIClientError



class TwitterApiStatusesDestoryClient(TwitterApiBaseClient):
    '''tweet検索apiクライアント
    \n http://westplain.sakuraweb.com/translate/twitter/Documentation/REST-APIs/Public-API/POST-statuses-destroy-id.cgi
    '''


    def __init__(self, api_key='', api_secret='', access_token='', access_secret=''):
        super().__init__(api_key, api_secret, access_token, access_secret)


    def setDestroyId(self, id:str):
        '''削除する対象のツイートidを指定
        \n エンドポイントの確定もあるので一度だけの呼び出しとする
        '''
        super()._validateMethodCallCorrectness(sys._getframe().f_code.co_name)

        p = re.compile('\d+')
        if p.fullmatch(id) is None:
            raise TwitterAPIClientError('Only numbers can be specified in the argument.')

        super()._addPath('statuses/destroy')
        super()._addPath(id)
        super()._addExtension('json')
    

    def setIsTrimUser(self, is_trim:bool):
        super()._validateMethodCallCorrectness(sys._getframe().f_code.co_name)
        
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
            'setDestroyId' : {
                'required' : True,
                'call_count' : {
                    'max' : 1
                }
            },
            'setIsTrimUser' : {
                'callable' : 'before_exec'
            }
        }
