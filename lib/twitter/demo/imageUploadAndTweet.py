from lib.twitter.statuses.update import TwitterApiStatusesUpdateInput, TwitterApiStatusesUpdateClient
from lib.twitter.media.upload import TwitterApiMediaUploadInput, TwitterApiMediaUploadClient


if __name__ == '__main__':
    # 動作確認
    image_path = './app/static/image/icon1.png'
    media_input = TwitterApiMediaUploadInput()
    media_input.setMediaFilePath(image_path)
    media_client = TwitterApiMediaUploadClient()
    media_res = media_client.exec(media_input)
    media_id = media_res.getMediaId()
    print(media_res.getStatus())
    print('media_id ... ' + media_id)
    print('media_type ... ' + media_res.getImageType())

    tweet_input = TwitterApiStatusesUpdateInput()
    tweet_input.setTweet('てすーと～')
    tweet_input.setMediaId(media_id)
    tweet_client = TwitterApiStatusesUpdateClient()
    tweet_res = tweet_client.exec(tweet_input)
