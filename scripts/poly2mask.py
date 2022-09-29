import argparse
import json
from PIL import Image, ImageDraw
import os

WIDTH = 1920
HEIGHT = 1080
SAVE_PATH = '/home/moborobot/batuhan/labelling/mask'


def list_merger(array_list):
    merged = []
    for element in array_list:
        merged += element
    return merged


def read_json(path_json):
    file = open(path_json)
    json_data = json.load(file)

    frames = json_data['frames']

    for frame in frames:
        try:
            name = frame['name']
            labels = frame['labels'][0]
            vertices = labels['poly2d'][0]['vertices']
            vertices = list_merger(vertices)
            img = Image.new('L', (WIDTH, HEIGHT), 0)
            ImageDraw.Draw(img).polygon(vertices, outline=1, fill=1)
            # mask = numpy.array(img)

            name = name.split('/')[-1]
            path_name = os.path.join(SAVE_PATH, name)

            img.save(path_name)

            # cv2.imwrite(path_name, mask)

        except IndexError:
            print(IndexError, frame)

    print('Masks created')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--json', type=str, required=True, help='Need to json path')
    args = parser.parse_args()

    read_json(args.json)


if __name__ == '__main__':
    main()
