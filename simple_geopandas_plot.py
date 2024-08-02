import shapefile as shp  # Requires the pyshp package
import matplotlib.pyplot as plt
import geopandas as gdp

#simple geopandas application using naturalearth shp file
fp = open("shp_file_path.txt")
filepath = fp.read()
sf = gdp.read_file(filepath)
plt.figure()
sf.plot()
plt.show()
