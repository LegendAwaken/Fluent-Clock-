# this class get the radius of the blur and blur the wincdow

# take screen shot of the windows

from pyautogui import screenshot
from PIL import Image, ImageFilter
from kivy.clock import Clock
import os


def WindowBlur(radius=5):
    try:
        get_image = screenshot()

        # save the acquired screenshot
        get_image.save('./image.png')

        # open the image
        image = Image.open('./image.png')

        # blur the image
        blurred_image = image.filter(ImageFilter.GaussianBlur(radius=radius))

        blurred_image_saved = blurred_image.save('./assets/blur_window.png')

        # return blurred png
        return blurred_image_saved

    except ValueError:
        return 'Radius cannot be string.'


def delete(file='./blur_window.png'):
    try:
        os.remove('./assets/blur_window.png')
        os.remove('./image.png')
    except FileNotFoundError:
        pass


Clock.schedule_interval(delete, 3)
