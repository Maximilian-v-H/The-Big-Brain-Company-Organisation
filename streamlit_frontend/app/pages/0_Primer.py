import streamlit as st

st.set_page_config(layout="wide")

st.title("Wildfire Awareness Quiz")

# load Style css
#with open('app/styles.css')as f:
#    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


# Start the quiz
st.write("To get started, let us see what questions we will touch upon on this learning journey. Feel free to answer the questions and see how you´d answer at the end of the. ")

with st.expander("**Question 1**: Take a guess, what percentage of brazil's area has already been affected by wildfires?", expanded=True):
    # Question 1 (Slider)
    q1_answer = st.slider("-", 0, 100, step=1, label_visibility="hidden")

# Question 2 (Multiple Choice)
with st.expander("**Question 2:** What is the common cause of wildfires in Brazil?", expanded=True):
    q2_options = ['Agriculture', 'Lightning strikes', 'Campfires', 'All of the above']
    q2_answer = st.radio("-", options=q2_options, key=1, label_visibility="hidden")

# Q3
with st.expander("Question 3: Effective wildfire prevention and management require which of the following policy actions?", expanded=True):
    q3_options = ['A) Strict enforcement of land use regulations', 'B) Investments in early detection and firefighting resources', 'C) Community education and engagement in prevention measures', 'All of the above']
    q3_answer = st.radio("-", options=q3_options, key=2, label_visibility="hidden")

# Question 4 (Checkbox)
with st.expander("Question 4: Wildfires only occur in the Amazon Rainforest.", expanded=True):
    q4_options = [True, False]
    q4_answer = st.radio("-", options=q3_options, key=3, label_visibility="hidden")


# Submit button
if st.button('Submit'):
    # Placeholder for checking answers - in a real app, you'd compare these with the correct answers
    st.write("Your answers have been submitted! Here's how you did:")
    st.write(f"Question 1: You answered {q1_answer}")
    st.write(f"Question 2: You answered {q2_answer}")
    st.write(f"Question 3: You answered {q3_answer}")
    st.write(f"Question 4: You answered {'True' if q4_answer else 'False'}")
    st.write("Thank you for participating! Scroll down to learn more about wildfires in Brazil and what you can do to help.")
