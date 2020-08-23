# ------------------------
# 定数定義
# ------------------------

class ApplicationConst:
    # tweet type
    TWEET_TYPE_REGULARLY = 1 # 頻度のテーブルをどこかに持つ
    TWEET_TYPE_REPLY = 2 # 返信先についてのテーブルをどこかに持つ
    TWEET_TYPE_WEIGHT_UP = 3
    TWEET_TYPE_WEIGHT_DOWN = 4
    TWEET_TYPE_WEIGHT_ENPTY = 5

    # permissions
    PERMISSION_ADMIN = 1
    PERMISSION_BACKEND = 2
    PERMISSION_NOMAL = 3

    PERMISSION_NAMES = {
        PERMISSION_NOMAL : '一般会員',
        PERMISSION_BACKEND : 'スタッフ',
        PERMISSION_ADMIN : '管理者'
    }

constant = ApplicationConst()
