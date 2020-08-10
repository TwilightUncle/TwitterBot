import json
from lib.twitter.object import tweets, entities


class ResponseObjectUsers(object):
    '''Apiレスポンスのユーザーオブジェクト
    \n http://westplain.sakuraweb.com/translate/twitter/API-Overview/Users.cgi
    '''


    def __init__(self, data):
        self.__row_data                             = data
        self.__created_at                           = data.get('created_at')
        self.__default_profile                      = data.get('default_profile')    # true のとき、 背景を変更指定してない
        self.__default_profile_image                = data.get('default_profile_image')    # true の時プロフ画をアップロードしていない
        self.__description                          = data.get('description')    # 自己紹介
        self.__entities                             = self.__makeEntitiesObject(data.get('entities'))
        self.__favourites_count                     = data.get('favourites_count')  # ユーザーがお気に入り登録した数
        self.__follow_request_sent                  = data.get('follow_request_sent')
        self.__followers_count                      = data.get('followers_count')    # フォロワー数
        self.__friends_count                        = data.get('friends_count')    # フォロー数
        self.__user_id                              = data.get('id_str') 
        self.__lang                                 = data.get('lang')
        self.__listed_count                         = data.get('listed_count')
        self.__location                             = data.get('location')
        self.__name                                 = data.get('name')
        self.__profile_background_image_url         = data.get('profile_background_image_url')
        self.__profile_background_image_url_https   = data.get('profile_background_image_url_https')
        self.__profile_image_url                    = data.get('profile_image_url')
        self.__profile_image_url_https              = data.get('profile_image_url_https')
        self.__protected                            = data.get('protected')
        self.__screen_name                          = data.get('screen_name')
        self.__status                               = self.__makeTweetObject(data.get('status'))
        self.__statuses_count                       = data.get('statuses_count')
        self.__url                                  = data.get('url')
    

    def __str__(self):
        return json.dumps(self.__row_data, indent=2)

        
    def __makeTweetObject(self, data):
        if data is None:
            return None
        return tweets.ResponseObjectTweets(data)
    

    def __makeEntitiesObject(self, data):
        if data is None:
            return None
        return entities.ResponseObjectEntities(data)
    

    # --------------------------------------------------------------
    # getter
    # --------------------------------------------------------------


    def getCreatedAt(self) -> str:
        return self.__created_at
    

    def getDefaultProfile(self) -> bool:
        return self.__default_profile
    

    def getDefaultProfileImage(self) -> bool:
        return self.__default_profile
    

    def getDescription(self) -> str:
        return self.__description
    

    def getEntities(self) -> entities.ResponseObjectEntities:
        return self.__entities
    

    def getFavoritesCount(self) -> int:
        return self.__favourites_count
    

    def getFollowRequestSent(self) -> bool:
        return self.__follow_request_sent
    

    def getFollowersCount(self) -> int:
        return self.__followers_count
    

    def getFrendsCount(self) -> int:
        return self.__friends_count
    

    def getUserId(self) -> str:
        return self.__user_id
    

    def getLang(self) -> str:
        return self.__lang
    

    def getListedCount(self) -> int:
        return self.__listed_count
    

    def getLocation(self) -> str:
        return self.__location
    

    def getUserName(self) -> str:
        return self.__name
    

    def getProfileBackgroundImageUrl(self) -> str:
        return self.__profile_background_image_url
    

    def getProfileBackgroundImageUrlHttps(self) -> str:
        return self.__profile_background_image_url_https
    

    def getProfileImageUrl(self) -> str:
        return self.__profile_image_url
    

    def getProfileImageUrlHttps(self) -> str:
        return self.__profile_image_url_https
    

    def getIsProtected(self) -> bool:
        return self.__protected
    

    def getScreenName(self) -> str:
        return self.__screen_name
    

    def getRecentTweet(self):
        return self.__status
    

    def getStatusesCount(self) -> int:
        return self.__statuses_count
    

    def getUrl(self) -> str:
        '''ユーザーが自分のプロフィールの関連項目として付けた URL
        '''
        return self.__url
