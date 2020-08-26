import urllib
from flask import current_app
from app.models import Bot
from app.views.common import saveUploadedImage, getAllErrorText
from lib.twitter import updateProfileImage


def saveImage(bot_id:int, profile_image, background_image) -> (str, str):
    '''return profile_image_saved_filename, background_image_saved_filename
    '''
    profile_image_saved_filename = ''
    background_image_saved_filename = ''

    if profile_image:
        profile_image_saved_filename = saveUploadedImage(
            profile_image, 
            f"{current_app.config['UPLOAD_BOT_PROFILE_IMAGE_FOLDER']}/{bot_id}"
        )
    # if background_image:
    #     background_image_saved_filename = saveUploadedImage(
    #         background_image, 
    #         f"{current_app.config['UPLOAD_BOT_PROFILE_BACKGROUND_IMAGE_FOLDER']}/{bot_id}"
    #     )

    return profile_image_saved_filename, background_image_saved_filename


def sendProfileImageForTwitter(bot:Bot, error:list, profile_image_filename:str, background_image_filename:str) -> list:
    try:
        if profile_image_filename != '':
            updateProfileImage(
                image_file_path=profile_image_filename,
                access_token=bot.access_token,
                access_secret=bot.secret_token
            )
        if background_image_filename != '':
            pass
    except urllib.error.HTTPError as err:
        text = getHttpErrorText(err)
        error.append(text)
    except Exception as err:
        error.append(getAllErrorText(err))
    
    return error
