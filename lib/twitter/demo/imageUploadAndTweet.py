from lib.twitter.statuses.update import statusesUpdate
from lib.twitter.media.upload import mediaUpload


if __name__ == '__main__':
    # 動作確認
    image_path = './app/static/image/icon1.png'
    media_res = mediaUpload(image_path)
    media_id = media_res.getMediaId()
    print(media_res.getStatus())
    print('media_id ... ' + media_id)
    print('media_type ... ' + media_res.getImageType())

    tweet_res = statusesUpdate(
        tweet='てすーと～',
        media_ids=[
            media_id
        ],
    )
