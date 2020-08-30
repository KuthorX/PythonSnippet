'''
Python 3.7

Require ffmpeg-python==0.2.0

Get snapshot based on video bitrate.

Run python snapshot_ffmpeg.py -h to get more info.
'''

import ffmpeg
import json
import os
from pathlib import Path
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", help="input video", default="test_video.mp4")
parser.add_argument("-o", help="output image directory", default="out/img")
args = parser.parse_args()


TEST_FILE = args.i
OUTPUT_DIR = args.o

# try to get r_frame_rate, pix_fmt, nb_frames to name output images
probe_data = ffmpeg.probe(TEST_FILE)
pj = json.dumps(probe_data)

for stream in probe_data["streams"]:
    if stream["codec_type"] == "video":
        pix_fmt = stream["pix_fmt"]
        r_frame_rate = stream["r_frame_rate"]
        nb_frames = stream["nb_frames"]

if pix_fmt is None or r_frame_rate is None:
    print("Error", "no pix_fmt or r_frame_rate")
    exit(-1)
if nb_frames is None:
    # default to 1000
    nb_frames = 1000


def get_digits_format(num):
    # ex: 10000 has 5 digits, so return %05d
    digits = 0
    num = int(num)
    while num > 0:
        num = int(num / 10)
        digits += 1
    return f'%0{digits}d'


prefix_f = get_digits_format(nb_frames)

# confirm img stored directory
base = os.path.basename(TEST_FILE)
file_name = os.path.splitext(base)[0]
target_dir = OUTPUT_DIR + f'/{file_name}'
Path(target_dir).mkdir(parents=True, exist_ok=True)

# ffmpeg will auto load pix_fmt and r_frame_rate
out, _ = (
    ffmpeg
    .input(TEST_FILE)
    .output(f'{target_dir}/{prefix_f}_{r_frame_rate.replace("/", "d")}_{pix_fmt}.jpg')
    .run(capture_stdout=True)
)

print('-'*11, 'end', '-' * 11)
