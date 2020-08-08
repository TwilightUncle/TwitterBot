import urllib.parse


class ResponseObjectSearchMetadata(object):
    '''Apiレスポンスの検索メタデータ
    \n http://westplain.sakuraweb.com/translate/twitter/Documentation/REST-APIs/Public-API/GET-search-tweets.cgi
    '''


    def __init__(self, data:dict):
        self.__max_id           = data.get('max_id_str')
        self.__since_id         = data.get('since_id_str')
        self.__refresh_url      = data.get('refresh_url')
        self.__next_results     = data.get('next_results')
        self.__results_count    = data.get('count')
        self.__query            = urllib.parse.unquote(data.get('query'), 'utf-8')
    

    def getMaxId(self):
        return self.__max_id
    

    def getSinceId(self):
        return self.__since_id
    

    def getRefreshUrl(self):
        return self.__refresh_url
    

    def getNextResults(self):
        return self.__next_results
    

    def getResultsCount(self):
        return self.__results_count
    

    def getSearchQuery(self):
        return self.__query
