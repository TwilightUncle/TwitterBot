from lib.twitter.account.update_profile_image import updateProfileImage


if __name__ == '__main__':
    # 動作確認
    image_path = './app/static/image/icon1.png'

    response    = updateProfileImage(image_path, False, True)

    print(response.getStatus())
    print(response.getUser())
