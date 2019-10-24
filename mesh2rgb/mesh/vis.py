from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import matplotlib.pyplot as plt
import numpy as np
import pyrender


def plot_mesh(vertices, triangles, subplot=[1, 1, 1], title='mesh', el=90, az=-90, lwdt=.1, dist=6, color="grey"):
    """ Plot the mesh

    Args:
        vertices: [nver, 3]
        triangles: [ntri, 3]
    """
    ax = plt.subplot(subplot[0], subplot[1], subplot[2], projection='3d')
    ax.plot_trisurf(vertices[:, 0], vertices[:, 1], vertices[:, 2], triangles=triangles, lw=lwdt, color=color, alpha=1)
    ax.axis("off")
    ax.view_init(elev=el, azim=az)
    ax.dist = dist
    plt.title(title)


def plot_raw(vertices: np.ndarray, w: int = 8, h: int = 8):
    """ Plot the raw vertex values

    Args:
        vertices: [nver, 3]
        w: figure width
        h: figure height

    """
    plt.figure(figsize=(w, h))
    plt.imshow(vertices)
    plt.show()


def pyrender_vertices(vertices: np.ndarray, colors: np.ndarray):
    """ Use pyrender to display vertices with corresponding colors

    Args:
        vertices: [nver, 3]
        colors: [nver, 3]

    """
    m = pyrender.Mesh.from_points(vertices, colors=colors)
    scene = pyrender.Scene(ambient_light=[.1, .1, .3], bg_color=[1, 1, 1])
    camera = pyrender.PerspectiveCamera(yfov=np.pi / 3.0)
    light = pyrender.DirectionalLight(color=[1, 1, 1], intensity=2e3)

    s = np.sqrt(2) / 2
    camera_pose = np.array([
        [0.0, -s, s, 300.3],
        [0.0, 0.0, 0.0, -150.0],
        [1.0, s, s, 150.35],
        [0.0, 0.0, 0.0, 1.0],
    ])
    scene.add(camera, pose=camera_pose)
    scene.add(m, pose=np.eye(4))
    scene.add(light, pose=np.eye(4))
    pyrender.Viewer(scene, use_raymond_lighting=True, point_size=2)
