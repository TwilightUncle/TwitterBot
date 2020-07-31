class TwitterRequiredParameterError(Exception):
    '''必須のリクエストパラメータをセットしないままリクエストを試みた場合に投げられます
    '''
    pass


class TwitterValidateParamaterError(Exception):
    '''各パラメータに必要な要件を満たしていないとき投げられる
    '''
    pass