from lib.twitter.account.update_profile import accountUpdateProfile


if __name__ == '__main__':
    # 動作確認

    response    = accountUpdateProfile(
        name='ダイエット支援bot☆くるみちゃん',
        location='ダイエットしてるおにいちゃんを応援できるところ',
        description='まだね、くるみ、おにいちゃんにかいはつされてるの'
    )

    print(response.getStatus())
    print(response.getUser())
