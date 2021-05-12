import cv2
from PIL import Image
from PIL import ImageFont, ImageDraw
import os
import numpy as np
import matplotlib.pyplot as plt
import text_to_image
import time

import PIL.Image
import PIL.ImageFont
import PIL.ImageOps
import PIL.ImageDraw
import ffmpeg

#picture = Image.open('vald.png') 

ASCIIS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']
PIXEL_ON = 0  # PIL color to use for "on"
PIXEL_OFF = 255  # PIL color to use for "off"

def resize_image(picture):
    width, height = picture.size
    newWidth = 100
    newHeight = int((newWidth/width) * height)
    #print(newHeight)
    return picture.resize((newWidth, newHeight))

def getsize(image):
    return image.size
#video = cv2.VideoCapture('-----')

def convert_to_gray(image):
    return image.convert('L')



#graypic = convert_to_gray(resize_image(picture))

# min value is 0, max is 256
def ascii_convert(image):
    pixels = image.getdata()
    chars = ""
    for i in range(len(pixels)):
        if i %100 == 0:
            chars += '\n'
        chars += (ASCIIS[pixels[i]//25])
    return chars

def print_to_file(chars, filename):
    with open(filename, 'w') as f:
        f.write(chars)
    f.close()

def load_video(video_path):
    return cv2.VideoCapture(video_path)

# returns all frames as PIL Images in a video file given as argument
def get_frames(video_name):
    video = cv2.VideoCapture(video_name)
    frames = []
    while(video.isOpened()):
        ret, frame = video.read()
        if ret == False:
            break
        frames.append(Image.fromarray(frame)) # conversion step
    return frames




def text_image(text_path, font_path=None):
    """Convert text file to a grayscale image with black characters on a white background.

    arguments:
    text_path - the content of this file will be converted to an image
    font_path - path to a font file (for example impact.ttf)
    """
    grayscale = 'L'
    # parse the file into lines
    with open(text_path) as text_file:  # can throw FileNotFoundError
        lines = tuple(l.rstrip() for l in text_file.readlines())

    # choose a font (you can see more detail in my library on github)
    large_font = 20  # get better resolution with larger size
    font_path = font_path or 'cour.ttf'  # Courier New. works in windows. linux may need more explicit path
    try:
        font = PIL.ImageFont.truetype(font_path, size=large_font)
    except IOError:
        font = PIL.ImageFont.load_default()
        #print('Could not use chosen font. Using default.')

    # make the background image based on the combination of font and lines
    pt2px = lambda pt: int(round(pt * 96.0 / 72))  # convert points to pixels
    max_width_line = max(lines, key=lambda s: font.getsize(s)[0])
    # max height is adjusted down because it's too large visually for spacing
    test_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    max_height = pt2px(font.getsize(test_string)[1])
    max_width = pt2px(font.getsize(max_width_line)[0])
    height = max_height * len(lines)  # perfect or a little oversized
    width = int(round(max_width + 40))  # a little oversized
    image = PIL.Image.new(grayscale, (width, height), color=PIXEL_OFF)
    draw = PIL.ImageDraw.Draw(image)

    # draw each line of text
    vertical_position = 5
    horizontal_position = 5
    line_spacing = int(round(max_height * 0.8))  # reduced spacing seems better
    for line in lines:
        draw.text((horizontal_position, vertical_position),
                  line, fill=PIXEL_ON, font=font)
        vertical_position += line_spacing
    # crop the text
    c_box = PIL.ImageOps.invert(image).getbbox()
    image = image.crop(c_box)
    return image

""" def do_something(frames):
    for frame in frames:
    os.system('clear') """
    
a = get_frames('mister v.MOV')
print("frames = ", len(a))
i = 0
for frame in a:     
    i += 1
    os.system('clear')
    #print(ascii_convert(convert_to_gray(resize_image(frame)))) 
    print_to_file(ascii_convert(convert_to_gray(resize_image(frame))), 'frames/'+str(i))

images = []

i = 0
for filename in os.listdir('frames'):
    i += 1
    image = text_image('frames/'+filename)
    images.append(image)
    image.save(fp= 'frame_images/image{:03}.png'.format(i))
#vidpath = 'video.avi'

#out = cv2.VideoWriter(vidpath,cv2.VideoWriter_fourcc(*'mp4v'),1, getsize(images[0]))



    #i = cv2.imread(image)}
    #out.write(np.array(image))

#out.release()

(ffmpeg
    .input('frame_images/image%03d.png' ,framerate=24)
    .output('video2.avi')
    .run()
)
     






#print_to_file(ascii_convert(convert_to_gray(resize_image(picture))), 'ascii_image.txt')