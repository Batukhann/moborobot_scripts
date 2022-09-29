import argparse
import csv
from os.path import join
import cv2
import open3d as o3d

PARAM_DIVIDER = 3
IMAGES_PATH = '/home/moborobot/batuhan/labelling/images'
PLY_PATH = '/home/moborobot/batuhan/labelling/pointclouds/ply'

WRITE_IMG_PATH = '/home/moborobot/batuhan/labelling/dataset/images'
WRITE_PLY_PATH = '/home/moborobot/batuhan/labelling/dataset/ply'


def read_and_write_ply(ply, ply_path):
    point_cloud = o3d.io.read_point_cloud(ply_path)

    path = join(WRITE_PLY_PATH, ply)

    o3d.io.write_point_cloud(path, point_cloud)


def read_and_write_img(img, img_path):
    image = cv2.imread(img_path)

    path = join(WRITE_IMG_PATH, img)

    cv2.imwrite(path, image)


def read_csv(path_csv):
    file = open(path_csv)
    csv_reader = csv.reader(file)

    counter = 0

    for row in csv_reader:
        if not counter % PARAM_DIVIDER == 0:
            counter += 1
            continue
        else:
            img_path = join(IMAGES_PATH, row[0])
            ply_path = join(PLY_PATH, row[1])

            read_and_write_img(row[0], img_path)
            read_and_write_ply(row[1], ply_path)

            counter += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', type=str, required=True, help='Need to dataset path')
    args = parser.parse_args()

    print(args.csv)

    read_csv(args.csv)


if __name__ == '__main__':
    main()
