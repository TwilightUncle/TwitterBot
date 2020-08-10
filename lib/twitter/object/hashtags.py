import json


class ResponseObjectHashtags(object):
    def __init__(self, data):
        self.__row_data = data
        self.__start    = None
        self.__end      = None
        self.__text     = data.get('text')

        indices = data.get('indices')
        if indices is not None:
            self.__start    = indices[0]
            self.__end      = indices[1]
    

    def __str__(self):
        return json.dumps(self.__row_data, indent=2)

    
    # --------------------------------------------------------------
    # getter
    # --------------------------------------------------------------    


    def getStart(self) -> int:
        return self.__start
    

    def getEnd(self) -> int:
        return self.__end
    

    def getText(self) -> str:
        return self.__text
