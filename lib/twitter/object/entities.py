import json
from lib.utils import checkIterableAndMap
from lib.twitter.object import hashtags, media, urls, userMentions


class ResponseObjectEntities(object):
    def __init__(self, data):
        self.__row_data         = data
        self.__hashtags         = checkIterableAndMap(data.get('hashtags')         , self.__makeHashtag     , 'list')
        self.__media            = checkIterableAndMap(data.get('media')            , self.__makeMedia       , 'list')
        self.__urls             = checkIterableAndMap(data.get('urls')             , self.__makeUrl         , 'list')
        self.__user_mentions    = checkIterableAndMap(data.get('user_mentions')    , self.__makeUserMention , 'list')
    

    def __str__(self):
        return json.dumps(self.__row_data, indent=2)
    

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
