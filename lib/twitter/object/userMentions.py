

class ResponseObjectUserMentions(object):
    def __init__(self, data):
        self.__mention_user_id          = data.get('id_str')
        self.__start                    = None
        self.__end                      = None
        self.__mention_user_name        = data.get('name')
        self.__mention_user_screen_name = data.get('screen_name')

        indices = data.get('indices')
        if indices is not None:
            self.__start = indices[0]
            self.__end = indices[1]
    

    # --------------------------------------------------------------
    # getter
    # --------------------------------------------------------------


    def getMentionUserId(self) -> str:
        return self.__mention_user_id
    

    def getStart(self) -> int:
        return self.__start
    

    def getEnd(self) -> int:
        return self.__end
    

    def getMentionUserName(self) -> str:
        return self.__mention_user_name
    

    def getMentionUserScreenName(self) -> str:
        return self.__mention_user_screen_name
