import json
from lib.twitter.object import size


class ResponseObjectSizes(object):
    def __init__(self, data):
        self.__row_data = data
        self.__thumb    = self.__makeSizeObject(data.get('thumb'))
        self.__large    = self.__makeSizeObject(data.get('large'))
        self.__medium   = self.__makeSizeObject(data.get('medium'))
        self.__small    = self.__makeSizeObject(data.get('small'))
    

    def __str__(self):
        return json.dumps(self.__row_data, indent=2)
    

    def __makeSizeObject(self, data):
        if data is None:
            return None
        return size.ResponseObjectSize(data)
    

    # --------------------------------------------------------------
    # getter
    # --------------------------------------------------------------


    def getThumbSize(self) -> size.ResponseObjectSize:
        return self.__thumb
    

    def getLargeSize(self) -> size.ResponseObjectSize:
        return self.__large
    

    def getMediumSize(self) -> size.ResponseObjectSize:
        return self.__medium
    

    def getSmallSize(self) -> size.ResponseObjectSize:
        return self.__small
