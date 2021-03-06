import json
from lib.twitter.object import users, entities


class ResponseObjectTweets(object):
    '''Apiレスポンスのツイートオブジェクト。
    \n http://westplain.sakuraweb.com/translate/twitter/API-Overview/Tweets.cgi
    '''


    def __init__(self, data:dict):
        self.__row_data         = data
        self.__contributors     = None              # ResponseObjectContributorsを参照
        self.__coordinates      = None              # ResponseObjectCoordinatesを参照
        self.__created_at       = None              # ツイートが作成された時のUTC時間
        self.__current_user_retweet = None          # このツイートのリツイートのツイートID
        self.__entities         = None              # ResponseObjectEntitiesを参照
        self.__favorite_count   = None              # ファボの数
        self.__tweet_id         = None              # このツイートのID
        self.__reply_tweet_id   = None              # リプ元のツイートID
        self.__reply_user_id    = None              # リプ元ツイートのユーザーID
        self.__lang             = None              # ツイートの言語
        self.__quoted_status_id = None              # 引用元ツイートID
        self.__quoted_status    = None              # 引用元ツイート情報
        self.__retweet_count    = None              # リツイートされた回数
        self.__retweeted_status = None              # リツイート元ツイート
        self.__text             = None              # ツイートの本文
        self.__user             = None              # 投稿ユーザー情報。ResponseObjectUserを参照

        self.__coordinates      = data.get('coordinates')
        self.__created_at       = data.get('created_at')
        self.__entities         = self.__makeEntitiesObject(data.get('entities'))
        self.__favorite_count   = data.get('favorite_count')
        self.__tweet_id         = data.get('id_str')
        self.__reply_tweet_id   = data.get('in_reply_to_status_id_str')
        self.__reply_user_id    = data.get('in_reply_to_user_id_str')
        self.__lang             = data.get('lang')
        self.__quoted_status_id = data.get('quoted_status_id_str')
        self.__quoted_status    = self.__makeTweetObject(data.get('quoted_status'))
        self.__retweet_count    = data.get('retweet_count')
        self.__retweeted_status = self.__makeTweetObject(data.get('retweeted_status'))
        self.__text             = data.get('text')
        self.__user             = self.__makeUserObject(data.get('user'))
    

    def __str__(self):
        return json.dumps(self.__row_data, indent=2)
    

    def __makeTweetObject(self, data):
        if data is None:
            return None
        return ResponseObjectTweets(data)
    

    def __makeUserObject(self, data):
        if data is None:
            return None
        return users.ResponseObjectUsers(data)
    

    def __makeEntitiesObject(self, data):
        if data is None:
            return None
        return entities.ResponseObjectEntities(data)
    

    # ---------------------------------------------------------------------------
    # getter
    # ---------------------------------------------------------------------------


    def getContributors(self):
        return self.__contributors


    def getCoordinates(self):
        return self.__coordinates
    

    def getCreatedAt(self) -> str:
        return self.__created_at
    

    def getCurrentUserRetweet(self):
        return self.__current_user_retweet
    

    def getEntities(self) -> entities.ResponseObjectEntities:
        return self.__entities
    

    def getFavoriteCount(self) -> int:
        return self.__favorite_count
    

    def getTweetId(self) -> str:
        return self.__tweet_id
    

    def getReplyTweetId(self) -> str:
        return self.__reply_tweet_id
    

    def getReplyUserId(self) -> str:
        return self.__reply_user_id
    

    def getLang(self) -> str:
        return self.__lang
    

    def getQuotedTweetId(self) -> str:
        return self.__quoted_status_id
    

    def getQuotedTweet(self):
        '''@return ResponseObjectTweets
        '''
        return self.__quoted_status
    

    def getRetweetCount(self) -> int:
        return self.__retweet_count
    

    def getRetweetedTweet(self):
        '''@return ResponseObjectTweets
        '''
        return self.__retweeted_status
    

    def getText(self) -> str:
        return self.__text
    

    def getUser(self):
        '''ツイート投稿ユーザー
        '''
        return self.__user
