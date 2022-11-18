import argparse
import os
from PIL import Image

# xml template
object_template = '''
\t<object>
\t\t<name>%(name)s</name>
\t\t<pose>Unspecified</pose>
\t\t<truncated>0</truncated>
\t\t<difficult>0</difficult>
\t\t<bndbox>
\t\t\t<xmin>%(xmin)d</xmin>
\t\t\t<ymin>%(ymin)d</ymin>
\t\t\t<xmax>%(xmax)d</xmax>
\t\t\t<ymax>%(ymax)d</ymax>
\t\t</bndbox>
\t</object>'''

start_template = '''<annotation>
\t<folder>xxx</folder>
\t<filename>xxx</filename>
\t<path>xxx</path>
\t<source>
\t\t<database>Unknown</database>
\t</source>
\t<size>
\t\t<width>%(width)d</width>
\t\t<height>%(height)d</height>
\t\t<depth>3</depth>
\t</size>
\t<segmented>0</segmented>'''

end_template = '''
</annotation>'''


# xml content
def get_xml_content(width, height, objects):
    content = start_template % {'width': width, 'height': height}
    for obj in objects:
        content += object_template % obj
    content += end_template
    return content


# txt to xml
def txt_to_xml(img_filepath, txt_filepath, class_names, xml_filepath):
    img = Image.open(img_filepath)
    width = img.width
    height = img.height
    objects = []
    with open(txt_filepath, 'r', encoding='utf-8') as f:
        for line in f:
            obj = line.strip('\n').split()
            name = class_names[int(obj[0])]
            yolo_x_center = float(obj[1])
            yolo_y_center = float(obj[2])
            yolo_width = float(obj[3])
            yolo_height = float(obj[4])
            xmin = round(yolo_x_center * width - 0.5 * yolo_width * width)
            ymin = round(yolo_y_center * height - 0.5 * yolo_height * height)
            xmax = round(yolo_x_center * width + 0.5 * yolo_width * width)
            ymax = round(yolo_y_center * height + 0.5 * yolo_height * height)
            objects.append({
                'name': name,
                'xmin': xmin,
                'ymin': ymin,
                'xmax': xmax,
                'ymax': ymax
            })
    if len(objects) >= 1:
        with open(xml_filepath, 'w', encoding='utf-8') as f:
            f.write(get_xml_content(width, height, objects))


# yolo => voc
def yolo_to_voc(img_dir, txt_dir, class_names):  # class_names correspond to configs
    print('yolo => voc ...')
    xml_dir = os.path.dirname(img_dir) + '/' + 'annotations'
    if not os.path.exists(xml_dir):
        os.makedirs(xml_dir)
    for txt_filename in os.listdir(txt_dir):
        img_filepath = img_dir + '/' + os.path.splitext(txt_filename)[0] + '.jpg'
        xml_filepath = xml_dir + '/' + os.path.splitext(txt_filename)[0] + '.xml'
        txt_filepath = txt_dir + '/' + txt_filename
        txt_to_xml(img_filepath, txt_filepath, class_names, xml_filepath)
    print('finish')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--img-dir', type=str)
    parser.add_argument('--txt-dir', type=str)
    parser.add_argument('--class-names', type=str, nargs='+')
    opt = parser.parse_args()
    yolo_to_voc(
        img_dir=opt.img_dir,
        txt_dir=opt.txt_dir,
        class_names=opt.class_names
    )
