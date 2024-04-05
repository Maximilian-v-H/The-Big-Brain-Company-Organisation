import streamlit as st

st.set_page_config(layout="wide")

st.title("Explore how AI can help identify wildfires")
st.image('assets/image_recog.png', caption='Simplified process of a computer vision model.')

st.write(
    "Imagine you're using a highly sophisticated camera that not only takes pictures but can also understand what it's seeing, just like a human does when they look at a photo. This is what we call 'Computer Vision' in the world of Artificial Intelligence (AI).")
st.write("")
st.write(
    "These AI models take pictures and look at them pixel by pixel, trying to relate (correlate) them with each other and find patterns. Given enough data (pictures) and some clever mathematics, we can actually detect wildfires")
st.write("")
st.image("assets/drohne.jpeg")
st.write("")
st.write(
    "If we equip drones with these models, or process images from drones with it - we can speed up the process of discovering and acting upon wildfires - potentially saving thousands of hectares of land.")

st.write("")
st.write("## Try it yourself - Upload a picture and see if the fire will be detected. (Feature not added yet!)")
# Start the quiz
with st.expander("", expanded=True):
    st.write("""If you want, upload a picture from the internet of a wildfire (or something else) and see yourself if the model correctly 
                determines if there is a wildfire or not.
             """)

    img_file_buffer = st.camera_input("Upload a picture of a wildfire and see if it will be correctly identified")

    # TODO: IMAGE PARSEN UND DANN IN MODEL
    # TODO: MODEL OUTPUT + BILD RENDERN

    st.write("""Such AI models will enable us to detect wildfires more reliably and earlier, 
             as we can take images from drones or endangered regions and feed them to the model.""")
