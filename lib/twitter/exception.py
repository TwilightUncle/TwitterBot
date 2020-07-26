class TwitterRequiredParameterError(Exception):
    '''必須のリクエストパラメータをセットしないままリクエストを試みた場合に投げられます
    '''
    pass
