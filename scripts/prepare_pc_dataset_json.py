import argparse
import csv
from os.path import join
import json

SERVER_PATH = 'items/ply/'
PARAM_DIVIDER = 3
JSON_PATH = '/home/moborobot/batuhan/labelling/ply.json'


def prepare_categories(dict_dataset):
    pedestrian = {'name': 'pedestrian'}
    vehicles = {'name': 'vehicles'}
    truck = {'name': 'truck'}
    bus = {'name': 'bus'}
    dict_dataset['config']['categories'].append(pedestrian)
    dict_dataset['config']['categories'].append(vehicles)
    dict_dataset['config']['categories'].append(truck)
    dict_dataset['config']['categories'].append(bus)


def json_save(dictionary):
    # Serializing json
    json_object = json.dumps(dictionary, indent=4)

    # Writing to sample.json
    with open(JSON_PATH, "w") as outfile:
        outfile.write(json_object)


def prepare_dataset(csv_file, dict_dataset):
    file = open(csv_file)
    csv_reader = csv.reader(file)

    counter = 0

    for row in csv_reader:
        if not counter % PARAM_DIVIDER == 0:
            counter += 1
            continue
        else:
            path_file = join(SERVER_PATH, row[1])
            path_dict = {'url': path_file}
            dict_dataset['frames'].append(path_dict)
            counter += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', type=str, required=True, help='Need to dataset path')
    args = parser.parse_args()

    dict_dataset = {
        "frames": [],
        "config": {"categories": []},
    }

    prepare_dataset(args.csv, dict_dataset)
    prepare_categories(dict_dataset)
    json_save(dict_dataset)


if __name__ == '__main__':
    main()
