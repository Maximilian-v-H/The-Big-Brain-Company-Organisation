import streamlit as st
from streamlit_folium import folium_static
import geemap.foliumap as geemap
import ee

st.set_page_config(layout="wide")
st.title("Now that we understand the implications of wildfires, lets see what we can do to help prevent them ")
