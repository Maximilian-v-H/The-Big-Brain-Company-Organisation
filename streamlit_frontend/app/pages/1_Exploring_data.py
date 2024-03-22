import streamlit as st
import leafmap.foliumap as leafmap
import geemap.foliumap as geemap
import ee
from map_generation.population_affected import population_affected_map
from streamlit_folium import folium_static
from streamlit_image_comparison import image_comparison
import base64

st.set_page_config(layout="wide")
st.title("Wildfire data exploration")
ee.Authenticate()
ee.Initialize(project='starthack-417820')

tab1, tab2, tab3 = st.tabs(["Burnt areas in Brazil", "Loss of fertile land", "Populations affected by wildfires."])
with tab1:
    # Load the shapefile for Brazil.
    brazil_shapefile = ee.FeatureCollection("projects/starthack-417820/assets/Brazil")

    # Load the .tif files into an ImageCollection.
    burnt_collection = ee.ImageCollection("projects/starthack-417820/assets/bra")

    # Get the number of images in the ImageCollection.
    num_images = burnt_collection.size().getInfo()
    print("Number of images in the collection:", num_images)

    # Convert the ImageCollection to a single multiband image.
    burnt_image = burnt_collection.toBands()

    # Reduce the multiband image to a single band image that represents the sum of all bands.
    burnt_count = burnt_image.reduce(ee.Reducer.sum())

    # Normalize the burnt count to a range of 0 to 1.
    max_burnt_count = burnt_count.reduceRegion(reducer=ee.Reducer.max(), geometry=brazil_shapefile, scale=800,
                                                 maxPixels=1e13).get('sum').getInfo()
    normalized_burnt_count = burnt_count.divide(max_burnt_count)

    # Define a color palette for the heatmap.
    heatmap_palette = ['#FF4500', '#B22222', '#8B0000', '#800000', '#550000', '#300000']

    Map = geemap.Map(center=[-10, -55], zoom=4)

    # Add the heatmap layer to the map.
    Map.addLayer(normalized_burnt_count, {'min': 0, 'max': 1, 'palette': heatmap_palette}, 'burnt Area Heatmap')

    # Define a Gaussian kernel with a radius of 3 pixels.
    gaussian_kernel = ee.Kernel.gaussian(radius=200, units='pixels', sigma=1)

    # Convolve the image with the Gaussian kernel to blur it.
    blurred_burnt_count = normalized_burnt_count.convolve(gaussian_kernel)

    # Add the heatmap layer to the map.
    Map.addLayer(blurred_burnt_count, {'min': 0, 'max': 1, 'palette': heatmap_palette}, 'burnt Area Heatmap')
    Map.addLayer(brazil_shapefile, name='Brazil', opacity=0.5)

    # Define the colors for the legend
    colors = ['#FF4500', '#B22222', '#8B0000', '#800000', '#550000', '#300000']

    # Define the labels for the legend
    labels = ['Low', 'Medium', 'High', 'Very High', 'Extreme', 'Code Red']

    # Create a dictionary mapping labels to colors
    legend_dict = dict(zip(labels, colors))

    # Add the custom legend to the map
    Map.add_legend(title="Burnt Area Heatmap from 2002-2020", legend_dict=legend_dict)
    Map.to_streamlit()

with tab2:
    col1, col2 = st.columns(2)

    # Use the first column to display the image comparison
    with col1:
        st.markdown("### Discover yourself:")
        st.markdown("")
        st.markdown("")
        st.markdown("")

        image_comparison(
            img1="assets/savanna_after.jpeg",
            img2="assets/rainforrest.jpeg",
            label1="Distaster: A burnt forest",
            label2="Untouched, healthy nature: The Rainforest",
            width=600,
            starting_position=30,
            show_labels=True,
            make_responsive=True,
            in_memory=True,
        )

    # Use the second column to display the GIF
    with col2:
        st.markdown("### Disaster in 20 years: Loss of humid forest (green), replaced by Savanna (yellow)")
        file_ = open("assets/savanna.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()

        st.markdown(
            f'<img src="data:image/gif;base64,{data_url}" alt="forest gif" width="600" height="500" >',
            unsafe_allow_html=True,
        )

with tab3:
    # Load the shapefile for Brazil.
    brazil_shapefile = ee.FeatureCollection("projects/starthack-417820/assets/Brazil")

    # Load the .tif files into an ImageCollection.
    burnt_collection = ee.ImageCollection("projects/starthack-417820/assets/bra")

    # Get the number of images in the ImageCollection.
    num_images = burnt_collection.size().getInfo()
    print("Number of images in the collection:", num_images)

    # Convert the ImageCollection to a single multiband image.
    burnt_image = burnt_collection.toBands()

    # Reduce the multiband image to a single band image that represents the sum of all bands.
    burnt_count = burnt_image.reduce(ee.Reducer.sum())

    # Normalize the burnt count to a range of 0 to 1.
    max_burnt_count = burnt_count.reduceRegion(reducer=ee.Reducer.max(), geometry=brazil_shapefile, scale=800,
                                                 maxPixels=1e13).get('sum').getInfo()
    normalized_burnt_count = burnt_count.divide(max_burnt_count)

    # Define a color palette for the heatmap.
    heatmap_palette = ['#FF4500', '#B22222', '#8B0000', '#800000', '#550000', '#300000']

    Map = geemap.Map(center=[-10, -55], zoom=4)

    # Add the heatmap layer to the map.
    Map.addLayer(normalized_burnt_count, {'min': 0, 'max': 1, 'palette': heatmap_palette}, 'burnt Area Heatmap')

    # Define a Gaussian kernel with a radius of 3 pixels.
    gaussian_kernel = ee.Kernel.gaussian(radius=200, units='pixels', sigma=1)

    # Convolve the image with the Gaussian kernel to blur it.
    blurred_burnt_count = normalized_burnt_count.convolve(gaussian_kernel)

    # Add the heatmap layer to the map.
    Map.addLayer(blurred_burnt_count, {'min': 0, 'max': 1, 'palette': heatmap_palette}, 'burnt Area Heatmap')
    Map.addLayer(brazil_shapefile, name='Brazil', opacity=0.5)

    # Define the colors for the legend
    colors = ['#FF4500', '#B22222', '#8B0000', '#800000', '#550000', '#300000']

    # Define the labels for the legend
    labels = ['Low', 'Medium', 'High', 'Very High', 'Extreme', 'Code Red']

    # Create a dictionary mapping labels to colors
    legend_dict = dict(zip(labels, colors))

    # Add the custom legend to the map
    Map.add_legend(title="Burnt Area Heatmap from 2002-2020", legend_dict=legend_dict)
    Map.to_streamlit()
