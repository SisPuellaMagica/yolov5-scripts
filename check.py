import argparse
import os
from PIL import Image
import xml.etree.ElementTree as ElementTree


# check img file
def check_img_file(img_filepath):
    try:
        Image.open(img_filepath)
        if os.path.splitext(img_filepath)[1].lower() != '.jpg':
            os.rename(img_filepath, os.path.splitext(img_filepath)[0] + '.jpg')
        return True
    except:
        return False


# check img dir
def check_img_dir(img_dir):
    flag = True
    for img_filename in os.listdir(img_dir):
        img_filepath = img_dir + '/' + img_filename
        if not check_img_file(img_filepath):
            flag = False
            print('illegal img', img_filepath)
    return flag


# check xml file
def check_xml_file(xml_filepath):
    if os.path.splitext(xml_filepath)[1].lower() != '.xml':
        return False
    try:
        root = ElementTree.parse(xml_filepath).getroot()
        if root.tag != 'annotation':
            return False
        width = int(root.find('size').find('width').text)
        height = int(root.find('size').find('height').text)
        object_nodes = root.findall('object')
        if not len(object_nodes) >= 1:
            return False
        for object_node in object_nodes:
            name = object_node.find('name').text
            if len(name.strip()) == 0:
                return False
            xmin = int(object_node.find('bndbox').find('xmin').text)
            ymin = int(object_node.find('bndbox').find('ymin').text)
            xmax = int(object_node.find('bndbox').find('xmax').text)
            ymax = int(object_node.find('bndbox').find('ymax').text)
            if not (0 <= xmin and xmin < xmax and xmax <= width and 0 <= ymin and ymin < ymax and ymax <= height):
                return False
        return True
    except:
        return False


# check xml dir
def check_xml_dir(xml_dir):
    flag = True
    for xml_filename in os.listdir(xml_dir):
        xml_filepath = xml_dir + '/' + xml_filename
        if not check_xml_file(xml_filepath):
            flag = False
            print('illegal xml', xml_filepath)
    return flag


# check dataset
def check(img_dir, xml_dir):
    print('check dataset ...')
    flag1 = check_img_dir(img_dir)
    flag2 = check_xml_dir(xml_dir)
    flag3 = True
    for xml_filename in os.listdir(xml_dir):
        img_filepath = img_dir + '/' + os.path.splitext(xml_filename)[0] + '.jpg'
        xml_filepath = xml_dir + '/' + xml_filename
        if check_img_file(img_filepath) and check_xml_file(xml_filepath):
            img = Image.open(img_filepath)
            size_node = ElementTree.parse(xml_filepath).getroot().find('size')
            if not (img.width == int(size_node.find('width').text) and img.height == int(size_node.find('height').text)):
                flag3 = False
                print('width or height does not match', img_filepath, xml_filepath)
        elif (not check_img_file(img_filepath)) and check_xml_file(xml_filepath):
            flag3 = False
            print('miss img', xml_filepath)
        else:
            flag3 = False
    flag = flag1 and flag2 and flag3
    if flag:
        print('no problem')
    else:
        print('please check your dataset')
    return flag


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--img-dir', type=str)
    parser.add_argument('--xml-dir', type=str)
    opt = parser.parse_args()
    check(opt.img_dir, opt.xml_dir)
