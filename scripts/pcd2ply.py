import argparse
import open3d as o3d
from os import listdir
from os.path import isfile, join
from natsort import natsorted

PATH_PLY = '/home/moborobot/batuhan/labelling/low_platform/pointclouds/ply'


def pcd2ply(pcd_path, pcd_name):
    ply_name = pcd_name.split('.')
    ply_name = ply_name[0] + '.ply'
    ply_path = join(PATH_PLY, ply_name)
    pcd = o3d.io.read_point_cloud(pcd_path)
    o3d.io.write_point_cloud(ply_path, pcd)


def read_pcd(path_pcd):
    for file in natsorted(listdir(path_pcd)):
        pcd2ply(join(path_pcd, file), file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, required=True, help='Need to point clouds path')
    args = parser.parse_args()

    read_pcd(args.path)


if __name__ == '__main__':
    main()
