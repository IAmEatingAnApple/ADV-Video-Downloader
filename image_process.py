from PIL import Image

def crop_thumbnail(path: str):
    img = Image.open(path)

    #crop from 640x480 to 640x360
    img2 = img.crop((0, 60, 640, 420))

    img2.save(path)