import math

from PIL import ImageColor
from PIL import Image

path ="Paragons/paragon7.jpg"
im  =Image.open(path)
print(im.size)
print(im.format_description)
def resize_image(input_path= path, output_path ="Paragons/paragon8.jpg", max_width =1200,max_height= 900):
    # Open the image file
    with Image.open(input_path) as img:
        # chage color from rgba to rgb , rgba not available to this format
        img = img.convert('RGB')
        aspect_ratio = min(max_width / img.width, max_height / img.height)
        new_size = (int(img.width * aspect_ratio), int(img.height * aspect_ratio))

        resized_img = img.resize(new_size)
        resized_img.save(output_path)

resize_image()




