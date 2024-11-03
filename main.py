
import math 
import numpy as np
import rasterio as rio
from rasterio.plot import show
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


zona_a_visualitzar = "mont_perdut"

dem = rio.open(zona_a_visualitzar + ".tif")

dem_array = dem.read(1).astype('float64')

dem_array = dem_array[::-1,:] # we invert the elements on the first dimension to have the plot pointing to the north

spacing = 30.9

x = np.linspace(0, dem_array.shape[1]*0.001*spacing, dem_array.shape[1])
y = np.linspace(0, dem_array.shape[0]*0.001*spacing, dem_array.shape[0])
X, Y = np.meshgrid(x, y)
Z = dem_array
plt.imshow(Z, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower', cmap='viridis', aspect='auto')
plt.title('Colormap of the altitude')
plt.colorbar()
plt.show()

# enter here the minimum elevation angle
pendent_permes = np.tan(np.radians(10.48)) 

print(pendent_permes)
print(dem_array.shape)

altitud_maxima = np.max(dem_array)
print(altitud_maxima)
altitud_minima = np.min(dem_array)
print(altitud_minima)

plt.subplot(2, 1, 1)
# Create a grid of values
x = np.linspace(0, dem_array.shape[1]*0.001*spacing, dem_array.shape[1])
y = np.linspace(0, dem_array.shape[0]*0.001*spacing, dem_array.shape[0])
X, Y = np.meshgrid(x, y)
Z = dem_array
plt.imshow(Z, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower', cmap='viridis', aspect='auto')
plt.title('Colormap of the altitude')
plt.colorbar()

# Cone matrix
Dk_max = math.trunc((altitud_maxima-altitud_minima)/spacing/pendent_permes)
Dl_max = math.trunc((altitud_maxima-altitud_minima)/spacing/pendent_permes)

cone_max = np.zeros((2*Dk_max, 2*Dl_max))
for k in range(0, 2*Dk_max):
    for l in range(0, 2*Dl_max):
        cone_max[k,l] = ((((k - Dk_max)**2+(l - Dl_max)**2)**0.5)*spacing)*pendent_permes

dem_array.size
altures_minimes_de_vol = np.zeros(dem_array.shape)
for j in range(0, dem_array.shape[1]):
    for i in range(0, dem_array.shape[0]):

        altitudij = dem_array[i][j]

        # dimensions of the searching zone
        Dk = math.trunc((altitud_maxima-altitudij)/spacing/pendent_permes)
        Dl = math.trunc((altitud_maxima-altitudij)/spacing/pendent_permes)

        k_min = max(0, (i-Dk))
        k_max = min(dem_array.shape[0], (i+Dk))
        l_min = max(0, (j-Dl))
        l_max = min(dem_array.shape[1],j+Dl)

        if k_max-k_min + l_max - l_min > 0:
            altures_minimes_de_vol[i][j] = np.max(dem_array[k_min: k_max, l_min : l_max] - cone_max[(Dk_max -(i - k_min)): (Dk_max+(k_max - i)), (Dl_max-(j - l_min)) : (Dl_max + (l_max - j))] - np.full((k_max-k_min, l_max - l_min), altitudij))
    print(j)

    if j in np.round(np.linspace(0, dem_array.shape[1] -1, 10)).astype(int):
        plt.subplot(2, 1, 2)
        Z = altures_minimes_de_vol
        plt.imshow(Z, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower', cmap='viridis', aspect='auto')
        plt.title('Colormap of the minimum flying altitude over the ground')
        plt.colorbar()
        plt.show(block = False)
        plt.pause(1)

plt.show()

np.save(zona_a_visualitzar + ".npy", altures_minimes_de_vol)