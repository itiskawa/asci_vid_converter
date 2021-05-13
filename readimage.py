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
import shutil

#picture = Image.open('vald.png') 

ASCIIS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.', ' ']
PIXEL_ON = 0  # PIL color to use for "on"
PIXEL_OFF = 255  # PIL color to use for "off"
IMAGE_WIDTH = 100

def resize_image(picture):
    width, height = picture.size
    newHeight = int((IMAGE_WIDTH/width) * height)
    return picture.resize((IMAGE_WIDTH, newHeight))

def getsize(image):
    return image.size

def convert_to_gray(image):
    return image.convert('L')

#graypic = convert_to_gray(resize_image(picture))

# min value is 0, max is 256
def ascii_convert(image):
    pixels = image.getdata()
    max_pixel = max(pixels)
    min_pixel = min(pixels)
    pixel_range = max_pixel - min_pixel
    ascii_range = len(ASCIIS) - 1
    chars = ""
    for i in range(len(pixels)):
        if i % IMAGE_WIDTH == 0:
            chars += '\n'
        map_index = round((pixels[i] - min_pixel) / pixel_range * ascii_range)
        chars += (ASCIIS[map_index])
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
    
def run_from_webcam():
    cap = cv2.VideoCapture(0)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    while(cap.isOpened() ):
        ret, frame = cap.read()
        if ret == True:
            frame = cv2.flip(frame,1)  
            frame_img = Image.fromarray(frame)
            print(ascii_convert(convert_to_gray(resize_image(frame_img)))) 
        else:
            break
    cap.release()

def convert_video_to_text_files(input_path, temp_path):
    a = get_frames(input_path)
    i = 0
    for frame in a:     
        #print(ascii_convert(convert_to_gray(resize_image(frame)))) 
        #os.system('clear')
        print_to_file(ascii_convert(convert_to_gray(resize_image(frame))), temp_path + str(i))
        i += 1
    return i

def convert_text_files_to_video(txt_files_path, img_files_path, out_path, num_text_files):
    image_paths = []
    for i in range(num_text_files):
        image = text_image(txt_files_path + str(i))
        filepath = img_files_path + str(i)+".png"
        image.save(fp= filepath)
        image_paths.append(filepath)

    vidpath = out_path + 'video.avi'
    w, h, _ = cv2.imread(image_paths[0]).shape
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")

    fps = 20
    out = cv2.VideoWriter(vidpath, fourcc, fps, (h, w))

    for filepath in image_paths:
        img = cv2.imread(filepath)
        out.write(img)
    out.release()
        
def run_from_file(input_path):
    temp_file_path = ".temp/"
    txt_files_path = temp_file_path + "text_frames/"
    img_files_path = temp_file_path + "image_frames/"

    out_path = "output/"
    if not os.path.isdir(out_path):
        os.mkdir(out_path)

    os.makedirs(txt_files_path)
    os.makedirs(img_files_path)
    
    num_frame = convert_video_to_text_files(input_path, txt_files_path)
    convert_text_files_to_video(txt_files_path, img_files_path, out_path, num_frame)
    shutil.rmtree(temp_file_path) 


run_from_file('input/mister v.MOV')
#run_from_webcam()