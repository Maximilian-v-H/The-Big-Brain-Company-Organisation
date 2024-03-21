import streamlit as st
import leafmap.foliumap as leafmap
from streamlit_folium import folium
from streamlit_folium import folium_static
import geemap
import ee

st.set_page_config(layout="wide")
st.title("Split-panel Map")


tab1, tab2, tab3 = st.tabs(["Burned areas in Brazil", "Loss of fertile land", "Populations affected by wildfires."])
with tab1:
    with st.expander("See source code"):
        with st.echo():
            m = leafmap.Map()
            m.split_map(
                left_layer='C:/Users/Jonas/Programming/FastAPI/assets/barea2006_bra.tif', right_layer='C:/Users/Jonas/Programming/FastAPI/assets/barea2011_bra.tif'
            )
            m.add_legend(title='ESA Land Cover', builtin_legend='ESA_WorldCover')

    m.to_streamlit(height=700)

with tab2:
    st.write("Noch mehr Daten")

with tab3:
    import streamlit as st
    from streamlit_folium import folium_static
    import ee
    
    st.write("Unglaublich viele Daten")
    

    ee.Authenticate()
    ee.Initialize(project='starthack-417820')

    
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