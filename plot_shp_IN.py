import shapefile as shp  # Requires the pyshp package
import matplotlib.pyplot as plt
import geopandas as gdp

# plot map based on shp file available from naturalearth
fp = open("IN_shp_file_path.txt","r")
filepath = fp.read()
sf = shp.Reader(filepath)
plt.figure()

for shape in sf.shapeRecords(): 
    if shape.record[4].find('IN-') != -1:
    #print(shape.record[4])
        for i in range(len(shape.shape.parts)):
            i_start = shape.shape.parts[i]
            #print ('istart : ',i_start)
            if i==len(shape.shape.parts)-1:
                i_end = len(shape.shape.points)
            else:
                i_end = shape.shape.parts[i+1]
            x = [i[0] for i in shape.shape.points[i_start:i_end]]
            y = [i[1] for i in shape.shape.points[i_start:i_end]]
            plt.plot(x,y)
plt.show()
