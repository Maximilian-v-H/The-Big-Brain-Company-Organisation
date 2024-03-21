import streamlit as st

st.set_page_config(layout="wide")

st.title("Explore how AI can help identify wildfires")
st.image('assets/image_recog.png', caption='Simplified process of a computer vision model.')

# Start the quiz
with st.expander("Try it yourself"):
    st.write("""If you want, upload a picture from the internet of a wildfire (or something else) and see yourself if the model correctly 
                determines if there is a wildfire or not.
             """)
    
    img_file_buffer = st.camera_input("Upload a picture of a wildfire and see if it will be correctly identified")

    # TODO: IMAGE PARSEN UND DANN IN MODEL
    # TODO: MODEL OUTPUT + BILD RENDERN

    st.write("""Such AI models will enable us to detect wildfires more reliably and earlier, 
             as we can take images from drones or endangered regions and feed them to the model.""")