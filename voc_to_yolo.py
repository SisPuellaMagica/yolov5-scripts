import argparse
import os
import xml.etree.ElementTree as ElementTree


# get class names
def get_class_names(xml_dir):
    class_names = []
    for xml_filename in os.listdir(xml_dir):
        xml_filepath = xml_dir + '/' + xml_filename
        object_nodes = ElementTree.parse(xml_filepath).getroot().findall('object')
        for object_node in object_nodes:
            name = object_node.find('name').text
            if name not in class_names:
                class_names.append(name)
    return class_names


# xml to txt
def xml_to_txt(xml_filepath, class_names, txt_filepath):
    root = ElementTree.parse(xml_filepath).getroot()
    width = int(root.find('size').find('width').text)
    height = int(root.find('size').find('height').text)
    object_nodes = root.findall('object')
    lines = []
    for object_node in object_nodes:
        xmin = int(object_node.find('bndbox').find('xmin').text)
        ymin = int(object_node.find('bndbox').find('ymin').text)
        xmax = int(object_node.find('bndbox').find('xmax').text)
        ymax = int(object_node.find('bndbox').find('ymax').text)
        idx = class_names.index(object_node.find('name').text)
        yolo_center_x = (xmin + xmax) / 2 / width
        yolo_center_y = (ymin + ymax) / 2 / height
        yolo_width = (xmax - xmin) / width
        yolo_height = (ymax - ymin) / height
        lines.append(str(idx) + ' ' + str(yolo_center_x) + ' ' + str(yolo_center_y) + ' ' + str(yolo_width) + ' ' + str(yolo_height))
    with open(txt_filepath, 'w', encoding='utf-8') as f:
        for i in range(len(lines)):
            f.write(lines[i])
            if i < len(lines) - 1:
                f.write('\n')


# voc => yolo
def voc_to_yolo(img_dir, xml_dir):
    print('voc => yolo ...')
    txt_dir = os.path.dirname(img_dir) + '/' + 'labels'
    if not os.path.exists(txt_dir):
        os.makedirs(txt_dir)
    class_names = get_class_names(xml_dir)
    for img_filename in os.listdir(img_dir):
        xml_filepath = xml_dir + '/' + os.path.splitext(img_filename)[0] + '.xml'
        txt_filepath = txt_dir + '/' + os.path.splitext(img_filename)[0] + '.txt'
        if os.path.exists(xml_filepath):
            xml_to_txt(xml_filepath, class_names, txt_filepath)
        else:
            file = open(txt_filepath, 'w', encoding='utf-8')
            file.close()
    print('finish')
    print('class_names', class_names)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--img-dir', type=str)
    parser.add_argument('--xml-dir', type=str)
    opt = parser.parse_args()
    voc_to_yolo(
        img_dir=opt.img_dir,
        xml_dir=opt.xml_dir
    )
