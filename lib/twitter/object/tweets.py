

class ResponseObjectTweets(object):
    '''Apiレスポンスのツイートオブジェクト。
    \n http://westplain.sakuraweb.com/translate/twitter/API-Overview/Tweets.cgi
    '''


    def __init__(self, data:dict):
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
        self.__quoted_status_id = None              # リツイート元ツイートID
        self.__quoted_status    = None              # 引用元ツイート情報
        self.__retweet_count    = None              # リツイートされた回数
        self.__text             = None              # ツイートの本文
        self.__user             = None              # 投稿ユーザー情報。ResponseObjectUserを参照

        self.__coordinates      = data.get('coordinates')
        self.__created_at       = data.get('created_at')
        self.__favorite_count   = data.get('favorite_count')
        self.__tweet_id         = data.get('id_str')
        self.__reply_tweet_id   = data.get('in_reply_to_status_id')
        self.__reply_user_id    = data.get('in_reply_to_user_id_str')
        self.__lang             = data.get('lang')
        self.__quoted_status_id = data.get('quoted_status_id_str')
        self.__retweet_count    = data.get('retweet_count')
        self.__text             = data.get('text')
    

    # ---------------------------------------------------------------------------
    # getter
    # ---------------------------------------------------------------------------


    def getContributors(self):
        return self.__contributors


    def getCoordinates(self):
        return self.__coordinates
    

    def getCreatedAt(self):
        return self.__created_at
    

    def getCurrentUserRetweet(self):
        return self.__current_user_retweet
    

    def getEntities(self):
        return self.__entities
    

    def getFavoriteCount(self):
        return self.__favorite_count
    

    def getContributorId(self):
        return self.__user_id
    

    def getReplyTweetId(self):
        return self.__reply_tweet_id
    

    def getReplyUserId(self):
        return self.__reply_user_id
    

    def getLang(self):
        return self.__lang
    

    def getQuotedTweetId(self):
        return self.__quoted_status_id
    

    def getQuotedTweet(self):
        return self.__quoted_status
    

    def getRetweetCount(self):
        return self.__retweet_count
    

    def getText(self):
        return self.__text
