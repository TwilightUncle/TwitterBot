import json
from lib.twitter.object import sizes


class ResponseObjectMedia(object):
    def __init__(self, data):
        self.__row_data         = data
        self.__display_url      = data.get('display_url')
        self.__expanded_url     = data.get('expanded_url')
        self.__media_id         = data.get('id_str')
        self.__start            = None
        self.__end              = None
        self.__media_url        = data.get('media_url')
        self.__media_url_https  = data.get('media_url_https')
        self.__sizes            = self.__makeObjectSizes(data.get('sizes'))
        self.__source_status_id = data.get('source_status_id_str')
        self.__type             = data.get('type')

        indices = data.get('indices')
        if indices is not None:
            self.__start = indices[0]
            self.__end = indices[1]
    

    def __str__(self):
        return json.dumps(self.__row_data, indent=2)
    

    def __makeObjectSizes(self, data):
        if data is None:
            return None
        return sizes.ResponseObjectSizes(data)
    

    # --------------------------------------------------------------
    # getter
    # --------------------------------------------------------------


    def getDisplayUrl(self) -> str:
        return self.__display_url
    

    def getExpandedUrl(self) -> str:
        return self.__expanded_url
    

    def getMediaId(self) -> str:
        return self.__media_id
    

    def getStart(self) -> int:
        return self.__start
    

    def getEnd(self) -> int:
        return self.__end
    

    def getMediaUrl(self) -> str:
        return self.__media_url

    
    def getMediaUrlHttps(self) -> str:
        return self.__media_url_https
    

    def getSizes(self) -> sizes.ResponseObjectSizes:
        return self.__sizes
    

    def getSourceTweetId(self) -> str:
        return self.__source_status_id
    

    def getMediaType(self) -> str:
        return self.__type
