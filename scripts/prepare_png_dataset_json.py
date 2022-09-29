import argparse
from os import listdir
from os.path import isfile, join
from natsort import natsorted
import json

SERVER_PATH = 'items/images/'
JSON_PATH = '/home/moborobot/batuhan/labelling/png.json'
PARAM_DIVIDER = 3


def prepare_categories(dict_dataset):
    road = {'name': 'road'}
    dict_dataset['config']['categories'].append(road)


def prepare_dataset(path_dataset, dict_dataset):
    counter = 0
    for file in natsorted(listdir(path_dataset)):
        if not counter % PARAM_DIVIDER == 0:
            counter += 1
            continue
        if isfile(join(path_dataset, file)):
            path_file = join(SERVER_PATH, file)
            path_dict = {'url': path_file}
            dict_dataset['frames'].append(path_dict)
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

    dict_dataset = {
        "frames": [],
        "config": {"categories": []},
    }

    prepare_dataset(args.path, dict_dataset)
    prepare_categories(dict_dataset)
    json_save(dict_dataset)


if __name__ == '__main__':
    main()
