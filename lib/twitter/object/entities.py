from lib.twitter.object import hashtags, media, urls, userMentions


class ResponseObjectEntities(object):
    def __init__(self, data):
        self.__hashtags         = []
        self.__media            = []
        self.__urls             = []
        self.__user_mentions    = []

        hashtags = data.get('hashtags')
        for hashtag in hashtags:
            self.__hashtags.append(self.__makeHashtag(hashtag))
        
        med = data.get('media	')
        for m in med:
            self.__media.append(self.__makeMedia(m))

        urls = data.get('urls')
        for url in urls:
            self.__urls.append(self.__makeUrl(url))
        
        user_mentions = data.get('user_mentions')
        for mention in user_mentions:
            self.__user_mentions.append(self.__makeUserMention(mention))
    

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
