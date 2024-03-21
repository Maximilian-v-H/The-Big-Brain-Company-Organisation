# streamlit_app.py
import streamlit as st


st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
)

# Define a function for each section of the app
def introduction():
    st.title("Data exploration for policy makers")
    st.write("""
    Welcome to our interactive journey through recent wildfire data in Brazil.
    """)
    st.write("""
     The goal of this learning experience is to equip you with a good understanding of the data around wildfires, to help you make informed decisions that help achieve the 2030 Goals for land restoration.
    """)
    
    
    st.markdown("""---""") 
    st.image('assets/icons.png', caption='Cooperation Partners')


def about_us():
    st.header("About Us")
    st.write("""
    -> We could add some stuff about G20 Land Initiative or Links etc. here <-
    """)

# Main app
def main():
    introduction()
    about_us()

if __name__ == "__main__":
    main()