# yolov5-scripts

这些脚本将帮助你使用 <a href="https://github.com/ultralytics/yolov5">yolov5</a> 训练自定义数据集。

## 检查数据集

数据集应组织成如下格式。

```
├── dataset
	├── annotations
		└── a.xml
		└── b.xml
		...
	├── images
		└── a.jpg
		└── b.jpg
		...
```

为避免后续步骤发生错误，你首先要检查数据集。

```sh
python check.py --img-dir img-dir --xml-dir xml-dir
```

可以检查出以下错误。

- 不合法的图片
- 不合法的 xml
- 图片和 xml 宽高不匹配
- xml 缺失对应图片

允许图片无 xml 对应，视为无目标物的背景图。推荐背景图占图片总数的 5% - 10% ，以取得更好训练效果。 

## 划分数据集

```sh
python split_train_val --img-dir img-dir --train-percent 0.9
```

训练集默认占比为 0.9。 

运行后，将会在图片目录的同级目录下生成 train.txt 和 val.txt ，你需要把它们写进 yolov5 的配置文件。

## voc 转 yolo

```sh
python voc_to_yolo.py --img-dir img-dir --xml-dir xml-dir
```

运行后，将会在图片目录的同级目录下生成一个 labels 文件夹，存放所有 yolo 格式的 txt 文件。

同时控制台会输出 class_names ，你需要把它写进 yolov5 的配置文件。

## 可选操作

### 分离背景图

```sh
python split_background.py --img-dir img-dir --xml-dir xml-dir
```

运行后，将会在图片目录的同级目录下生成一个 bakcgrounds 文件夹，存放所有背景图。

### 重命名

```sh
python rename.py --img-dir img-dir --xml-dir xml-dir --new-name xxx
```

运行后，文件将被重命名。

```
├── dataset
	├── annotations
		└── xxx_1.xml
		└── xxx_2.xml
		...
	├── images
		└── xxx_1.jpg
		└── xxx_2.jpg
		...
		└── background_1.jpg
		└── background_2.jpg
```

### 提取目标物图片

```sh
python extract_object.py --img-dir img-dir --xml-dir xml-dir
```

运行后，将会在图片目录的同级目录下生成一个 objects 文件夹，存放所有目标物图片。

### yolo 转 voc

数据集应组织成如下格式。

```
├── dataset
	├── images
		└── a.jpg
		└── b.jpg
		...
	├── labels
		└── a.txt
		└── b.txt
		...
```

确保参数 --class-names 和模型一致。

```sh
python yolo_to_voc.py --img-dir img-dir --txt-dir txt-dir --class-names name1 name2 name3
```

运行后，将会在图片目录的同级目录下生成一个 annotations 文件夹，存放所有 xml 文件。