import argparse
from os import listdir
from natsort import natsorted
import string
import csv

CSV_NAME = 'matches.csv'


def match_data(timestamps_img, timestamps_ply, dataset_ply):
    print('time stamps len image: ', len(timestamps_img))
    print('time stamps len ply: ', len(timestamps_ply))

    print('time stamps image: ', timestamps_img)
    print('time stamps ply: ', timestamps_ply)

    length_img_dataset = len(timestamps_img)
    length_ply_dataset = len(timestamps_ply)

    match_index_array = []

    for i in range(length_img_dataset):
        timestamp_image = timestamps_img[i]
        min_diff = 0
        for j in range(i, length_ply_dataset):
            timestamp_ply = timestamps_ply[j]
            diff = abs(timestamp_image - timestamp_ply)
            if j == i:
                min_diff = diff
                continue
            elif diff > min_diff:
                item = dataset_ply[j-1]
                match_index_array.append(item)
                break
            elif j == length_ply_dataset - 1:
                item = dataset_ply[j]
                match_index_array.append(item)
            min_diff = diff

    print('matched array length: ', len(match_index_array))

    return match_index_array


def get_time_stamp(dataset):
    new_dataset = []
    for data in dataset:
        split = data.split('-')
        timestamp = split[2]
        timestamp = timestamp.split('.')[0]
        timestamp = timestamp.translate(str.maketrans('', '', string.punctuation))
        timestamp = int(timestamp)
        new_dataset.append(timestamp)
    return new_dataset


def write_csv(dataset_img, dataset_ply):
    with open(CSV_NAME, 'w') as csvfile:
        # creating a csv dict writer object
        writer = csv.writer(csvfile)
        writer.writerows(zip(dataset_img, dataset_ply))


def read_data(args):
    path_img = args.path_img
    path_ply = args.path_ply

    dataset_img = natsorted(listdir(path_img))
    dataset_ply = natsorted(listdir(path_ply))

    timestamps_img = get_time_stamp(dataset_img)
    timestamps_ply = get_time_stamp(dataset_ply)

    matched_ply = match_data(timestamps_img, timestamps_ply, dataset_ply)

    write_csv(dataset_img, matched_ply)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path_img', type=str, required=True, help='Need to image dataset path')
    parser.add_argument('--path_ply', type=str, required=True, help='Need to ply dataset path')
    args = parser.parse_args()

    read_data(args)


if __name__ == '__main__':
    main()
