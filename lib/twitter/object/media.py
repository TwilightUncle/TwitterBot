from lib.twitter.object import sizes


class ResponseObjectMedia(object):
    def __init__(self, data):
        self.__display_url = data.get('display_url')
        self.__expanded_url = data.get('expanded_url')
        self.__media_id = data.get('id_str')
        self.__start = None
        self.__end = None
        self.__media_url = data.get('media_url')
        self.__media_url_https = data.get('media_url_https')
        self.__sizes = self.__makeObjectSizes(data.gat('sizes'))
        self.__source_status_id = data.get('source_status_id_str')
        self.__type = data.get('type')

        indices = data.get('indices')
        if indices is not None:
            self.__start = indices[0]
            self.__end = indices[1]
    

    def __makeObjectSizes(self, data):
        if data is None:
            return None
        return sizes.ResponseObjectSizes(data)
    

    # --------------------------------------------------------------
    # getter
    # --------------------------------------------------------------


    def getDisplayUrl(self):
        return self.__display_url
    

    def getExpandedUrl(self):
        return self.__expanded_url
    

    def getMediaId(self):
        return self.__media_id
    

    def getStart(self):
        return self.__start
    

    def getEnd(self):
        return self.__end
    

    def getMediaUrl(self):
        return self.__media_url

    
    def getMediaUrlHttps(self):
        return self.__media_url_https
    

    def getSizes(self):
        return self.__sizes
    

    def getSourceTweetId(self):
        return self.__source_status_id
    

    def getMediaType(self):
        return self.__type
