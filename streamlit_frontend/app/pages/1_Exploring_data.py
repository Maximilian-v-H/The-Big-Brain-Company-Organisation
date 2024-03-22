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

from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/earthengine',
          'https://www.googleapis.com/auth/devstorage.read_write']
SERVICE_ACCOUNT_FILE = 'starthack-417820-456004745901.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
ee.Initialize(credentials)

tab1, tab2, tab3, tab4 = st.tabs(
    ["Burnt areas in Brazil", "Loss of fertile land", "Danger of fire to protected areas", "Population affected"])
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
    # displaay image
    st.markdown("*The danger of fire to protected areas and conservation work*")
    img1_ = open("assets/restricted areas with wildfire.png", "rb")
    contents1 = img1_.read()
    data_url1 = base64.b64encode(contents1).decode("utf-8")
    img1_.close()

    img2_ = open("assets/restricted areas with and without wildfire.png", "rb")
    contents2 = img2_.read()
    data_url2 = base64.b64encode(contents2).decode("utf-8")
    img2_.close()

    # use button to switch between images
    show_all = st.toggle("Show only areas affected by fire", False)

    if show_all:
        st.text(
            "The image below shows the areas that have been affected by wildfires in Brazil.\nAs you can see almost all of the protected areas have been affected by wildfires.\nThis is a major concern for conservation efforts in Brazil.")

        st.markdown(
            f'<img src="data:image/png;base64,{data_url1}" alt="restricted areas with wildfire" width="800" height="500" >',
            unsafe_allow_html=True,
        )
    else:

        st.markdown(
            f'<img src="data:image/png;base64,{data_url2}" alt="restricted areas with and without wildfire" width="800" height="500" >',
            unsafe_allow_html=True,
        )

with tab4:
    img1 = open(f"assets/img1.png", "rb")
    contents = img1.read()
    data_url1 = base64.b64encode(contents).decode("utf-8")
    img1.close()

    img2 = open(f"assets/img2.png", "rb")
    contents = img2.read()
    data_url2 = base64.b64encode(contents).decode("utf-8")
    img2.close()

    img3 = open(f"assets/img3.png", "rb")
    contents = img3.read()
    data_url3 = base64.b64encode(contents).decode("utf-8")
    img3.close()

    img4 = open(f"assets/img4.png", "rb")
    contents = img4.read()
    data_url4 = base64.b64encode(contents).decode("utf-8")
    img4.close()

    # create a slider with 4 values
    st.markdown("### Population affected by wildfires in Brazil")

    st.markdown(
        "The images below show the population affected by wildfires in Brazil. You can choose a given radius and it will show you the population affected by wildfires in that radius.")
    radius = st.select_slider("Radius (km)", [0.5, 5, 10, 20])

    # display the map
    if radius == 0.5:
        st.markdown("Population affected by wildfires in Brazil with a radius of 0.5 km")
        st.markdown(
            f'<img src="data:image/png;base64,{data_url1}" alt="population affected by wildfires" width="800" height="700" >',
            unsafe_allow_html=True)
    elif radius == 5:
        st.markdown("Population affected by wildfires in Brazil with a radius of 5 km")
        st.markdown(
            f'<img src="data:image/png;base64,{data_url2}" alt="population affected by wildfires" width="800" height="700" >',
            unsafe_allow_html=True)
    elif radius == 10:
        st.markdown("Population affected by wildfires in Brazil with a radius of 10 km")
        st.markdown(
            f'<img src="data:image/png;base64,{data_url3}" alt="population affected by wildfires" width="800" height="700" >',
            unsafe_allow_html=True)
    else:
        st.markdown("Population affected by wildfires in Brazil with a radius of 20 km")
        st.markdown(
            f'<img src="data:image/png;base64,{data_url4}" alt="population affected by wildfires" width="800" height="700" >',
            unsafe_allow_html=True)
