import json
import urllib.parse


class ResponseObjectSearchMetadata(object):
    '''Apiレスポンスの検索メタデータ
    \n http://westplain.sakuraweb.com/translate/twitter/Documentation/REST-APIs/Public-API/GET-search-tweets.cgi
    '''


    def __init__(self, data:dict):
        self.__row_data         = data
        self.__max_id           = data.get('max_id_str')
        self.__since_id         = data.get('since_id_str')
        self.__refresh_url      = data.get('refresh_url')
        self.__next_results     = data.get('next_results')
        self.__results_count    = data.get('count')
        self.__query            = urllib.parse.unquote(data.get('query'), 'utf-8')
    

    def __str__(self):
        return json.dumps(self.__row_data, indent=2)
    

    def getMaxId(self) -> str:
        return self.__max_id
    

    def getSinceId(self) -> str:
        return self.__since_id
    

    def getRefreshUrl(self) -> str:
        return self.__refresh_url
    

    def getNextResults(self) -> str:
        return self.__next_results
    

    def getResultsCount(self) -> int:
        return self.__results_count
    

    def getSearchQuery(self) -> str:
        return self.__query
