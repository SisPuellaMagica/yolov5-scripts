import argparse
import os
import random


# split train and val dataset
def split_train_val(img_dir, train_percent=0.9):
    print('split train and val dataset with ' + train_percent + ' ...')
    img_list = os.listdir(img_dir)
    random.shuffle(img_list)
    img_num = len(img_list)
    train_num = int(img_num * train_percent)
    train_filepath = os.path.dirname(img_dir) + '/' + 'train.txt'
    val_filepath = os.path.dirname(img_dir) + '/' + 'val.txt'
    with open(train_filepath, 'w', encoding='utf-8') as f:
        for i in range(0, train_num):
            img_filepath = img_dir + '/' + img_list[i]
            f.write(img_filepath)
            if i < train_num - 1:
                f.write('\n')
    with open(val_filepath, 'w', encoding='utf-8') as f:
        for i in range(train_num, img_num):
            img_filepath = img_dir + '/' + img_list[i]
            f.write(img_filepath)
            if i < img_num - 1:
                f.write('\n')
    print('finish')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--img-dir', type=str)
    parser.add_argument('--train-percent', type=int, default=0.9)
    opt = parser.parse_args()
    split_train_val(
        img_dir=opt.img_dir,
        train_percent=opt.train_percent
    )
