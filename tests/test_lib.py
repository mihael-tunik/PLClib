import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PLClib import integer_labeling_v

def plot(x_, y_, z_):
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x_, y_, z_, s=0.2) 
    
    plt.xlim((-1, 1))
    plt.ylim((-1, 1))   
    
    plt.show()

def test(grid_dict, g_func):    
    x_, y_, z_ = integer_labeling_v(g_func, grid_dict)    
    plot(x_, y_, z_)


if __name__ == "__main__":    
    #grid_dict = {'Nxy': 300, 'Nz': 200, 'x_min': 0.0, 'x_max': 1.0, 'y_min': 0.0, 'y_max': 1.0, 'z_min': 0.0, 'z_max': 1.0}
    grid_dict = {'Nxy': 500, 'Nz': 500, 'x_min': -1.0, 'x_max': 1.0, 'y_min': -1.0, 'y_max': 1.0, 'z_min': -1.0, 'z_max': 1.0}
    
    x = np.linspace(grid_dict['x_min'], grid_dict['x_max'], grid_dict['Nxy'])
    y = np.linspace(grid_dict['y_min'], grid_dict['y_max'], grid_dict['Nxy'])
        
    x, y = np.meshgrid(x, y, indexing='ij')
    
    def ring(N, z):
            
        res = np.zeros((2, N, N))
        
        res[0, :, :] = x + y + z - 0.75
        res[1, :, :] = x**2 + y**2 + z**2 - 0.25  
        
        return res.ravel()
        
    def viviani(N, z):
        a = 0.3
        res = np.zeros((2, N, N))
        
        res[0, :, :] = (x-a)**2+y**2-a**2
        res[1, :, :] = x**2 + y**2 + z**2 - 4*a**2
        
        return res.ravel()
        
    test(grid_dict, viviani)
    


