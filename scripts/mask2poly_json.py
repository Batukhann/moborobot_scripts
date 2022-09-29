import argparse
from os import listdir
from os.path import isfile, join

import numpy as np
from natsort import natsorted
import json
import cv2
import matplotlib.pyplot as plt

SERVER_PATH = 'items/images/'
JSON_PATH = '/home/moborobot/batuhan/labelling/mask2poly.json'
PARAM_DIVIDER = 3

threshArea = 2500  # min segmented area in pixels
perApprox = 0.001  # Parameter specifying the approximation accuracy. This is the maximum distance between the original curve and its approximation.


def fill_labels(contours):
    labels = []
    dict_label = {'id': 0, "category": "road", 'attributes': {}, 'manuelShape': False}

    poly2d = []
    vertices = []

    labels.append(dict_label)

    l_counter = 1
    for contour in contours:
        for element in contour:
            coordinate = [int(element[0][0]), int(element[0][1])]
            vertices.append(coordinate)
            l_counter += 1

    dict_vertices = {'vertices': vertices}
    dict_vertices['types'] = 'L'*l_counter
    dict_vertices['closed'] = True

    poly2d.append(dict_vertices)
    dict_label['poly2d'] = poly2d

    return labels


def find_contours(mask):
    img_grey = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    ret, thresh_img = cv2.threshold(img_grey, 0.5, 255, 0)
    contours, _ = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    new_contours = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > threshArea:
            perimeter = cv2.arcLength(cnt, True)
            epsilon = perApprox * perimeter
            approx = cv2.approxPolyDP(cnt, epsilon, True)
            new_contours.append(approx)
            # new_contours = tuple(new_contours)

            # cv2.drawContours(mask, new_contours, -1, (0, 0, 255), 3)
            # cv2.imshow('newing2', mask)
            # cv2.waitKey(0)

            # print('Number of vertices in old contour: %d' % len(cnt))
            # print('Number of vertices in new contour: %d' % len(new_contours[0]))
    return new_contours


def prepare_categories(dict_dataset):
    road = {'name': 'road'}
    dict_dataset['config']['categories'].append(road)


def prepare_dataset(path_dataset, dict_dataset):
    counter = 0
    for file in natsorted(listdir(path_dataset)):
        if not counter % PARAM_DIVIDER == 0:
            counter += 1
            continue
        mask_path = join(path_dataset, file)
        if isfile(mask_path):
            mask = cv2.imread(mask_path)
            contours = find_contours(mask)
            labels = fill_labels(contours)

            path_file = join(SERVER_PATH, file)
            path_dict = {'url': path_file, 'index': int(counter / 3), 'labels': labels}

            dict_dataset.append(path_dict)
            counter += 1


def json_save(dictionary):
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)

    # Writing to sample.json
    with open(JSON_PATH, "w") as outfile:
        outfile.write(json_object)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, required=True, help='Need to dataset path')
    args = parser.parse_args()

    dict_dataset = []

    prepare_dataset(args.path, dict_dataset)
    # prepare_categories(dict_dataset)
    json_save(dict_dataset)


if __name__ == '__main__':
    main()
