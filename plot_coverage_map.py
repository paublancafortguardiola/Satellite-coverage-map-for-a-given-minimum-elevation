import math 
import time
import numpy as np
import rasterio as rio
from rasterio.plot import show
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

zona_a_visualitzar = "mont_perdut"

altures = np.load(zona_a_visualitzar + ".npy") # array with the allowed flying altitudes
dem = rio.open(zona_a_visualitzar + ".tif")
dem_array = dem.read(1).astype('float64') # array with the terrain altitude

dem_array = dem_array[::-1,:] # we invert the elements on the first dimension to have the plot pointing to the north


spacing = 30.9 # spacing between points: 30.9m and 30.9m for latitude < 50º

plt.subplot(2, 1, 1)
# Create a grid of values
x = np.linspace(0, dem_array.shape[1]*spacing, dem_array.shape[1])
y = np.linspace(0, dem_array.shape[0]*spacing, dem_array.shape[0])
X, Y = np.meshgrid(x, y)
Z = dem_array
plt.imshow(Z, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower', cmap='viridis', aspect='auto')
plt.title('Colormap of the altitude over sea level')
plt.colorbar()

plt.subplot(2, 1, 2)
Z = altures
plt.imshow(Z, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower', cmap='viridis', aspect='auto')
plt.title('Colormap of the minimum flying altitude over the ground')
plt.colorbar()
plt.show()

# Create a color matrix based on the altitud matrix
altures_normalized = (altures - np.min(altures)) / (np.max(altures) - np.min(altures))

# Prepare the 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

cmap = plt.cm.viridis_r

# Plot the surface with colors based on the altitud matrix
surf = ax.plot_surface(X, Y, dem_array, facecolors=cmap(altures_normalized), rstride=1, cstride=1, linewidth=0, antialiased=False)

# Create a colorbar
norm = plt.Normalize(vmin=np.min(altures), vmax=np.max(altures))
mappable = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
mappable.set_array([])
cbar = fig.colorbar(mappable, ax=ax, shrink=0.5, aspect=10)
cbar.set_label('Altitude Color Scale') 

# Set labels and title
ax.set_xlabel('X (meters)')
ax.set_ylabel('Y (meters)')
ax.set_zlabel('Altitude (meters)')
ax.set_zlim(np.min(dem_array),spacing*min(dem_array.shape))
ax.set_title('3D Surface with the altitude over sea level colored by minimum flying altitude')

# Show the plot
plt.show()
