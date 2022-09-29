import numpy as np


def rot2quat(rot):
    qw = np.sqrt(1 + np.sum(np.diag(rot))) / 2.0
    qx = (rot[2, 1] - rot[1, 2]) / (4 * qw)
    qy = (rot[0, 2] - rot[2, 0]) / (4 * qw)
    qz = (rot[1, 0] - rot[0, 1]) / (4 * qw)
    quat = np.array([qx, qy, qz, qw])
    return quat


rotation_matrix = np.array([[0.04903844, -0.99877136, 0.00714194],
                            [-0.04136177, -0.00917512, -0.99910211],
                            [0.9979401, 0.048699, -0.04176089]])

quat_matrix = rot2quat(rotation_matrix)

print(quat_matrix)
