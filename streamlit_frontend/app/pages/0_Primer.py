import streamlit as st

st.set_page_config(layout="wide")

st.title("Wildfire Awareness Quiz")

# load Style css
# with open('app/styles.css')as f:
#    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html = True)


# Start the quiz
st.write(
    "To get started, let us see what questions we will touch upon on this learning journey. Feel free to answer the questions and test your knowledge about wildfires in Brazil.")

with st.expander(
        "*Question 1*: Take a guess, what percentage of the Brazilian rain forest has been lost in the last 20 years?",
        expanded=True):
    # Question 1 (Slider)
    q1_answer = st.slider("-", 0., 20.0, step=0.1, label_visibility="hidden", value=2.0)

# Question 2 (Multiple Choice)
with st.expander("*Question 2:* What is the common cause of wildfires in Brazil?", expanded=True):
    q2_options = ['Agriculture', 'Lightning strikes', 'Campfires', 'All of the above']
    q2_answer = st.radio("-", options=q2_options, key=1, label_visibility="hidden")

# Q3
with st.expander(
        "Question 3: Effective wildfire prevention and management require which of the following policy actions?",
        expanded=True):
    q3_options = ['A) Strict enforcement of land use regulations',
                  'B) Investments in early detection and firefighting resources',
                  'C) Community education and engagement in prevention measures', 'All of the above']
    q3_answer = st.radio("-", options=q3_options, key=2, label_visibility="hidden")

# Question 4 (Checkbox)
with st.expander("Question 4: Wildfires and land degredation can cause accelerated climatic changes.", expanded=True):
    q4_options = [True, False]
    q4_answer = st.radio("-", options=q4_options, key=3, label_visibility="hidden")

# Submit button
if st.button('Submit'):
    # Placeholder for checking answers - in a real app, you'd compare these with the correct answers
    st.write("#### Your answers have been submitted! Here's how you did:")
    st.write(
        f"Question 1: Your guess ({q1_answer}) {'was actually pretty good!' if abs(q1_answer - 8.6) < 3 else ' was a little bit of'}. We have lost about 8.6% our rainforests!")
    st.write(
        f"Question 2: {'Correct - ' if q2_answer == 'Agriculture' else 'Not quite - '} most wildfires are caused by illegal fires (slash and burn) used to make more place for agriculture")
    st.write(
        f"Question 3: {'Awesome, you got it right - these are all necessary measures!.' if q3_answer == 'All of the above' else ('While your answer is correct, we actually need all of these policies to make a meaniningful impact')}")
    st.write(f"Question 4: {'Correct!' if q4_answer else 'False :('}")
    st.write("---")
    st.write(
        "## Thank you for participating! Check out the other pages to learn more about wildfires in Brazil and what you can do to help.")
