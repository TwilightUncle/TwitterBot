

class ResponseObjectHashtags(object):
    def __init__(self, data):
        self.__start    = None
        self.__end      = None
        self.__text     = data.get('text')

        indices = data.get('indices')
        if indices is not None:
            self.__start    = indices[0]
            self.__end      = indices[1]

    
    # --------------------------------------------------------------
    # getter
    # --------------------------------------------------------------    


    def getStart(self):
        return self.__start
    

    def getEnd(self):
        return self.__end
    

    def getText(self):
        return self.__text
