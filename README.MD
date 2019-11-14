# mesh2rgbd

This tool takes a mesh file as its input, and outputs an RGB image and a depth image. It is based on [face3d](https://github.com/YadiraF/face3d) by [YadiraF](https://github.com/YadiraF).

## Structure
```python
mesh2rgbd/mesh/        # written in python and c++
|  cython/               # c++ files, use cython to compile 
|  io.py                 # read & write obj
|  vis.py                # plot mesh
|  transform.py          # transform mesh & estimate matrix
|  light.py              # add light
|  render.py             # obj to image using rasterization render
```

## Getting Started
### Prerequisites
- Python 2 or Python 3 

- Python packages:
  * numpy 
  * skimage   
  * scipy
  * matplotlib
  * cython
  * tiffile
  
  * pyrender
  * scikit-image
  * plyfile
  
 
  
### Usage
1. Clone the repository

    ```bash
    git clone https://github.com/nsalminen/mesh2rgbd
    cd mesh2rgbd
    ```

2. Compile the C++ files to .so for Python use

    ```bash
    cd mesh2rgbd/mesh/cython
    python setup.py build_ext -i 
    ```
3. Refer to `render_mesh.py` for a basic example.
