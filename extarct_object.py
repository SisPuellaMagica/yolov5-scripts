import argparse
import os
from PIL import Image
import xml.etree.ElementTree as ElementTree


# get object img from xml
def get_object(img_filepath, xml_filepath, object_dir):
    img = Image.open(img_filepath)
    object_nodes = ElementTree.parse(xml_filepath).getroot().findall('object')
    i = 0
    for object_node in object_nodes:
        i += 1
        name = object_node.find('name').text
        if not os.path.exists(object_dir + '/' + name):
            os.makedirs(object_dir + '/' + name)
        xmin = int(object_node.find('bndbox').find('xmin').text)
        ymin = int(object_node.find('bndbox').find('ymin').text)
        xmax = int(object_node.find('bndbox').find('xmax').text)
        ymax = int(object_node.find('bndbox').find('ymax').text)
        crop = img.crop((xmin, ymin, xmax, ymax))
        crop.save(object_dir + '/' + name + '/' + os.path.splitext(os.path.basename(img_filepath))[0] + '_' + str(i) + '.jpg')


# extract object img
def extract_object(img_dir, xml_dir):
    print('extract object img ...')
    object_dir = os.path.dirname(img_dir) + '/' + 'objects'
    if not os.path.exists(object_dir):
        os.makedirs(object_dir)
    for xml_filename in os.listdir(xml_dir):
        img_filepath = img_dir + '/' + os.path.splitext(xml_filename)[0] + '.jpg'
        xml_filepath = xml_dir + '/' + xml_filename
        get_object(img_filepath, xml_filepath, object_dir)
    print('finish')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--img-dir', type=str)
    parser.add_argument('--xml-dir', type=str)
    opt = parser.parse_args()
    extract_object(
        img_dir=opt.img_dir,
        xml_dir=opt.xml_dir
    )
