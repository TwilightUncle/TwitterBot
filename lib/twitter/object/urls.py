

class ResponseObjectUrls(object):
    def __init__(self, data):
        self.__display_url = data.get('display_url')
        self.__expanded_url = data.get('expanded_url')
        self.__start = None
        self.__end = None
        self.__url = data.get('url')

        indices = data.get('indices')
        if indices is not None:
            self.__start = indices[0]
            self.__end = indices[1]
    

    # --------------------------------------------------------------
    # getter
    # --------------------------------------------------------------


    def getDisplayUrl(self) -> str:
        return self.__display_url
    

    def getExpandedUrl(self) -> str:
        return self.__expanded_url

    
    def getStart(self) -> int:
        return self.__start
    

    def getEnd(self) -> int:
        return self.__end
    

    def getUrl(self) -> str:
        return self.__url
