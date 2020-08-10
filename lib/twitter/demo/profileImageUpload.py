from lib.twitter.account.update_profile_image import TwitterApiAccountUpdateProfileImageInput, TwitterApiAccountUpdateProfileImageClient
from lib.twitter.media.upload import TwitterApiMediaUploadInput, TwitterApiMediaUploadClient


if __name__ == '__main__':
    # 動作確認
    image_path = './app/static/image/icon1.png'

    inp         = TwitterApiAccountUpdateProfileImageInput()
    inp.setImageFilePath(image_path)
    inp.setIncludeEntities(False)
    inp.setSkipStatus(True)

    client      = TwitterApiAccountUpdateProfileImageClient()
    response    = client.exec(inp)

    print(response.getStatus())
    print(response.getUser())
