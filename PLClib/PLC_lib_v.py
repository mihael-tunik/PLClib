import numpy as np
import ctypes
import os

from typing import Callable, Dict

class GridDesc(ctypes.Structure):
    _fields_ = [
        ("Nxy", ctypes.c_int), 
        ("Nz", ctypes.c_int),
        ("x_min", ctypes.c_double),
        ("x_max", ctypes.c_double),
        ("y_min", ctypes.c_double), 
        ("y_max", ctypes.c_double),
        ("z_min", ctypes.c_double), 
        ("z_max", ctypes.c_double)
    ]

def decorate(f):
    def f_ctypes_wrapper(size, z, data_ptr):
        data_array = f(size, z) #(2, size. size)
        length = 2 * size * size * ctypes.sizeof(ctypes.c_double) 
        ctypes.memmove(data_ptr, data_array.ctypes.data_as(ctypes.POINTER(ctypes.c_double)), length)
    return f_ctypes_wrapper
    

def integer_labeling_v(f: Callable[[int, float], type(np.ndarray)], grid_dict: Dict):
    
    buffer_size = 200000
    # create some memory buffers for return
    res_array = np.zeros(buffer_size, dtype=np.float64)
    size_array = np.zeros(1, dtype=np.int32)
    c_res_array = res_array.ctypes.data_as(ctypes.POINTER(ctypes.c_double))
    c_size_ptr = size_array.ctypes.data_as(ctypes.POINTER(ctypes.c_int32))
    
    # open lib
    dir_path = os.path.split(os.path.abspath(__file__))[0]    
    lib = ctypes.CDLL(f'{dir_path}/PLC_lib_vec.so')
    
    py_integer_labeling = lib.integer_labeling_3d_vec
    
    i_func = ctypes.CFUNCTYPE( ctypes.c_void_p, ctypes.c_int32, ctypes.c_double, ctypes.POINTER(ctypes.c_double) )
    
    py_integer_labeling.argtypes = [GridDesc, i_func, ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_int32)]

    f_wrapped = decorate(f)
    
    grid_desc = GridDesc(
        ctypes.c_int(grid_dict['Nxy']),
        ctypes.c_int(grid_dict['Nz']),
        ctypes.c_double(grid_dict['x_min']),
        ctypes.c_double(grid_dict['x_max']),
        ctypes.c_double(grid_dict['y_min']),
        ctypes.c_double(grid_dict['y_max']),
        ctypes.c_double(grid_dict['z_min']),
        ctypes.c_double(grid_dict['z_max'])
    )
    
    ### main call
    py_integer_labeling(grid_desc, i_func(f_wrapped), c_res_array, c_size_ptr)
    ###
    
    result = np.ctypeslib.as_array(c_res_array, shape=(1, buffer_size))
    size = np.ctypeslib.as_array(c_size_ptr, shape=(1,1))[0, 0]
    extracted_res = result[0,:size].reshape((size//3, 3))

    #print(extracted_res)
    x, y, z = extracted_res[:,0], extracted_res[:,1], extracted_res[:,2]
        
    return x, y, z



