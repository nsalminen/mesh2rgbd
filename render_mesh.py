""" Rendering of .ply files containing objects: mesh -> RGB, depth
"""

import os
import sys

import numpy as np
import tifffile as tiff

from mesh2rgb.mesh.io import load_ply
from mesh2rgb.mesh.vis import pyrender_vertices
from mesh2rgb.mesh.transform import world_to_image

sys.path.append('..')
from mesh2rgb import mesh


def save_depth(file, data):
    data = -data
    tiff.imsave(file, data.astype("uint16"), photometric='miniswhite')


def save_rgb(file, data):
    data = (data * 255).astype('uint8')
    tiff.imsave(file, data, photometric='rgb')


def project_vertices(vertices: np.ndarray, triangles: np.ndarray, colors: np.ndarray, triangle_mask: np.ndarray = None,
                     w: int = 512, h: int = 512):
    """ Render and save images with specified transformation
        Args:
            vertices: [3, nver]
            triangles: [3, ntri]
            colors: [3, nver]
            triangle_mask: [ntri, 3], indicates whether triangle should be displayed in rendering
            h: height of rendering
            w: width of rendering
        """
    obj = {}
    camera = {}
    colors = colors / np.max(colors)
    obj['s'] = [100, 100, 100]  # Use [1, 1, 1] to prevent object scaling
    obj['angles'] = [0, 0, 0]
    obj['t'] = [0, 0, 0]

    camera['proj_type'] = 'perspective'
    camera['at'] = [0, 0, 0]
    camera['near'] = 500
    camera['far'] = 4500
    # Eye position
    camera['fovy'] = 60
    camera['up'] = [0, 1, 0]
    # Z-axis: eye from far to near, looking at the center of face
    for p in np.arange(900, 250 - 1, -100):  # 1m -> .25m
        camera['eye'] = [0, 0, p]  # Stay in front of object
        image_vertices = world_to_image(vertices, triangles, colors, obj, camera, w, h)
        image, depth = mesh.render.render_rgbd(image_vertices, triangles, colors, triangle_mask, h, w)
        image = np.minimum((np.maximum(image, 0)), 1)
        save_rgb('{}/rgb_{}.tiff'.format(save_folder_rgb, p), image)
        save_depth('{}/d_{}.tiff'.format(save_folder_depth, p), depth)


save_folder_rgb = 'results/rgb'
save_folder_depth = 'results/depth'
if not os.path.exists(save_folder_rgb):
    os.makedirs(save_folder_rgb)
if not os.path.exists(save_folder_depth):
    os.makedirs(save_folder_depth)

ply_vertices, ply_triangles = load_ply("data/teapot.ply")  # Needs to be scaled to be visible
ply_colors = np.ones(ply_vertices.shape)

project_vertices(ply_vertices, ply_triangles, ply_colors)