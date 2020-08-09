from lib.twitter.object import hashtags, media, urls, userMentions


class ResponseObjectEntities(object):
    def __init__(self, data):
        self.__hashtags         = self.__checkNoneAndApplyListItems(data.get('hashtags')      , self.__makeHashtag)
        self.__media            = self.__checkNoneAndApplyListItems(data.get('media')         , self.__makeMedia)
        self.__urls             = self.__checkNoneAndApplyListItems(data.get('urls')          , self.__makeUrl)
        self.__user_mentions    = self.__checkNoneAndApplyListItems(data.get('user_mentions') , self.__makeUserMention)
    

    def __checkNoneAndApplyListItems(self, li:list, callback):
        '''リストの各要素に関数を適用する
        \n callback ... リストの各要素を引数として渡す関数
        '''
        if type(li) is not list:
            return None
        results = []
        for item in li:
            results.append(callback(item))
        return results
    

    def __makeHashtag(self, data):
        if data is None:
            return None
        return hashtags.ResponseObjectHashtags(data)
    

    def __makeMedia(self, data):
        if data is None:
            return None
        return media.ResponseObjectMedia(data)
    

    def __makeUrl(self, data):
        if data is None:
            return None
        return urls.ResponseObjectUrls(data)
    

    def __makeUserMention(self, data):
        if data is None:
            return None
        return userMentions.ResponseObjectUserMentions(data)
    

    # --------------------------------------------------------------
    # getter
    # --------------------------------------------------------------


    def getHashtags(self) -> [hashtags.ResponseObjectHashtags]:
        return self.__hashtags
    

    def getMedia(self) -> [media.ResponseObjectMedia]:
        return self.__media
    

    def getUrls(self) -> [urls.ResponseObjectUrls]:
        return self.__urls
    

    def getUserMentions(self) -> [userMentions.ResponseObjectUserMentions]:
        return self.__user_mentions
