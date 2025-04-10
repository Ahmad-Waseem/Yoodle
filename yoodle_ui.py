import streamlit as st
from streamlit_drawable_canvas import st_canvas
import yoodle_backend
import time

# Initialize model
try:
    YoodleV3 = yoodle_backend.MyModel()
except AttributeError as e:
    st.error(f"Error initializing the model: {e}. Please ensure 'yoodle_backend.py' and the 'MyModel' class exist and are correctly implemented.")
    st.stop()
except Exception as e:
    st.error(f"An unexpected error occurred during model initialization: {e}")
    st.stop()

# Page config
st.set_page_config(page_title="Yoodle - AI Buildings classifier", page_icon="🎨", layout="wide")

# Background image and custom CSS
page_bg_img = f'''
<style>
[data-testid="stAppViewBlockContainer"] {{
    background-image: url("https://raw.githubusercontent.com/Ahmad-Waseem/Yoodle/main/yoodle/Assets/toppng.com-jpg-black-and-white-istanbul-royalty-colorful-buildings-drawings-3001x1957.png");
    background-size: cover;
    padding-top: 1;
}}
.st-canvas-container > canvas {{
    border: 2px solid black; /* Add a border for visual clarity */
    max-width: 512px !important; /* Ensure it doesn't exceed the intended width */
    max-height: 512px !important; /* Ensure it doesn't exceed the intended height */
    width: 100% !important; /* Make it responsive within its container */
    height: auto !important;
}}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Labels
labels = ['Badshahi Mosque', 'Big Ben', 'Burj Khalifa', 'Burj ul Arab', 'Chrysler Building',
          'Cologne Cathedral', 'Colosseum of Rome', 'Easter Island', 'Eiffel Tower',
          'Future Museum', 'Taj Mahal']

# Session states
if 'building_choice' not in st.session_state:
    st.session_state.building_choice = 'None'
if 'current_N' not in st.session_state:
    st.session_state.current_N = 25
if 'prediction_done' not in st.session_state:
    st.session_state.prediction_done = False
if 'timer_started' not in st.session_state:
    st.session_state.timer_started = False
if 'reset' not in st.session_state:
    st.session_state.reset = False
if 'canvas_key' not in st.session_state:
    st.session_state.canvas_key = 0

# Output printer
def printOutput(num):
    st.divider()
    st.write(f"It is: <span style='font-size: 24px; font-weight: bold;'>{labels[num[0]]}</span>", unsafe_allow_html=True)
    st.divider()

# Sidebar info
st.sidebar.title("Yoodle V2")
st.sidebar.markdown("""
## Introduction
Welcome to the Yoodle App! This app uses an AI model to classify buildings based on their features.

## How to Use
1. Select the Landmark name from DropDown
2. Draw doodle under 25 seconds
3. Click the "Predict Now (skip timer)" button to get the result
4. See if model gives you correct image
""")

# Title
st.title("Yoodle!!")

# Select box
building = st.selectbox(
    'Select Building',
    ['None'] + labels,
    index=(['None'] + labels).index(st.session_state.building_choice)
)
st.session_state.building_choice = building

# Reset if needed
if st.session_state.reset:
    st.session_state.building_choice = 'None'
    st.session_state.current_N = 25
    st.session_state.prediction_done = False
    st.session_state.timer_started = False
    st.session_state.reset = False
    # Force a reset of the canvas by changing its key
    st.session_state.canvas_key += 1
    st.session_state.building_choice = 'None'
    st.session_state.current_N = 25
    st.session_state.prediction_done = False
    st.session_state.timer_started = False
    st.session_state.reset = False
    # Force a reset of the canvas by changing its key
    st.session_state.canvas_key += 1
    st.experimental_rerun()
    
if building != 'None':
    # Start timer once when dropdown changes from None
    if not st.session_state.timer_started:
        st.session_state.timer_started = True
        st.session_state.current_N = 25

    col1, col2 = st.columns(2)
    with col1:
        canvas_result = st_canvas(
            fill_color="rgb(255, 255, 255)",
            stroke_width=5,
            stroke_color="rgb(0, 0, 0)",
            background_color="rgb(255, 255, 255)",
            update_streamlit=True,
            height=512,
            width=512,
            drawing_mode="freedraw",
            point_display_radius=0,
            display_toolbar=False,
            key=f"canvas_{st.session_state.canvas_key}"
        )

    with col2:
        ph = st.empty()

        if st.button("Predict Now (skip timer)"):
            if canvas_result.image_data is not None:
                try:
                    response = YoodleV3.classify(canvas_result.image_data, building)
                    st.session_state.prediction_done = True
                    printOutput(response)
                except Exception as e:
                    st.error(f"Error during classification: {e}")

        # Timer display
        if st.session_state.current_N > 0 and not st.session_state.prediction_done:
            for secs in range(st.session_state.current_N, -1, -1):
                st.session_state.current_N = secs
                ph.metric("Countdown", f"{secs:02d}s left")
                time.sleep(1)
            if st.session_state.current_N <= 0 and not st.session_state.prediction_done:
                if canvas_result.image_data is not None:
                    try:
                        response = YoodleV3.classify(canvas_result.image_data, building)
                        st.session_state.prediction_done = True
                        printOutput(response)
                    except Exception as e:
                        st.error(f"Error during classification: {e}")




        # Reset button
        if st.session_state.prediction_done:
            if st.button("🔄 Reset"):
                st.session_state.reset = True
                