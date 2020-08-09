

class ResponseObjectSize(object):
    def __init__(self, data):
        self.__height   = data.get('h')
        self.__width    = data.get('w')
        self.__resize   = data.get('resize')
    

    # --------------------------------------------------------------
    # getter
    # --------------------------------------------------------------


    def getHeight(self) -> int:
        return self.__height
    

    def getWidth(self) -> int:
        return self.__width
    

    def getResize(self) -> str:
        '''戻り値は以下の二種類
        \n fit ... 元の縦横比を維持したまま一辺を合わせる形でサイズ変更
        \n crop ... 特定の解像度に合わせるためにメディアの切抜きが行われた
        '''
        return self.__resize
