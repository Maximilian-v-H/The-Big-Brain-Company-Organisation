import ee
import geemap.foliumap as geemap

ee.Authenticate()
ee.Initialize(project='starthack-417820')
Map = geemap.Map(center=[-10, -55], zoom=4)
Map.to_streamlit(height=700)
a = """
brazil_shapefile = geemap.shp_to_ee('Task2/Brazil/Brazil/Brazil.shp')
# Define the dataset and filter by date
dataset = ee.ImageCollection('MODIS/061/MCD64A1').filter(ee.Filter.date('2003-01-01', '2018-05-01'))
burnedArea = dataset.select('BurnDate')

# A FeatureCollection defining Brazil boundary.
fc = ee.FeatureCollection('USDOS/LSIB_SIMPLE/2017').filter(
    'country_na == "Brazil"'
)

# Clip the burned Area by the Brazil boundary FeatureCollection.
# Iterate over the ImageCollection and clip each image to the FeatureCollection.
ba_clip = burnedArea.map(lambda img: img.clipToCollection(fc))


# Visualization parameters
burnedAreaVis = {
    'min': 30.0,
    'max': 341.0,
    'palette': ['4e0400', '951003', 'c61503', 'ff1901']
}

# Create a map
Map = geemap.Map(center=[-10, -55], zoom=4)

# Add burned area layer to the map
Map.addLayer(ba_clip, burnedAreaVis, 'Burned Area')
Map.addLayer(brazil_shapefile, name='Brazil',opacity=0.5)
Map.addLayerControl()

# Display the map
Map.to_streamlit(height=700)
"""