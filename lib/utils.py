# ========================================================
# 便利かもしれない関数
# ========================================================
import random, string


def generateRandomString(n:int) -> str:
    '''アルファベットと数値のみのランダムな値を返します
    '''
    return ''.join(random.choices(string.ascii_letters + string.digits, k=n))


def checkIterableAndMap(func, container, ret_type=None):
    '''__getitem__はめんどくさいので考慮しません
    \n containerが回せないオブジェクトだったときNoneを返し、それ以外はmapそのままです。
    '''
    if hasattr(container, '__iter__'):
        results = map(func, container)
        if ret_type == 'list':
            results = list(results)
        return results
    return None
