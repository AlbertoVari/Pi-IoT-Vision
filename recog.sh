#!/bin/bash
fswebcam object.jpg
cp object.jpg images/object.jpg
rm object.jpg
python3 classify_image.py --model models/mobilenet_v1_1.0_224_quant.tflite --labels models/labels_mobilenet_quant_v1_224.txt --input images/object.jpg > label.txt
#python3 classify_image.py --model models/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite --labels models/inat_bird_labels.txt --input images/object.jpg > label.txt
cp label.txt images/label.txt
python3 send.py 1
