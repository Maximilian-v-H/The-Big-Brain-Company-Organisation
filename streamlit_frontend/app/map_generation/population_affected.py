import geemap.foliumap as geemap
import ee    
import os
def population_affected_map():
    brazil_shp = 'https://starthack2024-g20-13579.s3.eu-central-1.amazonaws.com/Brazil.shp'
    brazil_shapefile = geemap.shp_to_ee(brazil_shp)
    print(brazil_shp)
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

    # load population tif file
    pop = ee.Image("projects/starthack-417820/assets/bra_ppp_2020_UNadj_constrained")

    # Create a map
    population_map = geemap.Map(center=[-10, -55], zoom=4)

    # Add burned area layer to the map
    #Map.addLayer(ba_clip, burnedAreaVis, 'Burned Area')
    population_map.addLayer(brazil_shapefile, name='Brazil',opacity=0.5)
    population_map.addLayerControl()

    # add population layer
    # Apply a logarithmic transformation to the population values
    pop_log = pop.log()
    palette = ['blue', 'red']

    # Define the visualization parameters
    vis_params = {
        'min': 0,
        'max': pop_log.reduceRegion(reducer=ee.Reducer.max(), geometry=brazil_shapefile, scale=800, maxPixels=1e13).get('b1').getInfo(),
        'palette': palette
    }

    # Create a composite image of burned areas
    burnedAreaComposite = ba_clip.max()
    import ipywidgets as widgets

    # Create a slider for the buffer distance parameter
    buffer_slider = widgets.IntSlider(
        value=10000,  # Initial value
        min=0,  # Minimum value
        max=20000,  # Maximum value
        step=500,  # Increment size
        description='Buffer Distance:',
        continuous_update=True  # Only update when the user releases the slider
    )

    # Define a function to update the displayed population based on the slider value
    def update_population(buffer_distance):
        # Update the buffer distance
        bufferDistance = buffer_distance

        # Generate a buffer around the burned areas
        burnedBuffer = burnedAreaComposite.gt(0).fastDistanceTransform().sqrt().multiply(ee.Image.pixelArea().sqrt()).lte(bufferDistance)

        # Mask the population data with the buffered burned areas
        popWithinBurnedBuffer = pop.updateMask(burnedBuffer)

        # Visualization parameters for the population data
        popVis = {
            'min': 0,
            'max': 1000,
            'palette': ['00FFFF', '0000FF']
        }

        # Add the masked population layer to the map
        population_map.addLayer(popWithinBurnedBuffer, popVis, 'Population Near Burned Areas')

    # Create an interactive widget for the buffer distance parameter
    widgets.interact(update_population, buffer_distance=buffer_slider)

    return population_map
    
    # Display the map
    # Map.to_streamlit(height=700)

