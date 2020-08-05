import sys
from lib.twitter.base import TwitterApiBaseClient
from lib.twitter.exception import TwitterValidateParamaterError


class TwitterApiStatusesUpdateClient(TwitterApiBaseClient):
    '''tweet検索apiクライアント
    \n http://westplain.sakuraweb.com/translate/twitter/Documentation/REST-APIs/Public-API/GET-search-tweets.cgi
    '''


    def __init__(self, api_key='', api_secret='', access_token='', access_secret=''):
        super().__init__(api_key, api_secret, access_token, access_secret)
        super()._addPath('statuses/update')
        super()._addExtension('json')


    def setTweet(self, tweet:str):
        '''投稿するツイート文
        '''
        super()._validateMethodCallCorrectness(sys._getframe().f_code.co_name)

        MAX_LENGTH = 140
        if len(tweet) > MAX_LENGTH:
            raise TwitterValidateParamaterError('Too many characters. Excess:{}'.format(len(tweet) - MAX_LENGTH))

        super().setParam('status', tweet)
    

    def setReplyTargetId(self, id:str):
        '''リプする場合の対象tweet idをセット
        '''
        super()._validateMethodCallCorrectness(sys._getframe().f_code.co_name)
        super().setParam('in_reply_to_status_id', id)
    

    def setSensitive(self, is_sensitive:bool):
        '''センシティブなツイートをするときtrue
        '''
        super()._validateMethodCallCorrectness(sys._getframe().f_code.co_name)
        super().setParam('possibly_sensitive', 'true' if is_sensitive else 'false')
    

    # --------------------------
    # override functions
    # --------------------------
    

    def _requestMethod(self) -> str:
        return 'POST'

    
    def _getRequiredParameterKeys(self) -> list:
        return ['status']
    

    def _getFunctionsCallRule(self) -> dict:
        return {
            'setTweet' : {
                'required' : True
            },
            'setReplyTargetId' : {
                'callable' : 'before_exec'
            },
            'setSensitive' : {
                'callable' : 'before_exec'
            }
        }
