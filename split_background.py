import argparse
import os
from shutil import move


# split background img
def split_background(img_dir, xml_dir):
    print('split background img ...')
    background_dir = os.path.dirname(img_dir) + '/' + 'backgrounds'
    if not os.path.exists(background_dir):
        os.makedirs(background_dir)
    for img_filename in os.listdir(img_dir):
        img_filepath = img_dir + '/' + img_filename
        xml_filepath = xml_dir + '/' + os.path.splitext(img_filename)[0] + '.xml'
        if not os.path.exists(xml_filepath):
            move(img_filepath, background_dir + '/' + img_filename)
    print('finish')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--img-dir', type=str)
    parser.add_argument('--xml-dir', type=str)
    opt = parser.parse_args()
    split_background(
        img_dir=opt.img_dir,
        xml_dir=opt.xml_dir
    )
