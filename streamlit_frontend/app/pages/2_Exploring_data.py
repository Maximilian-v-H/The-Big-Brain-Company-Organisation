import streamlit as st
import leafmap.foliumap as leafmap
import geemap.foliumap as geemap
import ee
from map_generation.population_affected import population_affected_map
from streamlit_folium import folium_static

st.set_page_config(layout="wide")
st.title("Datenvisualisierung")
ee.Authenticate()
ee.Initialize(project='starthack-417820')

tab1, tab2, tab3 = st.tabs(["Burned areas in Brazil", "Loss of fertile land", "Populations affected by wildfires."])
with tab1:
    m = geemap.Map()  # Use geemap Map object
    m.split_map(
        left_layer='assets/barea2006_bra.tif', right_layer='assets/barea2011_bra.tif'
    )
    m.add_legend(title='ESA Land Cover', builtin_legend='ESA_WorldCover')
    folium_static(m, height=700)

with tab2:
    
    brazil_shapefile = ee.FeatureCollection("projects/starthack-417820/assets/Brazil")
        
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

    burnedBuffer = burnedAreaComposite.gt(0).fastDistanceTransform().sqrt().multiply(ee.Image.pixelArea().sqrt()).lte(1000)

    burnedBuffer2 = burnedAreaComposite.gt(0).fastDistanceTransform().sqrt().multiply(ee.Image.pixelArea().sqrt()).lte(5000)

    burnedBuffer3 = burnedAreaComposite.gt(0).fastDistanceTransform().sqrt().multiply(ee.Image.pixelArea().sqrt()).lte(10000)

    burnedBuffer4 = burnedAreaComposite.gt(0).fastDistanceTransform().sqrt().multiply(ee.Image.pixelArea().sqrt()).lte(20000)


    # Define a function to update the displayed population based on the slider value
    def update_population():
        buffer_distance = st.session_state.buffer_slider
        # Update the buffer distance
        if buffer_distance == 1000:
            popWithinBurnedBuffer = pop.updateMask(burnedBuffer)
        elif buffer_distance == 5000:
            popWithinBurnedBuffer = pop.updateMask(burnedBuffer2)
        elif buffer_distance == 10000:
            popWithinBurnedBuffer = pop.updateMask(burnedBuffer3)
        elif buffer_distance == 20000:
            popWithinBurnedBuffer = pop.updateMask(burnedBuffer4)
        else:
            popWithinBurnedBuffer = pop.updateMask(burnedBuffer)

        # Visualization parameters for the population data
        popVis = {
            'min': 0,
            'max': 1000,
            'palette': ['00FFFF', '0000FF']
        }

        # Add the masked population layer to the map
        population_map.addLayer(popWithinBurnedBuffer, popVis, 'Population Near Burned Areas')
    
    buffer_slider = st.slider("Buffer distance", 0, 20000, step=5000, label_visibility="hidden", key="buffer_slider", on_change=update_population)
    update_population()

    folium_static(population_map)

with tab3:
    a = """
    import streamlit as st
    from streamlit_folium import folium_static
    import ee
    
    st.write("Unglaublich viele Daten")

    
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