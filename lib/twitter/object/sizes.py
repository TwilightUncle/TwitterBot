from lib.twitter.object import size


class ResponseObjectSizes(object):
    def __init__(self, data):
        self.__thumb    = self.__makeSizeObject(data.get('thumb'))
        self.__large    = self.__makeSizeObject(data.get('large'))
        self.__medium   = self.__makeSizeObject(data.get('medium'))
        self.__small    = self.__makeSizeObject(data.get('small'))
    

    def __makeSizeObject(self, data):
        if data is None:
            return None
        return size.ResponseObjectSize(data)
    

    # --------------------------------------------------------------
    # getter
    # --------------------------------------------------------------


    def getThumbSize(self):
        return self.__thumb
    

    def getLargeSize(self):
        return self.__large
    

    def getMediumSize(self):
        return self.__medium
    

    def getSmallSize(self):
        return self.__small
