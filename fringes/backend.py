from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from mpl_toolkits import mplot3d
from scipy.signal import find_peaks
import math
import os

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

def load_im(name):
    directory = os.getcwd() + "/data/" + name
    img = plt.imread(directory)
    R, G, B = img[:,:,0], img[:,:,1], img[:,:,2]
    imgGray = 0.2989 * R + 0.5870 * G + 0.1140 * B
    return imgGray

def remove_noise(arr):
    noise = 0.8 * (np.mean(arr))
    it = [(lambda x: np.max(x-noise, 0))(i) for i in arr]
    no_noise = np.fromiter(it, dtype=float)
    no_noise = moving_average(no_noise, 10)
    return no_noise

def extract_fringes(im, hs):
    dis = np.array([remove_noise(im[h]) for h in hs])
    peaks = [find_peaks(d, height=10.0) for d in dis]
    peak_pos = list(p[0] for p in peaks)
    peak_height = list(p[1]['peak_heights'] for p in peaks)
    fig, axes = plt.subplots(nrows=1, ncols=3)
    
    for i, d in enumerate(dis):
        img = axes[i]
        img.plot(d)
        img.scatter(peak_pos[i], peak_height[i])
        img.set_ylabel('intensity')
        img.set_xlabel('pixel_horizontal_position')
        img.set_title("intensity distribution at h = {}".format(hs[i]))
        for j,p in enumerate(peak_pos[i]):
            img.text(p*(1.0+ 0.00), peak_height[i][j] * (1.0-0.1),  (p, peak_height[i][j]), fontsize=7)
        
    plt.show()
    
def show_im(im):
    plt.axis('off')
    plt.ion()
    display(plt.imshow(im))
    
def plot_3d_fringes(im):
    plt.ioff()
    hs=range(0, im.shape[0])
    dis = np.array([remove_noise(im[h]) for h in hs])
    peaks = [find_peaks(d, height=10.0) for d in dis]
    peak_pos = list(p[0] for p in peaks)
    peak_height = list(p[1]['peak_heights'] for p in peaks)
    peak_data = np.zeros(im.shape[0])
    fig = plt.figure(figsize=(10,10))
    ax = plt.axes(projection='3d')
    ax.set_xlabel('pixel horizontal position')
    ax.set_ylabel('pixel vertical position')
    ax.set_zlabel('Intensity')
    df = np.zeros(shape=im.shape)
    X = np.arange(0, dis.shape[1], 1)
    Y = np.arange(0, dis.shape[0], 1)
    X, Y = np.meshgrid(X, Y)

    fig.canvas.toolbar_visible = 'fade-in-fade-out'

    
    ax.set_title('Contour Plot');
    ax.contour3D(X, Y, 
                 dis, 75, 
                 cmap='viridis')
    ax.set_xlabel('pixel horizontal position')
    ax.set_ylabel('pixel vertical position')
    ax.set_zlabel('Intensity')
    plt.ion()
    display(fig.canvas)
    
    

    plt.ioff()
    fig = plt.figure(figsize=(10,10))
    ax = plt.axes(projection='3d')
    ax.set_title('Wireframe Plot');
    ax.set_xlabel('pixel horizontal position')
    ax.set_ylabel('pixel vertical position')
    ax.set_zlabel('Intensity')
    ax.plot_wireframe(X, Y, 
                 dis, color='black')
    plt.ion()
    display(fig.canvas)
    

    plt.ioff()
    fig = plt.figure(figsize=(10,10))
    ax = plt.axes(projection='3d')
    ax.set_title('Surface Plot');
    ax.plot_surface(X, Y, 
                 dis, rstride=1,
                    cmap='viridis', edgecolor='none')
    ax.set_xlabel('pixel horizontal position')
    ax.set_ylabel('pixel vertical position')
    ax.set_zlabel('Intensity')
    plt.ion()
    display(fig.canvas)