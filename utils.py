from PIL import Image
import os

def cut_photo(path):
    img = Image.open(path)
    width, height = img.size
    cropped_example = img.crop((0, 0, width, height - 60))
    cropped_example.save(path)

def cut_photo_2(path):
    img = Image.open(path)
    width, height = img.size
    cropped_example = img.crop((0, 0, width, height - width * 0.065))
    cropped_example.save(path)

def clear_mem():
    os.system('killall -9 chromedriver')
    os.system('killall -9 /opt/google/chrome/chrome')
